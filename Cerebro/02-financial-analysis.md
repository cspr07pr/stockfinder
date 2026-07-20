# Cerebro · 02 — Financial Analysis

**Enfoque:** analizar **los datos financieros**. Es la base cuantitativa que
alimenta la Valuación (06). Trabaja con hechos, no narrativas.

---

## Pasos

1. **Crecimiento.** Ingresos y utilidades: tasa de crecimiento (YoY y CAGR
   3–5 años). ¿Acelera o desacelera?
2. **Rentabilidad.** Márgenes bruto, operativo y neto. Tendencia. ROE / ROIC.
3. **Solidez del balance.** Deuda neta, deuda/EBITDA, liquidez (current ratio),
   cobertura de intereses.
4. **Flujo de caja.** Free Cash Flow: ¿positivo y creciente? Conversión de
   utilidad a caja. FCF margin.
5. **Calidad de las ganancias.** ¿La utilidad se respalda con caja? Dilución de
   acciones (shares outstanding en el tiempo).

## Fuentes

- **FMP** (income statement, balance sheet, cash flow, ratios).
- Finnhub (métricas básicas y estimados).

## Reglas de puntuación

| Sub-métrica | Favorable si |
|---|---|
| Crecimiento de ingresos | Sostenido y sano (no solo por adquisiciones) |
| Márgenes | Estables o en expansión |
| ROIC / ROE | Por encima del costo de capital |
| Apalancamiento | Deuda/EBITDA baja, buena cobertura |
| Free Cash Flow | Positivo, creciente, buena conversión |
| Dilución | Acciones estables o recompras |

## Reglas duras

- Distinguir **dato reportado (histórico)** de **estimado**. Nunca mezclarlos sin
  etiqueta.
- Si faltan estados financieros clave → `Suficiencia de datos: No`.

## Banderas rojas (críticas)

- FCF **negativo estructural** (varios años).
- Deuda insostenible / cobertura de intereses < 1.5x.
- Dilución agresiva y recurrente.

Devuelve el bloque de scorecard definido en `00-scorecard.md`.
