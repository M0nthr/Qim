from playwright.sync_api import Page, sync_playwright
import os

def test_footer_and_arena(page: Page):
    # 1. Test Mobile View (Standard MCQ)
    page.set_viewport_size({"width": 390, "height": 844})
    curr_dir = os.getcwd()
    page.goto(f"file://{curr_dir}/index.html")
    page.wait_for_selector(".glass-capsule")

    # Check mobile footer visibility
    page.screenshot(path="/home/jules/verification/footer_mobile_std.png")

    # 2. Test Desktop View (Standard MCQ)
    page.set_viewport_size({"width": 1280, "height": 800})
    page.wait_for_timeout(500)
    # Side nav should NOT be visible for MCQ
    page.screenshot(path="/home/jules/verification/footer_desktop_std.png")

    # 3. Test Desktop View (Order Section - Q9+)
    page.evaluate("Alpine.$data(document.querySelector('[x-data]')).currentQ = 9")
    page.wait_for_timeout(500)
    # Side nav SHOULD be visible, white footer hidden
    page.screenshot(path="/home/jules/verification/footer_desktop_long.png")

    # 4. Test Image Interaction (Burst & Modal)
    page.evaluate("Alpine.$data(document.querySelector('[x-data]')).currentQ = 24")
    page.wait_for_timeout(1000) # Burst
    # Click on a pin (Wait for burst to end first)
    page.wait_for_timeout(3000)
    page.click(".map-pin")
    page.wait_for_timeout(1000) # Zoom
    page.screenshot(path="/home/jules/verification/image_zoom_modal.png")

if __name__ == "__main__":
    if not os.path.exists("/home/jules/verification"):
        os.makedirs("/home/jules/verification")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_footer_and_arena(page)
        finally:
            browser.close()
