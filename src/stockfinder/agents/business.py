"""Sub-agente Business (Cerebro/01).

Analiza la calidad del negocio como proxy del moat: rentabilidad del capital
(ROIC, ROE) y margenes. Complementa con perfil (sector, industria, CEO).
"""

from __future__ import annotations

from ..scorecard import Scorecard, SubMetric
from .base import avg, lin, num

NAME = "Business"


def run(bundle, profile=None) -> Scorecard:
    ratios = bundle.ratios_ttm or {}
    km = bundle.key_metrics_ttm or {}
    prof = bundle.profile or {}

    roic = num(km, "returnOnInvestedCapitalTTM") or num(ratios, "returnOnCapitalEmployedTTM")
    roe = num(km, "returnOnEquityTTM")
    gross_m = num(ratios, "grossProfitMarginTTM")
    net_m = num(ratios, "netProfitMarginTTM")
    # ratios de FMP vienen en fraccion (0.46) -> a %
    roic, roe, gross_m, net_m = (_pct(x) for x in (roic, roe, gross_m, net_m))

    if roic is None and roe is None and gross_m is None:
        return Scorecard.insufficient(NAME, "sin ratios de rentabilidad")

    subs = [
        SubMetric("ROIC (retorno del capital)", _p(roic), lin(roic, 5, 30)),
        SubMetric("ROE", _p(roe), lin(roe, 8, 40)),
        SubMetric("Margen bruto (moat proxy)", _p(gross_m), lin(gross_m, 20, 60)),
        SubMetric("Margen neto", _p(net_m), lin(net_m, 5, 30)),
    ]
    score = avg([s.points for s in subs])

    sector = prof.get("sector") or "sector N/D"
    industry = prof.get("industry") or ""
    summary = (
        f"{prof.get('companyName', bundle.symbol)} — {sector}"
        f"{(' / ' + industry) if industry else ''}. "
        f"ROIC {_p(roic)}, ROE {_p(roe)}, margen bruto {_p(gross_m)}."
    )

    return Scorecard(
        agent=NAME, score=score, confidence="Media", submetrics=subs,
        summary=summary,
        extra={"roic": roic, "roe": roe, "gross_margin": gross_m,
               "sector": sector, "industry": industry, "ceo": prof.get("ceo")},
    )


def _pct(x):
    return x * 100 if x is not None else None


def _p(v):
    return f"{v:.1f}%" if v is not None else "N/D"
