# Test Plan — TestPilot UI Automation (Sauce Demo)

## 1. Objective

Validate the core user journeys of the Sauce Demo e-commerce web application
(login, product browsing/sorting, cart management, checkout, and
navigation/logout) through an automated Playwright + pytest suite built on
the Page Object Model, producing HTML/Allure reports with failure
screenshots for fast triage.

This test plan is written before any automation code, per the framework's
test-first approach. Expected results below were verified against the live
application on 2026-09-29, not assumed from memory.

## 2. Scope

- Login flows: valid login, invalid credentials, locked-out user, empty
  field validation, session handling.
- Inventory page: product listing, product count, all four sort orders,
  add-to-cart / remove-from-cart, cart badge state, known data-quality
  quirks of special test users (`problem_user`, `performance_glitch_user`).
- Cart page: item reflection, removal, navigation (Continue Shopping,
  Checkout).
- Checkout flow: "Your Information" field validation, order overview
  (payment/shipping info, item total, tax, total), Cancel from both
  checkout steps, order completion (confirmation page).
- Logout and menu navigation (hamburger menu: All Items, Logout, Reset App
  State).
- Data-driven coverage for negative login inputs and checkout field
  validation, using external JSON/CSV fixtures.

## 3. Out of Scope

- Visual regression / pixel-diff testing (e.g. asserting `problem_user`'s
  broken images pixel-for-pixel) — only functional impact is asserted.
- Performance/load testing of `performance_glitch_user` beyond a generous
  functional timeout.
- The "Dynamic Catalog" hamburger sub-menu and "Generate PDF order" button
  — present on the live site but outside the requirements given for this
  framework; may be added in a future iteration.
- Third-party/external links (e.g. "About", social icons in the footer)
  beyond confirming they exist — no assertions on the external destination
  site's content.
- Cross-browser/cross-device matrix (initial suite targets Chromium via
  Playwright; extending to Firefox/WebKit is a future enhancement).
- API-level or database-level validation (Sauce Demo exposes no test API).

## 4. Test Environment

| Item | Detail |
|---|---|
| Application Under Test | https://www.saucedemo.com |
| Browser(s) | Chromium (Playwright-managed), headless in CI / headed for local debugging |
| OS | Windows 11 (local dev), Linux (CI runner) |
| Test Users | `standard_user`, `locked_out_user`, `problem_user`, `performance_glitch_user` — password `secret_sauce` for all |
| Network | Public internet; no test data setup/teardown required (app has no persistent backend state) |

## 5. Tools

| Purpose | Tool |
|---|---|
| Language / runtime | Python 3.11+ |
| Browser automation | Playwright (sync API) |
| Test runner | pytest |
| Design pattern | Page Object Model |
| Data-driven testing | `pytest.mark.parametrize` fed by JSON/CSV fixture files |
| Reporting | pytest-html (default), allure-pytest (optional, richer report) |
| Failure evidence | Playwright screenshot-on-failure, attached to both report formats |
| Waiting strategy | Playwright auto-waiting + `expect()` web-first assertions only — no `time.sleep` |

All tools are free and open source.

## 6. Risks & Assumptions

- **Shared public environment**: saucedemo.com is a public demo instance with
  no isolated test environment; assume test data (products, prices) remains
  stable but note that the vendor could change copy/UI without notice
  (mitigate with resilient, semantic locators rather than brittle text/CSS
  matches where practical).
- **`performance_glitch_user` latency**: this user intentionally simulates
  slow page loads. Tests using it must use generous explicit `expect(...).
  to_be_visible(timeout=...)` waits rather than fixed sleeps, and should be
  isolated from the smoke suite's under-1-minute budget.
- **`problem_user` quirks**: this user is known to have broken product
  images and non-functional UI elements (e.g., sorting may not visibly
  reorder). Tests against this user assert the documented quirk itself
  (e.g., images fail to load) rather than treating it as a random flake.
- **No test isolation between runs**: cart contents reset only via full page
  reload/new session or "Reset App State"; tests must not depend on
  execution order and should reset state (fresh login / Reset App State) in
  setup.
- **Flakiness from network latency**: since this hits a real public site
  over the internet (not a local mock), occasional slowness is expected;
  mitigated by Playwright's built-in auto-waiting rather than arbitrary
  sleeps.
- **UI copy changes**: exact strings (e.g., confirmation message wording)
  were captured from the live site on 2026-09-29 and are asserted exactly;
  if the vendor updates copy, affected assertions will need updating.

## 7. Entry Criteria

- Test plan reviewed and approved.
- Framework scaffolding (Playwright + pytest + POM structure) implemented
  and able to launch a browser against saucedemo.com.
- Test data fixtures (`data/*.json`, `data/*.csv`) created for
  parametrized cases.
- Page Objects implemented for: Login, Inventory, Cart, Checkout (step one
  and two), Checkout Complete, and the common header/menu component.

## 8. Exit Criteria

- 100% of Smoke suite tests pass before any merge to the main branch.
- 100% of Regression suite tests pass (or failures are triaged, and
  understood to be environment/data flakiness rather than product defects)
  before a release/tag.
- No `time.sleep` present anywhere in the codebase (verified by code
  review / lint rule).
- HTML and Allure reports generate successfully with screenshots attached
  to every failed test.

## 9. Suite Execution Strategy

Tests are tagged with pytest markers registered in `pytest.ini` /
`pyproject.toml`:

```ini
[pytest]
markers =
    smoke: fast, critical-path checks (~5 tests, runs in under 1 minute)
    regression: full functional coverage (20+ tests)
```

Every smoke test is also part of the regression suite (regression is a
superset), achieved by applying both markers to the smoke-tagged tests.

**Run smoke suite:**
```bash
pytest -m smoke --html=report.html --self-contained-html
```

**Run regression suite:**
```bash
pytest -m regression --html=report.html --self-contained-html
```

**Run with Allure:**
```bash
pytest -m regression --alluredir=allure-results
allure serve allure-results
```

Smoke runs are intended for pre-merge CI gating (fast feedback); regression
runs are intended for nightly/pre-release gating.

## 10. Test Cases

Legend — Priority: P1 = critical path, P2 = important, P3 = edge case.
Suite: Smoke, Regression, or Both (Both = tagged with both markers).

| ID | Title | Preconditions | Steps | Expected Result | Priority | Suite | Data-driven |
|---|---|---|---|---|---|---|---|
| TC-LOGIN-001 | Valid login with standard_user | Browser open at login page | 1. Enter `standard_user` / `secret_sauce`. 2. Click Login. | Redirected to `/inventory.html`; page title "Products"; 6 products visible. | P1 | Both | N |
| TC-LOGIN-002 | Valid login with performance_glitch_user | Browser open at login page | 1. Enter `performance_glitch_user` / `secret_sauce`. 2. Click Login. | Login succeeds (with noticeable delay); redirected to `/inventory.html` within an extended timeout. | P2 | Regression | N |
| TC-LOGIN-003 | Valid login with problem_user | Browser open at login page | 1. Enter `problem_user` / `secret_sauce`. 2. Click Login. | Login succeeds; redirected to `/inventory.html`; product images render broken (known app quirk, asserted explicitly). | P2 | Regression | N |
| TC-LOGIN-004 | Locked-out user is denied access | Browser open at login page | 1. Enter `locked_out_user` / `secret_sauce`. 2. Click Login. | Login is rejected; error banner reads "Epic sadface: Sorry, this user has been locked out."; user remains on login page. | P1 | Both | N |
| TC-LOGIN-005 | Invalid credentials are rejected | Browser open at login page | 1. Enter a set of invalid username/password combinations. 2. Click Login. | Error banner reads "Epic sadface: Username and password do not match any user in this service"; user remains on login page. | P1 | Regression | Y |
| TC-LOGIN-006 | Empty username shows required-field error | Browser open at login page | 1. Leave Username blank; enter password `secret_sauce`. 2. Click Login. | Error banner reads "Epic sadface: Username is required". | P2 | Regression | N |
| TC-LOGIN-007 | Empty password shows required-field error | Browser open at login page | 1. Enter Username `standard_user`; leave Password blank. 2. Click Login. | Error banner reads "Epic sadface: Password is required". | P2 | Regression | N |
| TC-LOGIN-008 | Empty username and password shows required-field error | Browser open at login page | 1. Leave both fields blank. 2. Click Login. | Error banner reads "Epic sadface: Username is required" (username validated first). | P3 | Regression | N |
| TC-INV-001 | Inventory displays all 6 products | Logged in as standard_user | 1. Land on `/inventory.html`. | Exactly 6 product cards are displayed, each with name, description, price, and "Add to cart" button. | P1 | Both | N |
| TC-INV-002 | Default sort is Name (A to Z) | Logged in as standard_user | 1. Land on `/inventory.html`. 2. Read sort dropdown and product order. | Sort dropdown shows "Name (A to Z)" selected; products are alphabetically ascending by name. | P2 | Regression | N |
| TC-INV-003 | Sort by Name (Z to A) reorders products | Logged in as standard_user, on inventory page | 1. Select "Name (Z to A)" from sort dropdown. | Product list re-renders in reverse alphabetical order by name. | P2 | Regression | N |
| TC-INV-004 | Sort by Price (low to high) reorders products | Logged in as standard_user, on inventory page | 1. Select "Price (low to high)" from sort dropdown. | Products are ordered by ascending price ($7.99 → $49.99). | P2 | Regression | N |
| TC-INV-005 | Sort by Price (high to low) reorders products | Logged in as standard_user, on inventory page | 1. Select "Price (high to low)" from sort dropdown. | Products are ordered by descending price ($49.99 → $7.99). | P2 | Regression | N |
| TC-INV-006 | Add single product to cart updates badge and button | Logged in as standard_user, on inventory page | 1. Click "Add to cart" on "Sauce Labs Backpack". | Button changes to "Remove"; cart icon badge shows "1". | P1 | Both | N |
| TC-INV-007 | Add multiple products updates cart badge count | Logged in as standard_user, on inventory page | 1. Click "Add to cart" on 3 different products. | Cart icon badge shows "3"; all 3 buttons read "Remove". | P2 | Regression | N |
| TC-INV-008 | Remove product from inventory page | Logged in as standard_user, product already in cart | 1. Click "Remove" on a product already added. | Button reverts to "Add to cart"; cart badge count decrements (badge disappears if count reaches 0). | P2 | Regression | N |
| TC-CART-001 | Cart page reflects items added from inventory | Logged in as standard_user, 1+ items added to cart | 1. Click cart icon. | `/cart.html` lists exactly the items added, with correct name, description, and price; QTY = 1 each. | P1 | Both | N |
| TC-CART-002 | Remove item from cart page | On cart page with 1+ items | 1. Click "Remove" next to an item. | Item is removed from the cart list; cart badge count decrements accordingly. | P2 | Regression | N |
| TC-CART-003 | Continue Shopping returns to inventory | On cart page | 1. Click "Continue Shopping". | Redirected to `/inventory.html`; previously added items remain in cart (badge count preserved). | P2 | Regression | N |
| TC-CART-004 | Checkout button navigates to checkout step one | On cart page with 1+ items | 1. Click "Checkout". | Redirected to `/checkout-step-one.html`, "Checkout: Your Information" header shown. | P1 | Both | N |
| TC-CART-005 | Empty cart checkout is handled gracefully | On cart page with 0 items | 1. Click "Checkout". | **Corrected 2026-09-30 — an earlier manual check of this got a false negative from a flaky click and wrongly concluded it was a no-op; the automated regression test caught the real behavior.** The app does not validate cart contents before checkout: clicking Checkout with 0 items still navigates to `/checkout-step-one.html` and shows the (empty) "Checkout: Your Information" form. It does not error and does not stay on `/cart.html`. | P3 | Regression | N |
| TC-CHK-001 | Happy path checkout completes successfully | Logged in as standard_user, 1 item in cart, on checkout step one | 1. Enter First Name, Last Name, Zip/Postal Code. 2. Click Continue. 3. Review order overview. 4. Click Finish. | Redirected to `/checkout-complete.html`; page shows "Thank you for your order!" and "Your order has been dispatched, and will arrive just as fast as the pony can get there!"; cart badge is cleared. | P1 | Both | N |
| TC-CHK-002 | Missing First Name blocks checkout | On checkout step one, Last Name and Zip filled | 1. Leave First Name blank. 2. Click Continue. | Error banner reads "Error: First Name is required"; user remains on checkout step one. | P1 | Regression | Y |
| TC-CHK-003 | Missing Last Name blocks checkout | On checkout step one, First Name and Zip filled | 1. Leave Last Name blank. 2. Click Continue. | Error banner reads "Error: Last Name is required"; user remains on checkout step one. | P2 | Regression | Y |
| TC-CHK-004 | Missing Zip/Postal Code blocks checkout | On checkout step one, First Name and Last Name filled | 1. Leave Zip/Postal Code blank. 2. Click Continue. | Error banner reads "Error: Postal Code is required"; user remains on checkout step one. | P2 | Regression | Y |
| TC-CHK-005 | Cancel from checkout step one returns to cart | On checkout step one | 1. Click "Cancel". | Redirected to `/cart.html`; cart contents unchanged. | P2 | Regression | N |
| TC-CHK-006 | Cancel from checkout overview returns to inventory | On checkout step two (overview) | 1. Click "Cancel". | Redirected to `/inventory.html`; cart contents unchanged. | P2 | Regression | N |
| TC-CHK-007 | Order overview shows correct item total, tax, and total | On checkout step two (overview), with known cart contents | 1. Read Payment Information, Shipping Information, and Price Total section. | Payment Info shows "SauceCard #31337"; Shipping shows "Free Pony Express Delivery!"; Item total matches sum of cart item prices; Total equals item total + tax. | P1 | Regression | Y |
| TC-CHK-008 | Checkout with multiple items carries all items through to confirmation | Logged in as standard_user, 3 items in cart | 1. Complete checkout steps one and two. 2. Click Finish. | Order overview lists all 3 items with correct prices before Finish; confirmation page displays after Finish. | P2 | Regression | N |
| TC-LOGOUT-001 | Logout returns user to login page | Logged in as standard_user, on any authenticated page | 1. Open hamburger menu. 2. Click "Logout". | Redirected to `/`; login form is displayed; URL no longer contains an authenticated route. | P1 | Both | N |
| TC-LOGOUT-002 | Cart state persists across logout/re-login | Logged in as standard_user, item(s) in cart | 1. Add item(s) to cart. 2. Logout. 3. Log back in as standard_user. | **Corrected 2026-09-30 after live verification — the original assumption below this line was wrong.** Cart state is kept in browser storage independent of the login session: the inventory page shows the *same* cart badge count as before logout, not cleared. (Originally assumed: "Inventory page shows cart badge cleared (no residual items from the prior session)" — this was disproven live and inverted.) | P3 | Regression | N |
| TC-NAV-001 | Hamburger menu opens and closes | Logged in as standard_user, on inventory page | 1. Click hamburger icon. 2. Click the "X" close icon. | Menu slides open showing All Items, About, Logout, Reset App State; closes cleanly on "X" click. | P2 | Regression | N |
| TC-NAV-002 | "All Items" navigates back to inventory from any page | Logged in as standard_user, on cart or checkout page | 1. Open hamburger menu. 2. Click "All Items". | Redirected to `/inventory.html` with full 6-product list displayed. | P2 | Regression | N |
| TC-NAV-003 | "Reset App State" clears the cart badge, but not button state | Logged in as standard_user, 1+ items in cart | 1. Open hamburger menu. 2. Click "Reset App State". | **Corrected 2026-09-30 after live verification.** The cart badge/count is cleared, but an already-added product's button stays on "Remove" — it does **not** revert to "Add to cart" until the page is reloaded or revisited. (Originally assumed: "Add to cart buttons revert to their default (unadded) state without a page reload" — disproven live.) | P2 | Regression | N |
| TC-NAV-004 | "About" menu item is present and links out | Logged in as standard_user, on inventory page | 1. Open hamburger menu. 2. Inspect "About" link. | "About" link is present in the menu and points to an external URL (destination content not asserted; see Out of Scope). | P3 | Regression | N |

**Total: 35 test cases** (8 Login, 8 Inventory, 5 Cart, 8 Checkout, 2 Logout,
4 Navigation) — exceeds the 25-case minimum. 8 are tagged Both (forming the
Smoke suite: TC-LOGIN-001, TC-LOGIN-004, TC-INV-001, TC-INV-006,
TC-CART-001, TC-CART-004, TC-CHK-001, TC-LOGOUT-001), and the remaining 27
are Regression-only, giving a Regression suite of 35 (superset) and a Smoke
suite of 8 — still comfortably under the 1-minute budget in practice (runs
in ~8s locally).

## 11. Data-Driven Fixtures

| File | Used by | Contents |
|---|---|---|
| `data/users.json` | fixtures in `conftest.py` | The 4 named test accounts and what each is expected to do |
| `data/invalid_logins.json` | TC-LOGIN-004/005/006/007/008 | Rows of `{id, tc_id, username, password, expected_error}` covering locked-out, invalid-credential, and empty-field login rejections — all asserted against the same `error` banner |
| `data/sort_options.json` | TC-INV-002/003/004/005 | Rows of `{id, tc_id, option_value, expected_names, expected_prices}`, one per sort order, with the exact product order observed live (note: price ties are **not** simply reversed between low-to-high and high-to-low — see the regression suite report) |
| `data/checkout_data.csv` | TC-CHK-002/003/004 | Rows of `(id, tc_id, first_name, last_name, postal_code, expected_error)` covering each missing-field case |
| `data/checkout_cart_totals.json` | TC-CHK-007 | Product slug sets paired with the exact observed item total / tax / total (8% tax, rounded to the nearest cent) |

## 12. Logged Defects

Discrepancies found between this plan's assumptions and the app's live
behavior were filed as GitHub Issues with reproducible steps, expected vs.
actual results, and a severity rating, rather than silently "fixed" in the
plan:

| Issue | Test Case | Severity | Summary |
|---|---|---|---|
| [#1](https://github.com/swarnkarkuldeep/testpilot-ui-automation/issues/1) | TC-NAV-003 | Low | "Reset App State" clears the cart badge but leaves the "Remove" button stuck (stale UI state) |
| [#2](https://github.com/swarnkarkuldeep/testpilot-ui-automation/issues/2) | TC-LOGOUT-002 | Low | Cart contents persist across logout/login instead of resetting per session |
| [#3](https://github.com/swarnkarkuldeep/testpilot-ui-automation/issues/3) | TC-CART-005 | Medium | Checkout proceeds with an empty cart — no validation blocks it |
