"""Verify fixed evidence, financial arithmetic and the app entry point."""

from dataclasses import replace
import csv
from datetime import datetime
import json
import math
from pathlib import Path

from decision import DATA, BASE, STRESSES, TICKERS, archived_signal, evaluate
from verify_lab15 import verify_engine


def check():
    verify_engine()
    prices = (DATA / "prices.csv").read_text(encoding="utf-8-sig")
    rows = list(csv.DictReader(prices.splitlines()))
    for ticker in TICKERS:
        daily = json.loads((DATA / f"{ticker}_yahoo_daily.json").read_text(encoding="utf-8-sig"))
        month_end = {}
        for record in sorted(daily, key=lambda item: item["date"]):
            if record["adj_close"] is not None:
                month_end[record["date"][:7]] = record
        for row in rows:
            day = datetime.strptime(row["Date"], "%m/%d/%Y").date().isoformat()
            expected = month_end[day[:7]]
            assert day == expected["date"], (ticker, day)
            assert math.isclose(float(row[ticker]), expected["adj_close"], rel_tol=0, abs_tol=5.1e-8), (ticker, day)
    print("PASS: 244 month-end adjusted closes match saved daily observations")
    base = evaluate(prices)
    assert base["meta"]["months"] == 60
    portfolios = base["portfolios"]
    choice = portfolios["Constrained"]
    assert choice["weights"] == (0.4, 0.2, 0, 0.4)
    assert math.isclose(choice["net"], 0.057380543325933085)
    assert math.isclose(choice["volatility"], 0.07077843427994472)
    assert all(choice["rules"].values())
    assert not portfolios["Equal weight"]["rules"]["Net return hurdle"]
    assert not portfolios["Inverse volatility"]["rules"]["Fund cap"]
    assert not portfolios["60/40 benchmark"]["rules"]["Volatility ceiling"]
    assert evaluate(prices, replace(BASE, cap=0.2))["ceiling"] is None
    unavailable = evaluate(prices, replace(BASE, unavailable=("VT",)))
    assert unavailable["portfolios"]["Constrained"] is None
    assert not unavailable["portfolios"]["Equal weight"]["rules"]["Five-day liquidity"]
    signal = archived_signal()
    assert signal["observation"].isoformat() == "2026-09-30"
    assert signal["observation"] < signal["vintage"] < signal["decision"]
    assert signal["yield_percent"] == 5.29 and signal["review"]
    with (DATA / "lab17" / "DGS10_asof_2026-10-29.csv").open(encoding="utf-8-sig") as file:
        later = dict(csv.reader(file))
    print("Later vintage, same September 30 observation:", later["2026-09-30"])
    try:
        archived_signal(DATA / "missing")
    except FileNotFoundError:
        pass
    else:
        raise AssertionError("Missing signal archive was accepted")
    print("PASS: base choice, benchmark, baseline failures, liquidity, signal timing and missing signal")
    for name, scenario in STRESSES.items():
        result = evaluate(prices, scenario)
        print(name, result["ceiling"], result["portfolios"]["Constrained"])

    from streamlit.testing.v1 import AppTest

    app = AppTest.from_file(str(Path(__file__).with_name("app.py"))).run(timeout=45)
    assert not app.exception, app.exception
    assert len(app.dataframe) == 3
    assert any("No live allocation" in error.value for error in app.error)
    app.sidebar.checkbox[0].check().run(timeout=45)
    assert not app.exception and any("36 monthly returns" in item.value for item in app.caption)
    app.sidebar.checkbox[0].uncheck().run(timeout=45)
    app.sidebar.multiselect[0].set_value(["VT"]).run(timeout=45)
    assert not app.exception and any("Stop this scenario" in item.value for item in app.warning)
    print("PASS: Streamlit startup, three tables, window switch and liquidity stop")


if __name__ == "__main__":
    check()
