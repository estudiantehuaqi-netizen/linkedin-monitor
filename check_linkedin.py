import requests
import xml.etree.ElementTree as ET

FEED_URL = "https://www.linkedin.com/company/tspborgtr/posts-atom/"
WEBHOOK = "https://metx-digital.sg.larksuite.com/base/automation/webhook/event/WTqiakYyZwTVGVhKDVTlny8VgNe"


def fetch_feed():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    resp = requests.get(FEED_URL, headers=headers, timeout=30)
    resp.raise_for_status()

    return resp.text


def parse_latest_post(xml_data):

    root = ET.fromstring(xml_data)

    ns = {
        "atom": "http://www.w3.org/2005/Atom"
    }

    entry = root.find("atom:entry", ns)

    if entry is None:
        return None

    title = entry.find("atom:title", ns).text
    link = entry.find("atom:link", ns).attrib["href"]

    return title, link


def push_to_lark(title, link):

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

    xml_data = fetch_feed()

    result = parse_latest_post(xml_data)

    if not result:
        print("No post found")
        return

    title, link = result

    print("Latest post:", title)

    push_to_lark(title, link)


if __name__ == "__main__":
    main()
