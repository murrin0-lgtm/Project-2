# Reproduction log

## Fresh local copy — passed

- November 22, 2026, approximately 8:20 p.m. Eastern. Source, docs and data were copied to a clean workspace directory. A new environment was created with `py -3.11 -m venv .venv`.
- Windows, Python 3.11.4, pip 23.1.2, Streamlit 1.66.1, pandas 3.1.1, NumPy 2.4.6 and PyArrow 26.0.1. The README dependency install succeeded without account credentials.
- `.venv\Scripts\python.exe python/verify_project.py` exited 0. All 244 monthly prices reconciled to daily captures. Base constrained weights were 40/20/0/40, net estimate 5.7381%, annual volatility 7.0778%. Stress output matched the memo. Both signal vintages returned 5.29% on September 30. Streamlit tests verified three tables and the 36-month and liquidity controls.
- The main workspace app also started with `python -m streamlit run python/app.py` in headless mode, and the localhost health endpoint returned HTTP 200 `ok`. The local server was stopped after the check.

## Fresh GitHub clone — pending

Repository inspection on November 23, 2026 found that [commit `a96b66a`](https://github.com/murrin0-lgtm/Project-2/commit/a96b66a9c79e39d05df750100fe4c95ea123b8e6) contained only the prediction and validation Markdown files at the repository root. The README, app, inputs and dependency file were absent, so this revision could not be tested as a runnable app. The local reproduction above applies to the workspace copy.

After publishing, record the repository URL, commit ID, date, environment and exact commands. Repeat the README launch and suite from an actual clone with ordinary grader credentials. Verify the repository and manifest as a grader.
