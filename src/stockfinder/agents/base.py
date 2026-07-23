"""Utilidades numericas compartidas por los sub-agentes."""

from __future__ import annotations

from typing import Any


def num(d: dict[str, Any], *keys: str) -> float | None:
    """Primer valor numerico no nulo entre varias claves posibles."""
    for k in keys:
        v = d.get(k)
        if isinstance(v, (int, float)) and v is not None:
            return float(v)
        if isinstance(v, str):
            try:
                return float(v)
            except ValueError:
                continue
    return None


def clamp(x: float, lo: float = 0, hi: float = 100) -> float:
    return max(lo, min(hi, x))


def lin(value: float | None, worst: float, best: float) -> int:
    """Mapea `value` a 0-100 linealmente entre `worst` y `best` (con clamp).

    Si worst > best la escala se invierte (valores menores puntuan mas alto).
    Devuelve 50 si value es None (neutro).
    """
    if value is None:
        return 50
    if worst == best:
        return 50
    pct = (value - worst) / (best - worst)
    return int(round(clamp(pct * 100)))


def avg(points: list[int]) -> int:
    return int(round(sum(points) / len(points))) if points else 50


def pct(a: float | None, b: float | None) -> float | None:
    """Variacion a/b - 1 en %. None si no se puede."""
    if a is None or b in (None, 0):
        return None
    return (a / b - 1) * 100


def fmt_money(x: float | None) -> str:
    if x is None:
        return "N/D"
    ax = abs(x)
    if ax >= 1e12:
        return f"${x/1e12:.2f}T"
    if ax >= 1e9:
        return f"${x/1e9:.1f}B"
    if ax >= 1e6:
        return f"${x/1e6:.1f}M"
    return f"${x:,.0f}"
