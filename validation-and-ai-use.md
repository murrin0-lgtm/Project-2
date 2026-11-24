# Locked Changed-Input Record

Pre-run predicition commit: https://github.com/murrin0-lgtm/Project-2/blob/main/locked-changed-input-prediction.md

The net return hurdle rose from 5.50% to 6.50%. The highest estimated net
return among portfolios satisfying the other rules stayed at 5.93%, about
0.57 percentage points below the new hurdle. The constrained portfolio
showed “STOP: no feasible mix.”

The result matched my prediction. Raising planning CPI increased the
required return while leaving the portfolio return estimates and other
constraints unchanged. My committee recommendation remains $0 in live
allocation. The higher-CPI scenario reinforces that decision because no
portfolio clears the return hurdle while satisfying the other rules.

## Validation and AI use

OpenAI Codex organized the lab evidence, developed the Streamlit and mandate logic, wrote verification checks, and executed ordinary scenario runs.

## Data and implementation checks

- The starter parser assumed ISO dates. The bundled monthly CSV uses U.S. dates such as `9/30/2021`. Inspection of the actual file led to support for both formats. Tests retain rejection of duplicate or skipped months, invalid prices and short windows.
- The lineage check matches the date and value of all 244 monthly prices to saved daily data, allowing up to 0.000000051 USD of rounding. The [price data card](price-data-card.md) records the capture time, definitions, transformation, limitations and checksum.
- The [signal data card](signal-data-card.md) records the vintage, cutoff, units, checksum and rationale. The verification checks the September 30 observation, review status, chronological order and missing-archive failure. It also reports the same observation from the later vintage for comparison.

## Known answers and challenge cases

The suite checks an independent two-month arithmetic example with +10% and −10% returns, including the zero mean and sample standard deviation. It also runs the saved Meridian training check with a 6.51% return and 9.44% volatility, plus an edited correlation and an infeasible hurdle. For the retirement application, it checks the 40/20/0/40 base allocation, 5.7381% net estimate, 7.0778% volatility and individual rule verdicts. The Streamlit tests verify startup, visible tables, the 36-month control and a liquidity stop.

The [memo](decision-memo.md) records the estimate, window, cost, constraint and liquidity results. The VT return haircut directly challenges the highest-risk claim, that the constrained allocation can clear the net hurdle. It cuts the return ceiling to 5.13% and stops allocation. The 36-month estimate is an overlapping sensitivity window. Independent prospective validation and observed trade costs remain prerequisites to funding. See the [cold-run log](cold-run-log.md) for the environment and verification outcome.

### AI output review

The AI-authored first liquidity assertion expected no portfolio to satisfy the non-return rules when VT became unavailable. A test failure and inspection of the mandate showed that a 95% liquidity minimum allows up to 5% unavailable. The corrected check expects no portfolio to pass **all** the rules and separately checks that equal weight fails liquidity. Its 1.34% return ceiling explains the failure after applying the other rules. This records a check performed during Codex development. The student should independently reproduce or challenge this or another AI-assisted output for the submission.