# Investment committee decision memo

**AI use.** OpenAI Codex organized lab materials, implemented the app and verification checks, and drafted this memo for student review.

**Student statement for review.** After I independently review and approve the analysis and decision, I attest that they are mine. This project is for education, not investment advice.

## Decision requested

**Reject live allocation this cycle. Authorize 0%–0% ($0) to the process.** Use it for paper monitoring while the committee reviews estimate sensitivity and verifies liquidity. This is a decision about new funding under this process, with no instruction to liquidate existing assets. The committee oversees a hypothetical $100,000 retirement account with a 20-year horizon, an annual rebalance, and no planned withdrawals. The [mandate](mandate.md) targets CPI plus 3 points net of costs over rolling five-year periods.

## Base-case comparison

The September 2026 price window uses 60 monthly returns and a 10 bp cost allowance. The 5.50% net hurdle uses a 2.50% CPI assumption. Base case modeled liquidity is 100% for all four rows.

| Portfolio | BIL / IEF / LQD / VT | Est. net annual return | Est. annual volatility | Rule failures |
| --- | --- | ---: | ---: | --- |
| Equal weight | 25% / 25% / 25% / 25% | 3.12% | 7.50% | Net hurdle |
| Inverse volatility | 86.81% / 5.75% / 4.49% / 2.95% | 3.23% | 1.40% | Fund cap and net hurdle |
| Constrained | 40% / 20% / 0% / 40% | 5.74% | 7.08% | Passes modeled rules |
| Policy benchmark | 0% / 0% / 40% / 60% | 6.71% | 12.29% | Fund cap and volatility ceiling |

The selected mix clears the hurdle by about 24 bp and reaches the 40% cap in two funds. Compared with the 60/40 benchmark, it gives up about 98 bp of estimated net return for 5.21 points less estimated volatility. Its figures are sample-based estimates. The fund exposures, risk ceiling and liquidity mechanics are documented in the mandate.

## Stress results and reversal triggers

| Change from base | Result | Decision impact |
| --- | --- | --- |
| VT mean reduced by 2 percentage points | Maximum qualifying net return before the hurdle is 5.13% | Stop. The equity estimate is material to feasibility. |
| Latest 36 months | 6.15% net, 4.30% volatility, weights 40/40/5/15 | Feasible, but VT moves 25 points. Review estimation stability. |
| 50 bp annual implementation cost | 5.53% net, 7.66% volatility, weights 40/0/20/40 | Feasible with only about 3 bp of headroom. Validate trading cost before funding. |
| 30% fund cap and 8% volatility ceiling | Return ceiling 4.13% | Stop under the tighter policy. |
| VT is unavailable within five days | Return ceiling 1.34% | Stop. The liquidity rule permits at most 5% in VT under this stress. |

Reopen the decision once the desk validates five-day cash access for at least 95% of the portfolio, the committee approves its risk limit and benchmark, a separately supported return forecast clears the hurdle under the required stresses, and duration review is complete. Monitor the net-return margin, volatility, liquidity, fund caps, and DGS10. The October 6 signal replay used 5.29%, crossing the 5.00% trigger for a duration review. Any infeasible required case, unavailable evidence or breach pauses allocation. At the annual review, compare realized five-year net compounding with the CPI-based objective and benchmark before voting again.

Edition A was the saved Lab 15 prototype with an edited-versus-loaded comparison. Edition B adds mandate-based comparisons, cost and liquidity rules, a timestamped rate signal, and explicit stop logic. The base output alone could suggest allocation. The stress evidence changes the committee ask to rejection of live capital. Editions are kept privately.
