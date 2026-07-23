"""Helper HTTP minimo basado en la libreria estandar (urllib).

Se usa para el comando `check` y peticiones GET simples sin depender de
`requests`. Devuelve JSON ya parseado o lanza HttpError con contexto util.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


class HttpError(Exception):
    """Error de red o respuesta no-2xx, con codigo si aplica."""

    def __init__(self, message: str, status: int | None = None) -> None:
        super().__init__(message)
        self.status = status


def get_json(
    url: str,
    params: dict[str, Any] | None = None,
    timeout: float = 15.0,
) -> Any:
    """GET a `url` con querystring `params`; devuelve el JSON parseado."""
    if params:
        url = f"{url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "StockFinder/0.1"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
    except urllib.error.HTTPError as exc:  # respuesta con codigo de error
        raise HttpError(f"HTTP {exc.code} en {url.split('?')[0]}", exc.code) from exc
    except urllib.error.URLError as exc:  # sin conexion, DNS, timeout...
        raise HttpError(f"Fallo de red: {exc.reason}") from exc
    try:
        return json.loads(body)
    except json.JSONDecodeError as exc:
        raise HttpError("Respuesta no es JSON valido") from exc
