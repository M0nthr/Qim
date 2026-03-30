from playwright.sync_api import Page, expect, sync_playwright
import os

def test_header_and_timer(page: Page):
    # Set viewport to a common mobile size
    page.set_viewport_size({"width": 390, "height": 844})

    # Path to index.html
    curr_dir = os.getcwd()
    page.goto(f"file://{curr_dir}/index.html")

    # Wait for Alpine to init
    page.wait_for_selector(".glass-capsule")

    # 1. Take screenshot of the initial state (Header + Question area)
    page.screenshot(path="/home/jules/verification/header_initial.png")

    # 2. Trigger Danger Mode by setting Alpine data via $data
    # Use a simpler approach by calling global window object if possible or just wait 60s (not practical)
    # Instead, we can inject a script to modify the component data
    page.evaluate("""() => {
        const el = document.querySelector('[x-data]');
        const data = Alpine.$data(el);
        data.timeLeft = 5;
    }""")
    page.wait_for_timeout(1000) # Wait for UI to update

    # Take screenshot of Danger Mode
    page.screenshot(path="/home/jules/verification/header_danger.png")

    # 3. Test Party Mode (Progress 62%)
    page.evaluate("""() => {
        const el = document.querySelector('[x-data]');
        const data = Alpine.$data(el);
        data.currentQ = 16;
    }""")
    page.wait_for_timeout(1000)
    page.screenshot(path="/home/jules/verification/party_mode.png")

if __name__ == "__main__":
    if not os.path.exists("/home/jules/verification"):
        os.makedirs("/home/jules/verification")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_header_and_timer(page)
        finally:
            browser.close()
