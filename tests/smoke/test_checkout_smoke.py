import re

import allure
import pytest
from playwright.sync_api import expect

from pages.cart_page import CartPage
from pages.checkout_page import (
    CheckoutCompletePage,
    CheckoutStepOnePage,
    CheckoutStepTwoPage,
)


@allure.feature("Checkout")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.regression
def test_happy_path_checkout_completes(cart_page_with_item: CartPage) -> None:
    """TC-CHK-001: Completing checkout with valid information reaches the
    confirmation page and clears the cart badge."""
    page = cart_page_with_item.page
    cart_page_with_item.checkout()

    step_one = CheckoutStepOnePage(page)
    step_one.fill_information("Kuldeep", "Swarnkar", "500001")
    step_one.continue_to_overview()

    step_two = CheckoutStepTwoPage(page)
    step_two.finish()

    complete_page = CheckoutCompletePage(page)
    expect(page).to_have_url(re.compile(r".*/checkout-complete\.html"))
    expect(complete_page.complete_header).to_have_text("Thank you for your order!")
    expect(complete_page.complete_text).to_have_text(
        "Your order has been dispatched, and will arrive just as fast as the pony can get there!"
    )
    expect(complete_page.cart_badge).to_have_count(0)
