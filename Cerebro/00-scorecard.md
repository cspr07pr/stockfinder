# Cerebro · 00 — Scorecard y regla de decisión

Este archivo define **cómo puntúa cada sub-agente** y **cómo el Agente Principal
agrega** todo en una decisión final. Es la columna vertebral del sistema.

---

## 1. Formato de salida de cada sub-agente

Cada sub-agente **debe** devolver este bloque (sin excepción):

```
Agente: <nombre>
Suficiencia de datos: Sí | No
Puntaje: 0–100
Confianza: Alta | Media | Baja
Sub-métricas:
  - <métrica>: <valor> → <puntos>
  - ...
Banderas rojas: [lista o "ninguna"]
Resumen: <2–3 líneas>
```

Si **Suficiencia de datos = No**, el puntaje se reporta como `N/D` y el resumen
dice: «No tengo data suficiente para llegar a una conclusión de inversión.»
El Principal **no** debe rellenar ese hueco inventando.

---

## 2. Escala de puntaje (común a todos)

| Rango | Lectura |
|---|---|
| 80–100 | Muy favorable |
| 65–79 | Favorable |
| 50–64 | Neutral / mixto |
| 35–49 | Desfavorable |
| 0–34 | Muy desfavorable |

---

## 3. Pesos por defecto en la decisión global

Ajustables por el usuario. Suman 100%.

| Sub-agente | Peso |
|---|---|
| Financial Analysis | 20% |
| Valuation Analysis | 20% |
| **Risk Analysis** | **25%** |
| Business Analysis | 15% |
| Market Analysis | 10% |
| Technical / Momentum | 10% |

> Risk pesa más porque el usuario es **principiante** y prioriza la gestión de
> riesgo y el *timing*. Visual no puntúa: **presenta**, no decide.

**Puntaje global** = Σ (puntaje_agente × peso_agente).

Si algún agente devuelve `N/D`, el Principal lo marca y **reduce la confianza
global**; no lo cuenta como 0 ni como 100.

---

## 4. Banderas rojas críticas (veto)

Anulan un puntaje alto y fuerzan **Evitar** aunque el global sea bueno:

- Riesgo de la posición **excede la pérdida tolerable del perfil (8–10%)** sin
  un punto de salida claro.
- Señal contable grave (deuda insostenible, flujo de caja negativo estructural,
  dilución agresiva).
- Insider **selling** > $1M concentrado y sin contexto que lo explique.
- Acción rompe un soporte técnico mayor con volumen (tesis técnica invalidada).

---

## 5. Regla de decisión final

| Puntaje global | Banderas rojas | Decisión |
|---|---|---|
| ≥ 70 | ninguna crítica | **Invertir** (buen precio / oportunidad) |
| 55–69 | ninguna crítica | **Vigilar** — esperar mejor entrada/confirmación |
| < 55 | cualquiera | **Evitar** |
| cualquiera | ≥ 1 crítica | **Evitar** (veto) |

La decisión **siempre** se acompaña de **puntos de entrada y salida** y el
*timing* sugerido (prioridad del perfil).

---

## 6. ¿Cuándo revisar de nuevo? (si la decisión es Evitar/Vigilar)

Depende del motivo:

| Motivo del "Evitar/Vigilar" | Revisar en |
|---|---|
| Sobrevaluada (cara, pero buen negocio) | Próximo *earnings* o 1–2 trimestres |
| Técnica débil (sin soporte cerca) | Cuando toque el soporte clave identificado |
| Fundamentales deteriorándose | 2 trimestres (confirmar tendencia) |
| Falta de datos | Cuando haya nueva fuente/reporte disponible |

Siempre dar una **fecha o condición concreta**, no un "más adelante".
