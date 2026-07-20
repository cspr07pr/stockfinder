# Cerebro — Reglas y pasos del sistema

El "cómo pensar" de cada agente. El Agente Principal y los sub-agentes **deben
seguir** estas reglas antes de concluir. Ver `../CLAUDE.md` para la orquestación.

## Índice

| Archivo | Contenido |
|---|---|
| `00-scorecard.md` | Formato de salida, pesos, banderas rojas y **regla de decisión** |
| `01-business-analysis.md` | Negocio, moat, competencia, management |
| `02-financial-analysis.md` | Crecimiento, márgenes, balance, flujo de caja |
| `03-market-analysis.md` | Sector, índices, macro (FRED) |
| `04-technical-momentum.md` | Soportes/resistencias, momentum, entrada/salida |
| `05-risk-analysis.md` | Riesgo de la empresa + encaje con el perfil |
| `06-valuation-analysis.md` | Valuaciones y price targets (depende de 02) |
| `07-visual.md` | Reglas de presentación visual |
| `08-reporte-final.md` | Ensamblaje del reporte final |

## Orden de ejecución

```
Principal (entiende input + info general)
  → 01 Business → 02 Financial → 03 Market → 04 Technical
  → 06 Valuation (usa 02) → 05 Risk
  → 07 Visual (consolida) → 08 Reporte final
```

## Principio rector

Si no hay data suficiente, **decirlo**. La lógica manda; el gráfico solo ilustra.
