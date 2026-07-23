"""Scorecard y regla de decision (implementa Cerebro/00-scorecard.md).

Cada sub-agente devuelve un Scorecard; el Agente Principal los agrega con pesos
y produce una Decision (Invertir / Vigilar / Evitar). Una bandera roja critica
veta y fuerza Evitar aunque el puntaje global sea alto.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Pesos por defecto (suman 1.0). Ajustables. Visual no puntua.
WEIGHTS: dict[str, float] = {
    "Business": 0.15,
    "Financial": 0.20,
    "Market": 0.10,
    "Technical": 0.10,
    "Valuation": 0.20,
    "Risk": 0.25,
}

DATA_INSUFFICIENT = "No tengo data suficiente para llegar a una conclusion de inversion."


@dataclass
class SubMetric:
    name: str
    value: str
    points: int  # 0-100


@dataclass
class Scorecard:
    agent: str
    data_sufficient: bool = True
    score: float | None = None          # 0-100, o None si N/D
    confidence: str = "Media"           # Alta | Media | Baja
    submetrics: list[SubMetric] = field(default_factory=list)
    red_flags: list[str] = field(default_factory=list)
    critical_flags: list[str] = field(default_factory=list)  # vetan (Evitar)
    summary: str = ""
    extra: dict = field(default_factory=dict)  # datos utiles para el reporte

    @property
    def weight(self) -> float:
        return WEIGHTS.get(self.agent, 0.0)

    @classmethod
    def insufficient(cls, agent: str, reason: str = "") -> "Scorecard":
        return cls(
            agent=agent, data_sufficient=False, score=None, confidence="Baja",
            summary=DATA_INSUFFICIENT + (f" ({reason})" if reason else ""),
        )


@dataclass
class Decision:
    label: str                 # Invertir | Vigilar | Evitar | Sin decision
    global_score: float | None
    confidence: str
    missing_weight: float      # 0-1: peso de agentes sin datos
    critical_flags: list[str]
    cards: list[Scorecard]


def _confidence_num(c: str) -> int:
    return {"Alta": 3, "Media": 2, "Baja": 1}.get(c, 2)


def _num_confidence(n: float) -> str:
    if n >= 2.5:
        return "Alta"
    if n >= 1.6:
        return "Media"
    return "Baja"


def aggregate(cards: list[Scorecard]) -> Decision:
    """Combina los scorecards en una decision (ver Cerebro/00-scorecard.md)."""
    scored = [c for c in cards if c.data_sufficient and c.score is not None]
    total_w = sum(c.weight for c in scored)
    missing_w = round(1.0 - total_w, 3)

    if total_w > 0:
        global_score = round(sum(c.score * c.weight for c in scored) / total_w, 1)  # type: ignore[operator]
    else:
        global_score = None

    # Confianza: promedio ponderado de las confianzas, penalizado por datos faltantes.
    if scored:
        conf_num = sum(_confidence_num(c.confidence) * c.weight for c in scored) / total_w
    else:
        conf_num = 1.0
    if missing_w > 0.25:
        conf_num = min(conf_num, 1.4)   # muchos datos faltan -> Baja
    elif missing_w > 0.10:
        conf_num = min(conf_num, 2.2)   # algunos faltan -> tope Media
    confidence = _num_confidence(conf_num)

    critical = [f"[{c.agent}] {flag}" for c in cards for flag in c.critical_flags]

    # Regla de decision
    if critical:
        label = "Evitar"
    elif global_score is None:
        label = "Sin decision"
    elif global_score >= 70:
        label = "Invertir"
    elif global_score >= 55:
        label = "Vigilar"
    else:
        label = "Evitar"

    return Decision(
        label=label, global_score=global_score, confidence=confidence,
        missing_weight=missing_w, critical_flags=critical, cards=cards,
    )
