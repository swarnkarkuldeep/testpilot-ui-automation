import re

import allure
import pytest
from playwright.sync_api import Page, expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_loader import load_json

USERS = load_json("users.json")


@allure.feature("Login")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regression
def test_valid_login_redirects_to_inventory(page: Page) -> None:
    """TC-LOGIN-001: Valid login with standard_user redirects to
    /inventory.html with 6 products visible."""
    user = USERS["standard_user"]
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(user["username"], user["password"])

    inventory_page = InventoryPage(page)
    expect(page).to_have_url(re.compile(r".*/inventory\.html"))
    expect(inventory_page.page_title).to_have_text("Products")
    expect(inventory_page.inventory_items).to_have_count(6)


@allure.feature("Login")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regression
def test_locked_out_user_is_denied_access(page: Page) -> None:
    """TC-LOGIN-004: locked_out_user is rejected with the locked-out error
    and remains on the login page."""
    user = USERS["locked_out_user"]
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(user["username"], user["password"])

    expect(login_page.error_message).to_have_text(
        "Epic sadface: Sorry, this user has been locked out."
    )
    expect(page).to_have_url(re.compile(r".*saucedemo\.com/?$"))
