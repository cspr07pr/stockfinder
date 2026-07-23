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

OK = "\033[92mOK\033[0m"
FAIL = "\033[91mFALLA\033[0m"
SKIP = "\033[90m--\033[0m"


def _ping_fmp(key: str) -> str:
    data = get_json(
        "https://financialmodelingprep.com/api/v3/quote-short/AAPL",
        {"apikey": key},
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

    print("\n" + ("Todo listo ✅" if all_ok else "Hay fuentes por corregir ⚠"))
    return 0 if all_ok else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="stockfinder")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_check = sub.add_parser("check", help="valida las claves de API/.env")
    p_check.add_argument("--no-ping", action="store_true",
                         help="no hacer llamadas de red, solo verificar presencia")

    args = parser.parse_args(argv)
    if args.cmd == "check":
        return cmd_check(ping=not args.no_ping)
    return 2


if __name__ == "__main__":
    sys.exit(main())
