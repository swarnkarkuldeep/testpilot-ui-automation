"""Shared pytest configuration: browser/context setup from env-driven config,
and automatic screenshot-on-failure attached to both the pytest-html and
Allure reports.
"""

import os

import pytest
from playwright.sync_api import Page

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.config import Config
from utils.data_loader import load_json

SCREENSHOT_DIR = os.path.join("reports", "screenshots")
STANDARD_USER = load_json("users.json")["standard_user"]


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    return {
        **browser_type_launch_args,
        "headless": Config.HEADLESS,
        "slow_mo": Config.SLOW_MO_MS,
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "base_url": Config.BASE_URL,
        "viewport": {"width": 1440, "height": 900},
    }


@pytest.fixture(autouse=True)
def _default_timeout(page: Page) -> None:
    page.set_default_timeout(Config.DEFAULT_TIMEOUT_MS)


@pytest.fixture
def logged_in_page(page: Page) -> Page:
    """A fresh page already logged in as standard_user.

    Each test gets its own `page` (pytest-playwright is function-scoped by
    default), so logging in here does not leak state between tests.
    """
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(STANDARD_USER["username"], STANDARD_USER["password"])
    page.wait_for_url("**/inventory.html")
    return page


@pytest.fixture
def inventory_page(logged_in_page: Page) -> InventoryPage:
    return InventoryPage(logged_in_page)


@pytest.fixture
def cart_page_with_item(inventory_page: InventoryPage) -> CartPage:
    """Cart page holding a single item (Sauce Labs Backpack)."""
    inventory_page.add_to_cart("sauce-labs-backpack")
    inventory_page.go_to_cart()
    return CartPage(inventory_page.page)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    page: Page | None = item.funcargs.get("page")
    if page is None:
        return

    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    safe_name = "".join(c if c.isalnum() or c in "-_." else "_" for c in item.name)
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"{safe_name}.png")

    try:
        page.screenshot(path=screenshot_path, full_page=True)
    except Exception:
        return

    pytest_html = item.config.pluginmanager.getplugin("html")
    if pytest_html is not None:
        extra = getattr(report, "extra", [])
        extra.append(pytest_html.extras.image(screenshot_path))
        report.extra = extra

    try:
        import allure

        allure.attach.file(
            screenshot_path,
            name="screenshot-on-failure",
            attachment_type=allure.attachment_type.PNG,
        )
    except ImportError:
        pass
