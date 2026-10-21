"""Native Python Playwright MCP Server.

Provides browser automation tools for AI agents via Model Context Protocol (MCP).
"""

from typing import Optional
from mcp.server.fastmcp import FastMCP
from playwright.async_api import async_playwright, Browser, BrowserContext, Page

mcp = FastMCP("python-playwright")

_playwright = None
_browser: Optional[Browser] = None
_context: Optional[BrowserContext] = None
_page: Optional[Page] = None


async def _get_page() -> Page:
    global _playwright, _browser, _context, _page
    if _playwright is None:
        _playwright = await async_playwright().start()
        _browser = await _playwright.chromium.launch(headless=False)
        _context = await _browser.new_context()
        _page = await _context.new_page()
    elif _page is None or _page.is_closed():
        _page = await _context.new_page()
    return _page


@mcp.tool()
async def navigate_to(url: str) -> str:
    """Navigate the browser to a specific URL."""
    page = await _get_page()
    response = await page.goto(url)
    status = response.status if response else "unknown"
    title = await page.title()
    return f"Navigated to {url} (Status: {status}, Title: '{title}')"


@mcp.tool()
async def click_element(selector: str) -> str:
    """Click on a web element matching the given CSS or text selector."""
    page = await _get_page()
    await page.click(selector)
    return f"Clicked element matching '{selector}'"


@mcp.tool()
async def fill_input(selector: str, text: str) -> str:
    """Fill or type text into an input field matching the selector."""
    page = await _get_page()
    await page.fill(selector, text)
    return f"Filled '{selector}' with text: '{text}'"


@mcp.tool()
async def capture_screenshot(path: str = "reports/mcp_screenshot.png") -> str:
    """Take a screenshot of the current page and save to disk."""
    page = await _get_page()
    await page.screenshot(path=path, full_page=True)
    return f"Screenshot successfully saved to {path}"


@mcp.tool()
async def get_page_info() -> str:
    """Get current page URL, title, and body text summary."""
    page = await _get_page()
    title = await page.title()
    url = page.url
    content = await page.inner_text("body")
    summary = content[:1000] + ("..." if len(content) > 1000 else "")
    return f"URL: {url}\nTitle: {title}\nContent:\n{summary}"


@mcp.tool()
async def evaluate_javascript(script: str) -> str:
    """Evaluate a JavaScript expression or script in the browser console."""
    page = await _get_page()
    result = await page.evaluate(script)
    return f"Result: {result}"


@mcp.tool()
async def close_browser_session() -> str:
    """Close the current browser session."""
    global _playwright, _browser, _context, _page
    if _browser:
        await _browser.close()
    if _playwright:
        await _playwright.stop()
    _playwright = _browser = _context = _page = None
    return "Browser session closed."


if __name__ == "__main__":
    mcp.run()
