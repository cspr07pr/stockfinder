# Cerebro · 05 — Risk Analysis

**Enfoque:** dos riesgos a la vez → (a) el **riesgo de poseer esta empresa** y
(b) el **encaje con el perfil del inversionista**. Es el agente de **mayor peso**
(25%) porque el usuario es principiante y prioriza la gestión de riesgo.

---

## Perfil del inversionista (referencia)

| Dimensión | Valor |
|---|---|
| Horizonte | 3–5 años |
| Pérdida máxima tolerable | **8–10%** |
| Reacción a −15% | Mantener o comprar |
| Experiencia | Principiante |
| Estilo | Agresivo / especulativo |
| Instrumentos | Acciones, ETF, opciones |
| Frecuencia | Mensual |

> El perfil completo vive en `perfil de inversionistas/`. Pedir **capital
> disponible** y **reglas de gestión de riesgo** si no se conocen.

## Pasos

1. **Riesgo de la empresa.** Volatilidad (beta), drawdowns históricos, riesgo de
   negocio/financiero (enlaza con 01 y 02), riesgos regulatorios/legales.
2. **Encaje con el perfil.** ¿La volatilidad esperada cabe en la tolerancia de
   8–10%? ¿El horizonte de la tesis coincide con 3–5 años?
3. **Dimensionar la posición.** Con el capital disponible y la pérdida máxima,
   calcular tamaño de posición y **stop** coherente (position sizing).
4. **Escenario adverso.** ¿Qué pasa si cae −15%? Según el perfil, mantener/comprar
   — validar que el plan lo permite (liquidez, sin retiro próximo).

## Reglas de puntuación

| Sub-métrica | Favorable si |
|---|---|
| Volatilidad vs. tolerancia | La posición dimensionada respeta 8–10% |
| Riesgo de negocio/financiero | Bajo o controlado |
| Encaje de horizonte | Tesis madura en 3–5 años |
| Liquidez/flexibilidad | Sin necesidad de retirar capital |

## Bandera roja (crítica · veto)

- El riesgo de la posición **excede la pérdida tolerable (8–10%)** sin un punto
  de salida claro → fuerza **Evitar**.

Devuelve el bloque de scorecard definido en `00-scorecard.md`.
