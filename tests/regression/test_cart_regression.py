import re

import allure
import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutStepOnePage
from pages.inventory_page import InventoryPage


@allure.feature("Cart")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_remove_item_from_cart_page(cart_page_with_item: CartPage) -> None:
    """TC-CART-002: Removing an item from the cart page removes it from the
    list and decrements the cart badge."""
    expect(cart_page_with_item.cart_items).to_have_count(1)

    cart_page_with_item.remove_from_cart("sauce-labs-backpack")

    expect(cart_page_with_item.cart_items).to_have_count(0)
    expect(cart_page_with_item.cart_badge).to_have_count(0)


@allure.feature("Cart")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_continue_shopping_returns_to_inventory(cart_page_with_item: CartPage) -> None:
    """TC-CART-003: Continue Shopping returns to the inventory page with
    the previously added item still in the cart."""
    cart_page_with_item.continue_shopping()

    inventory_page = InventoryPage(cart_page_with_item.page)
    expect(inventory_page.page).to_have_url(re.compile(r".*/inventory\.html"))
    expect(inventory_page.cart_badge).to_have_text("1")
    expect(inventory_page.remove_button("sauce-labs-backpack")).to_be_visible()


@allure.feature("Cart")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.regression
def test_empty_cart_checkout_proceeds_to_checkout_step_one(inventory_page: InventoryPage) -> None:
    """TC-CART-005 (corrected 2026-09-30 after live verification): the app
    does not block checkout on an empty cart. Clicking Checkout with 0
    items still navigates to checkout step one, with an empty order — it
    does not error and does not stay on /cart.html. See docs/test_plan.md
    for the original (incorrect) assumption this replaced."""
    inventory_page.go_to_cart()
    cart_page = CartPage(inventory_page.page)
    expect(cart_page.cart_items).to_have_count(0)

    cart_page.checkout()

    step_one = CheckoutStepOnePage(cart_page.page)
    expect(step_one.page).to_have_url(re.compile(r".*/checkout-step-one\.html"))
    expect(step_one.page_title).to_have_text("Checkout: Your Information")
