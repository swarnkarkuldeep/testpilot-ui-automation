# TestPilot UI Automation

A portfolio-grade Playwright + pytest UI automation framework for
[saucedemo.com](https://www.saucedemo.com), a public demo e-commerce store.
It exercises the full customer journey — login, browsing/sorting, cart
management, checkout, and logout/navigation — through a Page Object Model
built on Playwright's auto-waiting and web-first assertions (no
`time.sleep` anywhere).

See [`docs/test_plan.md`](docs/test_plan.md) for the full test plan: scope,
out-of-scope, risks, entry/exit criteria, and the 35-case test catalogue
this suite implements (including a couple of documented cases where the
app's real behavior turned out to differ from the original plan — see its
"corrected" notes).

## Stack

- Python 3.11+
- Playwright (sync API), with tracing enabled on failure
- pytest, with `smoke` and `regression` markers, plus data-driven
  `@pytest.mark.parametrize` cases sourced from `data/*.json` / `data/*.csv`
- Reports: pytest-html (default, self-contained) and Allure (richer, with
  step-by-step actions, severity, and feature labels)
- CI: GitHub Actions (`.github/workflows/tests.yml`)

All tools are free and open source.

## Project structure

```
.github/workflows/tests.yml  CI: smoke on every push, regression on PRs + nightly
docs/test_plan.md            The test plan this suite implements
pages/                       Page Objects — locators and actions only, no assertions
  base_page.py                Shared helpers (navigate/click/fill/get_text) + common header/menu elements
  login_page.py, inventory_page.py, cart_page.py, checkout_page.py
tests/
  smoke/                      Critical-path tests (8, runs in ~10s)
  regression/                 Full functional coverage (40 total incl. smoke)
data/                        JSON/CSV fixtures for parametrized (data-driven) tests
utils/
  config.py                   Env-driven settings (BASE_URL, HEADLESS, timeouts)
  data_loader.py               JSON/CSV loading helpers for test data
  allure_helpers.py            Maps test-plan priorities (P1/P2/P3) to Allure severities
conftest.py                  Browser/context setup, fixtures, screenshot-on-failure hook
pytest.ini                   Marker registration, report/tracing defaults
reports/                     Generated: HTML report, screenshots, Playwright traces (gitignored)
```

## Setup

```bash
py -3.11 -m venv .venv           # see note below on the Python version
source .venv/Scripts/activate    # Windows Git Bash; use .venv\Scripts\activate.ps1 in PowerShell
python -m pip install -r requirements.txt
playwright install chromium
```

> **Python version note:** `playwright`'s `greenlet` dependency does not yet
> ship a prebuilt wheel for very new CPython releases (e.g. 3.14 at the time
> of writing), and building it from source requires the MSVC Build Tools on
> Windows. Use Python 3.11 or 3.12 to avoid that build step entirely.

## Configuration

All optional; they default to the values below.

| Env var | Default | Purpose |
|---|---|---|
| `BASE_URL` | `https://www.saucedemo.com` | Application under test |
| `HEADLESS` | `true` | Set to `false` to watch the browser locally |
| `DEFAULT_TIMEOUT_MS` | `10000` | Default Playwright action/assertion timeout |
| `SLOW_MO_MS` | `0` | Slow down actions by N ms, useful for debugging |

## Running tests

```bash
# Smoke suite (8 tests, ~10s)
pytest -m smoke

# Regression suite (40 tests, includes the smoke tests)
pytest -m regression

# Headed, slowed down, against a local mirror
HEADLESS=false SLOW_MO_MS=250 BASE_URL=http://localhost:3000 pytest -m smoke
```

Every run produces, under `reports/` (gitignored, regenerated each run):

- `reports/report.html` — a self-contained pytest-html report
- `reports/screenshots/<test_name>.png` — full-page screenshot for every
  failed test, embedded in the HTML report automatically
- `reports/test-results/` — a Playwright trace (`.zip`) for every failed
  test, since `pytest.ini` sets `--tracing=retain-on-failure`

Open a trace with:

```bash
playwright show-trace reports/test-results/<test-folder>/trace.zip
```

### Viewing the Allure report

Allure needs its own CLI (a separate download from `allure-pytest`, which
only *generates* the raw results). Install it once, then generate results
on any test run and serve them:

```bash
# Install the Allure CLI (one-time)
# macOS:    brew install allure
# Windows:  scoop install allure   (or download from https://github.com/allure-framework/allure2/releases)
# Linux:    see https://allurereport.org/docs/install-for-linux/

# Generate Allure results and open the report
pytest -m regression --alluredir=allure-results
allure serve allure-results
```

`allure serve` builds a temporary report and opens it in your browser. The
report includes, per test: severity (mapped from the test plan's P1/P2/P3
priorities — critical/normal/minor), a feature label (Login, Inventory,
Cart, Checkout, Logout, Navigation), a step-by-step breakdown of every page
object action performed, and the screenshot attached on failure.

## CI

`.github/workflows/tests.yml` runs on GitHub Actions:

| Trigger | Suite run |
|---|---|
| Push to any branch | Smoke |
| Pull request | Regression |
| Nightly (02:00 UTC) | Regression |
| Manual (`workflow_dispatch`) | Regression |

Every run uploads `reports/` and `allure-results/` as build artifacts
(kept 14 days), even on failure, so a failing CI run's screenshots and
traces are always downloadable from the workflow run page.

## Conventions

- No `time.sleep` anywhere — rely on Playwright auto-waiting and
  `expect()` web-first assertions.
- Page Objects expose locators and actions only; all assertions live in
  test files.
- Locators prefer the app's `data-test` attributes via
  `BasePage.test_id(name)`, with one documented exception (the hamburger
  menu toggle — see the comment in `base_page.py`).
- Semantic page object actions are wrapped in `@allure.step(...)` so the
  Allure report reads as a plain-English list of what each test did.
- Data-driven tests load their cases from `data/*.json` / `data/*.csv` via
  `utils/data_loader.py`, with a `priority` field per row (P1/P2/P3, from
  the test plan) applied to Allure severity via `utils/allure_helpers.py`.
