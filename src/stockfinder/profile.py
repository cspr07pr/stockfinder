"""Perfil del inversionista (refleja CLAUDE.md 3 y perfil de inversionistas/).

El capital disponible NO se versiona: se pasa en tiempo de ejecucion
(por ejemplo `analyze AAPL --capital 25000`).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class InvestorProfile:
    objetivo: str = "Crecer el capital"
    horizonte_anios: tuple[int, int] = (3, 5)
    max_loss_pct: float = 0.10          # tope duro de perdida por posicion (8-10%)
    reaccion_caida: str = "Mantener o comprar"
    experiencia: str = "Principiante"
    estilo: str = "Agresivo / especulativo"
    frecuencia: str = "Mensual"
    prioridad: str = "Puntos de entrada/salida y timing"
    capital: float | None = None        # se define en runtime

    # Umbral para diversificacion: fraccion max. sugerida del capital en 1 nombre.
    max_concentracion_sugerida: float = 0.5


DEFAULT_PROFILE = InvestorProfile()
