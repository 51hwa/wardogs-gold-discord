import os
import re
import requests
from bs4 import BeautifulSoup

URL = "https://wardogstats.app/gold?refresh=1"
WEBHOOK = os.environ["DISCORD_WEBHOOK"]

html = requests.get(URL, timeout=20).text
soup = BeautifulSoup(html, "html.parser")
text = soup.get_text(" ", strip=True)

match = re.search(r"1 gold bar.*?\$(\d[\d,]+)", text, re.I)

if not match:
    raise RuntimeError("금값을 찾지 못했습니다.")

price = match.group(1)

message = {
    "content": f"🪙 **WARDOGS 오늘의 금값**\n💰 1 Gold Bar: **${price}**\n\n출처: Wardogs Stats\nhttps://wardogstats.app/gold"
}

response = requests.post(WEBHOOK, json=message, timeout=20)
response.raise_for_status()

print(f"Gold price: ${price}")
