# Project 2 — Investment Management Application

**AI use.** OpenAI Codex organized lab materials, implemented the Python and Streamlit workflow, wrote verification checks, and drafted materials for student review.

**Student statement for review.** After I independently review and approve the analysis and decision, I attest that they are mine. This project is for education, not investment advice.

## Run the app

In the directory containing this README, use Python 3.11. Windows PowerShell commands:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe -m streamlit run python/app.py
```

On macOS or Linux use `python3.11 -m venv .venv` and substitute `.venv/bin/python` in the remaining commands. Open the localhost URL displayed in the terminal. Once dependencies are installed, the app uses frozen files and needs no internet connection, accounts or API keys. Use Ctrl+C to stop the server.

The default view shows the committee decision, portfolio weights and separate rule verdicts, required stresses, and the archived rate signal. The sidebar changes the estimation window, equity mean, annual cost, concentration cap, volatility limit, CPI assumption and liquidity availability. Reload a clean session to restore defaults. A failed screen produces a stop and shows whether the other rules still allow any mix. Liquidity shown is modeled. The archive intentionally replays a fixed historical decision.

Run `.venv\Scripts\python.exe python/verify_project.py` to execute the verification suite. Use the same macOS/Linux substitution as above.

## Review the evidence

- [Decision memo](docs/decision-memo.md) and [mandate](docs/mandate.md)
- [Validation and AI use](docs/validation-and-ai-use.md) and [cold-run evidence](docs/cold-run-log.md)
- [Price data card](docs/price-data-card.md) and [point-in-time signal card](docs/signal-data-card.md)
- [Submission manifest](docs/submission-manifest.md)

The app is the entry point. `python/decision.py` evaluates the policy, constructs the comparisons and reads the selected yield vintage. `python/portfolio.py` provides the estimator, covariance and baseline calculations. `python/verify_project.py` checks the inputs, known answers, failure modes and Streamlit interactions. The private Edition A/B copies sit outside the intended GitHub package.
