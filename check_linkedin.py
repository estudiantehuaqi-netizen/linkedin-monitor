import requests
import xml.etree.ElementTree as ET

FEED_URL = "https://rsshub.app/linkedin/company/tspborgtr"
WEBHOOK = "你的飞书webhook"


def get_latest_post():

    r = requests.get(FEED_URL, timeout=30)

    xml = r.text

    root = ET.fromstring(xml)

    channel = root.find("channel")
    item = channel.find("item")

    title = item.find("title").text
    link = item.find("link").text

    return title, link


def push(title, link):

    data = {
        "title": title,
        "url": link,
        "author": "TSPB"
    }

    requests.post(WEBHOOK, json=data)


def main():

    title, link = get_latest_post()

    print(title)
    print(link)

    push(title, link)


if __name__ == "__main__":
    main()
