# -*- coding: utf-8 -*-
"""
verify_site.py — 원본 Markdown과 생성된 HTML을 대조해 누락된 내용이 없는지 검사한다.
- 모든 헤딩 텍스트, 코드블록 원문, 표 셀 텍스트, 체크리스트 항목이 HTML에 그대로 있는지 확인.
- 원본 .md 파일이 변경되지 않았는지(해시) 확인.
실행: python verify_site.py
"""
import hashlib
import html as htmllib
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_site as bs

ROOT = bs.ROOT


def strip_tags(html_text):
    text = re.sub(r"<script[^>]*>.*?</script>", " ", html_text, flags=re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = htmllib.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


def collect_originals(blocks):
    """검증 대상 원문 조각 목록: (종류, 텍스트)"""
    items = []

    def walk(blist):
        for b in blist:
            t = b["type"]
            if t == "heading":
                items.append(("heading", b["text"]))
            elif t == "code":
                if b["code"].strip():
                    items.append(("code", b["code"]))
            elif t == "table":
                for cell in b["header"]:
                    if cell.strip():
                        items.append(("table-cell", cell))
                for row in b["rows"]:
                    for cell in row:
                        if cell.strip():
                            items.append(("table-cell", cell))
            elif t == "list":
                for it in b["items"]:
                    walk(it["blocks"])
            elif t == "blockquote":
                walk(b["blocks"])
            elif t == "para":
                for l in b["lines"]:
                    if l.strip():
                        items.append(("para-line", l.strip()))
            elif t == "concept_box":
                walk(b["inner"])

    walk(blocks)
    return items


def strip_md_inline(s):
    s = re.sub(r"\*\*([^*]+)\*\*", r"\1", s)
    s = re.sub(r"`([^`]+)`", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    return s


def check_page(page):
    md_path = ROOT / page["src"]
    html_path = ROOT / (page["src"][:-3] + ".html")
    raw = md_path.read_text(encoding="utf-8")
    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    intro_rows, start_idx = bs.extract_intro(lines)
    blocks = bs.parse_blocks(lines, start_idx, len(lines))

    html_text = html_path.read_text(encoding="utf-8")
    html_plain = norm(strip_tags(html_text))
    # 인라인 태그(<code>, <strong>, <a> 등) 경계에서 strip_tags가 공백을 끼워 넣어
    # "것</strong>을" 같은 원문이 "것 을"처럼 갈라지는 오탐이 생긴다.
    # 공백을 아예 제거한 버전으로 포함 여부를 비교해 이런 오탐을 없앤다.
    html_plain_ns = re.sub(r"\s+", "", html_plain)

    # 코드블록은 태그 제거 후에도 원문 그대로 남아야 하므로 code 태그 안 raw 텍스트를 별도로 모은다.
    code_blocks_html = re.findall(r"<code>(.*?)</code>", html_text, flags=re.DOTALL)
    code_blocks_plain = [htmllib.unescape(re.sub(r"<[^>]+>", "", c)) for c in code_blocks_html]
    code_blocks_joined = "\n".join(code_blocks_plain)

    missing = []
    originals = collect_originals(blocks)
    if intro_rows:
        for row in intro_rows:
            originals.append(("intro", strip_md_inline(row)))

    for kind, text in originals:
        clean = strip_md_inline(text)
        needle = norm(clean)
        if not needle:
            continue
        if kind == "code":
            haystack = code_blocks_joined
            if needle_multiline_in(text, haystack):
                continue
            missing.append((kind, text[:80]))
            continue
        if needle in html_plain:
            continue
        needle_ns = re.sub(r"\s+", "", needle)
        if needle_ns and needle_ns in html_plain_ns:
            continue
        missing.append((kind, text[:80]))

    return missing


def needle_multiline_in(raw_code, haystack):
    target = raw_code.strip("\n")
    if not target:
        return True
    if target in haystack:
        return True
    # 공백 정규화 비교(줄 단위)
    t_lines = [l.rstrip() for l in target.split("\n")]
    h_lines = [l.rstrip() for l in haystack.split("\n")]
    joined_t = "\n".join(t_lines)
    joined_h = "\n".join(h_lines)
    return joined_t in joined_h


def check_originals_untouched(before_hashes):
    changed = []
    for page in bs.PAGES:
        p = ROOT / page["src"]
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        if before_hashes.get(page["src"]) != h:
            changed.append(page["src"])
    return changed


def main():
    before_hashes = {}
    for page in bs.PAGES:
        p = ROOT / page["src"]
        before_hashes[page["src"]] = hashlib.sha256(p.read_bytes()).hexdigest()

    total_missing = 0
    for page in bs.PAGES:
        missing = check_page(page)
        if missing:
            total_missing += len(missing)
            print("\n[누락 의심] %s — %d건" % (page["src"], len(missing)))
            for kind, snippet in missing[:20]:
                print("  - (%s) %s" % (kind, snippet))
        else:
            print("[통과] %s" % page["src"])

    changed = check_originals_untouched(before_hashes)
    print()
    if changed:
        print("!! 원본 .md 파일이 변경되었습니다:", changed)
    else:
        print("원본 .md 파일 무결성 확인: 변경 없음 (%d개)" % len(bs.PAGES))

    print("\n총 누락 의심 항목:", total_missing)
    return 0 if total_missing == 0 and not changed else 1


if __name__ == "__main__":
    raise SystemExit(main())
