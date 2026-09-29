import re

import allure
import pytest
from playwright.sync_api import Page, expect

from pages.login_page import LoginPage
from utils.allure_helpers import apply_priority
from utils.data_loader import load_json

USERS = load_json("users.json")
INVALID_LOGINS = load_json("invalid_logins.json")


@allure.feature("Login")
@pytest.mark.regression
@pytest.mark.parametrize("case", INVALID_LOGINS, ids=[row["id"] for row in INVALID_LOGINS])
def test_login_is_rejected(page: Page, case: dict) -> None:
    """Data-driven login rejection scenarios: locked-out user, invalid
    credentials, and empty-field validation (TC-LOGIN-004, TC-LOGIN-005,
    TC-LOGIN-006, TC-LOGIN-007, TC-LOGIN-008 — see `case["tc_id"]`).

    All of these render through the same login error banner, so one
    parametrized assertion covers every row.
    """
    apply_priority(case["priority"])
    allure.dynamic.title(f"Login is rejected: {case['id']} ({case['tc_id']})")

    login_page = LoginPage(page)
    login_page.open()
    login_page.login(case["username"], case["password"])

    expect(login_page.error_message).to_have_text(case["expected_error"])
    expect(page).to_have_url(re.compile(r".*saucedemo\.com/?$"))


@allure.feature("Login")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_performance_glitch_user_can_login(page: Page) -> None:
    """TC-LOGIN-002: performance_glitch_user logs in successfully, despite
    the deliberately added latency."""
    user = USERS["performance_glitch_user"]
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(user["username"], user["password"])

    expect(page).to_have_url(re.compile(r".*/inventory\.html"), timeout=15000)


@allure.feature("Login")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_problem_user_login_shows_broken_images(page: Page) -> None:
    """TC-LOGIN-003: problem_user logs in successfully, but every product
    image is the same broken placeholder image (a known app quirk)."""
    user = USERS["problem_user"]
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(user["username"], user["password"])

    expect(page).to_have_url(re.compile(r".*/inventory\.html"))

    product_images = page.locator('img[data-test$="-img"]')
    expect(product_images).to_have_count(6)
    first_image_src = product_images.first.get_attribute("src")

    # problem_user's known quirk: every product renders the exact same
    # broken placeholder image, rather than each product's own picture.
    expect(page.locator(f'img[data-test$="-img"][src="{first_image_src}"]')).to_have_count(6)
