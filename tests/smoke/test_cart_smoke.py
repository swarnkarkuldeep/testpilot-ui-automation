import re

import allure
import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage


@allure.feature("Cart")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regression
def test_cart_reflects_added_item(inventory_page: InventoryPage) -> None:
    """TC-CART-001: The cart page lists exactly the item added from
    inventory, with matching name and price."""
    inventory_page.add_to_cart("sauce-labs-backpack")
    inventory_page.go_to_cart()

    cart_page = CartPage(inventory_page.page)
    expect(cart_page.cart_items).to_have_count(1)
    expect(cart_page.item_names).to_have_text("Sauce Labs Backpack")
    expect(cart_page.item_prices).to_have_text("$29.99")


@allure.feature("Cart")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regression
def test_checkout_button_navigates_to_checkout_step_one(cart_page_with_item: CartPage) -> None:
    """TC-CART-004: Clicking Checkout from the cart page navigates to
    checkout step one."""
    cart_page_with_item.checkout()

    expect(cart_page_with_item.page).to_have_url(re.compile(r".*/checkout-step-one\.html"))
    expect(cart_page_with_item.page_title).to_have_text("Checkout: Your Information")
