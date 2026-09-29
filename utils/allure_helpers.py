"""Maps this project's test-plan priorities (P1/P2/P3) to Allure severities."""

import allure

SEVERITY_BY_PRIORITY = {
    "P1": allure.severity_level.CRITICAL,
    "P2": allure.severity_level.NORMAL,
    "P3": allure.severity_level.MINOR,
}


def apply_priority(priority: str) -> None:
    """Set the current test's Allure severity from a test-plan priority string."""
    allure.dynamic.severity(SEVERITY_BY_PRIORITY[priority])
