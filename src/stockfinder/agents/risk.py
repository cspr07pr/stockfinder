"""Sub-agente Risk (Cerebro/05). Agente de mayor peso.

Evalua el riesgo de la empresa y su encaje con el perfil. Dimensiona la posicion
con el capital disponible y valida que el stop quepa en la perdida maxima (8-10%).
Bandera critica (veto): el riesgo excede la perdida tolerable sin salida clara.
"""

from __future__ import annotations

from ..profile import DEFAULT_PROFILE
from ..scorecard import Scorecard, SubMetric
from .base import avg, lin, num

NAME = "Risk"


def run(bundle, profile=None) -> Scorecard:
    profile = profile or DEFAULT_PROFILE
    tech = getattr(bundle, "tech", None) or {}
    price = tech.get("price") or bundle.price
    if not price:
        return Scorecard.insufficient(NAME, "sin precio para dimensionar")

    beta = num(bundle.fh_metrics or {}, "beta")
    stop = tech.get("stop")
    stop_pct = tech.get("stop_pct")
    max_loss = profile.max_loss_pct * 100

    subs: list[SubMetric] = []
    red, crit = [], []

    # 1) Volatilidad (beta)
    if beta is not None:
        subs.append(SubMetric("Volatilidad (beta)", f"{beta:.2f}", lin(beta, 2.2, 0.6)))

    # 2) Stop dentro de la tolerancia
    if stop_pct is not None:
        ok_stop = stop_pct <= max_loss
        subs.append(SubMetric("Stop vs perdida maxima",
                              f"{stop_pct:.1f}% (tope {max_loss:.0f}%)",
                              90 if ok_stop else 25))
        if not ok_stop:
            # Precio extendido sobre el soporte: no es veto, es "esperar entrada".
            red.append(f"A este precio el stop en soporte ({stop_pct:.1f}%) excede tu "
                       f"perdida maxima ({max_loss:.0f}%): esperar entrada cerca del soporte")

    # 3) Dimensionamiento y concentracion (requiere capital)
    sizing = {}
    if profile.capital and stop and price > stop:
        max_loss_usd = profile.capital * profile.max_loss_pct
        risk_per_share = price - stop
        shares_by_risk = max_loss_usd / risk_per_share
        shares_by_cap = profile.capital / price
        shares = int(min(shares_by_risk, shares_by_cap))
        position_value = shares * price
        concentration = position_value / profile.capital
        subs.append(SubMetric("Concentracion en 1 nombre",
                              f"{concentration*100:.0f}% del capital",
                              lin(concentration, 1.0, profile.max_concentracion_sugerida)))
        if concentration > profile.max_concentracion_sugerida:
            red.append(f"Posicion completa = {concentration*100:.0f}% del capital "
                       "(alta concentracion para principiante)")
        sizing = {
            "capital": profile.capital, "max_loss_usd": round(max_loss_usd),
            "entry": round(price, 2), "stop": stop,
            "risk_per_share": round(risk_per_share, 2),
            "shares_full": shares, "position_value": round(position_value),
            "concentration": round(concentration, 3),
            "shares_half": shares // 2,
        }
    elif not profile.capital:
        red.append("Falta el capital disponible para dimensionar la posicion (--capital)")

    score = avg([s.points for s in subs]) if subs else 50
    conf = "Alta" if (beta is not None and stop_pct is not None) else "Media"

    parts = []
    if beta is not None:
        parts.append(f"beta {beta:.2f}")
    if stop_pct is not None:
        parts.append(f"stop {stop_pct:.1f}% (tope {max_loss:.0f}%)")
    if sizing:
        parts.append(f"posicion completa ~{sizing['shares_full']} acc "
                     f"({sizing['concentration']*100:.0f}% del capital)")
    summary = "Riesgo/perfil: " + ", ".join(parts) + "." if parts else "Riesgo evaluado."

    return Scorecard(
        agent=NAME, score=score, confidence=conf, submetrics=subs,
        red_flags=red, critical_flags=crit, summary=summary,
        extra={"beta": beta, "sizing": sizing},
    )
