from playwright.sync_api import sync_playwright
import time

EXTENSION_PATH = "/home/ktreanor/Claude/detrump"
OUTPUT = "/home/ktreanor/Claude/detrump/screenshot.png"

with sync_playwright() as p:
    context = p.chromium.launch_persistent_context(
        "",
        headless=False,
        args=[
            f"--disable-extensions-except={EXTENSION_PATH}",
            f"--load-extension={EXTENSION_PATH}",
            "--window-size=1280,800",
        ],
        viewport={"width": 1280, "height": 800},
    )

    page = context.new_page()
    page.goto("https://apnews.com/hub/donald-trump", wait_until="domcontentloaded", timeout=30000)
    time.sleep(6)  # let images load and content scripts run

    # Dismiss notification popup if present
    for selector in ["text=Later", "text=No thanks", "text=Not now", "[aria-label='Close']"]:
        try:
            btn = page.locator(selector).first
            if btn.is_visible(timeout=1500):
                btn.click()
                time.sleep(0.5)
                break
        except Exception:
            pass

    page.keyboard.press("Escape")
    time.sleep(1)

    # Scroll down to show article thumbnails
    page.evaluate("window.scrollBy(0, 200)")
    time.sleep(2)

    page.screenshot(path=OUTPUT, full_page=False)
    print(f"Screenshot saved to {OUTPUT}")
    context.close()
