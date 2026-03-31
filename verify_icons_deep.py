from playwright.sync_api import Page, sync_playwright
import os

def test_icon_logic_deep(page: Page):
    page.set_viewport_size({"width": 390, "height": 844})
    curr_dir = os.getcwd()
    page.goto(f"file://{curr_dir}/index.html")

    # Wait for Alpine
    page.wait_for_selector(".glass-capsule")

    # 1. Start at Q1 (Section: tf) - Burst should be visible
    page.wait_for_timeout(500)
    burst_visible = page.is_visible(".large-burst-overlay.active")
    print(f"Burst visible at start: {burst_visible}")

    # 2. Go to Q5 (Section: mcq) - New burst
    page.evaluate("Alpine.$data(document.querySelector('[x-data]')).currentQ = 5")
    page.wait_for_timeout(500)
    burst_mcq = page.is_visible(".large-burst-overlay.active")
    print(f"Burst visible at MCQ: {burst_mcq}")

    # 3. Wait for burst to end
    page.wait_for_timeout(3000)

    # 4. Go back to Q1 (Section: tf) - NO burst should trigger
    page.evaluate("Alpine.$data(document.querySelector('[x-data]')).currentQ = 1")
    page.wait_for_timeout(500)
    burst_back = page.is_visible(".large-burst-overlay.active")
    print(f"Burst visible when going back to TF: {burst_back}")

    # Take screenshot for visual proof of static header nodes
    page.screenshot(path="/home/jules/verification/back_navigation_no_burst.png")

if __name__ == "__main__":
    if not os.path.exists("/home/jules/verification"):
        os.makedirs("/home/jules/verification")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_icon_logic_deep(page)
        finally:
            browser.close()
