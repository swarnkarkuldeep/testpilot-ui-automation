import allure
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage


@allure.feature("Inventory")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regression
def test_inventory_displays_all_six_products(inventory_page: InventoryPage) -> None:
    """TC-INV-001: Inventory page displays exactly 6 product cards, each
    with a name, price, and Add to cart button."""
    expect(inventory_page.inventory_items).to_have_count(6)
    expect(inventory_page.item_names).to_have_count(6)
    expect(inventory_page.item_prices).to_have_count(6)
    expect(inventory_page.add_to_cart_button("sauce-labs-backpack")).to_be_visible()


@allure.feature("Inventory")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regression
def test_add_single_product_updates_badge_and_button(inventory_page: InventoryPage) -> None:
    """TC-INV-006: Adding a product to the cart flips its button to Remove
    and shows a cart badge count of 1."""
    inventory_page.add_to_cart("sauce-labs-backpack")

    expect(inventory_page.remove_button("sauce-labs-backpack")).to_be_visible()
    expect(inventory_page.cart_badge).to_have_text("1")
