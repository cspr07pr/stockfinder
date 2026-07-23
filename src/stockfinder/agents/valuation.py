"""Sub-agente Valuation (Cerebro/06).

Depende de Financial. Calcula P/E y price targets en 3 escenarios (rango, nunca
un solo numero) con supuestos etiquetados. Responde: barata / justa / cara.
"""

from __future__ import annotations

from ..scorecard import Scorecard, SubMetric
from .base import avg, lin, num, pct

NAME = "Valuation"


def run(bundle, profile=None) -> Scorecard:
    price = bundle.price
    if not price:
        return Scorecard.insufficient(NAME, "sin precio actual")

    pe = num(bundle.ratios_ttm, "priceToEarningsRatioTTM", "peRatioTTM")
    pt = bundle.price_target or {}
    t_low = num(pt, "targetLow")
    t_cons = num(pt, "targetConsensus", "targetMedian")
    t_high = num(pt, "targetHigh")

    if t_cons is None and pe is None:
        return Scorecard.insufficient(NAME, "sin datos de valuacion")

    upside = pct(t_cons, price)  # % hasta el consenso

    subs = []
    if upside is not None:
        subs.append(SubMetric("Upside a consenso", f"{upside:+.1f}%", lin(upside, -20, 30)))
    if pe is not None:
        if pe <= 0:
            # P/E negativo = sin utilidades: no se puede valuar por P/E, se penaliza.
            subs.append(SubMetric("P/E (TTM)", f"{pe:.1f} (sin utilidades)", 15))
        else:
            subs.append(SubMetric("P/E (TTM)", f"{pe:.1f}", lin(pe, 45, 15)))  # menor = mejor
    score = avg([s.points for s in subs]) if subs else 50

    # Veredicto textual
    if upside is None:
        verdict = "sin consenso"
    elif upside > 12:
        verdict = "con descuento"
    elif upside > -5:
        verdict = "cerca de valor justo"
    else:
        verdict = "cara"

    red = []
    if pe is not None and pe <= 0:
        red.append("Sin utilidades (P/E negativo): no valuable por multiplos de ganancias")
    elif pe is not None and pe > 35:
        red.append(f"P/E elevado ({pe:.0f}) vs. mercado")
    if upside is not None and upside < -10:
        red.append("Precio por encima del consenso de analistas")

    scenarios = {
        "bajista": {"rango": _band(t_low), "supuesto": "target bajo de analistas"},
        "base": {"rango": _band(t_cons), "supuesto": "consenso de analistas"},
        "alcista": {"rango": _band(t_high), "supuesto": "target alto de analistas"},
    }

    summary = (
        f"P/E {(f'{pe:.1f}' if pe else 'N/D')}, precio ${price:.0f} {verdict}; "
        f"consenso ${_n(t_cons)} (rango ${_n(t_low)}-${_n(t_high)})."
    )

    return Scorecard(
        agent=NAME, score=score, confidence="Media", submetrics=subs,
        red_flags=red, summary=summary,
        extra={"pe": pe, "price": price, "target_low": t_low,
               "target_consensus": t_cons, "target_high": t_high,
               "upside": upside, "verdict": verdict, "scenarios": scenarios},
    )


def _band(center, spread=0.05):
    if center is None:
        return None
    return (round(center * (1 - spread)), round(center * (1 + spread)))


def _n(v):
    return f"{v:.0f}" if v is not None else "N/D"
