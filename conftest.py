import logging
from typing import Any, Callable, Dict, List
import pytest
from playwright.sync_api import Page, expect

logger = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def base_url() -> str:
    """Base URL fixture for the application under test."""
    return "https://codemify.com"


@pytest.fixture
def home_page(page: Page, base_url: str) -> Page:
    """Reusable fixture that navigates to the homepage and verifies it loaded."""
    logger.info("[Fixture: home_page] Navigating to homepage: %s", base_url)
    page.goto(base_url, wait_until="domcontentloaded", timeout=45000)
    logger.info("[Fixture: home_page] Homepage loaded: %s", page.url)
    return page


@pytest.fixture
def prices_page(home_page: Page) -> Page:
    """Reusable fixture that navigates to the Plans and Prices page."""
    logger.info("[Fixture: prices_page] Clicking 'Prices' link in navigation")
    prices_link = home_page.locator('a[href="/experts"]:has-text("Prices")').first
    if not prices_link.is_visible():
        prices_link = home_page.locator('text="Prices"').first
    prices_link.click()
    home_page.wait_for_load_state("domcontentloaded")
    logger.info("[Fixture: prices_page] Prices page loaded: %s", home_page.url)
    return home_page
