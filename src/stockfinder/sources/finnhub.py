"""Conector a Finnhub.

Cubre perfil, transacciones de insiders (SEC), recomendaciones de analistas y
metricas basicas. El endpoint 'price-target' es premium (403) y no se usa: el
price target lo cubre FMP.
"""

from __future__ import annotations

from typing import Any

from .http import get_json

BASE = "https://finnhub.io/api/v1"


class Finnhub:
    """Cliente de Finnhub. Devuelve datos ya parseados."""

    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("Finnhub: falta la API key")
        self._key = api_key

    def _get(self, path: str, **params: Any) -> Any:
        params["token"] = self._key
        return get_json(f"{BASE}/{path}", params)

    def quote(self, symbol: str) -> dict[str, Any]:
        """Cotizacion: c=actual, h, l, o, pc=cierre previo."""
        return self._get("quote", symbol=symbol)

    def profile(self, symbol: str) -> dict[str, Any]:
        return self._get("stock/profile2", symbol=symbol)

    def insider_transactions(self, symbol: str) -> list[dict[str, Any]]:
        """Form 4 de la SEC. Cada item: name, share, change, transactionPrice..."""
        data = self._get("stock/insider-transactions", symbol=symbol)
        return data.get("data", []) if isinstance(data, dict) else []

    def recommendations(self, symbol: str) -> list[dict[str, Any]]:
        """Tendencia de recomendaciones (strongBuy, buy, hold, sell, strongSell)."""
        return self._get("stock/recommendation", symbol=symbol)

    def metrics(self, symbol: str) -> dict[str, Any]:
        """Metricas basicas (beta, 52w high/low, margenes...)."""
        data = self._get("stock/metric", symbol=symbol, metric="all")
        return data.get("metric", {}) if isinstance(data, dict) else {}
