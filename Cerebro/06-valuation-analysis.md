# Cerebro · 06 — Valuation Analysis

**Enfoque:** con los datos de **Financial Analysis (02)**, determinar qué
valuaciones aplicar y asignar **price targets**. Aquí se contesta: ¿la acción está
**barata, justa o cara**?

> Depende de 02. No empezar sin el scorecard de Financial Analysis.

---

## Pasos

1. **Elegir métodos según el tipo de empresa.**
   - Múltiplos relativos: P/E, EV/EBITDA, P/S, P/FCF vs. peers e histórico propio.
   - Flujo descontado (DCF) si hay FCF estable y predecible.
   - Casos especiales: P/B para financieras, crecimiento para growth.
2. **Definir supuestos y ETIQUETARLOS.** Tasa de crecimiento, margen, tasa de
   descuento, múltiplo de salida. Cada escenario declara sus supuestos.
3. **Construir 3 escenarios (rango, nunca un solo número):**
   - **Bajista / conservador**
   - **Base**
   - **Alcista / optimista**
4. **Price targets.** Traducir cada escenario a un **rango de precio** y compararlo
   con el precio actual → margen de seguridad (upside/downside).
5. **Veredicto de precio.** Barata / justa / cara, con el margen de seguridad.

## Fuentes

- FMP (múltiplos, estimados de analistas, históricos).
- Finnhub (consensus/estimates) como referencia externa tipo analista.

## Reglas duras

- **Nunca un único valor:** siempre un **rango** de price target.
- **Etiquetar supuestos** en cada escenario (crecimiento y margen mínimo).
- **Histórico sólido, proyectado punteado** (coordinación con Visual, 07).
- Si no hay base financiera suficiente (02 = N/D) → Valuación = `N/D`.

## Reglas de puntuación

| Sub-métrica | Favorable si |
|---|---|
| Margen de seguridad | Precio actual bajo el escenario base |
| Múltiplos vs. historia/peers | En descuento razonable |
| Consistencia de supuestos | Conservadores y justificados |

## Bandera roja

- Solo se justifica la compra con supuestos extremos (crecimiento irreal).

Devuelve el bloque de scorecard definido en `00-scorecard.md`.
