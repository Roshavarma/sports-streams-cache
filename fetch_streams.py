import json
import os
from playwright.sync_api import sync_playwright

def fetch_live_data():
    with sync_playwright() as p:
        print("🚀 Launching Headless Browser...")
        browser = p.chromium.launch(headless=True)
        
        # Spoofing a standard desktop browser to avoid bot detection
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        intercepted_data = None

        # Network interceptor: Listen for the specific background API call
        def catch_response(response):
            nonlocal intercepted_data
            if "autumn-darkness" in response.url or "workers.dev" in response.url:
                if response.status == 200:
                    try:
                        intercepted_data = response.json()
                        print(f"✅ Target API Response Caught! URL: {response.url}")
                    except Exception as e:
                        print("⚠️ Error parsing intercepted JSON:", e)

        page.on("response", catch_response)

        print("🔄 Loading target site and waiting for JS decryption...")
        try:
            # Load the wrapper site and let it naturally execute the hashing logic
            page.goto("https://footxweb.pages.dev/", wait_until="networkidle", timeout=30000)
        except Exception as e:
            print("⚠️ Page load timeout or error, but data might still be caught.", e)

        # Save the successfully intercepted payload to the repo cache
        if intercepted_data:
            file_path = os.path.join(os.getcwd(), "live_sports_data.json")
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(intercepted_data, f, indent=4)
            print(f"💾 Successfully saved fresh data to {file_path}")
        else:
            print("❌ Failed to catch the API request. The site may require a simulated click.")

        browser.close()

if __name__ == "__main__":
    fetch_live_data()
