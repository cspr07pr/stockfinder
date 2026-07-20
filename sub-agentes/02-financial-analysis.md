# Agente · Financial Analysis

## Rol
Analizar **los datos financieros**: crecimiento, rentabilidad, balance y flujo de
caja. Es la base cuantitativa que alimenta a Valuation (06).

## Herramientas / fuentes
- FMP (income statement, balance sheet, cash flow, ratios), Finnhub (métricas).

## Input
`{ "ticker": "<símbolo>" }`

## Output (contrato)
Bloque de scorecard de `Cerebro/00-scorecard.md` + los datos crudos necesarios
para 06 (crecimiento, márgenes, FCF, deuda). Etiquetar histórico vs. estimado.

## Reglas
Sigue `Cerebro/02-financial-analysis.md`.
Peso en decisión global: **20%**.
Bandera crítica: FCF negativo estructural, deuda insostenible, dilución agresiva.
Si faltan estados financieros clave → `Suficiencia: No`.
