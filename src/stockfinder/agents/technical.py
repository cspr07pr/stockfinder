"""Sub-agente Technical / Momentum (Cerebro/04).

Lee el historico de precios: tendencia (medias 50/200), momentum (RSI),
soportes/resistencias y zonas de entrada/salida. El stop debe caber en la
perdida maxima del perfil (8-10%); si no, la senal no es accionable.
"""

from __future__ import annotations

from ..profile import DEFAULT_PROFILE
from ..scorecard import Scorecard, SubMetric
from .base import avg, lin

NAME = "Technical"


def run(bundle, profile=None) -> Scorecard:
    profile = profile or DEFAULT_PROFILE
    hist = bundle.history
    if not hist or len(hist) < 60:
        return Scorecard.insufficient(NAME, "historico insuficiente")

    # precios: la fuente los da mas reciente primero
    closes = [h["price"] for h in hist if isinstance(h.get("price"), (int, float))]
    price = closes[0]
    sma50 = _sma(closes, 50)
    sma200 = _sma(closes, 200)
    rsi = _rsi(closes, 14)

    recent = closes[:22]           # ~1 mes de trading
    yearly = closes[:252]          # ~1 anio
    recent_low, recent_high = min(recent), max(recent)
    low_52, high_52 = min(yearly), max(yearly)

    above_200 = sma200 is not None and price > sma200
    dist_200 = ((price / sma200 - 1) * 100) if sma200 else None

    # soporte de referencia (mas cercano por debajo del precio)
    supports = sorted([s for s in [recent_low, sma200, low_52] if s and s < price], reverse=True)
    support = supports[0] if supports else recent_low
    resistance = max(recent_high, high_52)

    # zona de entrada/stop/objetivo
    entry_zone = (round(support), round(support * 1.03))
    stop = round(support * 0.97)
    stop_pct = (price - stop) / price * 100
    target = round(resistance)

    # --- puntuacion ---
    subs = [
        SubMetric("Tendencia (vs 200 DMA)",
                  f"{'sobre' if above_200 else 'bajo'} 200DMA ({_p(dist_200)})",
                  lin(dist_200, -15, 15) if dist_200 is not None else 50),
        SubMetric("Momentum (RSI 14)", f"{rsi:.0f}" if rsi else "N/D", _rsi_score(rsi)),
        SubMetric("Cercania a soporte",
                  f"soporte ${support:.0f} ({(price/support-1)*100:+.1f}%)",
                  lin((price / support - 1) * 100, 15, 0)),  # mas cerca = mejor entrada
    ]
    score = avg([s.points for s in subs])

    red, crit = [], []
    if sma200 and price < sma200 * 0.95:
        crit.append("Precio rompio soporte mayor (bajo 200 DMA)")
    if rsi and rsi > 75:
        red.append(f"Sobrecompra (RSI {rsi:.0f})")
    if stop_pct > profile.max_loss_pct * 100:
        red.append(f"Stop natural ({stop_pct:.1f}%) excede tu perdida maxima")

    summary = (
        f"{'Sobre' if above_200 else 'Bajo'} 200DMA (${_n(sma200)}), RSI {_n(rsi)}. "
        f"Soporte ${support:.0f}, resistencia ${resistance:.0f}. "
        f"Entrada ${entry_zone[0]}-{entry_zone[1]}, stop ${stop}."
    )

    return Scorecard(
        agent=NAME, score=score,
        confidence="Alta" if sma200 else "Media",
        submetrics=subs, red_flags=red, critical_flags=crit, summary=summary,
        extra={"price": price, "sma50": sma50, "sma200": sma200, "rsi": rsi,
               "support": support, "resistance": resistance, "recent_low": recent_low,
               "recent_high": recent_high, "low_52": low_52, "high_52": high_52,
               "entry_zone": entry_zone, "stop": stop, "stop_pct": stop_pct,
               "target": target},
    )


def _sma(closes, n):
    return round(sum(closes[:n]) / n, 2) if len(closes) >= n else None


def _rsi(closes, n=14):
    if len(closes) < n + 1:
        return None
    # closes vienen mas reciente primero; recorremos hacia el pasado
    gains, losses = 0.0, 0.0
    for i in range(n):
        delta = closes[i] - closes[i + 1]
        if delta >= 0:
            gains += delta
        else:
            losses -= delta
    if losses == 0:
        return 100.0
    rs = (gains / n) / (losses / n)
    return round(100 - 100 / (1 + rs), 1)


def _rsi_score(rsi):
    if rsi is None:
        return 50
    # ideal 40-65 (sano, sin sobrecompra); penaliza extremos
    if 40 <= rsi <= 65:
        return 85
    if 30 <= rsi < 40:
        return 70   # algo sobrevendido = posible entrada
    if 65 < rsi <= 75:
        return 55
    if rsi > 75:
        return 30   # sobrecompra
    return 45       # <30 muy sobrevendido


def _p(v):
    return f"{v:+.1f}%" if v is not None else "N/D"


def _n(v):
    return f"{v:.0f}" if v is not None else "N/D"
