# StockFinder — código (Python)

Implementación del sistema descrito en `../CLAUDE.md`. El Agente Principal
(`orchestrator`) coordina a los sub-agentes (`agents/`), que leen datos de las
fuentes (`sources/`) y devuelven un scorecard.

## Requisitos
- Python 3.12+
- Claves configuradas en `../API/.env` (ver `../API/README.md`)

## Instalación
```powershell
# desde la raíz del repo
python -m pip install -r requirements.txt
```

## Verificar que las fuentes funcionan
El paquete usa layout `src/`, así que se indica con `PYTHONPATH`:
```powershell
$env:PYTHONPATH="src"; python -m stockfinder check   # valida claves + ping
python -m stockfinder check --no-ping                # solo presencia de claves
```
> En Git Bash: `PYTHONPATH=src python -m stockfinder check`
> (o instala en editable con `python -m pip install -e .` y omite PYTHONPATH).

**Nota FMP:** los endpoints `v3` quedaron obsoletos (403 "Legacy"). Se usa la
API `stable` (`/stable/quote?symbol=...`).

> El comando `check` no requiere las dependencias de `requirements.txt`
> (usa solo la librería estándar), así que sirve como primera prueba tras
> instalar Python.

## Estructura
```
src/stockfinder/
├─ __main__.py     # CLI (check; luego analyze <TICKER>)
├─ config.py       # carga de API/.env (sin exponer valores)
├─ sources/        # conectores: fmp, finnhub, fred, schwab (OAuth)
├─ agents/         # sub-agentes (próxima fase)
├─ scorecard.py    # pesos y regla de decisión (próxima fase)
└─ orchestrator.py # Agente Principal (próxima fase)
```

## Estado
- ✅ Config + carga de claves
- ✅ `check` (validación de fuentes)
- ✅ Conectores FMP, Finnhub y FRED (datos reales verificados)
- ⬜ Conector Schwab (OAuth)
- ⬜ Sub-agentes y scorecard
- ⬜ Orquestador + reporte

### Conectores disponibles (`sources/`)
| Fuente | Métodos clave |
|---|---|
| `fmp.FMP` | quote, profile, income_statement, balance_sheet, cash_flow, ratios_ttm, key_metrics_ttm, price_target_consensus, analyst_estimates, historical_prices |
| `finnhub.Finnhub` | quote, profile, insider_transactions, recommendations, metrics |
| `fred.FRED` | latest, observations, yoy, macro_snapshot |
