import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
import sys

DISCORD_WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")

FEEDS = [
    {
        "name": "TLDR Tech",
        "url": "https://tldr.tech/api/rss/tech",
        "color": 0x00A8E8,
        "emoji": "💻",
    },
    {
        "name": "TLDR AI",
        "url": "https://tldr.tech/api/rss/ai",
        "color": 0x7C3AED,
        "emoji": "🤖",
    },
]

MAX_ITEMS_PER_FEED = 5


def fetch_rss(url: str) -> list[dict]:
    resp = requests.get(url, timeout=15)
    resp.raise_for_status()
    root = ET.fromstring(resp.content)
    channel = root.find("channel")
    items = []
    for item in channel.findall("item")[:MAX_ITEMS_PER_FEED]:
        title = item.findtext("title", "").strip()
        link = item.findtext("link", "").strip()
        description = item.findtext("description", "").strip()
        # Strip HTML tags from description
        import re
        description = re.sub(r"<[^>]+>", "", description)
        description = description[:200].strip()
        if description and not description.endswith("…"):
            description = description + "…" if len(description) == 200 else description
        items.append({"title": title, "link": link, "description": description})
    return items


def build_embed(feed: dict, items: list[dict]) -> dict:
    today = datetime.now(timezone.utc).strftime("%Y년 %m월 %d일")
    fields = []
    for item in items:
        value = f"{item['description']}\n[읽기]({item['link']})" if item["description"] else f"[읽기]({item['link']})"
        fields.append({
            "name": f"{item['title']}",
            "value": value,
            "inline": False,
        })
    return {
        "title": f"{feed['emoji']} {feed['name']} — {today}",
        "color": feed["color"],
        "fields": fields,
        "footer": {"text": "tldr.tech"},
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def send_to_discord(embeds: list[dict]) -> None:
    payload = {"embeds": embeds}
    resp = requests.post(DISCORD_WEBHOOK_URL, json=payload, timeout=15)
    resp.raise_for_status()
    print(f"Discord 전송 완료: HTTP {resp.status_code}")


def main():
    if not DISCORD_WEBHOOK_URL:
        print("❌ DISCORD_WEBHOOK_URL 환경변수가 설정되지 않았습니다.")
        sys.exit(1)

    embeds = []
    for feed in FEEDS:
        print(f"[{feed['name']}] RSS 가져오는 중...")
        try:
            items = fetch_rss(feed["url"])
            print(f"  → {len(items)}개 항목 수신")
            embeds.append(build_embed(feed, items))
        except Exception as e:
            print(f"  ❌ 오류: {e}")

    if embeds:
        send_to_discord(embeds)
    else:
        print("전송할 내용이 없습니다.")


if __name__ == "__main__":
    main()
