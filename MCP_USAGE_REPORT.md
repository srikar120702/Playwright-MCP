# Model Context Protocol (MCP) Usage Report

This document details where and how the **Playwright MCP Server** was utilized throughout the project lifecycle, from interactive site exploration to automated test generation.

---

## 1. Overview of MCP in the Workflow

Traditional test automation requires developers to manually open developer tools, inspect complex DOM structures, guess CSS selectors, and troubleshoot flaky locators through trial and error.

In this workflow, the **Playwright MCP Server** functioned as the AI assistant's **live browser bridge**. Instead of writing tests blindly, the AI agent used MCP tools to interact with the real browser, discover exact locators, test interactions live, and then generate fully verified `pytest-playwright` tests.

---

## 2. Where the MCP Was Used (Phase-by-Phase)

### Phase 1: Tool Registration & Discovery
* **Tool Implementation**: Built a native Python MCP server ([playwright_mcp.py](file:///d:/playwright/playwright_mcp.py)) using `mcp.server.fastmcp` and Python's `playwright.async_api`.
* **Registration**: Configured in [mcp_config.json](file:///C:/Users/Srikar%20G%20S%20S/.gemini/config/mcp_config.json) under `playwright-python`.
* **Tool Discovery**: The agent discovered and loaded 7 core tools:
  * `navigate_to`
  * `click_element`
  * `fill_input`
  * `capture_screenshot`
  * `get_page_info`
  * `evaluate_javascript`
  * `close_browser_session`

---

### Phase 2: Live Browser Launch & Homepage Discovery
* **Action**: When asked to open the browser and test MCP, the agent used:
  1. `navigate_to(url="https://codemify.com")`
     * **Result**: Launched a real Chromium instance headed and navigated to `https://codemify.com/` (HTTP 200).
  2. `capture_screenshot(path="reports/mcp_test_screenshot.png")`
     * **Result**: Visual snapshot confirmed full page rendering.
  3. `get_page_info()`
     * **Result**: Extracted active DOM content, discovering key navigation menu links (`QA Courses`, `AI Courses`, `Prices`, `Schedule`, etc.).

---

### Phase 3: Navigating to "AI Courses" -> "Machine Learning"
When you requested:
> *"click on ai cources on the top banner and go to machine learning"*

The MCP server was used at every step to explore the DOM and execute the actions:

1. **Locating "AI Courses" Menu**:
   * **MCP Tool**: `evaluate_javascript`
   * **Script**: Queried all links and buttons matching `"AI Courses"`.
   * **Discovery**: Identified `<a href="#submenu:MLcourses" class="...">AI Courses</a>`.
2. **Opening the Submenu**:
   * **MCP Tool**: `click_element(selector='a[href="#submenu:MLcourses"]')`
   * **Result**: Triggered the dropdown menu on the live page, revealing course items (`Schedule`, `Machine Learning`, `Deep Learning`, `AI Engineering`).
3. **Locating & Clicking "Machine Learning"**:
   * **MCP Tool**: `evaluate_javascript`
   * **Discovery**: Located the submenu item `<a href="/machine-learning-beginner">Machine Learning</a>`.
   * **MCP Tool**: `click_element(selector='a[href="/machine-learning-beginner"]')`
   * **Result**: Browser smoothly transitioned to the course landing page.
4. **Verifying Page & State**:
   * **MCP Tool**: `get_page_info()`
     * Verified current URL: `https://codemify.com/machine-learning-beginner`
     * Verified title: `Machine Learning Beginner - Data Science Course`
     * Verified curriculum headings and course levels.
   * **MCP Tool**: `capture_screenshot(path="reports/ai_courses_ml.png")`
     * Verified visual layout.

---

### Phase 4: Translating MCP Discoveries into Automated Pytest Code
Because the MCP server pre-validated the exact DOM behavior, the generated test in [test_ai_courses_navigation.py](file:///d:/playwright/tests/generated/test_ai_courses_navigation.py) used the exact selectors and role locators discovered via MCP:
* Used `a[href="#submenu:MLcourses"]` to trigger the submenu.
* Used `get_by_role("menuitem", name=re.compile("Machine Learning"))` to click the target item.
* Asserted URL `https://codemify.com/machine-learning-beginner` and title.

---

### Phase 5: Parallel Execution, Logging & Tracing
The test suite was then upgraded with:
* **Pytest Logging**: `log_cli = true` in [pytest.ini](file:///d:/playwright/pytest.ini) to print every step in real-time.
* **Playwright Tracing**: `--tracing on` in [pytest.ini](file:///d:/playwright/pytest.ini) to record full execution traces (`trace.zip`).
* **Parallel Execution**: `-n auto` via `pytest-xdist` to run multiple tests simultaneously across worker processes.

---

## 3. Summary Mapping Table

| User Prompt | MCP Tool Called | Purpose | Generated Artifact / Test |
| :--- | :--- | :--- | :--- |
| *"lets test the mcp now open the browser"* | `navigate_to` | Launched Chromium headed and navigated to `https://codemify.com/` | Verified live page load |
| *"lets test the mcp..."* | `capture_screenshot` | Saved initial visual rendering | [reports/mcp_test_screenshot.png](file:///d:/playwright/reports/mcp_test_screenshot.png) |
| *"lets test the mcp..."* | `get_page_info` | Extracted titles and navigation links | Discovered `AI Courses` menu |
| *"click on ai cources..."* | `evaluate_javascript` | Inspected banner DOM attributes | Discovered `#submenu:MLcourses` |
| *"click on ai cources..."* | `click_element` | Opened the course menu dropdown | Live dropdown opened |
| *"go to machine learning"* | `evaluate_javascript` | Inspected submenu DOM links | Discovered `/machine-learning-beginner` |
| *"go to machine learning"* | `click_element` | Clicked course link | Navigated to ML page |
| *"go to machine learning"* | `capture_screenshot` | Captured final page proof | [reports/ai_courses_ml.png](file:///d:/playwright/reports/ai_courses_ml.png) |
| *"create a test for the same"* | *Code Generation* | Authored test based on MCP findings | [test_ai_courses_navigation.py](file:///d:/playwright/tests/generated/test_ai_courses_navigation.py) |

---

## 4. Viewing Playwright Traces

The traces captured from the test runs are saved in `test-results/`. You can inspect them interactively with:

```bash
playwright show-trace "test-results/tests-generated-test-ai-courses-navigation-py-test-navigate-to-machine-learning-course-chromium/trace.zip"
```
