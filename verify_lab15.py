"""Known answers from the Lab 15 training case and price estimator."""
import copy
import statistics

import portfolio as p


def verify_engine():
    base = p.search_portfolios(p.SLEEVES, p.CORRELATIONS, .065, .03)
    assert base["weights"] == [0, .2, .25, .55], base
    assert f"{base['return']:.2%}" == "6.51%"
    assert f"{base['volatility']:.2%}" == "9.44%"
    stressed = copy.deepcopy(p.SLEEVES)
    stressed[3]["return"] = .07
    attack = p.search_portfolios(stressed, p.CORRELATIONS, .065, .03)
    assert attack["weights"] == [0, .1, .1, .8], attack
    assert f"{attack['return']:.2%}" == "6.53%"
    assert f"{attack['volatility']:.2%}" == "12.94%"
    assert abs(p.largest_weight_change(base, attack) - 25) < 1e-10
    correlations = copy.deepcopy(p.CORRELATIONS)
    correlations[2][3] = correlations[3][2] = .5
    changed = p.search_portfolios(p.SLEEVES, correlations, .065, .03)
    assert changed["weights"] == [0, .4, 0, .6], changed
    assert f"{changed['return']:.2%}" == "6.52%"
    assert f"{changed['volatility']:.2%}" == "9.73%"
    assert p.search_portfolios(p.SLEEVES, p.CORRELATIONS, .50, .03) is None
    assert p.search_portfolios(p.SLEEVES, p.CORRELATIONS, .065, .03, .2) is None
    print("PASS: Meridian base, one-point stress, 25-point change, covariance change, infeasibility")

    # Synthetic prices test the estimator only; never used as the student's fund data.
    text = "Date,A,B,C\n2025-01-31,100,100,100\n2025-02-28,110,105,90\n2025-03-31,99,115.5,94.5\n"
    sleeves, corr, meta = p.estimate_from_csv(text)
    assert abs(sleeves[0]["return"]) < 1e-12
    assert abs(sleeves[0]["volatility"] - statistics.stdev([.1, -.1]) * 12 ** .5) < 1e-12
    assert meta["months"] == 2
    for invalid, short in [(text.replace("2025-02-28", "2025-01-30"), False),
                           (text.replace(",110,", ",0,"), False), (text, True)]:
        try:
            p.estimate_from_csv(invalid, short)
        except ValueError:
            pass
        else:
            raise AssertionError("Bad CSV or short window was accepted")
    print("PASS: arithmetic annualization, sample volatility, invalid prices/dates and short window")


if __name__ == "__main__":
    verify_engine()
