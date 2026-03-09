import re
import requests
from html import unescape

FEED_URL = "https://www.linkedin.com/company/tspborgtr/posts-atom/"
WEBHOOK = "https://metx-digital.sg.larksuite.com/base/automation/webhook/event/WTqiakYyZwTVGVhKDVTlny8VgNe"


def fetch_feed():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }
    resp = requests.get(FEED_URL, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.text


def clean_text(text: str) -> str:
    text = unescape(text)
    text = re.sub(r"<.*?>", "", text, flags=re.S)
    return text.strip()


def parse_latest_post(feed_text: str):
    # 先找第一条 entry
    entry_match = re.search(r"<entry\b.*?</entry>", feed_text, re.S | re.I)
    if not entry_match:
        print("No entry found in feed")
        return None

    entry = entry_match.group(0)

    # 抓标题
    title_match = re.search(r"<title\b[^>]*>(.*?)</title>", entry, re.S | re.I)
    title = clean_text(title_match.group(1)) if title_match else "Latest LinkedIn Post"

    # 抓链接
    link_match = re.search(r'<link\b[^>]*href="([^"]+)"', entry, re.S | re.I)
    if not link_match:
        print("No link found in feed entry")
        return None

    link = unescape(link_match.group(1)).strip()

    return title, link


def push_to_lark(title: str, link: str):
    payload = {
        "title": title,
        "url": link,
        "author": "TSPB"
    }

    resp = requests.post(
        WEBHOOK,
        headers={"Content-Type": "application/json"},
        json=payload,
        timeout=20
    )
    resp.raise_for_status()
    print("Push success:", link)


def main():
    feed_text = fetch_feed()

    # 调试时可看前300个字符
    print("Feed preview:", feed_text[:300].replace("\n", " "))

    result = parse_latest_post(feed_text)

    if not result:
        print("No post found")
        return

    title, link = result
    print("Latest post title:", title)
    print("Latest post link:", link)

    push_to_lark(title, link)


if __name__ == "__main__":
    main()
