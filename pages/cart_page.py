import allure
from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class CartPage(BasePage):
    URL_PATH = "/cart.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.cart_items = self.test_id("inventory-item")
        self.item_names = self.test_id("inventory-item-name")
        self.item_prices = self.test_id("inventory-item-price")
        self.continue_shopping_button = self.test_id("continue-shopping")
        self.checkout_button = self.test_id("checkout")

    @allure.step("Open the cart page")
    def open(self) -> None:
        self.navigate(self.URL_PATH)

    def remove_button(self, product_slug: str) -> Locator:
        return self.test_id(f"remove-{product_slug}")

    @allure.step("Remove {product_slug} from the cart")
    def remove_from_cart(self, product_slug: str) -> None:
        self.click(self.remove_button(product_slug))

    @allure.step("Continue shopping")
    def continue_shopping(self) -> None:
        self.click(self.continue_shopping_button)

    @allure.step("Proceed to checkout")
    def checkout(self) -> None:
        self.click(self.checkout_button)
