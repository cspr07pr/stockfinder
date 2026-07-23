# Perfil del inversionista

Perfil que condiciona **todo** el análisis, en especial Risk Analysis (05) y las
recomendaciones de entrada/salida. Es la fuente de verdad del perfil; el resumen
en `../CLAUDE.md` §3 debe coincidir con este archivo.

> Última actualización: 2026-07-22

---

## 1. Objetivo y horizonte

| Dimensión | Valor |
|---|---|
| Objetivo principal | **Crecer el capital** |
| Horizonte para alcanzarlo | **3–5 años** |
| Expectativa de retorno | **~$500–1000 mensuales** |
| ¿Retiro de capital próximo? | **No** |

## 2. Tolerancia al riesgo

| Dimensión | Valor |
|---|---|
| Pérdida máxima tolerable | **8–10%** |
| Reacción ante −15% en pocas semanas | **Mantener o comprar** |
| Estilo de inversión | **Agresivo / especulativo** |

> El límite de **8–10%** es un tope duro: Risk (05) y Technical (04) deben ubicar
> el **stop** dentro de ese rango; si no es posible, la operación no es accionable.

## 3. Operativa

| Dimensión | Valor |
|---|---|
| Experiencia | **Principiante** |
| Instrumentos | **Acciones, ETF, opciones** |
| Frecuencia de operación | **Mensual** |
| Prioridad al recomendar | **Puntos de entrada/salida y *timing* de posiciones** |

## 4. Implicaciones para los agentes

- **Risk (05):** peso mayor (25%). Dimensiona posición contra el 8–10% y valida
  el escenario −15% (el perfil dice mantener/comprar → debe haber liquidez).
- **Technical (04):** foco en zonas de entrada/salida y timing (prioridad).
- **Valuation (06):** margen de seguridad acorde a estilo agresivo, pero sin
  justificar compras con supuestos irreales.
- Por ser **principiante**, el reporte explica el "por qué" en lenguaje claro.

---

## 5. Datos pendientes (Claude debe pedirlos)

Estos datos faltan y el Agente Principal debe solicitarlos antes de dimensionar
posiciones:

- [ ] **Capital disponible** para invertir: `<pendiente>`
- [ ] **Reglas de gestión de riesgo** propias (p. ej. % máx. por posición,
      diversificación, uso de stop-loss, apalancamiento en opciones):
      `<pendiente>`

> Mientras estén pendientes, Risk (05) trabaja con supuestos **etiquetados** y lo
> declara; no inventa cifras de capital.
