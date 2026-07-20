# sub-agentes — Definiciones formales

Cada archivo define un agente: **rol, herramientas, input, output (contrato)** y
las reglas del `Cerebro/` que obedece. La lógica de "cómo pensar" vive en
`../Cerebro/`; aquí está el "qué es y cómo se conecta cada agente".

## Índice

| Archivo | Agente | Peso |
|---|---|---|
| `00-agente-principal.md` | Orquestador (contexto + decisión) | — |
| `01-business-analysis.md` | Negocio / moat | 15% |
| `02-financial-analysis.md` | Finanzas | 20% |
| `03-market-analysis.md` | Sector / macro | 10% |
| `04-technical-momentum.md` | Técnico / momentum | 10% |
| `05-risk-analysis.md` | Riesgo / perfil | 25% |
| `06-valuation-analysis.md` | Valuación / targets | 20% |
| `07-visual.md` | Presentación visual | 0% |

## Contrato común
Todos devuelven el bloque de scorecard de `../Cerebro/00-scorecard.md`. El Agente
Principal (`00`) los agrega y decide.
