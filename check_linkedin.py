import requests

FEED_URL = "https://rsshub.app/linkedin/company/tspborgtr"
WEBHOOK = "https://metx-digital.sg.larksuite.com/base/automation/webhook/event/WTqiakYyZwTVGVhKDVTlny8VgNe"


def get_feed():
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(FEED_URL, headers=headers, timeout=30)

    print("Status code:", r.status_code)
    print("Content-Type:", r.headers.get("Content-Type"))
    print("Preview:")
    print(r.text[:500])

    return r


def main():
    r = get_feed()

    if r.status_code != 200:
        print("Request failed")
        return

    if "<rss" not in r.text and "<?xml" not in r.text:
        print("Not XML / RSS")
        return

    print("Looks like valid RSS/XML")


if __name__ == "__main__":
    main()
