import allure
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_loader import load_json

STANDARD_USER = load_json("users.json")["standard_user"]


@allure.feature("Logout")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.regression
def test_cart_persists_across_logout_and_relogin(inventory_page: InventoryPage) -> None:
    """TC-LOGOUT-002 (corrected 2026-09-30 after live verification): cart
    state is kept in browser storage independent of the login session, so
    the cart badge shows the SAME count after logging back in — it is not
    cleared. See docs/test_plan.md for the original (incorrect) assumption
    this replaced."""
    inventory_page.add_to_cart("sauce-labs-backpack")
    expect(inventory_page.cart_badge).to_have_text("1")

    inventory_page.open_menu()
    inventory_page.logout()

    login_page = LoginPage(inventory_page.page)
    expect(login_page.login_button).to_be_visible()
    login_page.login(STANDARD_USER["username"], STANDARD_USER["password"])

    re_logged_in_inventory = InventoryPage(inventory_page.page)
    expect(re_logged_in_inventory.cart_badge).to_have_text("1")
