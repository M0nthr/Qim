from playwright.sync_api import sync_playwright
import os

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        path = 'file://' + os.path.abspath('index.html')
        page.goto(path)

        # Trigger Party Mode (61.8% of 25 is approx 16)
        print("Moving to Q16 to trigger Party Mode...")
        page.evaluate("() => { qimam.currentQ = 16; }")
        page.wait_for_timeout(500)

        is_partying = page.locator(".glass-capsule").evaluate("el => el.classList.contains('is-partying')")
        print(f"Is Partying Active: {is_partying}")

        party_text_opacity = page.locator(".party-text").evaluate("el => window.getComputedStyle(el).opacity")
        print(f"Party Text Opacity: {party_text_opacity}")

        page.screenshot(path="party_mode.png")

        # Check Timer transition to Warning (38.2% of 60s is ~23s)
        print("Setting time to 22s (Warning zone < 38.2%)...")
        page.evaluate("() => { qimam.timeLeft = 22; }")
        page.wait_for_timeout(1100) # wait for interval

        time_state = page.evaluate("() => qimam.timeState")
        print(f"Time State at 22s: {time_state}")

        # Check Timer transition to Danger (23.6% of 60s is ~14s)
        print("Setting time to 13s (Danger zone < 23.6%)...")
        page.evaluate("() => { qimam.timeLeft = 13; }")
        page.wait_for_timeout(1100)

        time_state_danger = page.evaluate("() => qimam.timeState")
        print(f"Time State at 13s: {time_state_danger}")

        page.screenshot(path="timer_danger.png")

        browser.close()

if __name__ == "__main__":
    run()
