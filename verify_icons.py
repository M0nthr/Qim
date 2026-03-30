from playwright.sync_api import Page, sync_playwright
import os

def test_icon_burst(page: Page):
    page.set_viewport_size({"width": 390, "height": 844})
    curr_dir = os.getcwd()
    page.goto(f"file://{curr_dir}/index.html")

    # Wait for Alpine
    page.wait_for_selector(".glass-capsule")

    # 1. Take screenshot of the first section burst (should trigger on load)
    # The burst lasts 3 seconds, so we catch it at 1 second
    page.wait_for_timeout(1000)
    page.screenshot(path="/home/jules/verification/icon_burst_tf.png")

    # 2. Transition to next section (mcq) to trigger new burst
    page.evaluate("""() => {
        const el = document.querySelector('[x-data]');
        const data = Alpine.$data(el);
        data.currentQ = 5;
    }""")
    page.wait_for_timeout(1000)
    page.screenshot(path="/home/jules/verification/icon_burst_mcq.png")

    # 3. Wait for burst to disappear and check static icon in header
    page.wait_for_timeout(3000)
    page.screenshot(path="/home/jules/verification/after_burst.png")

if __name__ == "__main__":
    if not os.path.exists("/home/jules/verification"):
        os.makedirs("/home/jules/verification")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            test_icon_burst(page)
        finally:
            browser.close()
