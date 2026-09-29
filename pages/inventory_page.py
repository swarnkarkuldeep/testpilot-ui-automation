import allure
from playwright.sync_api import Locator, Page

from pages.base_page import BasePage


class InventoryPage(BasePage):
    URL_PATH = "/inventory.html"

    def __init__(self, page: Page):
        super().__init__(page)
        self.sort_dropdown = self.test_id("product-sort-container")
        self.inventory_items = self.test_id("inventory-item")
        self.item_names = self.test_id("inventory-item-name")
        self.item_prices = self.test_id("inventory-item-price")

    @allure.step("Open the inventory page")
    def open(self) -> None:
        self.navigate(self.URL_PATH)

    def add_to_cart_button(self, product_slug: str) -> Locator:
        return self.test_id(f"add-to-cart-{product_slug}")

    def remove_button(self, product_slug: str) -> Locator:
        return self.test_id(f"remove-{product_slug}")

    @allure.step("Add {product_slug} to cart")
    def add_to_cart(self, product_slug: str) -> None:
        self.click(self.add_to_cart_button(product_slug))

    @allure.step("Remove {product_slug} from cart")
    def remove_from_cart(self, product_slug: str) -> None:
        self.click(self.remove_button(product_slug))

    @allure.step("Sort products by {option_value}")
    def sort_by(self, option_value: str) -> None:
        self.sort_dropdown.select_option(option_value)
