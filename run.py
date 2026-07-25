#!/usr/bin/env python
"""Lanzador de StockFinder sin configurar PYTHONPATH.

Uso (desde la carpeta del proyecto):
    python run.py check
    python run.py schwab-login
    python run.py analyze AAPL --capital 25000
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src"))

from stockfinder.__main__ import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
