"""Conector a Financial Modeling Prep (API 'stable').

Cubre fundamentales, ratios, valuacion, price targets e historico de precios.
Los endpoints 'v3' quedaron obsoletos (403 Legacy); se usa siempre '/stable'.
"""

from __future__ import annotations

from typing import Any

from .http import HttpError, get_json

BASE = "https://financialmodelingprep.com/stable"


class FMP:
    """Cliente de FMP. Cada metodo devuelve datos ya parseados."""

    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("FMP: falta la API key")
        self._key = api_key

    def _get(self, path: str, **params: Any) -> Any:
        params["apikey"] = self._key
        return get_json(f"{BASE}/{path}", params)

    def _first(self, path: str, **params: Any) -> dict[str, Any]:
        """Endpoints que devuelven una lista de un solo elemento."""
        data = self._get(path, **params)
        if isinstance(data, list) and data:
            return data[0]
        if isinstance(data, dict):
            return data
        raise HttpError(f"FMP {path}: respuesta vacia o inesperada")

    # --- precio / perfil ---
    def quote(self, symbol: str) -> dict[str, Any]:
        return self._first("quote", symbol=symbol)

    def profile(self, symbol: str) -> dict[str, Any]:
        return self._first("profile", symbol=symbol)

    # --- estados financieros (mas reciente primero) ---
    def income_statement(self, symbol: str, limit: int = 5,
                         period: str = "annual") -> list[dict[str, Any]]:
        return self._get("income-statement", symbol=symbol, limit=limit, period=period)

    def balance_sheet(self, symbol: str, limit: int = 5,
                      period: str = "annual") -> list[dict[str, Any]]:
        return self._get("balance-sheet-statement", symbol=symbol, limit=limit, period=period)

    def cash_flow(self, symbol: str, limit: int = 5,
                  period: str = "annual") -> list[dict[str, Any]]:
        return self._get("cash-flow-statement", symbol=symbol, limit=limit, period=period)

    # --- ratios / metricas / valuacion ---
    def ratios_ttm(self, symbol: str) -> dict[str, Any]:
        return self._first("ratios-ttm", symbol=symbol)

    def key_metrics_ttm(self, symbol: str) -> dict[str, Any]:
        return self._first("key-metrics-ttm", symbol=symbol)

    def price_target_consensus(self, symbol: str) -> dict[str, Any]:
        return self._first("price-target-consensus", symbol=symbol)

    def analyst_estimates(self, symbol: str, period: str = "annual",
                          limit: int = 4) -> list[dict[str, Any]]:
        return self._get("analyst-estimates", symbol=symbol, period=period, limit=limit)

    # --- historico de precios (EOD light: date, price, volume) ---
    def historical_prices(self, symbol: str) -> list[dict[str, Any]]:
        return self._get("historical-price-eod/light", symbol=symbol)
