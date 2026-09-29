import re

import allure
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@allure.feature("Logout")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regression
def test_logout_returns_to_login_page(inventory_page: InventoryPage) -> None:
    """TC-LOGOUT-001: Logging out from the hamburger menu returns the user
    to the login page."""
    inventory_page.open_menu()
    inventory_page.logout()

    login_page = LoginPage(inventory_page.page)
    expect(inventory_page.page).to_have_url(re.compile(r".*saucedemo\.com/?$"))
    expect(login_page.login_button).to_be_visible()
