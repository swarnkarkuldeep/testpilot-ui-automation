import allure
import pytest
from playwright.sync_api import expect

from pages.inventory_page import InventoryPage
from utils.allure_helpers import apply_priority
from utils.data_loader import load_json

SORT_OPTIONS = load_json("sort_options.json")


@allure.feature("Inventory")
@pytest.mark.regression
@pytest.mark.parametrize("case", SORT_OPTIONS, ids=[row["id"] for row in SORT_OPTIONS])
def test_sort_products(inventory_page: InventoryPage, case: dict) -> None:
    """Data-driven product sorting (TC-INV-002, TC-INV-003, TC-INV-004,
    TC-INV-005 — see `case["tc_id"]`), asserting the exact product order
    observed live for each of the 4 sort options."""
    apply_priority(case["priority"])
    allure.dynamic.title(f"Sort products: {case['option_label']} ({case['tc_id']})")

    inventory_page.sort_by(case["option_value"])

    expect(inventory_page.item_names).to_have_text(case["expected_names"])
    expect(inventory_page.item_prices).to_have_text(case["expected_prices"])


@allure.feature("Inventory")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_add_multiple_products_updates_badge_count(inventory_page: InventoryPage) -> None:
    """TC-INV-007: Adding 3 different products shows a cart badge count of
    3, with each button flipped to Remove."""
    slugs = ["sauce-labs-backpack", "sauce-labs-bike-light", "sauce-labs-bolt-t-shirt"]
    for slug in slugs:
        inventory_page.add_to_cart(slug)

    expect(inventory_page.cart_badge).to_have_text("3")
    for slug in slugs:
        expect(inventory_page.remove_button(slug)).to_be_visible()


@allure.feature("Inventory")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.regression
def test_remove_product_from_inventory_page(inventory_page: InventoryPage) -> None:
    """TC-INV-008: Removing an already-added product from the inventory
    page reverts its button and decrements the cart badge to nothing."""
    inventory_page.add_to_cart("sauce-labs-backpack")
    expect(inventory_page.cart_badge).to_have_text("1")

    inventory_page.remove_from_cart("sauce-labs-backpack")

    expect(inventory_page.add_to_cart_button("sauce-labs-backpack")).to_be_visible()
    expect(inventory_page.cart_badge).to_have_count(0)
