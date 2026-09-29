import re

import allure
import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutCompletePage, CheckoutStepOnePage, CheckoutStepTwoPage
from pages.inventory_page import InventoryPage
from utils.allure_helpers import apply_priority
from utils.data_loader import load_csv, load_json

CHECKOUT_FIELD_CASES = load_csv("checkout_data.csv")
CART_TOTAL_CASES = load_json("checkout_cart_totals.json")


@allure.feature("Checkout")
@pytest.mark.regression
@pytest.mark.parametrize(
    "case", CHECKOUT_FIELD_CASES, ids=[row["id"] for row in CHECKOUT_FIELD_CASES]
)
def test_checkout_field_validation(cart_page_with_item: CartPage, case: dict) -> None:
    """Data-driven checkout field validation (TC-CHK-002, TC-CHK-003,
    TC-CHK-004 — see `case["tc_id"]`): a missing First Name, Last Name, or
    Postal Code blocks checkout with the matching required-field error."""
    apply_priority(case["priority"])
    allure.dynamic.title(f"Checkout field validation: {case['id']} ({case['tc_id']})")

    cart_page_with_item.checkout()

    step_one = CheckoutStepOnePage(cart_page_with_item.page)
    step_one.fill_information(case["first_name"], case["last_name"], case["postal_code"])
    step_one.continue_to_overview()

    expect(step_one.error_message).to_have_text(case["expected_error"])
    expect(step_one.page).to_have_url(re.compile(r".*/checkout-step-one\.html"))


@allure.feature("Checkout")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_cancel_from_checkout_step_one_returns_to_cart(cart_page_with_item: CartPage) -> None:
    """TC-CHK-005: Cancel on checkout step one returns to the cart page
    with its contents unchanged."""
    cart_page_with_item.checkout()
    step_one = CheckoutStepOnePage(cart_page_with_item.page)

    step_one.cancel()

    expect(step_one.page).to_have_url(re.compile(r".*/cart\.html"))
    expect(cart_page_with_item.cart_items).to_have_count(1)


@allure.feature("Checkout")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_cancel_from_checkout_overview_returns_to_inventory(cart_page_with_item: CartPage) -> None:
    """TC-CHK-006: Cancel on the checkout overview page returns to the
    inventory page with cart contents unchanged."""
    cart_page_with_item.checkout()
    step_one = CheckoutStepOnePage(cart_page_with_item.page)
    step_one.fill_information("Kuldeep", "Swarnkar", "500001")
    step_one.continue_to_overview()

    step_two = CheckoutStepTwoPage(cart_page_with_item.page)
    step_two.cancel()

    inventory_page = InventoryPage(cart_page_with_item.page)
    expect(inventory_page.page).to_have_url(re.compile(r".*/inventory\.html"))
    expect(inventory_page.cart_badge).to_have_text("1")


@allure.feature("Checkout")
@pytest.mark.regression
@pytest.mark.parametrize("case", CART_TOTAL_CASES, ids=[row["id"] for row in CART_TOTAL_CASES])
def test_checkout_overview_totals(inventory_page: InventoryPage, case: dict) -> None:
    """TC-CHK-007: The checkout overview's item total, tax, and total match
    the exact values observed live for each cart composition (8% tax,
    rounded to the nearest cent)."""
    apply_priority(case["priority"])
    allure.dynamic.title(f"Checkout overview totals: {case['id']} ({case['tc_id']})")

    for slug in case["product_slugs"]:
        inventory_page.add_to_cart(slug)
    inventory_page.go_to_cart()

    cart_page = CartPage(inventory_page.page)
    cart_page.checkout()

    step_one = CheckoutStepOnePage(cart_page.page)
    step_one.fill_information("Kuldeep", "Swarnkar", "500001")
    step_one.continue_to_overview()

    step_two = CheckoutStepTwoPage(cart_page.page)
    expect(step_two.payment_info_value).to_have_text("SauceCard #31337")
    expect(step_two.shipping_info_value).to_have_text("Free Pony Express Delivery!")
    expect(step_two.subtotal_label).to_have_text(case["expected_subtotal"])
    expect(step_two.tax_label).to_have_text(case["expected_tax"])
    expect(step_two.total_label).to_have_text(case["expected_total"])


@allure.feature("Checkout")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_checkout_with_multiple_items_reaches_confirmation(inventory_page: InventoryPage) -> None:
    """TC-CHK-008: Checking out with 3 items carries all of them through to
    the overview, and completes to the confirmation page."""
    slugs = ["sauce-labs-backpack", "sauce-labs-bike-light", "sauce-labs-bolt-t-shirt"]
    for slug in slugs:
        inventory_page.add_to_cart(slug)
    inventory_page.go_to_cart()

    cart_page = CartPage(inventory_page.page)
    cart_page.checkout()

    step_one = CheckoutStepOnePage(cart_page.page)
    step_one.fill_information("Kuldeep", "Swarnkar", "500001")
    step_one.continue_to_overview()

    step_two = CheckoutStepTwoPage(cart_page.page)
    expect(step_two.item_names).to_have_count(3)
    step_two.finish()

    complete_page = CheckoutCompletePage(cart_page.page)
    expect(complete_page.page).to_have_url(re.compile(r".*/checkout-complete\.html"))
    expect(complete_page.complete_header).to_have_text("Thank you for your order!")
