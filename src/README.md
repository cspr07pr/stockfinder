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
```powershell
python -m stockfinder check            # valida claves + ping a FMP/Finnhub/FRED
python -m stockfinder check --no-ping  # solo verifica que las claves existan
```

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
- ⬜ Conectores completos (FMP, Finnhub, FRED, Schwab OAuth)
- ⬜ Sub-agentes y scorecard
- ⬜ Orquestador + reporte
