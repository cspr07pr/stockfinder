# referencias — Scorecard y visuales a conectar

Aquí viven (a) el **formato exacto del scorecard** que cada sub-agente entrega y
(b) el **catálogo de visuales** que el agente Visual debe reproducir. La lógica
de decisión está en `../Cerebro/`; aquí está el "cómo se ve y cómo se reporta".

## Contenido

| Archivo | Qué es |
|---|---|
| `scorecard-plantilla.md` | Plantilla rellenable del scorecard + ejemplo + JSON |
| `visuales.md` | Catálogo de visuales (mapea el dashboard de referencia a StockFinder) |
| `screen-hot-visual.png` | Referencia de estilo visual (dashboard fintech) |
| `ejemplos/aapl-dashboard.html` | **Ejemplo real** del reporte visual (AAPL) que aplica las 4 reglas |
| `../sub-agentes/valuation-analysis/valuation-toolkit.jpg` | Métodos de valuación de referencia |

> `ejemplos/aapl-dashboard.html` es la plantilla visual de referencia: gauge del
> scorecard, escenarios de precio como rangos con supuestos, niveles técnicos,
> KPIs financieros, riesgo dimensionado al perfil e insiders >$1M. Ábrelo en el
> navegador para ver el objetivo de diseño del agente Visual.

## Regla transversal
Todo visual respeta las 4 reglas de `../Cerebro/07-visual.md`:
rango (nunca una línea), supuestos etiquetados, histórico sólido / proyectado
punteado, y **el agente decide, no el gráfico**.
