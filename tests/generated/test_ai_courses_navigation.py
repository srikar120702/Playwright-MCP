import re
from playwright.sync_api import Page, expect


def test_navigate_to_machine_learning_course(page: Page, base_url: str) -> None:
    # 1. Open the homepage
    page.goto(base_url)
    expect(page).to_have_title(re.compile("Codemify"))

    # 2. Click "AI Courses" in the top navigation bar
    ai_courses_nav = page.locator('a[href="#submenu:MLcourses"]').first
    expect(ai_courses_nav).to_be_visible()
    ai_courses_nav.click()

    # 3. Click "Machine Learning" from the dropdown submenu
    ml_course_link = page.get_by_role("menuitem", name=re.compile("Machine Learning", re.IGNORECASE))
    expect(ml_course_link).to_be_visible()
    ml_course_link.click()

    # 4. Verify navigation to the Machine Learning course page
    expect(page).to_have_url(re.compile(r".*/machine-learning-beginner.*"))
    expect(page).to_have_title(re.compile("Machine Learning Beginner"))

    # 5. Verify headline text on the page
    headline = page.locator("text=START YOUR AI ENGINEER CAREER IN 3 MONTHS")
    expect(headline).to_be_visible()

    # 6. Capture screenshot as visual proof
    page.screenshot(path="reports/test_ml_navigation_screenshot.png")
