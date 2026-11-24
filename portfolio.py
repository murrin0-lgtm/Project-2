"""Lab 14 portfolio baselines. Run from this folder: py portfolio.py.

Course-authored training inputs, not market estimates. All rates are decimals.
"""

import math
import sys
import csv
import io
import statistics
from datetime import date

# Editable inputs; matrix rows and columns follow this sleeve order.
SLEEVES = [
    {"name": "Treasury bills", "return": 0.035, "volatility": 0.005, "reserve_eligible": True},
    {"name": "Treasury 10-year note", "return": 0.043, "volatility": 0.070, "reserve_eligible": True},
    {"name": "Investment-grade bond fund", "return": 0.050, "volatility": 0.060, "reserve_eligible": False},
    {"name": "Global equity index fund", "return": 0.080, "volatility": 0.160, "reserve_eligible": False},
]
CORRELATIONS = [
    [1.00, 0.10, 0.05, 0.00],
    [0.10, 1.00, 0.80, -0.10],
    [0.05, 0.80, 1.00, 0.25],
    [0.00, -0.10, 0.25, 1.00],
]
OBJECTIVE_RETURN = 0.065  # CPI estimate of 2.5% plus 4%.


def validate_inputs(sleeves, correlations):
    """Reject malformed, out-of-range or asymmetric correlation inputs."""
    n = len(sleeves)
    if not n or len(correlations) != n or any(len(row) != n for row in correlations):
        raise ValueError("Correlation table must have one row and column per sleeve.")
    for sleeve in sleeves:
        if not math.isfinite(sleeve["volatility"]) or sleeve["volatility"] <= 0:
            raise ValueError("Every volatility must be finite and positive.")
        if not math.isfinite(sleeve["return"]):
            raise ValueError("Every expected return must be finite.")
    for i in range(n):
        for j in range(n):
            value = correlations[i][j]
            if not math.isfinite(value) or not -1 <= value <= 1:
                raise ValueError(f"Correlation [{i}][{j}] must be between -1 and 1; got {value}.")
            if not math.isclose(value, correlations[j][i], rel_tol=0, abs_tol=1e-12):
                raise ValueError(f"Correlation table must be symmetric: [{i}][{j}] differs from [{j}][{i}].")
        if not math.isclose(correlations[i][i], 1, rel_tol=0, abs_tol=1e-12):
            raise ValueError("Each diagonal correlation must equal 1.")


def build_covariance_matrix(sleeves, correlations):
    validate_inputs(sleeves, correlations)
    return [
        [correlations[i][j] * a["volatility"] * b["volatility"]
         for j, b in enumerate(sleeves)]
        for i, a in enumerate(sleeves)
    ]


def equal_weights(sleeves):
    return [1 / len(sleeves)] * len(sleeves)


def inverse_volatility_weights(sleeves):
    inverse = [1 / sleeve["volatility"] for sleeve in sleeves]
    return [value / sum(inverse) for value in inverse]


def define_portfolios(sleeves):
    benchmark = {"Investment-grade bond fund": 0.40, "Global equity index fund": 0.60}
    return {
        "Benchmark": [benchmark.get(s["name"], 0) for s in sleeves],
        "Equal weight": equal_weights(sleeves),
        "Inverse volatility": inverse_volatility_weights(sleeves),
    }


def expected_return(weights, sleeves):
    return sum(weight * sleeve["return"] for weight, sleeve in zip(weights, sleeves))


def portfolio_volatility(weights, covariance):
    # Include every pair, including both off-diagonal covariance terms.
    variance = sum(
        weights[i] * weights[j] * covariance[i][j]
        for i in range(len(weights))
        for j in range(len(weights))
    )
    if variance < -1e-12:
        raise ValueError("Inputs produce a negative portfolio variance.")
    return math.sqrt(max(0, variance))


def reserve_eligible_weight(weights, sleeves):
    return sum(w for w, s in zip(weights, sleeves) if s["reserve_eligible"])


def meets_objective(portfolio_return, objective):
    return portfolio_return >= objective


def search_portfolios(sleeves, correlations, objective, reserve_minimum, maximum_weight=1.0):
    """Exhaustive long-only search in 5-percentage-point steps; None if infeasible.

    Optional per-fund cap supports the Project 2 mandate. Ties retain the first
    mix encountered in ascending asset-weight order.
    """
    covariance = build_covariance_matrix(sleeves, correlations)
    if not math.isfinite(objective):
        raise ValueError("Objective must be finite.")
    if not 0 <= reserve_minimum <= 1 or not 0 < maximum_weight <= 1:
        raise ValueError("Reserve minimum and maximum weight must be valid fractions.")

    def mixes(remaining, count):
        if count == 1:
            if remaining / 20 <= maximum_weight + 1e-12:
                yield [remaining / 20]
            return
        for units in range(remaining + 1):
            if units / 20 <= maximum_weight + 1e-12:
                for rest in mixes(remaining - units, count - 1):
                    yield [units / 20] + rest

    best = None
    for weights in mixes(20, len(sleeves)):
        result = expected_return(weights, sleeves)
        reserve = reserve_eligible_weight(weights, sleeves)
        if result < objective - 1e-12 or reserve < reserve_minimum - 1e-12:
            continue
        volatility = portfolio_volatility(weights, covariance)
        if best is None or volatility < best["volatility"] - 1e-12:
            best = {"weights": weights, "return": result,
                    "volatility": volatility, "reserve": reserve}
    return best


def estimate_from_csv(csv_text, last_36=False):
    """Estimate annual arithmetic means, sample volatilities and correlations.

    Input: ISO date then 3-6 ticker columns; strictly consecutive monthly prices.
    Last 36 means 36 returns, requiring 37 prices. Never fill missing prices.
    """
    rows = list(csv.reader(io.StringIO(csv_text.lstrip("\ufeff"))))
    if not rows or not 4 <= len(rows[0]) <= 7:
        raise ValueError("CSV needs a date column and three to six ticker columns.")
    names = [name.strip() for name in rows[0][1:]]
    if any(not name for name in names) or len(set(names)) != len(names):
        raise ValueError("Ticker names must be nonempty and unique.")
    prices, dates = [], []
    for line, row in enumerate(rows[1:], 2):
        if len(row) != len(names) + 1:
            raise ValueError(f"CSV row {line}: wrong number of columns.")
        try:
            parts = row[0].split("/")
            if len(parts) == 3:
                month, day_of_month, year = map(int, parts)
                day = date(year, month, day_of_month)
            else:
                day = date.fromisoformat(row[0])
            values = [float(value) for value in row[1:]]
        except ValueError as error:
            raise ValueError(f"CSV row {line}: enter ISO or US dates and numeric prices.") from error
        if any(not math.isfinite(value) or value <= 0 for value in values):
            raise ValueError(f"CSV row {line}: prices must be finite and positive.")
        if dates and (day.year * 12 + day.month) != (dates[-1].year * 12 + dates[-1].month + 1):
            raise ValueError("Prices must be oldest first, with exactly one observation per consecutive month.")
        dates.append(day)
        prices.append(values)
    minimum = 37 if last_36 else 3
    if len(prices) < minimum:
        raise ValueError(f"At least {minimum} monthly prices are required for this window.")
    returns = [[now[i] / previous[i] - 1 for i in range(len(names))]
               for previous, now in zip(prices, prices[1:])]
    if last_36:
        returns = returns[-36:]
    columns = list(zip(*returns))
    deviations = [statistics.stdev(column) for column in columns]
    if any(value <= 1e-15 for value in deviations):
        raise ValueError("A fund has zero return variability; correlation cannot be estimated.")
    sleeves = [{"name": name, "return": statistics.mean(column) * 12,
                "volatility": deviation * math.sqrt(12), "reserve_eligible": False}
               for name, column, deviation in zip(names, columns, deviations)]
    correlations = [[1.0 if i == j else max(-1.0, min(1.0, statistics.correlation(a, b)))
                     for j, b in enumerate(columns)] for i, a in enumerate(columns)]
    return sleeves, correlations, {"months": len(returns),
                                  "first_return_month": dates[-len(returns)].isoformat(),
                                  "last_month": dates[-1].isoformat()}


def largest_weight_change(first, second):
    """Largest absolute weight movement in percentage points, if both feasible."""
    if first is None or second is None:
        return None
    return max(abs(a - b) for a, b in zip(first["weights"], second["weights"])) * 100


def main():
    try:
        covariance = build_covariance_matrix(SLEEVES, CORRELATIONS)
        print("Course training values; CPI estimate: 2.5%; objective: "
              f"{OBJECTIVE_RETURN:.2%}")
        print("Weight order: " + " / ".join(s["name"] for s in SLEEVES))
        for name, weights in define_portfolios(SLEEVES).items():
            result = expected_return(weights, SLEEVES)
            print(f"\n{name}")
            print("  Weights (%): " + " / ".join(f"{w * 100:.1f}" for w in weights))
            print(f"  Expected return: {result:.2%}")
            print(f"  Volatility: {portfolio_volatility(weights, covariance):.2%}")
            print(f"  Reserve-eligible: {reserve_eligible_weight(weights, SLEEVES):.1%}")
            print(f"  Meets objective: {'yes' if meets_objective(result, OBJECTIVE_RETURN) else 'no'}")
    except ValueError as error:
        print(f"Cannot run: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
