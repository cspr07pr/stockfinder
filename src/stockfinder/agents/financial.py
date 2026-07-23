"""Sub-agente Financial (Cerebro/02).

Analiza crecimiento, rentabilidad, solidez del balance y flujo de caja.
Distingue dato historico de estimacion; si faltan estados clave -> N/D.
"""

from __future__ import annotations

from ..scorecard import Scorecard, SubMetric
from .base import avg, fmt_money, lin, num, pct

NAME = "Financial"


def run(bundle, profile=None) -> Scorecard:
    inc = bundle.income          # anual, mas reciente primero
    cf = bundle.cash_flow
    if not inc or not cf:
        return Scorecard.insufficient(NAME, "sin estados financieros")

    latest, prev = inc[0], (inc[1] if len(inc) > 1 else {})
    rev = num(latest, "revenue")
    if rev in (None, 0):
        return Scorecard.insufficient(NAME, "sin ingresos")

    # --- crecimiento ---
    growth = pct(rev, num(prev, "revenue"))

    # --- margenes ---
    gross_m = _ratio(num(latest, "grossProfit"), rev)
    op_m = _ratio(num(latest, "operatingIncome"), rev)
    net_m = _ratio(num(latest, "netIncome"), rev)
    gross_m_prev = _ratio(num(prev, "grossProfit"), num(prev, "revenue"))
    margin_trend = (gross_m - gross_m_prev) if (gross_m and gross_m_prev) else None

    # --- flujo de caja ---
    fcf = num(cf[0], "freeCashFlow")
    if fcf is None:
        fcf = _diff(num(cf[0], "operatingCashFlow"), num(cf[0], "capitalExpenditure"))
    fcf_m = _ratio(fcf, rev)
    fcf_pos_years = sum(1 for c in cf if (num(c, "freeCashFlow") or 0) > 0)

    # --- apalancamiento ---
    bal = bundle.balance[0] if bundle.balance else {}
    net_debt = num(bal, "netDebt")
    ebitda = num(latest, "ebitda")
    if ebitda is None:
        ebitda = _sum(num(latest, "operatingIncome"), num(cf[0], "depreciationAndAmortization"))
    debt_ebitda = (net_debt / ebitda) if (net_debt is not None and ebitda) else None

    # --- dilucion ---
    shares_now = num(latest, "weightedAverageShsOut", "weightedAverageShsOutDil")
    shares_old = num(inc[-1], "weightedAverageShsOut", "weightedAverageShsOutDil")
    dilution = pct(shares_now, shares_old)  # >0 = mas acciones (dilucion)

    # --- puntuacion ---
    subs = [
        SubMetric("Crecimiento ingresos YoY", _p(growth, "%"), lin(growth, -5, 20)),
        SubMetric("Margen bruto", _p(gross_m, "%"), lin(gross_m, 20, 60)),
        SubMetric("Margen operativo", _p(op_m, "%"), lin(op_m, 5, 35)),
        SubMetric("Margen FCF", _p(fcf_m, "%"), lin(fcf_m, 0, 30)),
        SubMetric("Deuda neta / EBITDA", _p(debt_ebitda, "x"), lin(debt_ebitda, 5, 0)),
    ]
    score = avg([s.points for s in subs])

    red, crit = [], []
    if fcf is not None and fcf_pos_years <= max(0, len(cf) // 2 - 1):
        crit.append("Free Cash Flow negativo estructural")
    if debt_ebitda is not None and debt_ebitda > 4:
        red.append(f"Apalancamiento alto (deuda neta/EBITDA {debt_ebitda:.1f}x)")
    if dilution is not None and dilution > 5:
        red.append(f"Dilucion de acciones (+{dilution:.1f}% acumulado)")

    conf = "Alta" if len(inc) >= 3 and bundle.balance else "Media"
    summary = (
        f"Ingresos {fmt_money(rev)} ({_p(growth,'%')} YoY), margen bruto {_p(gross_m,'%')}, "
        f"margen FCF {_p(fcf_m,'%')}, deuda neta/EBITDA {_p(debt_ebitda,'x')}."
    )

    return Scorecard(
        agent=NAME, score=score, confidence=conf, submetrics=subs,
        red_flags=red, critical_flags=crit, summary=summary,
        extra={"revenue": rev, "growth": growth, "gross_margin": gross_m,
               "fcf": fcf, "fcf_margin": fcf_m, "net_debt": net_debt,
               "debt_ebitda": debt_ebitda},
    )


# --- helpers locales ---
def _ratio(a, b):
    return (a / b * 100) if (a is not None and b) else None


def _diff(a, b):
    return (a - abs(b)) if (a is not None and b is not None) else None


def _sum(a, b):
    return (a + b) if (a is not None and b is not None) else None


def _p(v, unit=""):
    if v is None:
        return "N/D"
    return f"{v:.1f}{unit}"
