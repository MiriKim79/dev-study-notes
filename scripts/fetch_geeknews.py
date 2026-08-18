# -*- coding: utf-8 -*-
"""
fetch_geeknews.py — GeekNews(news.hada.io) 공개 Atom 피드에서 최신 글 목록을 가져와
assets/news-feed.json으로 저장한다. 외부 라이브러리 없이 표준 라이브러리만 사용한다.

GitHub Actions에서 매일 실행되고, 결과 JSON이 바뀌면 그 변경분만 커밋된다.
사이트(index.html)는 이 JSON을 빌드 시점이 아니라 "브라우저에서 방문할 때" 그대로
fetch해서 보여주므로, 이 스크립트가 새 파일을 커밋하기만 하면 별도로 build_site.py를
다시 돌리지 않아도 다음 방문자에게 최신 목록이 보인다.

실행: python scripts/fetch_geeknews.py
"""
import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FEED_URL = "https://news.hada.io/rss"
OUTPUT = ROOT / "assets" / "news-feed.json"
MAX_ITEMS = 8
NS = {"a": "http://www.w3.org/2005/Atom"}


def fetch_feed_xml():
    req = urllib.request.Request(
        FEED_URL,
        headers={"User-Agent": "Mozilla/5.0 (dev-study-notes news digest bot)"},
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return resp.read()


def strip_html(text):
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def parse_entries(xml_bytes):
    root = ET.fromstring(xml_bytes)
    items = []
    for entry in root.findall("a:entry", NS)[:MAX_ITEMS]:
        title_el = entry.find("a:title", NS)
        link_el = entry.find("a:link", NS)
        published_el = entry.find("a:published", NS)
        content_el = entry.find("a:content", NS)

        title = (title_el.text or "").strip() if title_el is not None else ""
        url = link_el.get("href") if link_el is not None else ""
        published = (published_el.text or "").strip() if published_el is not None else ""
        summary = strip_html(content_el.text) if content_el is not None and content_el.text else ""
        summary = summary[:110] + ("…" if len(summary) > 110 else "")

        if not (title and url):
            continue
        items.append({
            "source": "GeekNews",
            "title": title,
            "url": url,
            "date": published[:10] if published else "",
            "summary": summary,
        })
    return items


def main():
    try:
        xml_bytes = fetch_feed_xml()
        items = parse_entries(xml_bytes)
    except Exception as e:
        # 피드 서버가 잠깐 죽어 있어도 워크플로 전체가 실패 처리되지 않도록,
        # 실패 시 기존 파일을 건드리지 않고 조용히 종료한다.
        print("GeekNews 피드 수집 실패, 기존 파일 유지:", e, file=sys.stderr)
        return 0

    if not items:
        print("GeekNews 피드에서 항목을 찾지 못했습니다. 기존 파일 유지.", file=sys.stderr)
        return 0

    payload = {
        "updated_at": items[0]["date"] if items else "",
        "items": items,
    }
    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print("생성:", OUTPUT, f"({len(items)}건)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
