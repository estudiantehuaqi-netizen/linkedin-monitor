from playwright.sync_api import sync_playwright
import requests
import re

PAGE_URL = "https://www.linkedin.com/company/tspborgtr/posts/"
WEBHOOK = "https://metx-digital.sg.larksuite.com/base/automation/webhook/event/WTqiakYyZwTVGVhKDVTlny8VgNe"


def get_latest_post():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(PAGE_URL, wait_until="networkidle", timeout=60000)

        html = page.content()
        print("Page loaded, html length:", len(html))

        # 直接从渲染后的 HTML 里抓最新 activity id
        matches = re.findall(r"urn:li:activity:(\d+)", html)

        if not matches:
            browser.close()
            print("No activity id found")
            return None

        post_id = matches[0]
        browser.close()

        return post_id


def push_to_lark(post_id: str):
    post_url = f"https://www.linkedin.com/feed/update/urn:li:activity:{post_id}/"

    payload = {
        "title": "Latest LinkedIn Post",
        "url": post_url,
        "author": "TSPB"
    }

    resp = requests.post(
        WEBHOOK,
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=20
    )
    resp.raise_for_status()

    print("Push success:", post_url)


def main():
    post_id = get_latest_post()

    if not post_id:
        print("No post found")
        return

    print("Latest post id:", post_id)
    push_to_lark(post_id)


if __name__ == "__main__":
    main()
