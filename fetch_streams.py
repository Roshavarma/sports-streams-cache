import json
import os
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

def fetch_live_data():
    with sync_playwright() as p:
        print("🚀 Launching Stealth Browser...")
        
        # Disable automation trackers
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        # Spoofing a realistic Windows desktop browser in India
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={'width': 1920, 'height': 1080},
            locale="en-IN",
            timezone_id="Asia/Kolkata",
            extra_http_headers={
                "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7"
            }
        )
        
        # Apply the V2 stealth mask to the entire browser context
        stealth = Stealth()
        stealth.apply_stealth_sync(context)
        
        page = context.new_page()

        intercepted_data = None

        def catch_response(response):
            nonlocal intercepted_data
            if "autumn-darkness" in response.url or "workers.dev" in response.url:
                if response.status == 200:
                    try:
                        intercepted_data = response.json()
                        print(f"✅ Target API Response Caught! URL: {response.url}")
                    except Exception as e:
                        print("⚠️ Error parsing JSON:", e)

        # Listen for the background network requests
        page.on("response", catch_response)

        print("🔄 Loading target site and calculating decryption hash...")
        try:
            page.goto("https://footxweb.pages.dev/", wait_until="domcontentloaded", timeout=30000)
            
            # Give the JavaScript 10 seconds to draw the canvas, do the math, and call the API
            print("⏳ Waiting 10 seconds for background decryption...")
            page.wait_for_timeout(10000) 
        except Exception as e:
            print("⚠️ Page load timeout, checking if data was caught anyway...")

        # Save the successfully intercepted payload
        if intercepted_data:
            file_path = os.path.join(os.getcwd(), "streams.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(intercepted_data, f, indent=4)
            print(f"💾 Successfully saved fresh data to streams.json")
        else:
            print("❌ Failed to catch the API request.")
            
        # Take a screenshot so we can see what the bot is looking at
        page.screenshot(path="debug_screenshot.png")
        print("📸 Saved 'debug_screenshot.png'. Check your repo to see what happened!")

        browser.close()

if __name__ == "__main__":
    fetch_live_data()
