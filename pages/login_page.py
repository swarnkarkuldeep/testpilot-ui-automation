import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    URL_PATH = "/"

    def __init__(self, page: Page):
        super().__init__(page)
        self.username_input = self.test_id("username")
        self.password_input = self.test_id("password")
        self.login_button = self.test_id("login-button")
        self.error_message = self.test_id("error")
        self.error_dismiss_button = self.test_id("error-button")

    @allure.step("Open the login page")
    def open(self) -> None:
        self.navigate(self.URL_PATH)

    @allure.step("Log in as {username}")
    def login(self, username: str, password: str) -> None:
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)
        self.click(self.login_button)
