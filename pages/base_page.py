"""Shared base class for all Page Objects.

Holds only generic Playwright helpers (navigation, click, fill, read text,
and building locators from the app's `data-test` attributes). No assertions
live here or in any subclass — assertions belong in the tests.
"""

from __future__ import annotations

import allure
from playwright.sync_api import Locator, Page

from utils.config import Config


class BasePage:
    def __init__(self, page: Page):
        self.page = page

        # Header/menu elements shared by every authenticated page (absent
        # only on the login page, where they simply go unused).
        self.page_title = self.test_id("title")
        # The app's `data-test="open-menu"`/`"close-menu"` attributes sit on
        # decorative <img> elements that the react-burger-menu library's own
        # <button> visually covers, so a real click actually lands on that
        # button. Target it by its accessible name instead.
        self.menu_button = self.page.get_by_role("button", name="Open Menu")
        self.close_menu_button = self.page.get_by_role("button", name="Close Menu")
        self.cart_link = self.test_id("shopping-cart-link")
        self.cart_badge = self.test_id("shopping-cart-badge")
        self.all_items_link = self.test_id("inventory-sidebar-link")
        self.about_link = self.test_id("about-sidebar-link")
        self.logout_link = self.test_id("logout-sidebar-link")
        self.reset_app_state_link = self.test_id("reset-sidebar-link")

    @allure.step("Navigate to {path}")
    def navigate(self, path: str = "/") -> None:
        self.page.goto(f"{Config.BASE_URL}{path}")

    def test_id(self, name: str) -> Locator:
        """Build a locator from the app's `data-test` attribute (its de facto test-id)."""
        return self.page.locator(f'[data-test="{name}"]')

    def click(self, locator: Locator) -> None:
        locator.click()

    def fill(self, locator: Locator, value: str) -> None:
        locator.fill(value)

    def get_text(self, locator: Locator) -> str:
        return (locator.text_content() or "").strip()

    @allure.step("Open the hamburger menu")
    def open_menu(self) -> None:
        self.click(self.menu_button)

    @allure.step("Close the hamburger menu")
    def close_menu(self) -> None:
        self.click(self.close_menu_button)

    @allure.step("Go to the cart")
    def go_to_cart(self) -> None:
        self.click(self.cart_link)

    @allure.step("Go to All Items")
    def go_to_all_items(self) -> None:
        self.click(self.all_items_link)

    @allure.step("Log out")
    def logout(self) -> None:
        self.click(self.logout_link)

    @allure.step("Reset app state")
    def reset_app_state(self) -> None:
        self.click(self.reset_app_state_link)
