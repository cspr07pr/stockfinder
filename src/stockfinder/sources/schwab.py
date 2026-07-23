"""Conector a Charles Schwab (OAuth 2.0 + Market Data).

Flujo de tres patas:
  1) build_authorize_url(): URL que el USUARIO abre en su navegador.
  2) Tras autorizar, Schwab redirige a la callback con ?code=...
  3) exchange_code(url): intercambia ese code por access/refresh tokens.
  4) Los tokens se guardan en API/schwab_token.json (git lo ignora).

El access token dura ~30 min; se refresca solo con el refresh token (~7 dias).
Este modulo nunca maneja la contrasena de Schwab: el login lo hace el usuario.
"""

from __future__ import annotations

import base64
import json
import time
import urllib.parse
from pathlib import Path
from typing import Any

from ..config import REPO_ROOT, Config
from .http import HttpError, get_json, post_form

AUTHORIZE_URL = "https://api.schwabapi.com/v1/oauth/authorize"
TOKEN_URL = "https://api.schwabapi.com/v1/oauth/token"
MARKETDATA = "https://api.schwabapi.com/marketdata/v1"


class SchwabAuth:
    """Maneja el OAuth de Schwab y persiste los tokens."""

    def __init__(self, cfg: Config) -> None:
        if not (cfg.schwab_app_key and cfg.schwab_app_secret):
            raise ValueError("Schwab: faltan SCHWAB_APP_KEY / SCHWAB_APP_SECRET")
        self._key = cfg.schwab_app_key
        self._secret = cfg.schwab_app_secret
        self._callback = cfg.schwab_callback_url
        tp = Path(cfg.schwab_token_path)
        self._token_path = tp if tp.is_absolute() else REPO_ROOT / tp

    # --- URLs / auth ---
    def build_authorize_url(self) -> str:
        params = {
            "client_id": self._key,
            "redirect_uri": self._callback,
            "response_type": "code",
        }
        return f"{AUTHORIZE_URL}?{urllib.parse.urlencode(params)}"

    def _basic_header(self) -> dict[str, str]:
        raw = f"{self._key}:{self._secret}".encode()
        return {"Authorization": "Basic " + base64.b64encode(raw).decode()}

    @staticmethod
    def _extract_code(redirect_url_or_code: str) -> str:
        s = redirect_url_or_code.strip()
        if "code=" in s:
            query = urllib.parse.urlparse(s).query or s.split("?", 1)[-1]
            code = urllib.parse.parse_qs(query).get("code", [""])[0]
            if code:
                return code
        return s  # el usuario pego solo el code

    # --- intercambio / refresh ---
    def exchange_code(self, redirect_url_or_code: str) -> dict[str, Any]:
        code = self._extract_code(redirect_url_or_code)
        tok = post_form(
            TOKEN_URL,
            {"grant_type": "authorization_code", "code": code,
             "redirect_uri": self._callback},
            headers=self._basic_header(),
        )
        return self._store(tok)

    def refresh(self) -> dict[str, Any]:
        tok = self._load()
        rt = tok.get("refresh_token")
        if not rt:
            raise HttpError("Schwab: no hay refresh_token; corre 'schwab-login'")
        new = post_form(
            TOKEN_URL,
            {"grant_type": "refresh_token", "refresh_token": rt},
            headers=self._basic_header(),
        )
        new.setdefault("refresh_token", rt)  # a veces no lo reenvia
        return self._store(new)

    # --- token persistido ---
    def _store(self, tok: dict[str, Any]) -> dict[str, Any]:
        tok["obtained_at"] = int(time.time())
        tok["expires_at"] = int(time.time()) + int(tok.get("expires_in", 1800)) - 60
        self._token_path.parent.mkdir(parents=True, exist_ok=True)
        self._token_path.write_text(json.dumps(tok, indent=2), encoding="utf-8")
        return tok

    def _load(self) -> dict[str, Any]:
        if not self._token_path.exists():
            raise HttpError("Schwab: sin token guardado; corre 'schwab-login'")
        return json.loads(self._token_path.read_text(encoding="utf-8"))

    def access_token(self) -> str:
        """Devuelve un access token valido, refrescando si expiro."""
        tok = self._load()
        if time.time() >= tok.get("expires_at", 0):
            tok = self.refresh()
        return tok["access_token"]

    @property
    def has_token(self) -> bool:
        return self._token_path.exists()


class SchwabClient:
    """Llamadas de Market Data con el access token (se refresca solo)."""

    def __init__(self, auth: SchwabAuth) -> None:
        self._auth = auth

    def _bearer(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self._auth.access_token()}"}

    def quote(self, symbol: str) -> dict[str, Any]:
        data = get_json(f"{MARKETDATA}/quotes",
                        {"symbols": symbol.upper()}, headers=self._bearer())
        return data.get(symbol.upper(), data) if isinstance(data, dict) else {}

    def price_history(self, symbol: str, period_type: str = "year",
                      period: int = 1, frequency_type: str = "daily") -> list[dict]:
        data = get_json(
            f"{MARKETDATA}/pricehistory",
            {"symbol": symbol.upper(), "periodType": period_type, "period": period,
             "frequencyType": frequency_type},
            headers=self._bearer(),
        )
        return data.get("candles", []) if isinstance(data, dict) else []
