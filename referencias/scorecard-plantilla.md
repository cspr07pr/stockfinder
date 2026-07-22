# Scorecard — Plantilla oficial

Formato **obligatorio** que cada sub-agente entrega al Agente Principal. La
definición de escala, pesos y regla de decisión está en
`../Cerebro/00-scorecard.md`. Aquí está la plantilla lista para rellenar.

---

## Plantilla (texto)

```
Agente: <Business | Financial | Market | Technical | Risk | Valuation>
Suficiencia de datos: <Sí | No>
Puntaje: <0–100 | N/D>
Confianza: <Alta | Media | Baja>
Sub-métricas:
  - <métrica>: <valor> → <puntos>
  - <métrica>: <valor> → <puntos>
Banderas rojas: <lista | ninguna>
Resumen: <2–3 líneas>
```

Si `Suficiencia de datos: No` → `Puntaje: N/D` y el resumen dice:
«No tengo data suficiente para llegar a una conclusión de inversión.»

---

## Formato JSON (para el Principal)

```json
{
  "agente": "Financial",
  "suficiencia_datos": true,
  "puntaje": 72,
  "confianza": "Media",
  "peso": 0.20,
  "sub_metricas": [
    { "nombre": "Crecimiento ingresos (CAGR 3a)", "valor": "12%", "puntos": 75 },
    { "nombre": "Margen operativo (tendencia)", "valor": "+2pp", "puntos": 80 },
    { "nombre": "Deuda/EBITDA", "valor": "1.4x", "puntos": 70 },
    { "nombre": "Free Cash Flow", "valor": "+creciente", "puntos": 78 }
  ],
  "banderas_rojas": [],
  "resumen": "Crecimiento sano y FCF positivo; balance conservador."
}
```

---

## Ejemplo agregado (lo que arma el Principal)

```
DECISIÓN: Vigilar   ·   Puntaje global: 63/100   ·   Confianza: Media

| Agente      | Peso | Puntaje | Confianza | Banderas |
|-------------|------|---------|-----------|----------|
| Financial   | 20%  | 72      | Media     | —        |
| Valuation   | 20%  | 55      | Media     | —        |
| Risk        | 25%  | 60      | Alta      | —        |
| Business    | 15%  | 78      | Alta      | —        |
| Market      | 10%  | 58      | Media     | —        |
| Technical   | 10%  | 50      | Baja      | —        |

Global = 0.20·72 + 0.20·55 + 0.25·60 + 0.15·78 + 0.10·58 + 0.10·50 = 63
```

Regla de decisión (de `../Cerebro/00-scorecard.md`):
≥70 Invertir · 55–69 **Vigilar** · <55 Evitar · bandera crítica = veto.
