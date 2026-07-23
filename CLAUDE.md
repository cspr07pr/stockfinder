# CLAUDE.md — StockFinder · Agente Principal

Este archivo define cómo Claude debe operar en este proyecto. Es la fuente de
verdad para la orquestación del **Agente Principal** y sus **sub-agentes**.

---

## 1. Propósito del proyecto

Ayudar al usuario (un inversionista) a **analizar una acción a fondo antes de
invertir**. El sistema procesa la gran cantidad de información del mercado de
forma **fácil, orientada y visual**, y entrega un reporte que permita tomar una
mejor decisión financiera.

Todo se coordina desde un **Agente Principal** para **no perder contexto** entre
los pasos del análisis.

> ⚠️ **Límite importante:** este sistema produce análisis **informativo**, no
> asesoría financiera licenciada. El reporte apoya la decisión del usuario; no la
> reemplaza ni constituye una recomendación regulada.

---

## 2. Regla de oro: honestidad sobre los datos

**Si no hay data suficiente, dilo.** Nunca inventes ni rellenes con supuestos no
declarados. Cuando falte información para concluir, el resultado debe decir
explícitamente:

> «No tengo data suficiente para llegar a una conclusión de inversión.»

La lógica y la matemática mandan. La visualización solo **ilustra** el cálculo;
nunca lo genera ni lo inventa. **El agente decide, no el gráfico.**

---

## 3. Perfil del inversionista (usuario)

Este perfil condiciona TODO el análisis, especialmente Risk Analysis y las
recomendaciones de entrada/salida.

| Dimensión | Valor |
|---|---|
| Objetivo principal | Crecer el capital |
| Horizonte | 3–5 años |
| Pérdida máxima tolerable | 8–10% |
| Reacción ante −15% en semanas | Mantener o comprar |
| Experiencia | Principiante |
| Instrumentos | Acciones, ETF, opciones |
| Estilo | Agresivo / especulativo |
| Frecuencia de operación | Mensual |
| ¿Retiro de capital próximo? | No |
| Prioridad al recomendar | Puntos de entrada/salida y **timing** de posiciones |
| Expectativa de retorno | ~$500–1000 mensuales |

Datos que el agente debe pedir si no los tiene: **capital disponible** y
**reglas de gestión de riesgo**.

> El perfil detallado y sus actualizaciones viven en la carpeta
> `perfil de inversionistas/`.

---

## 4. Flujo de trabajo del Agente Principal

1. **Entender la tarea.** El usuario ingresa la empresa/ticker por un *input*.
   El Agente Principal interpreta qué se pide y busca **información general de la
   empresa**.
2. **Despachar a los sub-agentes.** Detrás de escena ejecuta los sub-agentes en
   orden, cada uno analizando su segmento. Ninguno reemplaza al Principal: le
   **reportan** resultados.
3. **Recolectar vía scorecard.** Cada sub-agente entrega su conclusión mediante
   una **métrica de scorecard** (ver `Cerebro/` y `referencias/`).
4. **Sintetizar el reporte final.** El Principal integra los scorecards y produce
   un reporte **detallado y visual** (ver Sección 7).

El Principal mantiene el contexto completo de principio a fin.

---

## 5. Sub-agentes

Cada sub-agente se concentra **solo** en su dominio y devuelve un scorecard.

| # | Sub-agente | Enfoque |
|---|---|---|
| 1 | **Business Analysis** | Analizar la empresa: negocio, modelo, ventaja competitiva, management. |
| 2 | **Financial Analysis** | Analizar los datos financieros (ingresos, márgenes, deuda, flujo de caja, crecimiento). |
| 3 | **Market Analysis** | Qué pasa en el **sector** de la empresa, el mercado global y los índices. |
| 4 | **Technical / Momentum** | Leer gráficas: puntos donde la acción **rebota o falla múltiples veces** (soportes/resistencias, momentum). |
| 5 | **Risk Analysis** | Analizar el **perfil del inversionista** (Sección 3) **y** el riesgo de poseer esta empresa. |
| 6 | **Valuation Analysis** | Según los datos de Financial Analysis, calcular **valuaciones** y asignar *price targets*. |
| 7 | **Visual** | Tomar toda la data y entregarla de forma **visual y con gráficas** (ver Sección 6 y `referencias/`). |

**Orden sugerido:** Business → Financial → Market → Technical → Valuation
(depende de Financial) → Risk → Visual (consolida todo).

Los pasos y reglas `.md` de cada dominio se definen en la carpeta **`Cerebro/`**.
Antes de concluir, cada agente **debe seguir las reglas de su `.md` en Cerebro**.

---

## 6. Reglas del agente Visual

1. **Nunca una sola línea.** Muestra siempre un **rango**, no un único valor. Una
   línea sola transmite falsa certeza.
2. **Etiqueta los supuestos.** Cada escenario declara de dónde sale: qué tasa de
   crecimiento y qué margen se asumen. Sin supuestos, el número no significa nada.
3. **El pasado no se proyecta.** Distingue visualmente lo real de lo estimado:
   histórico en **línea sólida**, futuro proyectado en **línea punteada**.
   Siempre, sin excepción.
4. **El agente decide, no el gráfico.** El razonamiento va primero; la gráfica
   después, solo para ilustrar.

Los visuales concretos a conectar se listan en `referencias/`.

---

## 7. Contenido del reporte final

El reporte que entrega el Agente Principal debe incluir, como mínimo:

- **Veredicto de precio:** ¿la empresa está en un **buen precio**?
- **Decisión:** ¿se puede **invertir** o se debe **evitar**?
- **Si se evita:** en cuánto tiempo se debería **revisar de nuevo** el análisis.
- **Escenarios de precio:** diferentes **precios aproximados** donde la acción
  podría encontrarse, usando los datos del `Cerebro/` **y** estimaciones tipo
  analista financiero. (Siempre como rango, con supuestos etiquetados.)
- **Inversionistas relacionados:** inversionistas importantes o relacionados que
  tengan **otras empresas exitosas**.
- **SEC insider buying/selling:** todas las compras/ventas de *insiders*
  relevantes. **Relevante = monto total superior a $1M USD.**
- **Entrega visual:** el reporte se presenta con gráficas siguiendo la Sección 6.

Todo con foco en **puntos de entrada/salida y timing**, según el perfil.

---

## 8. Fuentes de datos

Para los datos de mercado se usan:

- **FMP** (Financial Modeling Prep)
- **Charles Schwab** (bróker + market data, vía OAuth 2.0)
- **Finnhub**
- **FRED** (datos macroeconómicos)
- **Robinhood** (opcional)

> Las claves/config de estas fuentes van en `API/` y **nunca se suben al repo**
> (ver `.gitignore`). Nunca coloques claves en el chat ni en archivos versionados.

---

## 9. Estructura de carpetas

```
Agente Principal/
├─ CLAUDE.md                  ← este archivo (orquestación)
├─ Cerebro/                   ← reglas y pasos .md por dominio (el "cómo pensar")
├─ Instrucciones/             ← brief del proyecto y del perfil
├─ sub-agentes/               ← definiciones de cada sub-agente
├─ Subs/
│  ├─ Analisis/
│  └─ Technicals/
├─ perfil de inversionistas/  ← perfil detallado del usuario
├─ referencias/               ← scorecard + visuales a conectar
└─ API/                       ← integraciones de datos (claves NO versionadas)
```

---

## 10. Convenciones para Claude

- Responder en **español** (idioma del usuario), salvo términos técnicos.
- Ante falta de datos: declararlo (Sección 2), no inventar.
- Separar siempre **dato histórico** de **estimación**.
- No dar asesoría financiera personalizada regulada; el output es informativo.
- Respetar el perfil del inversionista en toda recomendación.
