"""Conector a FRED (Reserva Federal de St. Louis) para datos macro.

Series usadas por Market Analysis:
  FEDFUNDS  tasa de fondos federales      CPIAUCSL  IPC (nivel)
  CPILFESL  IPC subyacente (core)         UNRATE    desempleo
  DGS10     bono 10 anios                 T10Y2Y    spread 10a-2a (curva)
"""

from __future__ import annotations

from typing import Any

from .http import HttpError, get_json

BASE = "https://api.stlouisfed.org/fred"


class FRED:
    """Cliente de FRED. Devuelve observaciones y agregados macro."""

    def __init__(self, api_key: str) -> None:
        if not api_key:
            raise ValueError("FRED: falta la API key")
        self._key = api_key

    def observations(self, series_id: str, limit: int = 13,
                     sort_order: str = "desc") -> list[dict[str, Any]]:
        data = get_json(
            f"{BASE}/series/observations",
            {"series_id": series_id, "api_key": self._key, "file_type": "json",
             "limit": limit, "sort_order": sort_order},
        )
        return data.get("observations", []) if isinstance(data, dict) else []

    def latest(self, series_id: str) -> tuple[float, str]:
        """Ultimo valor valido (float) y su fecha."""
        for obs in self.observations(series_id, limit=5, sort_order="desc"):
            val = obs.get("value", ".")
            if val not in (".", "", None):
                return float(val), obs.get("date", "")
        raise HttpError(f"FRED {series_id}: sin observaciones validas")

    def yoy(self, series_id: str) -> float:
        """Variacion interanual (%) para series mensuales.

        Pide un margen extra de observaciones y toma la #12 entre las VALIDAS,
        para tolerar meses vacios ('.') sin romper el calculo de 12 meses.
        """
        obs = [o for o in self.observations(series_id, limit=20, sort_order="desc")
               if o.get("value") not in (".", "", None)]
        if len(obs) < 13:
            raise HttpError(f"FRED {series_id}: faltan datos para YoY")
        latest = float(obs[0]["value"])
        year_ago = float(obs[12]["value"])
        return round((latest / year_ago - 1) * 100, 2)

    def macro_snapshot(self) -> dict[str, Any]:
        """Resumen macro para el agente Market. Cada campo puede faltar."""
        snap: dict[str, Any] = {}
        # (clave, funcion) — se ignora la que falle para no romper todo el snapshot
        getters = {
            "fed_funds": lambda: self.latest("FEDFUNDS"),
            "cpi_yoy": lambda: self.yoy("CPIAUCSL"),
            "core_cpi_yoy": lambda: self.yoy("CPILFESL"),
            "unemployment": lambda: self.latest("UNRATE"),
            "treasury_10y": lambda: self.latest("DGS10"),
            "yield_curve_10y2y": lambda: self.latest("T10Y2Y"),
        }
        for key, fn in getters.items():
            try:
                snap[key] = fn()
            except (HttpError, ValueError):
                snap[key] = None
        return snap
