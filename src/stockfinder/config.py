"""Carga de configuracion y claves desde API/.env.

Usa solo la libreria estandar para que el comando `check` funcione sin necesidad
de instalar dependencias primero. Nunca imprime los valores de las claves.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

# Raiz del repo = tres niveles arriba de este archivo:
#   src/stockfinder/config.py -> stockfinder -> src -> <raiz>
REPO_ROOT = Path(__file__).resolve().parents[2]
ENV_PATH = REPO_ROOT / "API" / ".env"


def _parse_env(path: Path) -> dict[str, str]:
    """Parser minimo de archivos .env (KEY=VALOR). Ignora comentarios y vacios."""
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        data[key.strip()] = value.strip().strip('"').strip("'")
    return data


@dataclass(frozen=True)
class Config:
    """Claves de las 4 fuentes. Los campos vacios indican fuente no configurada."""

    fmp_api_key: str = ""
    finnhub_api_key: str = ""
    fred_api_key: str = ""
    schwab_app_key: str = ""
    schwab_app_secret: str = ""
    schwab_callback_url: str = "https://127.0.0.1"
    schwab_token_path: str = "API/schwab_token.json"

    def has(self, source: str) -> bool:
        """True si la fuente indicada tiene lo minimo para funcionar."""
        return {
            "fmp": bool(self.fmp_api_key),
            "finnhub": bool(self.finnhub_api_key),
            "fred": bool(self.fred_api_key),
            "schwab": bool(self.schwab_app_key and self.schwab_app_secret),
        }.get(source, False)


def load_config(env_path: Path = ENV_PATH) -> Config:
    """Lee API/.env y devuelve un Config. No lanza si faltan claves."""
    env = _parse_env(env_path)
    return Config(
        fmp_api_key=env.get("FMP_API_KEY", ""),
        finnhub_api_key=env.get("FINNHUB_API_KEY", ""),
        fred_api_key=env.get("FRED_API_KEY", ""),
        schwab_app_key=env.get("SCHWAB_APP_KEY", ""),
        schwab_app_secret=env.get("SCHWAB_APP_SECRET", ""),
        schwab_callback_url=env.get("SCHWAB_CALLBACK_URL", "https://127.0.0.1"),
        schwab_token_path=env.get("SCHWAB_TOKEN_PATH", "API/schwab_token.json"),
    )
