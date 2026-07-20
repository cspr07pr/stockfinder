# Cerebro · 03 — Market Analysis

**Enfoque:** qué está pasando **fuera de la empresa**: su **sector**, el mercado
global y los índices. Contexto macro y sectorial.

---

## Pasos

1. **Sector / industria.** ¿En qué ciclo está? ¿Viento a favor o en contra?
   Tendencias estructurales (demanda, regulación, tecnología).
2. **Comparables (peers).** Cómo se comporta la acción vs. sus pares y vs. el
   ETF del sector.
3. **Mercado global e índices.** Estado de S&P 500 / Nasdaq, régimen (risk-on /
   risk-off), amplitud del mercado.
4. **Macro (FRED).** Tasas de interés, inflación, empleo, curva de rendimientos.
   ¿El entorno favorece a este tipo de empresa?
5. **Sensibilidad.** ¿La acción es cíclica, defensiva, sensible a tasas?

## Fuentes

- **FRED** (tasas, inflación, empleo, PIB, curva).
- FMP / Finnhub (sector performance, peers, índices).

## Reglas de puntuación

| Sub-métrica | Favorable si |
|---|---|
| Momentum del sector | Sector en tendencia alcista/estable |
| Posición vs. peers | La empresa lidera o mejora relativo |
| Régimen de mercado | Risk-on / amplitud sana |
| Entorno macro | Tasas/inflación favorables al perfil de la empresa |

## Banderas rojas

- Sector en declive estructural.
- Macro claramente adverso (p. ej. subida de tasas para empresa muy endeudada).

Devuelve el bloque de scorecard definido en `00-scorecard.md`.
