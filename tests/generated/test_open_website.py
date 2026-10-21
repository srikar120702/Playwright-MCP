from playwright.sync_api import Page, expect


def test_open_website(page: Page, base_url: str) -> None:
    page.goto(base_url)
    # Verify the page loaded and has a title
    assert page.title() != ""
