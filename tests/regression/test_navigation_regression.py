import allure
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage


@allure.feature("Navigation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_hamburger_menu_opens_and_closes(inventory_page: InventoryPage) -> None:
    """TC-NAV-001: The hamburger menu opens to show all navigation links and
    closes cleanly via the close icon."""
    inventory_page.open_menu()

    expect(inventory_page.all_items_link).to_be_visible()
    expect(inventory_page.about_link).to_be_visible()
    expect(inventory_page.logout_link).to_be_visible()
    expect(inventory_page.reset_app_state_link).to_be_visible()

    inventory_page.close_menu()

    expect(inventory_page.all_items_link).to_be_hidden()


@allure.feature("Navigation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_all_items_navigates_back_to_inventory(inventory_page: InventoryPage) -> None:
    """TC-NAV-002: "All Items" navigates back to the inventory page with
    the full product list, from another page in the app."""
    inventory_page.add_to_cart("sauce-labs-backpack")
    inventory_page.go_to_cart()

    inventory_page.open_menu()
    inventory_page.go_to_all_items()

    expect(inventory_page.inventory_items).to_have_count(6)
    expect(inventory_page.page_title).to_have_text("Products")


@allure.feature("Navigation")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_reset_app_state_clears_cart_badge(inventory_page: InventoryPage) -> None:
    """TC-NAV-003 (corrected 2026-09-30 after live verification): "Reset App
    State" clears the cart badge/count, but it does NOT revert an
    already-added product's button back to "Add to cart" — the button stays
    on "Remove" until the page is reloaded or revisited. See
    docs/test_plan.md for the original (incorrect) assumption this
    replaced."""
    inventory_page.add_to_cart("sauce-labs-backpack")
    expect(inventory_page.cart_badge).to_have_text("1")

    inventory_page.open_menu()
    inventory_page.reset_app_state()

    expect(inventory_page.cart_badge).to_have_count(0)
    expect(inventory_page.remove_button("sauce-labs-backpack")).to_be_visible()


@allure.feature("Navigation")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.regression
def test_about_link_points_to_external_site(inventory_page: InventoryPage) -> None:
    """TC-NAV-004: The "About" menu item is present and points to an
    external URL (destination content is out of scope — see
    docs/test_plan.md)."""
    inventory_page.open_menu()

    expect(inventory_page.about_link).to_be_visible()
    expect(inventory_page.about_link).to_have_attribute("href", "https://saucelabs.com/")
