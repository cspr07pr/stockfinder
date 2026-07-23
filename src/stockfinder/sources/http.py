"""Helper HTTP minimo basado en la libreria estandar (urllib).

Se usa para el comando `check` y peticiones GET simples sin depender de
`requests`. Devuelve JSON ya parseado o lanza HttpError con contexto util.
"""

from __future__ import annotations

import gzip
import json
import urllib.error
import urllib.parse
import urllib.request
import zlib
from typing import Any


def _decode(raw: bytes, encoding: str | None) -> str:
    """Descomprime gzip/deflate si aplica y decodifica a texto."""
    enc = (encoding or "").lower()
    try:
        if enc == "gzip":
            raw = gzip.decompress(raw)
        elif enc == "deflate":
            raw = zlib.decompress(raw)
    except (OSError, zlib.error):
        pass
    return raw.decode("utf-8", "replace")


class HttpError(Exception):
    """Error de red o respuesta no-2xx, con codigo si aplica."""

    def __init__(self, message: str, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status


def get_json(
    url: str,
    params: dict[str, Any] | None = None,
    headers: dict[str, str] | None = None,
    timeout: float = 15.0,
) -> Any:
    """GET a `url` con querystring `params` y headers opcionales; devuelve JSON."""
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    h = {"User-Agent": "StockFinder/0.1"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, headers=h)
    return _read_json(req, timeout, url)


def post_form(
    url: str,
    data: dict[str, Any],
    headers: dict[str, str] | None = None,
    timeout: float = 20.0,
) -> Any:
    """POST application/x-www-form-urlencoded (para el token OAuth)."""
    body = urllib.parse.urlencode(data).encode("utf-8")
    h = {"User-Agent": "StockFinder/0.1",
         "Content-Type": "application/x-www-form-urlencoded"}
    if headers:
        h.update(headers)
    req = urllib.request.Request(url, data=body, headers=h, method="POST")
    return _read_json(req, timeout, url)


def _read_json(req: urllib.request.Request, timeout: float, url: str) -> Any:
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = _decode(resp.read(), resp.headers.get("Content-Encoding"))
    except urllib.error.HTTPError as exc:
        detail = ""
        try:
            detail = " " + _decode(exc.read(), exc.headers.get("Content-Encoding"))[:300]
        except Exception:
            pass
        raise HttpError(f"HTTP {exc.code} en {url.split('?')[0]}{detail}", exc.code) from exc
    except urllib.error.URLError as exc:
        raise HttpError(f"Fallo de red: {exc.reason}") from exc
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise HttpError("Respuesta no es JSON valido") from exc
