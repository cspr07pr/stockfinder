"""CLI de StockFinder.

Uso:
    python -m stockfinder check          # valida claves y hace ping a las fuentes
    python -m stockfinder check --no-ping  # solo verifica presencia de claves

(El comando de analisis `analyze <TICKER>` se agrega en la siguiente fase.)
"""

from __future__ import annotations

import argparse
import sys

from .config import ENV_PATH, load_config
from .sources.http import HttpError, get_json

# La consola de Windows suele venir en cp1252; forzamos UTF-8 para acentos/simbolos.
try:
    sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[union-attr]
except Exception:
    pass

OK = "OK   "
FAIL = "FALLA"
SKIP = "--   "


def _ping_fmp(key: str) -> str:
    # Los endpoints v3 quedaron como "Legacy" (403). Se usa la API stable.
    data = get_json(
        "https://financialmodelingprep.com/stable/quote",
        {"symbol": "AAPL", "apikey": key},
    )
    if isinstance(data, list) and data and "price" in data[0]:
        return f"AAPL ~${data[0]['price']}"
    raise HttpError("respuesta inesperada (¿clave invalida?)")


def _ping_finnhub(key: str) -> str:
    data = get_json("https://finnhub.io/api/v1/quote", {"symbol": "AAPL", "token": key})
    if isinstance(data, dict) and data.get("c"):
        return f"AAPL ~${data['c']}"
    raise HttpError("respuesta inesperada (¿clave invalida?)")


def _ping_fred(key: str) -> str:
    data = get_json(
        "https://api.stlouisfed.org/fred/series/observations",
        {"series_id": "FEDFUNDS", "api_key": key, "file_type": "json",
         "limit": 1, "sort_order": "desc"},
    )
    obs = data.get("observations") if isinstance(data, dict) else None
    if obs:
        return f"FEDFUNDS {obs[0]['value']}%"
    raise HttpError("respuesta inesperada (¿clave invalida?)")


def cmd_check(ping: bool) -> int:
    cfg = load_config()
    print(f"Leyendo claves de: {ENV_PATH}\n")

    rows: list[tuple[str, bool, object]] = [
        ("FMP", cfg.has("fmp"), lambda: _ping_fmp(cfg.fmp_api_key)),
        ("Finnhub", cfg.has("finnhub"), lambda: _ping_finnhub(cfg.finnhub_api_key)),
        ("FRED", cfg.has("fred"), lambda: _ping_fred(cfg.fred_api_key)),
    ]

    all_ok = True
    for name, present, pinger in rows:
        if not present:
            print(f"  {name:<10} {FAIL}  clave ausente en API/.env")
            all_ok = False
            continue
        if not ping:
            print(f"  {name:<10} {OK}  clave presente")
            continue
        try:
            detail = pinger()  # type: ignore[operator]
            print(f"  {name:<10} {OK}  {detail}")
        except HttpError as exc:
            print(f"  {name:<10} {FAIL}  {exc}")
            all_ok = False

    # Schwab: OAuth, no se puede validar con un simple ping aqui.
    if cfg.has("schwab"):
        print(f"  {'Schwab':<10} {OK}  App Key/Secret presentes (OAuth se prueba aparte)")
    else:
        print(f"  {'Schwab':<10} {FAIL}  App Key/Secret ausentes")
        all_ok = False

    print("\n" + ("Todo listo. Las 4 fuentes responden."
                  if all_ok else "Hay fuentes por corregir."))
    return 0 if all_ok else 1


def cmd_analyze(symbol: str, capital: float | None) -> int:
    from .orchestrator import analyze
    from .report import render_text

    print(f"Analizando {symbol.upper()}... (trayendo datos de las fuentes)\n")
    result = analyze(symbol, capital=capital)
    print(render_text(result))
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="stockfinder")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check", help="valida las claves de API/.env")
    p_check.add_argument("--no-ping", action="store_true",
                         help="no hacer llamadas de red, solo verificar presencia")

    p_an = sub.add_parser("analyze", help="analiza un ticker y genera el reporte")
    p_an.add_argument("symbol", help="ticker, p. ej. AAPL")
    p_an.add_argument("--capital", type=float, default=None,
                      help="capital disponible en USD (para dimensionar la posicion)")

    args = parser.parse_args(argv)
    if args.cmd == "check":
        return cmd_check(ping=not args.no_ping)
    if args.cmd == "analyze":
        return cmd_analyze(args.symbol, args.capital)
    return 2


if __name__ == "__main__":
    sys.exit(main())
