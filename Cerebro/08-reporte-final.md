# Cerebro · 08 — Ensamblaje del reporte final

El Agente Principal integra los scorecards y produce el reporte. Estructura
mínima obligatoria:

---

## 1. Encabezado
- Empresa / ticker, fecha, precio actual.
- **Decisión:** Invertir / Vigilar / Evitar (regla de `00-scorecard.md`).
- **Puntaje global** y confianza.

## 2. Veredicto de precio
- ¿Buen precio? (barata / justa / cara, de Valuation 06).
- **Si Evitar/Vigilar:** cuándo revisar de nuevo (tabla de `00-scorecard.md`).

## 3. Puntos de entrada, salida y timing
- Zona de entrada, stop (respetando 8–10%) y objetivos (de Technical 04 + Risk 05).
- *Timing* sugerido — prioridad del perfil.

## 4. Escenarios de precio
- Rango de precios bajista / base / alcista (de Valuation 06).
- Supuestos etiquetados. Histórico sólido, proyección punteada.

## 5. Resumen por sub-agente
- Una fila por agente: puntaje, confianza, resumen, banderas rojas.

## 6. Inversionistas relacionados
- Inversionistas importantes o relacionados que tengan **otras empresas
  exitosas**. Solo con fuente verificable; si no hay dato → declararlo.

## 7. SEC Insider Buying & Selling
- Listar compras/ventas de *insiders* **relevantes**.
- **Relevante = monto total > $1M USD.** Debajo de ese umbral, se omite.
- Indicar: insider, cargo, tipo (compra/venta), monto, fecha.
- Fuente: registros SEC (Form 4) vía FMP/Finnhub.

## 8. Entrega visual
- Gráficas según `07-visual.md` y los formatos de `referencias/`.

---

## Regla transversal
Si el sistema no tiene datos suficientes en un bloque, ese bloque dice
explícitamente: «No tengo data suficiente para llegar a una conclusión de
inversión.» No se inventa ni se interpola.
