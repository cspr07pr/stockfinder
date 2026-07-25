# 📊 StockFinder

**Un sistema de agentes que analiza una acción a fondo antes de invertir.**

StockFinder procesa la enorme cantidad de información del mercado de forma fácil,
orientada y visual. Un **Agente Principal** coordina a 6 sub-agentes
especializados (negocio, finanzas, mercado, técnico, valuación y riesgo), reúne
sus conclusiones en un **scorecard** y entrega un veredicto claro:
**Invertir · Vigilar · Evitar · Sin decisión** — en texto y en un dashboard visual.

> ⚠️ **Aviso:** StockFinder produce análisis **informativo**, no asesoría
> financiera licenciada. El reporte apoya tu decisión; no la reemplaza ni
> constituye una recomendación regulada.

---

## ✨ Qué hace

Con un solo comando, para cualquier ticker:

```powershell
python run.py analyze AAPL --capital 25000 --open
```

1. Trae datos reales de **FMP, Finnhub, FRED y Charles Schwab**.
2. Ejecuta los **6 sub-agentes**, cada uno siguiendo sus reglas en `Cerebro/`.
3. Cada agente entrega un **scorecard** (puntaje 0–100 + confianza + banderas).
4. El **Agente Principal** los agrega con pesos y **decide**.
5. Genera el reporte: decisión, veredicto de precio, **puntos de entrada/salida y
   timing**, escenarios de precio, e **insiders SEC > $1M**.
6. Con `--html`, un **dashboard visual** (ver `referencias/ejemplos/`).

### 🥇 La regla de oro
**Si no hay data suficiente, lo dice.** Nunca inventa. Cuando falta información,
el resultado declara: *«No tengo data suficiente para llegar a una conclusión de
inversión.»* La lógica manda; el gráfico solo ilustra.

---

## 🤖 Los agentes

| # | Sub-agente | Enfoque | Peso |
|---|---|---|---|
| 1 | **Business** | Negocio, moat, calidad (ROIC, márgenes) | 15% |
| 2 | **Financial** | Crecimiento, márgenes, deuda, flujo de caja | 20% |
| 3 | **Market** | Sector, índices y macro (FRED) | 10% |
| 4 | **Technical** | Soportes/resistencias, momentum, entrada/salida | 10% |
| 5 | **Risk** | Riesgo de la empresa + tu perfil, position sizing | 25% |
| 6 | **Valuation** | P/E, price targets, escenarios (depende de Financial) | 20% |
| — | **Visual** | Presenta todo con gráficas (no decide) | — |

**Regla de decisión:** ≥70 Invertir · 55–69 Vigilar · <55 Evitar. Una **bandera
roja crítica** (p. ej. FCF negativo estructural, ruptura de soporte mayor) veta y
fuerza *Evitar*. Si falta >50% del peso en datos → *Sin decisión*.

---

## 🚀 Inicio rápido

### Requisitos
- Python 3.12+
- Claves de API (todas con plan gratuito): FMP, Finnhub, FRED. Schwab es opcional
  (bróker + precios en tiempo real, vía OAuth).

### 1) Configura las claves
```powershell
cd API
Copy-Item .env.example .env
# edita API/.env con tus claves (ver API/README.md)
```
> `API/.env` está en `.gitignore`: **tus claves nunca se suben al repo**.

### 2) Verifica las fuentes
```powershell
python run.py check
```
```
FMP        OK   AAPL ~$320.7
Finnhub    OK   AAPL ~$320.7
FRED       OK   FEDFUNDS 3.63%
Schwab     OK   App Key/Secret presentes
```

### 3) Analiza
```powershell
python run.py analyze AAPL --capital 25000          # reporte de texto
python run.py analyze AAPL --capital 25000 --html   # + dashboard HTML
python run.py analyze AAPL --capital 25000 --open   # + lo abre en el navegador
```

### 4) (Opcional) Conecta Charles Schwab
```powershell
python run.py schwab-login     # interactivo: abre la URL, autoriza, pega la redireccion
python run.py schwab-test AAPL # confirma cotizaciones en tiempo real
```
Si FMP no cubre un ticker, Schwab actúa de **fallback** para precio e historial.

---

## 🗂️ Estructura

```
stockfinder/
├─ run.py                     ← lanzador (python run.py <comando>)
├─ CLAUDE.md                  ← orquestación (cómo piensa el sistema)
├─ Cerebro/                   ← reglas .md por dominio + scorecard + decisión
├─ sub-agentes/               ← definiciones formales de cada agente
├─ referencias/               ← scorecard, catálogo visual y ejemplo HTML
├─ perfil de inversionistas/  ← perfil del usuario
├─ API/                       ← claves (NO versionadas) + guía
└─ src/stockfinder/           ← código Python
   ├─ sources/    fmp · finnhub · fred · schwab (OAuth)
   ├─ agents/     los 6 sub-agentes
   ├─ scorecard.py · orchestrator.py · report.py · visual.py
   └─ config.py · profile.py
```

## 🔌 Fuentes de datos

| Fuente | Aporta |
|---|---|
| **FMP** | Fundamentales, ratios, valuación, price targets, histórico |
| **Finnhub** | Perfil, insiders SEC, recomendaciones de analistas |
| **FRED** | Macro: tasas, inflación, empleo, curva |
| **Charles Schwab** | Precios y cotizaciones en tiempo real (OAuth 2.0) |

---

## 👤 Perfil del inversionista

El análisis se adapta a un perfil (ver `perfil de inversionistas/`): objetivo de
crecer capital en 3–5 años, pérdida máxima tolerable **8–10%**, estilo agresivo,
prioridad en **puntos de entrada/salida y timing**. El **capital** se pasa en cada
análisis con `--capital` (no se versiona por privacidad).

## ⚙️ Ajustar el sistema

- **Pesos y umbrales de decisión:** `src/stockfinder/scorecard.py` (`WEIGHTS`).
- **Reglas de cada agente:** `Cerebro/*.md` (el "cómo pensar") y
  `src/stockfinder/agents/*.py` (la implementación).

---

*Proyecto personal de análisis. Output informativo, no asesoría financiera regulada.*
