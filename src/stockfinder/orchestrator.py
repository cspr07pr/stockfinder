"""Agente Principal (orquestador).

Recibe el ticker, trae datos de las fuentes, ejecuta los sub-agentes en el orden
definido (Cerebro), agrega los scorecards y arma el resultado del analisis.
Mantiene el contexto completo de principio a fin.
"""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Any

from .agents import business, financial, market, risk, technical, valuation
from .config import Config, load_config
from .profile import DEFAULT_PROFILE, InvestorProfile
from .scorecard import Decision, Scorecard, aggregate
from .sources.finnhub import Finnhub
from .sources.fmp import FMP
from .sources.fred import FRED
from .sources.http import HttpError
from .sources.schwab import SchwabAuth, SchwabClient


@dataclass
class MarketData:
    symbol: str
    price: float | None = None
    quote: dict = field(default_factory=dict)
    profile: dict = field(default_factory=dict)
    income: list = field(default_factory=list)
    balance: list = field(default_factory=list)
    cash_flow: list = field(default_factory=list)
    ratios_ttm: dict = field(default_factory=dict)
    key_metrics_ttm: dict = field(default_factory=dict)
    price_target: dict = field(default_factory=dict)
    analyst_estimates: list = field(default_factory=list)
    history: list = field(default_factory=list)
    insiders: list = field(default_factory=list)
    recommendations: list = field(default_factory=list)
    fh_metrics: dict = field(default_factory=dict)
    fh_profile: dict = field(default_factory=dict)
    macro: dict = field(default_factory=dict)
    tech: dict = field(default_factory=dict)   # se llena tras el agente Technical
    price_source: str = "FMP"
    history_source: str = "FMP"
    warnings: list = field(default_factory=list)


@dataclass
class Analysis:
    symbol: str
    decision: Decision
    data: MarketData
    insiders_relevantes: list[dict[str, Any]]
    profile: InvestorProfile


def _safe(target: MarketData, label: str, fn):
    """Ejecuta una llamada a fuente; ante error registra warning y sigue."""
    try:
        return fn()
    except (HttpError, ValueError, KeyError, TypeError) as exc:
        target.warnings.append(f"{label}: {exc}")
        return None


def fetch(symbol: str, cfg: Config) -> MarketData:
    d = MarketData(symbol=symbol)
    fmp = FMP(cfg.fmp_api_key) if cfg.has("fmp") else None
    fh = Finnhub(cfg.finnhub_api_key) if cfg.has("finnhub") else None
    fr = FRED(cfg.fred_api_key) if cfg.has("fred") else None

    if fmp:
        q = _safe(d, "fmp.quote", lambda: fmp.quote(symbol))
        d.quote = q or {}
        d.price = (q or {}).get("price")
        d.profile = _safe(d, "fmp.profile", lambda: fmp.profile(symbol)) or {}
        d.income = _safe(d, "fmp.income", lambda: fmp.income_statement(symbol, limit=5)) or []
        d.balance = _safe(d, "fmp.balance", lambda: fmp.balance_sheet(symbol, limit=5)) or []
        d.cash_flow = _safe(d, "fmp.cashflow", lambda: fmp.cash_flow(symbol, limit=5)) or []
        d.ratios_ttm = _safe(d, "fmp.ratios", lambda: fmp.ratios_ttm(symbol)) or {}
        d.key_metrics_ttm = _safe(d, "fmp.keymetrics", lambda: fmp.key_metrics_ttm(symbol)) or {}
        d.price_target = _safe(d, "fmp.pricetarget", lambda: fmp.price_target_consensus(symbol)) or {}
        d.analyst_estimates = _safe(d, "fmp.estimates", lambda: fmp.analyst_estimates(symbol)) or []
        d.history = _safe(d, "fmp.history", lambda: fmp.historical_prices(symbol)) or []
    if fh:
        d.insiders = _safe(d, "finnhub.insiders", lambda: fh.insider_transactions(symbol)) or []
        d.recommendations = _safe(d, "finnhub.recs", lambda: fh.recommendations(symbol)) or []
        d.fh_metrics = _safe(d, "finnhub.metrics", lambda: fh.metrics(symbol)) or {}
        d.fh_profile = _safe(d, "finnhub.profile", lambda: fh.profile(symbol)) or {}
        if not d.price and d.quote is not None:
            fq = _safe(d, "finnhub.quote", lambda: fh.quote(symbol)) or {}
            d.price = fq.get("c") or d.price
    if fr:
        d.macro = _safe(d, "fred.macro", lambda: fr.macro_snapshot()) or {}

    # Fallback Schwab: si FMP no cubre el ticker (402/premium), usar precio e
    # historial en tiempo real del broker para rescatar Technical y Risk.
    if cfg.has("schwab") and (not d.price or not d.history):
        try:
            client = SchwabClient(SchwabAuth(cfg))
            if not d.price:
                q = _safe(d, "schwab.quote", lambda: client.quote(symbol)) or {}
                quote = q.get("quote", q)
                d.price = quote.get("lastPrice") or quote.get("mark") or d.price
                if d.price:
                    d.price_source = "Schwab (tiempo real)"
            if not d.history:
                candles = _safe(d, "schwab.history",
                                lambda: client.price_history(symbol)) or []
                if candles:
                    d.history = _schwab_history(candles)
                    d.history_source = "Schwab"
        except (HttpError, ValueError) as exc:
            d.warnings.append(f"schwab.fallback: {exc}")
    return d


def _schwab_history(candles: list[dict]) -> list[dict]:
    """Convierte candles de Schwab (mas antiguo primero) al formato del sistema
    (mas reciente primero, con 'price' = cierre)."""
    out = [{"price": c.get("close"), "date": c.get("datetime")}
           for c in candles if c.get("close")]
    out.reverse()
    return out


def relevant_insiders(insiders: list, threshold: float = 1_000_000) -> list[dict]:
    """Transacciones de insiders con impacto > umbral (Cerebro: $1M)."""
    out = []
    for t in insiders:
        change = t.get("change") or 0
        price = t.get("transactionPrice") or 0
        value = abs(change * price)
        if value >= threshold:
            out.append({
                "name": t.get("name"), "date": t.get("transactionDate") or t.get("filingDate"),
                "change": change, "price": price, "value": value,
                "side": "venta" if change < 0 else "compra",
            })
    out.sort(key=lambda x: x["value"], reverse=True)
    return out


def analyze(symbol: str, capital: float | None = None,
            cfg: Config | None = None) -> Analysis:
    cfg = cfg or load_config()
    prof = dataclasses.replace(DEFAULT_PROFILE, capital=capital)
    data = fetch(symbol.upper(), cfg)

    # Orden Cerebro: Business -> Financial -> Market -> Technical -> Valuation -> Risk
    cards: list[Scorecard] = []
    cards.append(business.run(data, prof))
    cards.append(financial.run(data, prof))
    cards.append(market.run(data, prof))

    tech_card = technical.run(data, prof)
    data.tech = tech_card.extra          # Risk usa el stop/precio del tecnico
    cards.append(tech_card)

    cards.append(valuation.run(data, prof))
    cards.append(risk.run(data, prof))

    decision = aggregate(cards)
    return Analysis(
        symbol=symbol.upper(), decision=decision, data=data,
        insiders_relevantes=relevant_insiders(data.insiders), profile=prof,
    )
