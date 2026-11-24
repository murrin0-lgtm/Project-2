"""Project 2 mandate, portfolio comparisons, and archived monitoring signal."""

import csv
import math
from dataclasses import dataclass, replace
from datetime import date
from pathlib import Path

import portfolio as engine

DATA = Path(__file__).resolve().parents[1] / "data"
TICKERS = ("BIL", "IEF", "LQD", "VT")
BENCHMARK = (0, 0, 0.4, 0.6)
EPS = 1e-12


@dataclass(frozen=True)
class Scenario:
    last_36: bool = False
    haircut: float = 0
    cost: float = 0.001
    cap: float = 0.40
    risk_limit: float = 0.10
    inflation: float = 0.025
    unavailable: tuple = ()


BASE = Scenario()
STRESSES = {
    "Estimates: VT −2 percentage points": replace(BASE, haircut=0.02),
    "Window: 36 months": replace(BASE, last_36=True),
    "Costs: 50 bp per year": replace(BASE, cost=0.005),
    "Constraints: 30% fund cap, 8% volatility": replace(BASE, cap=0.30, risk_limit=0.08),
    "Liquidity: VT unavailable": replace(BASE, unavailable=("VT",)),
}


def evaluate(prices, scenario=BASE):
    sleeves, correlations, meta = engine.estimate_from_csv(prices, scenario.last_36)
    if tuple(sleeve["name"] for sleeve in sleeves) != TICKERS:
        raise ValueError("Expected BIL, IEF, LQD, VT in that order.")
    sleeves[-1]["return"] -= scenario.haircut
    covariance = engine.build_covariance_matrix(sleeves, correlations)
    target = scenario.inflation + 0.03

    def metrics(weights):
        gross = engine.expected_return(weights, sleeves)
        volatility = engine.portfolio_volatility(weights, covariance)
        liquid = sum(w for ticker, w in zip(TICKERS, weights) if ticker not in scenario.unavailable)
        net = gross - scenario.cost
        rules = {
            "Fully invested": math.isclose(sum(weights), 1, abs_tol=EPS),
            "Long-only, eligible ETFs": min(weights) >= -EPS,
            "Fund cap": max(weights) <= scenario.cap + EPS,
            "Five-day liquidity": liquid >= 0.95 - EPS,
            "Volatility ceiling": volatility <= scenario.risk_limit + EPS,
            "Net return hurdle": net >= target - EPS,
        }
        return dict(weights=weights, gross=gross, net=net, volatility=volatility,
                    liquid=liquid, rules=rules)

    best = None
    ceiling = None
    for a in range(21):
        for b in range(21 - a):
            for c in range(21 - a - b):
                units = (a, b, c, 20 - a - b - c)
                if max(units) > 20 * scenario.cap + EPS:
                    continue
                candidate = metrics(tuple(unit / 20 for unit in units))
                rules = candidate["rules"]
                if all(value for key, value in rules.items() if key != "Net return hurdle"):
                    ceiling = candidate["net"] if ceiling is None else max(ceiling, candidate["net"])
                    if rules["Net return hurdle"] and (
                        best is None or candidate["volatility"] < best["volatility"] - EPS
                    ):
                        best = candidate
    return {
        "meta": meta,
        "target": target,
        "ceiling": ceiling,
        "portfolios": {
            "Equal weight": metrics(engine.equal_weights(sleeves)),
            "Inverse volatility": metrics(engine.inverse_volatility_weights(sleeves)),
            "Constrained": best,
            "60/40 benchmark": metrics(BENCHMARK),
        },
    }


def archived_signal(directory=DATA / "lab17"):
    """Replay a fixed decision using only the selected completed vintage."""
    decision_day = date(2026, 10, 6)
    vintage = date(2026, 10, 5)
    cutoff = date(2026, 9, 30)
    with (directory / f"DGS10_asof_{vintage}.csv").open(encoding="utf-8-sig", newline="") as file:
        observations = {}
        for day_text, value in list(csv.reader(file))[1:]:
            day = date.fromisoformat(day_text)
            if day <= cutoff and value.strip() not in ("", "."):
                observations[day] = float(value)
    if not observations:
        raise ValueError("Archived DGS10 has no usable observations.")
    observation = max(observations)
    if (cutoff - observation).days > 7 or not math.isfinite(observations[observation]):
        raise ValueError("Archived DGS10 is stale or invalid.")
    yield_percent = observations[observation]
    return dict(decision=decision_day, vintage=vintage, observation=observation,
                yield_percent=yield_percent, review=yield_percent >= 5.0)
