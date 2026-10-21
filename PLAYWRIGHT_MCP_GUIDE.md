# Playwright Model Context Protocol (MCP) Guide

This guide explains how the **Playwright MCP Server** works, whether you can use Python instead of Node/npx, and what capabilities and workflows you can unlock with it.

---

## 1. Python vs. `npx`: Can We Use Python Only?

**Yes!** An MCP server is simply an independent background process that talks to AI assistants (Antigravity, Cursor, Claude Desktop, Windsurf) over standard input/output (`stdio`) using JSON-RPC.

* **Native Python MCP (`playwright_mcp.py`)**:
  We configured a 100% native Python Playwright MCP server using the official Python `mcp` SDK and Python `playwright`. It runs directly via `python D:/playwright/playwright_mcp.py` without requiring Node.js or `npm`.
* **Why do many tutorials use `npx`?**
  Microsoft's official `@playwright/mcp` package was written in TypeScript by the core Playwright team. Running `npx @playwright/mcp@latest` executes that external tool in the background—it never touches or alters your Python repository code.
* **Both options are fully supported**, and your test suite remains 100% Python (`pytest-playwright`).

---

## 2. MCP Server Configuration

The MCP server is configured in your global Antigravity configuration file (`~/.gemini/config/mcp_config.json`):

```json
{
  "mcpServers": {
    "playwright-python": {
      "command": "python",
      "args": ["D:/playwright/playwright_mcp.py"]
    }
  }
}
```

*(If you ever wish to use Microsoft's official `@playwright/mcp` server instead, replace `"command": "python"` and args with `"command": "npx"`, `"args": ["@playwright/mcp@latest"]`.)*

---

## 3. Available Tools & Capabilities

The Python Playwright MCP server exposes the following tools directly to the AI agent:

| Tool Name | Parameters | Description |
| :--- | :--- | :--- |
| `navigate_to` | `url: str` | Opens Chromium and navigates to the specified URL. |
| `click_element` | `selector: str` | Clicks an element matched by CSS, XPath, or text selector. |
| `fill_input` | `selector: str`, `text: str` | Types or fills text into an input field or text area. |
| `capture_screenshot` | `path: str` | Captures a full-page screenshot and saves it to disk (e.g. `reports/`). |
| `get_page_info` | *none* | Retrieves the active page URL, title, and body text summary. |
| `evaluate_javascript` | `script: str` | Executes custom JavaScript inside the browser context and returns output. |
| `close_browser_session` | *none* | Closes the open browser and page context cleanly. |

---

## 4. What You Can Do With This MCP

By connecting Playwright as an MCP server, your AI agent transforms from a static code assistant into an **autonomous web testing and automation agent**:

### 🎯 1. Autonomous Test Generation
* **What it does**: Instead of guessing DOM selectors from static HTML, the AI agent can navigate the target website in real-time, inspect live elements, interact with buttons, and automatically generate verified `pytest-playwright` test scripts into `tests/generated/`.
* **Example prompt to agent**:
  > *"Navigate to https://codemify.com using the MCP, inspect the navigation bar and contact buttons, and write a pytest test verifying that clicking 'Courses' routes to the correct page."*

### 🔍 2. Interactive Bug Reproduction & Debugging
* **What it does**: When a test fails in CI or local runs, the agent can use the MCP tools to replicate the exact steps, evaluate JavaScript on the page, check console state, and diagnose broken locators or timing issues.
* **Example prompt to agent**:
  > *"Open the login flow on the staging URL, try submitting an empty form, and check if the validation error banner appears."*

### 📸 3. Visual Verification & Layout Auditing
* **What it does**: The agent can trigger `capture_screenshot` across various URLs or viewport sizes to inspect layout shifts, verify responsive design, or confirm visual appearance.
* **Example prompt to agent**:
  > *"Go to the homepage, take a screenshot of the hero section, and verify that the call-to-action button is visible."*

### 📝 4. Form Automation & End-to-End User Journeys
* **What it does**: The agent can perform multi-step user journeys (e.g., searching for a product, adding items to a cart, filling checkout forms) to validate end-to-end user workflows before writing test assertions.

### 🌐 5. Dynamic Content & SPA Inspection
* **What it does**: Many modern websites load content dynamically via JavaScript / React. The MCP server allows the agent to wait for hydration, query live DOM nodes, and evaluate JS expressions that static scrapers cannot reach.

---

## 5. Quick Verification

You can test running the native Python MCP server manually in PowerShell:
```powershell
python D:/playwright/playwright_mcp.py
```
*(The server will start and wait for standard MCP JSON-RPC messages via stdin/stdout).*
