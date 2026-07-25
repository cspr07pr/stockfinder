"""Render del reporte visual (dashboard HTML) a partir del Analysis.

Reusa el sistema de diseno de referencias/ejemplos/. Data-driven: refleja el
scorecard real y maneja los casos N/D (agentes sin datos). Aplica las reglas del
agente Visual: rango (no una sola linea), supuestos etiquetados, historico vs
estimado, y "el agente decide, no el grafico".
"""

from __future__ import annotations

import html
import math

from .agents.base import fmt_money
from .orchestrator import Analysis
from .report import _when_to_review

# Longitud del arco del gauge (semicirculo r=86): pi * r
_ARC = math.pi * 86


def _esc(s) -> str:
    return html.escape(str(s))


def _cls(score) -> str:
    if score is None:
        return "nd"
    if score >= 70:
        return "good"
    if score >= 55:
        return "warn"
    return "bad"


def _decision_cls(label: str) -> str:
    return {"Invertir": "good", "Vigilar": "warn",
            "Evitar": "bad", "Sin decision": "nd"}.get(label, "nd")


def _card(cards, name):
    return next((c for c in cards if c.agent == name), None)


def render_html(a: Analysis) -> str:
    d = a.decision
    data = a.data
    dec_cls = _decision_cls(d.label)
    price = f"${data.price:.2f}" if data.price else "N/D"
    gs = f"{d.global_score:.0f}" if d.global_score is not None else "N/D"

    body: list[str] = []

    # --- header ---
    body.append(f"""
    <div class="top">
      <div class="tick">
        <div class="logo">{_esc(a.symbol[:4])}</div>
        <div>
          <h1>{_esc(a.symbol)}</h1>
          <div class="sub">Reporte StockFinder · {price}
            {' · ' + _esc(data.price_source) if data.price_source != 'FMP' else ''}</div>
        </div>
      </div>
      <div class="spacer"></div>
      <span class="pill {dec_cls}"><span class="dot"></span>{_esc(d.label.upper())}</span>
      <div class="glob"><span class="v t-{dec_cls}">{gs}</span><span class="d">/100 · {_esc(d.confidence)}</span></div>
    </div>
    """)

    body.append('<div class="grid">')

    # --- veredicto ---
    val = _card(d.cards, "Valuation")
    verdict = val.extra.get("verdict", "N/D") if (val and val.data_sufficient) else "sin datos"
    review = _when_to_review(a) if d.label in ("Evitar", "Vigilar", "Sin decision") else "—"
    insufficient = ('<p class="warn-note">No tengo data suficiente para una conclusion '
                    f'(falta {d.missing_weight*100:.0f}% del peso).</p>'
                    if d.label == "Sin decision" else "")
    body.append(f"""
    <div class="card verdict col-8">
      <span class="eyebrow">Veredicto del Agente Principal</span>
      <div class="big t-{dec_cls}">{_esc(d.label)}</div>
      {insufficient}
      <div class="vgrid">
        <div class="b"><div class="q">Veredicto de precio</div><div class="a">{_esc(verdict)}</div></div>
        <div class="b"><div class="q">Cuando revisar</div><div class="a">{_esc(review)}</div></div>
      </div>
    </div>
    """)

    # --- gauge ---
    if d.global_score is not None:
        offset = _ARC * (1 - d.global_score / 100)
        arc = (f'<path d="M14 100 A86 86 0 0 1 186 100" fill="none" stroke="var(--{dec_cls})" '
               f'stroke-width="16" stroke-linecap="round" stroke-dasharray="{_ARC:.1f}" '
               f'stroke-dashoffset="{offset:.1f}"/>')
        gauge_val = f'<div class="val t-{dec_cls}">{gs}</div>'
    else:
        arc = ""
        gauge_val = '<div class="val t-nd">N/D</div>'
    on = {"bad": "z-bad", "warn": "z-warn", "good": "z-good"}.get(dec_cls, "")
    body.append(f"""
    <div class="card col-4">
      <h3>Scorecard global</h3><div class="cap">Suma ponderada de 6 agentes</div>
      <div class="gauge">
        <svg width="200" height="112" viewBox="0 0 200 112" role="img" aria-label="Puntaje {gs}">
          <path d="M14 100 A86 86 0 0 1 186 100" fill="none" stroke="var(--line-2)" stroke-width="16" stroke-linecap="round"/>
          {arc}
        </svg>
        {gauge_val}<div class="of">de 100</div>
      </div>
      <div class="zones">
        <div class="z-bad {on if dec_cls=='bad' else ''}">Evitar<br>&lt;55</div>
        <div class="z-warn {on if dec_cls=='warn' else ''}">Vigilar<br>55-69</div>
        <div class="z-good {on if dec_cls=='good' else ''}">Invertir<br>&ge;70</div>
      </div>
    </div>
    """)

    # --- puntaje por agente ---
    rows = []
    for c in d.cards:
        sc = f"{c.score:.0f}" if c.score is not None else "N/D"
        w = c.score if c.score is not None else 0
        cc = _cls(c.score)
        rows.append(f"""
        <div class="brow"><div class="nm">{_esc(c.agent)}<small>PESO {c.weight*100:.0f}%</small></div>
          <div class="track"><div class="fill f-{cc}" style="width:{w}%"></div></div>
          <div class="sc t-{cc}">{sc}</div></div>""")
    body.append(f"""
    <div class="card col-6">
      <h3>Puntaje por agente</h3><div class="cap">Peso x puntaje = aporte a la decision</div>
      <div class="bars">{''.join(rows)}</div>
    </div>
    """)

    # --- financial KPIs ---
    fin = _card(d.cards, "Financial")
    if fin and fin.data_sufficient:
        e = fin.extra
        g = e.get("growth")
        kpis = f"""
        <div class="kpi"><div class="k">Ingresos</div><div class="v">{fmt_money(e.get('revenue'))}
          {f'<small class="up">▲{g:.0f}%</small>' if g and g>=0 else (f'<small class="dn">▼{abs(g):.0f}%</small>' if g else '')}</div></div>
        <div class="kpi"><div class="k">Margen bruto</div><div class="v">{_pctd(e.get('gross_margin'))}</div></div>
        <div class="kpi"><div class="k">Margen FCF</div><div class="v">{_pctd(e.get('fcf_margin'))}</div></div>
        <div class="kpi"><div class="k">Deuda neta/EBITDA</div><div class="v">{_xd(e.get('debt_ebitda'))}</div></div>"""
    else:
        kpis = '<div class="nd-box">Sin datos financieros (FMP no cubre este ticker).</div>'
    body.append(f"""
    <div class="card col-6">
      <div class="card-head"><div><h3>Financiero</h3><div class="cap">Ultimo año fiscal (dato real)</div></div>
        <span class="tag t-{_cls(fin.score) if fin else 'nd'}">{('Puntaje '+f'{fin.score:.0f}') if fin and fin.score is not None else 'N/D'}</span></div>
      <div class="kpis">{kpis}</div>
    </div>
    """)

    # --- escenarios de precio ---
    body.append(_scenarios_html(val, data.price))

    # --- technical ---
    body.append(_technical_html(_card(d.cards, "Technical")))

    # --- risk ---
    body.append(_risk_html(_card(d.cards, "Risk"), a.profile))

    # --- insiders ---
    body.append(_insiders_html(a.insiders_relevantes))

    # --- inversionistas relacionados ---
    body.append("""
    <div class="card col-6">
      <h3>Inversionistas relacionados</h3><div class="cap">Con otras empresas exitosas</div>
      <div class="nd-box">Requiere fuente institucional (13F), no incluida en el plan actual.</div>
    </div>
    """)

    body.append("</div>")  # /grid

    # --- footer ---
    notes = ""
    if data.history_source == "Schwab" or data.price_source.startswith("Schwab"):
        notes += "Precio/tecnico via Schwab (FMP no cubre este ticker). "
    body.append(f"""
    <div class="foot">
      <strong>Datos:</strong> {notes}Historico = dato real; escenarios = estimacion tipo analista.
      Reporte <strong>informativo</strong>, no asesoria financiera regulada.
      Fuentes: FMP, Finnhub, FRED, Charles Schwab.
    </div>
    """)

    return f"<title>StockFinder · {_esc(a.symbol)}</title>\n{_CSS}\n<div class=\"wrap\">{''.join(body)}</div>"


def _scenarios_html(val, price) -> str:
    if not (val and val.data_sufficient and val.extra.get("scenarios")):
        return """
        <div class="card col-12"><h3>Escenarios de precio</h3>
          <div class="nd-box">Sin datos de valuacion suficientes para escenarios.</div></div>"""
    scn = val.extra["scenarios"]
    pts = [price] if price else []
    for s in scn.values():
        if s.get("rango"):
            pts += list(s["rango"])
    lo_s, hi_s = min(pts) * 0.94, max(pts) * 1.06
    span = hi_s - lo_s or 1

    def pos(x):
        return (x - lo_s) / span * 100

    colors = {"bajista": "bad", "base": "warn", "alcista": "good"}
    bands = []
    now = f'<div class="now-line" style="left:{pos(price):.1f}%"></div>' if price else ""
    for name, s in scn.items():
        rng = s.get("rango")
        if not rng:
            continue
        cc = colors.get(name, "warn")
        bands.append(f"""
        <div class="srow">{now}
          <div class="sband b-{cc}" style="left:{pos(rng[0]):.1f}%;width:{pos(rng[1])-pos(rng[0]):.1f}%">${rng[0]}-{rng[1]}</div></div>
        <div class="slabel"><span class="t-{cc}">{name.capitalize()}</span><span class="as">{_esc(s.get('supuesto',''))}</span></div>""")
    now_tag = (f'<div class="now-tag" style="left:{pos(price):.1f}%">Hoy ${price:.0f}</div>'
               if price else "")
    return f"""
    <div class="card col-12">
      <div class="card-head"><div><h3>Escenarios de precio</h3>
        <div class="cap">Rango, nunca un solo numero · supuestos etiquetados</div></div>
        <span class="tag t-{_cls(val.score)}">{('Valuation '+f'{val.score:.0f}') if val.score is not None else 'N/D'}</span></div>
      <div class="scn"><div class="srow" style="height:22px">{now_tag}</div>{''.join(bands)}</div>
      <div class="legend"><span><span class="swatch sw-solid"></span>Dato real</span>
        <span><span class="swatch sw-dash"></span>Estimacion (proyeccion)</span></div>
    </div>
    """


def _technical_html(tech) -> str:
    if not (tech and tech.data_sufficient):
        return """
        <div class="card col-7"><h3>Technical · niveles</h3>
          <div class="nd-box">Historico de precios insuficiente.</div></div>"""
    e = tech.extra
    rows = [
        (f"${e['resistance']:.0f}", "Resistencia / techo", "res"),
        (f"${e['price']:.0f}", "Precio actual", "now"),
        (f"${e['support']:.0f}", "Soporte / zona de entrada", "sup"),
    ]
    if e.get("sma200"):
        rows.append((f"${e['sma200']:.0f}", "Media movil 200 dias", "ma"))
    lr = "".join(f"""<div class="lrow"><div class="lv">{v}</div><div class="lb">{_esc(lb)}</div>
        <span class="chip c-{c}">{c.upper()}</span></div>""" for v, lb, c in rows)
    return f"""
    <div class="card col-7">
      <div class="card-head"><div><h3>Technical · niveles clave</h3>
        <div class="cap">RSI {e.get('rsi','N/D')} · entrada/salida</div></div>
        <span class="tag t-{_cls(tech.score)}">Puntaje {tech.score:.0f}</span></div>
      <div class="ladder">{lr}</div>
    </div>
    """


def _risk_html(rk, profile) -> str:
    if not rk:
        return '<div class="card col-5"><h3>Risk</h3><div class="nd-box">Sin datos.</div></div>'
    s = rk.extra.get("sizing", {})
    beta = rk.extra.get("beta")
    if s:
        conc = s["concentration"]
        seg_on = min(5, max(1, round(conc * 5)))
        segs = "".join(f'<i class="{"max" if i==4 else ("on" if i<seg_on else "")}"></i>' for i in range(5))
        detail = f"""
        <div class="seg">{segs}</div>
        <div class="rlab"><span>Media posicion: {s['shares_half']} acc</span>
          <span class="t-bad">{conc*100:.0f}% del capital</span></div>
        <div class="note">Entrada ${s['stop']}+ · stop ${s['stop']} · {s['shares_full']} acc = {fmt_money(s['position_value'])}</div>"""
    else:
        detail = '<div class="nd-box">Falta capital o soporte para dimensionar.</div>'
    cap = fmt_money(profile.capital) if profile.capital else "N/D"
    return f"""
    <div class="card col-5">
      <div class="card-head"><div><h3>Risk · tu perfil</h3>
        <div class="cap">Capital {cap} · perdida max 8-10%</div></div>
        <span class="tag t-{_cls(rk.score)}">Puntaje {rk.score:.0f}</span></div>
      <div class="rmeta">beta {beta:.2f}</div>{detail}
    </div>
    """ if beta is not None else f"""
    <div class="card col-5">
      <div class="card-head"><div><h3>Risk · tu perfil</h3><div class="cap">Capital {cap}</div></div>
        <span class="tag t-{_cls(rk.score)}">Puntaje {rk.score:.0f}</span></div>{detail}
    </div>
    """


def _insiders_html(insiders) -> str:
    if not insiders:
        items = '<div class="nd-box">Sin transacciones > $1M en el periodo disponible.</div>'
    else:
        items = ""
        for t in insiders[:6]:
            side = t["side"]
            ic = "ic-sell" if side == "venta" else "ic-buy"
            items += f"""
            <div class="li"><div class="ic {ic}">{'VE' if side=='venta' else 'CO'}</div>
              <div class="m"><div class="t">{_esc(t['name'])}</div>
                <div class="s">{t['change']:+} @ ${t['price']} · {_esc(t['date'])}</div></div>
              <div class="amt t-{'bad' if side=='venta' else 'good'}">{fmt_money(t['value'])}<small>{side.upper()}</small></div></div>"""
    return f"""
    <div class="card col-6">
      <h3>SEC Insiders</h3><div class="cap">Relevante = monto &gt; $1M</div>
      {items}
    </div>
    """


def _pctd(v):
    return f"{v:.1f}%" if v is not None else "N/D"


def _xd(v):
    return f"{v:.1f}x" if v is not None else "N/D"


_CSS = """<style>
:root{--bg:#eceef5;--card:#fff;--ink:#1c1e26;--ink-2:#5a5f6e;--ink-3:#8a90a0;--line-2:#eef0f6;
--accent:#6c5ce7;--accent-soft:#ece9fd;--good:#2fb37a;--good-soft:#e2f5ec;--warn:#e8a33d;--warn-soft:#fcefda;
--bad:#e85d7a;--bad-soft:#fce4ea;--nd:#8a90a0;--nd-soft:#eef0f6;
--shadow:0 1px 2px rgba(28,30,38,.04),0 8px 24px rgba(28,30,38,.06);--r:20px;
--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}
@media(prefers-color-scheme:dark){:root{--bg:#101118;--card:#191b24;--ink:#eef0f6;--ink-2:#a2a8ba;--ink-3:#6c7286;
--line-2:#20232e;--accent:#8b7bff;--accent-soft:#241f45;--good:#3ccb8a;--good-soft:#12281f;--warn:#f0b45a;
--warn-soft:#2c2413;--bad:#ff7593;--bad-soft:#2e1620;--nd:#6c7286;--nd-soft:#20232e;
--shadow:0 1px 2px rgba(0,0,0,.3),0 10px 30px rgba(0,0,0,.35);}}
:root[data-theme="light"]{--bg:#eceef5;--card:#fff;--ink:#1c1e26;--ink-2:#5a5f6e;--ink-3:#8a90a0;--line-2:#eef0f6;
--good:#2fb37a;--good-soft:#e2f5ec;--warn:#e8a33d;--warn-soft:#fcefda;--bad:#e85d7a;--bad-soft:#fce4ea;--nd:#8a90a0;--nd-soft:#eef0f6;}
:root[data-theme="dark"]{--bg:#101118;--card:#191b24;--ink:#eef0f6;--ink-2:#a2a8ba;--ink-3:#6c7286;--line-2:#20232e;
--good:#3ccb8a;--good-soft:#12281f;--warn:#f0b45a;--warn-soft:#2c2413;--bad:#ff7593;--bad-soft:#2e1620;--nd:#6c7286;--nd-soft:#20232e;}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);-webkit-font-smoothing:antialiased;
line-height:1.45;font-variant-numeric:tabular-nums}
.wrap{max-width:1120px;margin:0 auto;padding:28px 20px 60px}
h1,h3{margin:0}
.eyebrow{font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-3);font-weight:700}
.top{display:flex;flex-wrap:wrap;align-items:center;gap:14px 18px;margin-bottom:20px}
.tick{display:flex;align-items:center;gap:13px}
.logo{width:46px;height:46px;border-radius:13px;background:var(--ink);color:var(--card);display:grid;place-items:center;font-weight:800;font-size:15px}
.tick h1{font-size:22px;font-weight:800}
.tick .sub{color:var(--ink-2);font-size:13px}
.spacer{flex:1}
.pill{display:inline-flex;align-items:center;gap:8px;padding:8px 14px;border-radius:999px;font-weight:700;font-size:13px}
.pill.good{background:var(--good-soft);color:var(--good)}.pill.warn{background:var(--warn-soft);color:var(--warn)}
.pill.bad{background:var(--bad-soft);color:var(--bad)}.pill.nd{background:var(--nd-soft);color:var(--nd)}
.pill .dot{width:8px;height:8px;border-radius:50%;background:currentColor}
.glob{display:flex;align-items:baseline;gap:7px}.glob .v{font-size:26px;font-weight:800}.glob .d{color:var(--ink-3);font-size:13px}
.grid{display:grid;grid-template-columns:repeat(12,1fr);gap:16px}
.card{background:var(--card);border-radius:var(--r);box-shadow:var(--shadow);padding:20px;border:1px solid var(--line-2)}
.col-4{grid-column:span 4}.col-5{grid-column:span 5}.col-6{grid-column:span 6}.col-7{grid-column:span 7}.col-8{grid-column:span 8}.col-12{grid-column:span 12}
@media(max-width:860px){.col-4,.col-5,.col-6,.col-7,.col-8{grid-column:span 12}}
.card h3{font-size:15px;font-weight:700}
.card .cap{color:var(--ink-3);font-size:12px;margin-bottom:14px}
.card-head{display:flex;justify-content:space-between;align-items:flex-start;gap:10px}
.tag{font-size:11px;font-weight:700;padding:4px 9px;border-radius:8px;background:var(--line-2);color:var(--ink-2);white-space:nowrap}
.t-good{color:var(--good)}.t-warn{color:var(--warn)}.t-bad{color:var(--bad)}.t-nd{color:var(--nd)}
.nd-box{background:var(--nd-soft);color:var(--ink-2);border-radius:12px;padding:14px;font-size:12.5px}
.verdict{background:linear-gradient(135deg,var(--nd-soft),var(--card))}
.verdict .big{font-size:24px;font-weight:800;margin:4px 0}
.warn-note{margin:0 0 6px;color:var(--ink-2);font-size:13px}
.vgrid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px}
.vgrid .b{background:var(--card);border:1px solid var(--line-2);border-radius:12px;padding:11px 12px}
.vgrid .q{font-size:11px;color:var(--ink-3);font-weight:700;text-transform:uppercase;letter-spacing:.05em}
.vgrid .a{font-size:14px;font-weight:600;margin-top:3px}
.gauge{display:flex;flex-direction:column;align-items:center}
.gauge .val{font-size:38px;font-weight:800;margin-top:-44px}.gauge .of{color:var(--ink-3);font-size:13px}
.zones{display:flex;gap:6px;margin-top:14px;font-size:11px}
.zones div{flex:1;text-align:center;padding:6px 2px;border-radius:8px;font-weight:700}
.z-bad{background:var(--bad-soft);color:var(--bad)}.z-warn{background:var(--warn-soft);color:var(--warn)}.z-good{background:var(--good-soft);color:var(--good)}
.z-bad.z-bad,.z-warn.z-warn,.z-good.z-good{}
.zones .z-bad,.zones .z-warn,.zones .z-good{outline:2px solid transparent;outline-offset:-2px}
.zones .z-bad:where(.on){}
.bars{display:flex;flex-direction:column;gap:12px}
.brow{display:grid;grid-template-columns:104px 1fr 34px;align-items:center;gap:10px}
.brow .nm{font-size:13px;font-weight:600}
.brow .nm small{display:block;color:var(--ink-3);font-weight:600;font-size:10px;letter-spacing:.04em}
.track{height:9px;background:var(--line-2);border-radius:999px;overflow:hidden}
.fill{height:100%;border-radius:999px}
.f-good{background:var(--good)}.f-warn{background:var(--warn)}.f-bad{background:var(--bad)}.f-nd{background:var(--nd)}
.brow .sc{text-align:right;font-weight:800;font-size:14px}
.kpis{display:grid;grid-template-columns:1fr 1fr;gap:12px}
.kpi{background:var(--line-2);border-radius:14px;padding:14px}
.kpi .k{font-size:12px;color:var(--ink-2);font-weight:600}
.kpi .v{font-size:20px;font-weight:800;margin-top:4px}.kpi .v small{font-size:12px;font-weight:700}
.up{color:var(--good)}.dn{color:var(--bad)}
.scn{position:relative;margin-top:4px}
.srow{position:relative;height:42px;margin:0 6px}
.now-line{position:absolute;top:0;bottom:0;width:2px;background:var(--ink);border-radius:2px;z-index:3}
.now-tag{position:absolute;transform:translateX(-50%);background:var(--ink);color:var(--card);font-size:11px;font-weight:700;padding:3px 7px;border-radius:7px;white-space:nowrap}
.sband{position:absolute;height:26px;top:0;border-radius:8px;border:2px dashed;display:flex;align-items:center;justify-content:center;font-size:11.5px;font-weight:700}
.slabel{display:flex;justify-content:space-between;font-size:12px;margin:2px 6px 0}.slabel .as{color:var(--ink-3)}
.b-good{background:var(--good-soft);border-color:var(--good);color:var(--good)}
.b-warn{background:var(--warn-soft);border-color:var(--warn);color:var(--warn)}
.b-bad{background:var(--bad-soft);border-color:var(--bad);color:var(--bad)}
.legend{display:flex;flex-wrap:wrap;gap:14px;margin-top:14px;font-size:12px;color:var(--ink-2)}
.legend span{display:inline-flex;align-items:center;gap:7px}
.swatch{width:22px;border-top:3px solid var(--ink-2);border-radius:2px}.sw-dash{border-top-style:dashed;border-color:var(--accent)}
.ladder{display:flex;flex-direction:column}
.lrow{display:flex;align-items:center;gap:12px;padding:11px 0;border-bottom:1px solid var(--line-2)}.lrow:last-child{border-bottom:0}
.lrow .lv{width:80px;font-weight:800;font-size:14px}.lrow .lb{flex:1;font-size:12.5px;color:var(--ink-2)}
.chip{font-size:10px;font-weight:700;padding:3px 8px;border-radius:7px}
.c-res{background:var(--bad-soft);color:var(--bad)}.c-now{background:var(--accent-soft);color:var(--accent)}
.c-sup{background:var(--good-soft);color:var(--good)}.c-ma{background:var(--line-2);color:var(--ink-2)}
.rmeta{font-size:13px;color:var(--ink-2);font-weight:600;margin-bottom:4px}
.seg{display:flex;gap:4px;margin:12px 0 8px}.seg i{height:12px;flex:1;border-radius:4px;background:var(--line-2)}
.seg i.on{background:var(--warn)}.seg i.max{background:var(--bad)}
.rlab{display:flex;justify-content:space-between;font-size:12px;color:var(--ink-2)}
.note{margin-top:12px;padding:11px 13px;border-radius:12px;background:var(--accent-soft);color:var(--ink-2);font-size:12px;font-weight:600}
.li{display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid var(--line-2)}.li:last-child{border-bottom:0}
.li .ic{width:34px;height:34px;border-radius:11px;display:grid;place-items:center;font-weight:800;font-size:12px;flex-shrink:0}
.ic-sell{background:var(--bad-soft);color:var(--bad)}.ic-buy{background:var(--good-soft);color:var(--good)}
.li .m{flex:1;min-width:0}.li .m .t{font-weight:700;font-size:13px}.li .m .s{color:var(--ink-3);font-size:11px}
.li .amt{font-weight:800;font-size:14px;text-align:right;white-space:nowrap}.li .amt small{display:block;color:var(--ink-3);font-weight:600;font-size:10px}
.foot{margin-top:22px;color:var(--ink-3);font-size:11.5px;line-height:1.6}.foot strong{color:var(--ink-2)}
</style>"""
