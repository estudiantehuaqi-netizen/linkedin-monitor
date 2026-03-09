import requests
import xml.etree.ElementTree as ET

FEED_URL = "https://www.linkedin.com/company/tspborgtr/posts-atom/"
WEBHOOK = "你的飞书webhook"


def get_latest_post():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(FEED_URL, headers=headers, timeout=30)

    text = r.text

    print("Feed preview:", text[:200])

    if "<entry>" not in text:
        print("No post detected")
        return None

    root = ET.fromstring(text)

    ns = {"a": "http://www.w3.org/2005/Atom"}

    entry = root.find("a:entry", ns)

    title = entry.find("a:title", ns).text
    link = entry.find("a:link", ns).attrib["href"]

    return title, link


def push_to_lark(title, link):

    data = {
        "title": title,
        "url": link,
        "author": "TSPB"
    }

    requests.post(WEBHOOK, json=data)


def main():

    result = get_latest_post()

    if not result:
        return

    title, link = result

    print("Latest post:", title)
    print(link)

    push_to_lark(title, link)


if __name__ == "__main__":
    main()
