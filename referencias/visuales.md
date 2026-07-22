# Catálogo de visuales a conectar

Mapea cada componente del dashboard de referencia (`screen-hot-visual.png`) a un
uso concreto en StockFinder, con el agente dueño y la regla visual que aplica.
Estilo objetivo: tarjetas limpias, mismo lenguaje visual del dashboard.

> Reglas de `../Cerebro/07-visual.md`: **rango** (nunca una línea sola),
> **supuestos etiquetados**, **histórico sólido / proyectado punteado**,
> **el agente decide, no el gráfico**.

---

## 1. Barras pareadas — (ref: tarjeta "Revenue", income vs expense)
- **Uso StockFinder:** ingresos vs. costos/gastos por periodo, o precio vs. volumen.
- **Agente:** Financial (02).
- **Reglas:** histórico en sólido; si se proyecta, barras futuras punteadas/atenuadas.

## 2. Burbujas proporcionales — (ref: "Weekly Expense", 48/32/13/7%)
- **Uso:** composición (mix de ingresos por segmento) **o** peso de cada agente
  en el scorecard global (25/20/20/15/10/10).
- **Agente:** Business (02/01) o Principal (scorecard).
- **Reglas:** etiquetar qué representa cada burbuja.

## 3. Medidor / gauge — (ref: "Saving Goal", $1,052 de $1,200)
- **Uso A:** **Scorecard global 0–100** con la zona de decisión
  (Evitar / Vigilar / Invertir).
- **Uso B:** precio actual vs. price target base (progreso hacia objetivo).
- **Agente:** Principal / Valuation (06).
- **Reglas:** mostrar el **rango** de targets, no solo un punto.

## 4. Barra de progreso segmentada — (ref: "Spending Limit", $252 de $1,200)
- **Uso:** tamaño de posición vs. **pérdida máxima tolerable (8–10%)**, o margen
  de seguridad consumido.
- **Agente:** Risk (05).
- **Reglas:** marcar el umbral 8–10% como límite duro.

## 5. Barras apiladas — (ref: "Daily Expense" por categoría)
- **Uso:** desglose en el tiempo (ingresos por segmento por trimestre) o aporte de
  cada agente al puntaje.
- **Agente:** Financial (02) / Principal.
- **Reglas:** histórico sólido; trimestres estimados punteados/atenuados.

## 6. Tarjetas-KPI con progreso — (ref: "Dream Car / House Saving", $X de $Y)
- **Uso:** una tarjeta por **escenario de precio** (bajista / base / alcista) con
  precio actual → target y su **supuesto** (crecimiento y margen).
- **Agente:** Valuation (06) + Visual (07).
- **Reglas:** cada tarjeta declara su supuesto; siempre 3 (rango, no un número).

## 7. Ítems de lista con icono y monto — (ref: "Spotify / Youtube / Google")
- **Uso:** lista de **SEC insiders >$1M** (insider, cargo, compra/venta, monto,
  fecha) e inversionistas relacionados.
- **Agente:** Principal (reporte, `../Cerebro/08-reporte-final.md`).
- **Reglas:** solo montos verificables; si no hay dato, declararlo.

---

## Gráfico técnico (no está en el dashboard, pero es obligatorio)
- **Uso:** precio histórico (línea sólida) con **zonas** de soporte/resistencia y
  bandas de entrada / stop / objetivo.
- **Agente:** Technical (04).
- **Reglas:** zonas, no precios únicos; stop dentro del 8–10%.

## Panel de valuación (ref: `valuation-toolkit.jpg`)
- **Uso:** al presentar los price targets, indicar **qué métodos** se usaron
  (DCF, múltiplos, DDM…) y el **margen de seguridad** aplicado:
  Riesgo Bajo 20–30% · Medio 30–50% · Alto 50%+.
- **Agente:** Valuation (06).
- **Principio:** ningún modelo es perfecto; usar varios y **respetar el rango**.
