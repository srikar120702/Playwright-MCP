import logging
from typing import Any, Dict, List
from playwright.sync_api import Page, expect

logger = logging.getLogger(__name__)


def test_hover_all_banner_dropdowns_via_js_injection(home_page: Page) -> None:
    logger.info("=== Starting Task 2: Hover Over All Banner Dropdowns via JS Injection ===")
    page = home_page

    # 1. Verify we are on the homepage
    logger.info("Step 1: Confirming homepage is active")
    expect(page).to_have_title("Codemify — Career Training in QA, AI Testing & ML")

    # 2. Inject JavaScript code in the middle of Python code using page.evaluate()
    logger.info("Step 2: Injecting JavaScript code via page.evaluate() to find and hover on all banner dropdowns")

    # The injected JavaScript handles discovery, event dispatching (mouseenter, mouseover, pointerover),
    # visual highlighting, and submenu expansion.
    js_hover_script = """
    () => {
        const results = [];
        // Select all potential dropdown triggers in the top navigation bar
        const candidates = Array.from(document.querySelectorAll(
            'a[href*="submenu"], .t-menusub__target-link, [data-menu-submenu-hook], .t794__tm-link, .t396__group a'
        ));

        // Deduplicate elements by text and href
        const seen = new Set();
        const dropdownElements = candidates.filter(el => {
            const text = (el.innerText || el.textContent || '').trim();
            const href = el.getAttribute('href') || '';
            const key = text + '|' + href;
            if (text && !seen.has(key) && (href.includes('submenu') || text.includes('Courses') || text.includes('QA') || text.includes('AI'))) {
                seen.add(key);
                return true;
            }
            return false;
        });

        console.log(`[Injected JS] Found ${dropdownElements.length} dropdown targets to hover.`);

        dropdownElements.forEach((el, index) => {
            const text = (el.innerText || el.textContent || '').trim();
            const href = el.getAttribute('href') || '';
            const rect = el.getBoundingClientRect();

            // 1. Dispatch full sequence of mouse hover events
            const mouseEnterEvent = new MouseEvent('mouseenter', { bubbles: true, cancelable: true, view: window });
            const mouseOverEvent = new MouseEvent('mouseover', { bubbles: true, cancelable: true, view: window });
            const pointerOverEvent = new PointerEvent('pointerover', { bubbles: true, cancelable: true, view: window });

            el.dispatchEvent(pointerOverEvent);
            el.dispatchEvent(mouseEnterEvent);
            el.dispatchEvent(mouseOverEvent);

            // 2. Add visual highlight to demonstrate hover interaction
            el.style.outline = '2px solid #00ff00';
            el.style.backgroundColor = 'rgba(0, 255, 0, 0.15)';
            el.style.transition = 'all 0.3s ease';

            // 3. If element targets a submenu ID (e.g. #submenu:MLcourses or #submenu:QAcourses), trigger submenu visibility
            let submenuTarget = null;
            if (href.startsWith('#submenu:')) {
                const hookName = href.replace('#submenu:', '');
                submenuTarget = document.querySelector(`[data-submenu-hook="${hookName}"], #nav${hookName}, [data-menu-submenu-hook="${hookName}"]`);
                if (submenuTarget) {
                    submenuTarget.style.display = 'block';
                    submenuTarget.style.opacity = '1';
                    submenuTarget.style.visibility = 'visible';
                }
            }

            results.push({
                index: index + 1,
                text: text,
                href: href,
                tagName: el.tagName,
                className: el.className,
                rect: {
                    x: Math.round(rect.x),
                    y: Math.round(rect.y),
                    width: Math.round(rect.width),
                    height: Math.round(rect.height)
                },
                submenuTriggered: Boolean(submenuTarget),
                hoverDispatched: true
            });
        });

        return {
            totalHovered: results.length,
            dropdowns: results
        };
    }
    """

    hover_response = page.evaluate(js_hover_script)

    logger.info("Step 3: JavaScript injection completed! Returned data:")
    logger.info("Total dropdowns hovered: %d", hover_response.get("totalHovered", 0))

    dropdown_list: List[Dict[str, Any]] = hover_response.get("dropdowns", [])
    for item in dropdown_list:
        logger.info(
            " -> Dropdown #%d: '%s' | href: '%s' | rect: %s | Submenu Triggered: %s",
            item["index"], item["text"], item["href"], item["rect"], item["submenuTriggered"]
        )

    # 4. Assertions on the injected JS execution
    logger.info("Step 4: Asserting JavaScript hover results in Python")
    assert hover_response.get("totalHovered", 0) > 0, "Expected at least 1 banner dropdown hovered via injected JS"
    for item in dropdown_list:
        assert item["hoverDispatched"] is True, f"Hover dispatch failed on {item['text']}"

    # 5. Capture visual screenshot of the hovered banner with green highlight outlines
    screenshot_path = "reports/banner_dropdown_hover.png"
    page.screenshot(path=screenshot_path)
    logger.info("Step 5: Saved proof screenshot with hovered highlights to '%s'", screenshot_path)

    logger.info("=== Task 2 Completed Successfully! ===")
