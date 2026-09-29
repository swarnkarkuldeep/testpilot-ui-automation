"""Page Objects for the three-step checkout flow.

Kept in one module since they form a single logical flow (step one -> step
two/overview -> complete) and are small enough individually to stay
readable together.
"""

import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class CheckoutStepOnePage(BasePage):
    URL_PATH = "/checkout-step-one.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.first_name_input = self.test_id("firstName")
        self.last_name_input = self.test_id("lastName")
        self.postal_code_input = self.test_id("postalCode")
        self.continue_button = self.test_id("continue")
        self.cancel_button = self.test_id("cancel")
        self.error_message = self.test_id("error")

    @allure.step("Open checkout step one")
    def open(self) -> None:
        self.navigate(self.URL_PATH)

    @allure.step("Fill checkout information: {first_name} {last_name}, {postal_code}")
    def fill_information(self, first_name: str, last_name: str, postal_code: str) -> None:
        self.fill(self.first_name_input, first_name)
        self.fill(self.last_name_input, last_name)
        self.fill(self.postal_code_input, postal_code)

    @allure.step("Continue to checkout overview")
    def continue_to_overview(self) -> None:
        self.click(self.continue_button)

    @allure.step("Cancel checkout")
    def cancel(self) -> None:
        self.click(self.cancel_button)


class CheckoutStepTwoPage(BasePage):
    URL_PATH = "/checkout-step-two.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.item_names = self.test_id("inventory-item-name")
        self.item_prices = self.test_id("inventory-item-price")
        self.payment_info_value = self.test_id("payment-info-value")
        self.shipping_info_value = self.test_id("shipping-info-value")
        self.subtotal_label = self.test_id("subtotal-label")
        self.tax_label = self.test_id("tax-label")
        self.total_label = self.test_id("total-label")
        self.finish_button = self.test_id("finish")
        self.cancel_button = self.test_id("cancel")

    @allure.step("Finish checkout")
    def finish(self) -> None:
        self.click(self.finish_button)

    @allure.step("Cancel checkout")
    def cancel(self) -> None:
        self.click(self.cancel_button)


class CheckoutCompletePage(BasePage):
    URL_PATH = "/checkout-complete.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.complete_header = self.test_id("complete-header")
        self.complete_text = self.test_id("complete-text")
        self.back_home_button = self.test_id("back-to-products")
