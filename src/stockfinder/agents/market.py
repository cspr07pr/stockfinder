"""Sub-agente Market (Cerebro/03).

Contexto externo: macro (FRED) y sentimiento de analistas. Determina si el
entorno favorece a la accion.
"""

from __future__ import annotations

from ..scorecard import Scorecard, SubMetric
from .base import avg, lin

NAME = "Market"


def _val(x):
    """macro_snapshot da tuplas (valor, fecha) para 'latest' y float para yoy."""
    if isinstance(x, (tuple, list)):
        return x[0]
    return x


def run(bundle, profile=None) -> Scorecard:
    macro = bundle.macro or {}
    core_cpi = _val(macro.get("core_cpi_yoy"))
    curve = _val(macro.get("yield_curve_10y2y"))
    unrate = _val(macro.get("unemployment"))
    fed = _val(macro.get("fed_funds"))

    subs = []
    if core_cpi is not None:
        subs.append(SubMetric("Inflacion subyacente (core CPI YoY)",
                              f"{core_cpi:.1f}%", lin(core_cpi, 5, 2)))  # menor = mejor
    if curve is not None:
        subs.append(SubMetric("Curva 10a-2a", f"{curve:+.2f}", lin(curve, -1, 1)))
    if unrate is not None:
        subs.append(SubMetric("Desempleo", f"{unrate:.1f}%", lin(unrate, 6.5, 3.5)))

    # Sentimiento de analistas
    rec = (bundle.recommendations or [{}])[0]
    total = sum(rec.get(k, 0) for k in ("strongBuy", "buy", "hold", "sell", "strongSell"))
    bull_ratio = None
    if total:
        bull_ratio = (rec.get("strongBuy", 0) + rec.get("buy", 0)) / total * 100
        subs.append(SubMetric("Analistas alcistas", f"{bull_ratio:.0f}%", lin(bull_ratio, 30, 85)))

    if not subs:
        return Scorecard.insufficient(NAME, "sin datos macro ni sentimiento")

    score = avg([s.points for s in subs])

    red = []
    if curve is not None and curve < 0:
        red.append("Curva de rendimientos invertida (senal recesiva)")

    macro_txt = []
    if fed is not None:
        macro_txt.append(f"Fed {fed:.2f}%")
    if core_cpi is not None:
        macro_txt.append(f"core CPI {core_cpi:.1f}%")
    if bull_ratio is not None:
        macro_txt.append(f"{bull_ratio:.0f}% analistas alcistas")
    summary = "Entorno: " + ", ".join(macro_txt) + "."

    return Scorecard(
        agent=NAME, score=score, confidence="Media", submetrics=subs,
        red_flags=red, summary=summary,
        extra={"core_cpi": core_cpi, "fed_funds": fed, "yield_curve": curve,
               "unemployment": unrate, "bull_ratio": bull_ratio},
    )
