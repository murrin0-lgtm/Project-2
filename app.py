"""Run from the project root with streamlit run python/app.py."""

import hashlib

import streamlit as st

from decision import BASE, DATA, STRESSES, TICKERS, Scenario, archived_signal, evaluate

st.set_page_config(page_title="Retirement Portfolio Review", layout="wide")
st.title("Retirement Portfolio Review")
st.caption("Educational committee replay · $100,000 · 20 years · annual rebalance")

try:
    prices = (DATA / "prices.csv").read_text(encoding="utf-8-sig")
    signal = archived_signal()
    base = evaluate(prices)
    scenarios = {name: evaluate(prices, scenario) for name, scenario in STRESSES.items()}
except (ValueError, OSError) as error:
    st.error(f"Stop and review inputs. {error}")
    st.stop()

if base["portfolios"]["Constrained"] is None or any(
    result["portfolios"]["Constrained"] is None for result in scenarios.values()
):
    st.error("Stop · No live allocation (0%–0%). The base case or a required stress has no passing mix.")
else:
    st.info("Review · Paper pilot only until estimates, liquidity and the rate signal receive committee sign-off.")

with st.sidebar:
    st.header("Scenario controls")
    last_36 = st.checkbox("Use the latest 36 months")
    haircut = st.number_input("VT return haircut (percentage points)", 0.0, 30.0, 0.0, 0.25)
    cost = st.number_input("Annual implementation cost (bp)", 0, 500, 10, 5)
    cap = st.slider("Maximum fund weight (%)", 20, 40, 40)
    risk = st.slider("Maximum annual volatility (%)", 1, 15, 10)
    inflation = st.slider("Planning CPI (%)", 0.0, 10.0, 2.5, 0.1)
    unavailable = st.multiselect("Funds unavailable within five days", TICKERS)

active = Scenario(last_36, haircut / 100, cost / 10000, cap / 100, risk / 100,
                  inflation / 100, tuple(unavailable))
result = base if active == BASE else evaluate(prices, active)
meta = result["meta"]
st.caption(f"{meta['months']} monthly returns through {meta['last_month']} · "
           f"net hurdle {result['target']:.2%} · fund cap {active.cap:.0%} · "
           f"volatility limit {active.risk_limit:.0%} · cost {active.cost * 10000:.0f} bp")
st.subheader("Portfolio comparison")
rows, verdicts = [], []
for name, portfolio in result["portfolios"].items():
    if portfolio is None:
        rows.append({"Portfolio": name, "Verdict": "STOP: no feasible mix"})
        continue
    rules = portfolio["rules"]
    rows.append({
        "Portfolio": name,
        **{ticker: f"{weight:.1%}" for ticker, weight in zip(TICKERS, portfolio["weights"])},
        "Gross annual": f"{portfolio['gross']:.2%}",
        "Net annual": f"{portfolio['net']:.2%}",
        "Annual volatility": f"{portfolio['volatility']:.2%}",
        "Five-day liquidity": f"{portfolio['liquid']:.1%}",
        "Verdict": "Pass" if all(rules.values()) else "Fail",
    })
    verdicts.append({"Portfolio": name, **{rule: "Pass" if passed else "Fail"
                                           for rule, passed in rules.items()}})
st.dataframe(rows, hide_index=True, width="stretch")
st.dataframe(verdicts, hide_index=True, width="stretch")
if result["portfolios"]["Constrained"] is None:
    ceiling = result["ceiling"]
    detail = ("The non-return rules also leave no feasible mix." if ceiling is None
              else f"Highest net return under the other rules: {ceiling:.2%}.")
    st.warning(f"Stop this scenario. {detail}")
st.caption("The 60/40 benchmark is a policy reference. All liquidity verdicts use modeled availability.")

st.subheader("Required stress runs")
stress_rows = []
for name, case in {"Base": base, **scenarios}.items():
    choice = case["portfolios"]["Constrained"]
    ceiling = case["ceiling"]
    stress_rows.append({
        "Case": name,
        "Tolerable net return ceiling": "—" if ceiling is None else f"{ceiling:.2%}",
        "Selected net annual": "—" if choice is None else f"{choice['net']:.2%}",
        "Selected volatility": "—" if choice is None else f"{choice['volatility']:.2%}",
        "Decision": "Stop" if choice is None else "Feasible",
    })
st.dataframe(stress_rows, hide_index=True, width="stretch")

st.subheader("Archived interest-rate signal")
state = "Duration review required" if signal["review"] else "Routine monitoring"
st.write(f"{signal['yield_percent']:.2f}% on {signal['observation']} · {state}")
st.caption(f"DGS10 vintage {signal['vintage']} · decision replay {signal['decision']} · "
           "5.00% review threshold. The signal does not automatically place trades.")
with st.expander("Input provenance"):
    st.write("Bundled monthly adjusted closes through September 2026. "
             "Fixed historical estimates use arithmetic returns and sample covariance.")
    st.code(hashlib.sha256((DATA / "prices.csv").read_bytes()).hexdigest(), language=None)
