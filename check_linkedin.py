import re
import requests

LINKEDIN_PAGE = "https://www.linkedin.com/company/tspborgtr/posts/"
WEBHOOK = "https://metx-digital.sg.larksuite.com/base/automation/webhook/event/WTqiakYyZwTVGVhKDVTlny8VgNe"


def fetch_html(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.text


def extract_latest_post_id(html: str):
    match = re.search(r'activity:(\d+)', html)
    if match:
        return match.group(1)
    return None


def push_to_lark(post_id: str):
    post_url = f"https://www.linkedin.com/feed/update/urn:li:activity:{post_id}/"

    data = {
        "title": "Latest LinkedIn Post",
        "url": post_url,
        "author": "TSPB"
    }

    resp = requests.post(
        WEBHOOK,
        headers={"Content-Type": "application/json"},
        json=data,
        timeout=20
    )
    resp.raise_for_status()
    print("Push success:", post_url)


def main():
    html = fetch_html(LINKEDIN_PAGE)
    latest_post_id = extract_latest_post_id(html)

    if not latest_post_id:
        print("No post id found.")
        return

    print("Latest post id:", latest_post_id)
    push_to_lark(latest_post_id)


if __name__ == "__main__":
    main()
