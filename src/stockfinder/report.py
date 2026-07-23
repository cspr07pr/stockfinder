"""Render del reporte final en texto (Cerebro/08-reporte-final.md)."""

from __future__ import annotations

from .agents.base import fmt_money
from .orchestrator import Analysis


def _bar(score: float | None, width: int = 20) -> str:
    if score is None:
        return "N/D"
    n = int(round(score / 100 * width))
    return "#" * n + "." * (width - n)


def _when_to_review(a: Analysis) -> str:
    cards = {c.agent: c for c in a.decision.cards}
    val = cards.get("Valuation")
    tech = cards.get("Technical")
    if val and val.extra.get("verdict") == "cara":
        return "Proximo earnings o en 1-2 trimestres (esperar mejor valuacion)."
    if tech and tech.extra.get("support"):
        return f"Cuando el precio toque el soporte ${tech.extra['support']:.0f}."
    return "En 1 trimestre (revisar evolucion)."


def render_text(a: Analysis) -> str:
    d = a.decision
    data = a.data
    L: list[str] = []
    W = 68

    L.append("=" * W)
    price = f"${data.price:.2f}" if data.price else "N/D"
    L.append(f" StockFinder  ·  {a.symbol}  ·  {price}")
    L.append("=" * W)

    gs = f"{d.global_score:.0f}/100" if d.global_score is not None else "N/D"
    L.append(f" DECISION: {d.label.upper()}   |   Global {gs}   |   Confianza {d.confidence}")
    if d.missing_weight > 0:
        L.append(f" (peso sin datos: {d.missing_weight*100:.0f}% -> confianza reducida)")
    L.append("")

    # Veredicto de precio
    val = next((c for c in d.cards if c.agent == "Valuation"), None)
    if val and val.data_sufficient:
        L.append(f" Veredicto de precio: {val.extra.get('verdict','N/D')}")
    if d.label in ("Evitar", "Vigilar", "Sin decision"):
        L.append(f" Cuando revisar de nuevo: {_when_to_review(a)}")
    L.append("")

    # Entrada/salida/timing
    tech = next((c for c in d.cards if c.agent == "Technical"), None)
    if tech and tech.data_sufficient:
        e = tech.extra
        L.append(" Puntos de entrada / salida (prioridad del perfil):")
        L.append(f"   Entrada:   ${e['entry_zone'][0]}-{e['entry_zone'][1]} (zona de soporte)")
        L.append(f"   Stop:      ${e['stop']}  ({e['stop_pct']:.1f}% bajo el precio)")
        L.append(f"   Objetivo:  ${e['target']} (resistencia)")
    rk = next((c for c in d.cards if c.agent == "Risk"), None)
    if rk and rk.extra.get("sizing"):
        s = rk.extra["sizing"]
        L.append(f"   Dimension: {s['shares_full']} acc ~{fmt_money(s['position_value'])} "
                 f"({s['concentration']*100:.0f}% del capital); media posicion {s['shares_half']} acc.")
    L.append("")

    # Escenarios de precio
    if val and val.extra.get("scenarios"):
        L.append(" Escenarios de precio (rango; supuestos etiquetados):")
        for name, sc in val.extra["scenarios"].items():
            rng = sc["rango"]
            rng_txt = f"${rng[0]}-${rng[1]}" if rng else "N/D"
            L.append(f"   {name.capitalize():9} {rng_txt:16} [{sc['supuesto']}]")
        L.append("")

    # Scorecard por agente
    L.append(" Scorecard por agente:")
    L.append(f"   {'Agente':11} {'Peso':>5} {'Punt':>5}  {'Barra':22} Conf")
    for c in d.cards:
        sc = f"{c.score:.0f}" if c.score is not None else "N/D"
        L.append(f"   {c.agent:11} {c.weight*100:>4.0f}% {sc:>5}  {_bar(c.score):22} {c.confidence}")
    L.append("")

    # Resumenes y banderas
    L.append(" Detalle:")
    for c in d.cards:
        L.append(f"   [{c.agent}] {c.summary}")
        for f in c.red_flags:
            L.append(f"       - bandera: {f}")
        for f in c.critical_flags:
            L.append(f"       - CRITICA: {f}")
    L.append("")

    # Insiders
    L.append(" SEC Insiders (relevantes > $1M):")
    if a.insiders_relevantes:
        for t in a.insiders_relevantes[:8]:
            L.append(f"   {t['side'].upper():6} {fmt_money(t['value']):>9}  "
                     f"{t['name']}  ({t['change']:+} @ ${t['price']}, {t['date']})")
    else:
        L.append("   Sin transacciones > $1M en el periodo disponible.")
    L.append("")

    # Inversionistas relacionados (limitacion de datos honesta)
    L.append(" Inversionistas relacionados:")
    L.append("   Requiere fuente institucional (13F) no incluida en el plan actual.")
    L.append("")

    # Avisos de datos
    if data.warnings:
        L.append(" Avisos de datos:")
        for w in data.warnings[:8]:
            L.append(f"   - {w}")
        L.append("")

    L.append(" Reporte informativo, no asesoria financiera regulada.")
    L.append("=" * W)
    return "\n".join(L)
