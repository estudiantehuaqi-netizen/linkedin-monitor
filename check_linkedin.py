import re
import requests
import json

LINKEDIN_PAGE = "https://www.linkedin.com/company/tspborgtr/posts/"
WEBHOOK = "https://metx-digital.sg.larksuite.com/base/automation/webhook/event/WTqiakYyZwTVGVhKDVTlny8VgNe"


def fetch_html(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.text


def extract_post(html):

    # 找 JSON 数据块
    match = re.search(r'<code id="bpr-guid-[^"]+">(.*?)</code>', html)

    if not match:
        print("No JSON block found")
        return None

    data = match.group(1)
    data = data.replace("&quot;", '"')

    try:
        obj = json.loads(data)
    except:
        print("JSON parse error")
        return None

    text = json.dumps(obj)

    match2 = re.search(r'"activityUrn":"urn:li:activity:(\d+)"', text)

    if not match2:
        print("No activity id found")
        return None

    return match2.group(1)


def push_to_lark(post_id):

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

    html = fetch_html(LINKEDIN_PAGE)

    post_id = extract_post(html)

    if not post_id:
        print("No post detected")
        return

    print("Latest post id:", post_id)

    push_to_lark(post_id)


if __name__ == "__main__":
    main()
