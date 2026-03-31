from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        path = 'file://' + os.path.abspath('index.html')

        # Desktop Mode - Long Question
        page.set_viewport_size({"width": 1280, "height": 800})
        page.goto(path)

        # Q10 is Order
        page.evaluate("() => { qimam.currentQ = 10; }")
        page.wait_for_timeout(1000)

        side_nav = page.locator(".side-nav-btn")
        is_side_nav_visible = side_nav.is_visible()
        print(f"Desktop Side Nav Visible (Q10): {is_side_nav_visible}")

        footer = page.locator(".footer-hub")
        footer_bg = footer.evaluate("el => window.getComputedStyle(el).backgroundColor")
        # In desktop long mode, we expect background to be transparent (rgba(0, 0, 0, 0))
        print(f"Desktop Footer BG (Q10): {footer_bg}")

        page.screenshot(path="desktop_order.png")

        # Mobile Mode
        page.set_viewport_size({"width": 375, "height": 812})
        page.wait_for_timeout(1000)

        is_side_nav_mobile = side_nav.is_visible()
        print(f"Mobile Side Nav Visible (Q10): {is_side_nav_mobile}")

        footer_bg_mobile = footer.evaluate("el => window.getComputedStyle(el).backgroundColor")
        # In mobile, footer hub background should be white (rgb(255, 255, 255))
        print(f"Mobile Footer BG (Q10): {footer_bg_mobile}")

        page.screenshot(path="mobile_view.png")

        browser.close()

if __name__ == "__main__":
    run()
