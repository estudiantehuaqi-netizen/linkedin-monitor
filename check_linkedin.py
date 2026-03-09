import requests
import re

WEBHOOK = "https://metx-digital.sg.larksuite.com/base/automation/webhook/event/WTqiakYyZwTVGVhKDVTlny8VgNe"

url = "https://www.linkedin.com/company/tspborgtr/posts/"

headers = {
    "User-Agent": "Mozilla/5.0"
}

html = requests.get(url, headers=headers).text

match = re.search(r'activity:(\d+)', html)

if match:
    post_id = match.group(1)
    post_url = f"https://www.linkedin.com/feed/update/urn:li:activity:{post_id}/"

    data = {
        "title": "New LinkedIn Post",
        "url": post_url,
        "author": "TSPB"
    }

    requests.post(WEBHOOK, json=data)
