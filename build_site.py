# -*- coding: utf-8 -*-
"""
build_site.py — 개발 학습·실전 노트의 Markdown 원본을 학습용 HTML로 변환한다.

- 원본 .md 파일은 절대 읽기만 하고 수정하지 않는다.
- 표준 라이브러리만 사용한다(외부 markdown 라이브러리·CDN 없음).
- 실행: python build_site.py
- Markdown을 수정한 뒤 다시 이 스크립트를 실행하면 HTML이 재생성된다.
"""
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent

# ==========================================================================
# 1. 사이트에 포함되는 문서 목록(메타데이터) — 실제 파일명을 기준으로 한다.
# ==========================================================================
PLAYBOOK_DIR = "개발 기초·실전 가이드"
TEMPLATE_DIR = "GitHub 팀 협업 템플릿"

PAGES = [
    {
        "key": "playbook-hub",
        "src": f"{PLAYBOOK_DIR}.md",
        "title": "개발 기초·실전 가이드",
        "kicker": "가이드 모음",
        "cat": "start",
        "icon": "📚",
        "hub": None,
        "hub_children": ["team-start", "frontend", "backend", "ai", "git"],
    },
    {
        "key": "team-start",
        "src": f"{PLAYBOOK_DIR}/팀 개발 시작 가이드.md",
        "title": "팀 개발 시작 가이드",
        "kicker": "개발 기초·실전 가이드",
        "cat": "start",
        "icon": "🚀",
        "hub": "playbook-hub",
    },
    {
        "key": "frontend",
        "src": f"{PLAYBOOK_DIR}/프론트엔드 기초 가이드.md",
        "title": "프론트엔드 기초 가이드",
        "kicker": "개발 기초·실전 가이드",
        "cat": "frontend",
        "icon": "🎨",
        "hub": "playbook-hub",
    },
    {
        "key": "backend",
        "src": f"{PLAYBOOK_DIR}/백엔드 기초 가이드.md",
        "title": "백엔드 기초 가이드",
        "kicker": "개발 기초·실전 가이드",
        "cat": "backend",
        "icon": "🛠️",
        "hub": "playbook-hub",
    },
    {
        "key": "ai",
        "src": f"{PLAYBOOK_DIR}/생성형 AI 기능 개발 기초 가이드.md",
        "title": "생성형 AI 기능 개발 기초 가이드",
        "kicker": "개발 기초·실전 가이드",
        "cat": "ai",
        "icon": "🤖",
        "hub": "playbook-hub",
    },
    {
        "key": "git",
        "src": f"{PLAYBOOK_DIR}/Git·GitHub 기초 가이드.md",
        "title": "Git·GitHub 기초 가이드",
        "kicker": "개발 기초·실전 가이드",
        "cat": "git",
        "icon": "🌿",
        "hub": "playbook-hub",
    },
    {
        "key": "collab-method",
        "src": "개발 협업 방식 선택 가이드.md",
        "title": "개발 협업 방식 선택 가이드",
        "kicker": "협업 방식",
        "cat": "collab",
        "icon": "🧭",
        "hub": None,
    },
    {
        "key": "github-hub",
        "src": f"{TEMPLATE_DIR}.md",
        "title": "GitHub 팀 협업 가이드",
        "kicker": "협업 템플릿",
        "cat": "github",
        "icon": "🤝",
        "hub": None,
        "hub_children": ["contributing", "agents", "claude", "planning", "issue-pr"],
    },
    {
        "key": "contributing",
        "src": f"{TEMPLATE_DIR}/팀 GitHub 협업 규칙 (CONTRIBUTING.md).md",
        "title": "팀 GitHub 협업 규칙 (CONTRIBUTING.md)",
        "kicker": "GitHub 팀 협업 가이드",
        "cat": "github",
        "icon": "📋",
        "hub": "github-hub",
    },
    {
        "key": "agents",
        "src": f"{TEMPLATE_DIR}/AI 코딩 에이전트 작업 규칙 (AGENTS.md).md",
        "title": "AI 코딩 에이전트 작업 규칙 (AGENTS.md)",
        "kicker": "GitHub 팀 협업 가이드",
        "cat": "github",
        "icon": "🧠",
        "hub": "github-hub",
    },
    {
        "key": "claude",
        "src": f"{TEMPLATE_DIR}/Claude Code 작업 규칙 (CLAUDE.md).md",
        "title": "Claude Code 작업 규칙 (CLAUDE.md)",
        "kicker": "GitHub 팀 협업 가이드",
        "cat": "github",
        "icon": "⚙️",
        "hub": "github-hub",
    },
    {
        "key": "planning",
        "src": f"{TEMPLATE_DIR}/기획·API·일정 템플릿 (PLANNING.md).md",
        "title": "기획·API·일정 템플릿 (PLANNING.md)",
        "kicker": "GitHub 팀 협업 가이드",
        "cat": "github",
        "icon": "🗂️",
        "hub": "github-hub",
    },
    {
        "key": "issue-pr",
        "src": f"{TEMPLATE_DIR}/GitHub Issue·PR 템플릿 예시.md",
        "title": "GitHub Issue·PR 템플릿 예시",
        "kicker": "GitHub 팀 협업 가이드",
        "cat": "github",
        "icon": "🏷️",
        "hub": "github-hub",
    },
]
PAGES_BY_KEY = {p["key"]: p for p in PAGES}

# 학습 추천 순서(이전/다음 네비게이션에 사용) — index.html 포함
STUDY_ORDER = [
    "index",
    "playbook-hub",
    "team-start",
    "git",
    "frontend",
    "backend",
    "ai",
    "collab-method",
    "github-hub",
    "contributing",
    "agents",
    "claude",
    "planning",
    "issue-pr",
]

CAT_LABEL = {
    "start": "팀 개발 시작",
    "frontend": "프론트엔드",
    "backend": "백엔드",
    "ai": "생성형 AI",
    "git": "Git·GitHub",
    "collab": "협업 방식",
    "github": "GitHub 팀 협업",
}


def url_of(key):
    if key == "index":
        return "index.html"
    return PAGES_BY_KEY[key]["src"][:-3] + ".html"


def prefix_of(key):
    """루트 기준 상대 경로 접두사('' 또는 '../')."""
    if key == "index":
        return ""
    src = PAGES_BY_KEY[key]["src"]
    return "../" if "/" in src else ""


def rel_link(from_key, to_key):
    """from_key 페이지에서 to_key 페이지로 가는 상대 경로."""
    from_prefix = prefix_of(from_key)
    to_url = url_of(to_key)
    to_src = "" if to_key == "index" else PAGES_BY_KEY[to_key]["src"]
    to_in_sub = "/" in to_src if to_key != "index" else False
    from_in_sub = from_prefix == "../"

    if to_key == "index":
        return ("../" if from_in_sub else "") + "index.html"
    if from_in_sub and to_in_sub:
        # 둘 다 서브폴더에 있을 때: 같은 폴더인지 확인
        from_src = PAGES_BY_KEY[from_key]["src"]
        if from_src.split("/")[0] == to_src.split("/")[0]:
            return to_src.split("/")[-1][:-3] + ".html"
        return "../" + to_url
    if from_in_sub and not to_in_sub:
        return "../" + to_url
    if not from_in_sub and to_in_sub:
        return to_url
    return to_url


# ==========================================================================
# 2. 마크다운 파서 (표준 라이브러리만 사용, 이 저장소 문서에서 실제로
#    쓰인 구문만 지원한다: 헤딩 h1~h3, 문단, 굵게, 인라인 코드, 링크,
#    가로줄, blockquote, 펜스 코드블록(중첩 백틱 길이 포함),
#    순서/비순서 리스트(체크박스·중첩 포함), GFM 표)
# ==========================================================================
FENCE_OPEN_RE = re.compile(r"^(`{3,}|~{3,})\s*([^\s`]*)\s*$")
HEADING_RE = re.compile(r"^(#{1,3})\s+(.*)$")
HR_RE = re.compile(r"^-{3,}\s*$")
LIST_MARKER_RE = re.compile(r"^([-*]|\d+[.)])\s+(.*)$")
CHECKBOX_RE = re.compile(r"^\[( |x|X)\]\s?(.*)$")
SEP_CELL_RE = re.compile(r"^:?-{1,}:?$")
LABEL_RE = re.compile(r"^\*\*([^*]{1,14}):\*\*\s*(.*)$")


def is_ordered_marker(marker):
    return marker[0].isdigit()


def strip_table_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def is_table_start(lines, i, end):
    if i + 1 >= end:
        return False
    if "|" not in lines[i]:
        return False
    sep = lines[i + 1]
    if "|" not in sep and "-" not in sep:
        return False
    cells = strip_table_row(sep)
    return len(cells) > 0 and all(SEP_CELL_RE.match(c) for c in cells if c != "") and any(c for c in cells)


def parse_fence(lines, i, end):
    m = FENCE_OPEN_RE.match(lines[i])
    fence_char = m.group(1)[0]
    fence_len = len(m.group(1))
    lang = m.group(2) or ""
    i += 1
    close_re = re.compile(r"^" + re.escape(fence_char) + ("{%d,}" % fence_len) + r"\s*$")
    content = []
    while i < end:
        if close_re.match(lines[i]):
            i += 1
            break
        content.append(lines[i])
        i += 1
    else:
        pass
    return {"type": "code", "lang": lang, "code": "\n".join(content)}, i


def parse_blockquote(lines, i, end):
    content = []
    while i < end and lines[i].lstrip().startswith(">"):
        l = lines[i].lstrip()[1:]
        if l.startswith(" "):
            l = l[1:]
        content.append(l)
        i += 1
    sub_blocks = parse_blocks(content, 0, len(content))
    return {"type": "blockquote", "blocks": sub_blocks}, i


def parse_table(lines, i, end):
    header = strip_table_row(lines[i])
    i += 2  # 헤더 + 구분행
    rows = []
    while i < end and lines[i].strip() != "" and "|" in lines[i] and not FENCE_OPEN_RE.match(lines[i]):
        rows.append(strip_table_row(lines[i]))
        i += 1
    return {"type": "table", "header": header, "rows": rows}, i


def parse_paragraph(lines, i, end):
    content = []
    while i < end:
        line = lines[i]
        if line.strip() == "":
            break
        if FENCE_OPEN_RE.match(line):
            break
        if HEADING_RE.match(line):
            break
        if HR_RE.match(line):
            break
        if line.lstrip().startswith(">"):
            break
        if is_table_start(lines, i, end):
            break
        content.append(line.rstrip())
        i += 1
    return {"type": "para", "lines": content}, i


def parse_list(lines, i, end):
    first = lines[i]
    indent = len(first) - len(first.lstrip(" "))
    m0 = LIST_MARKER_RE.match(first.strip())
    ordered = is_ordered_marker(m0.group(1))
    items = []
    while i < end:
        line = lines[i]
        if line.strip() == "":
            j = i
            while j < end and lines[j].strip() == "":
                j += 1
            if j >= end:
                i = j
                break
            nxt = lines[j]
            nxt_indent = len(nxt) - len(nxt.lstrip(" "))
            nxt_is_item = bool(LIST_MARKER_RE.match(nxt.strip())) and nxt_indent == indent
            if nxt_is_item or nxt_indent > indent:
                i = j
                continue
            break
        cur_indent = len(line) - len(line.lstrip(" "))
        if cur_indent != indent:
            break
        m = LIST_MARKER_RE.match(line.strip())
        if not m:
            break
        marker_text = line.strip()[: m.start(2)]
        content_col = indent + len(marker_text)
        first_content = m.group(2)
        item_lines = [first_content]
        i += 1
        while i < end:
            l2 = lines[i]
            if l2.strip() == "":
                j = i
                while j < end and lines[j].strip() == "":
                    j += 1
                if j < end:
                    l2i = len(lines[j]) - len(lines[j].lstrip(" "))
                    if l2i >= content_col:
                        item_lines.append("")
                        i = j
                        continue
                break
            l2_indent = len(l2) - len(l2.lstrip(" "))
            if l2_indent >= content_col:
                if len(l2) >= content_col and l2[:content_col].strip() == "":
                    item_lines.append(l2[content_col:])
                else:
                    item_lines.append(l2.strip())
                i += 1
                continue
            break
        checked = None
        cb = CHECKBOX_RE.match(item_lines[0])
        if cb:
            checked = cb.group(1).lower() == "x"
            item_lines[0] = cb.group(2)
        sub_blocks = parse_blocks(item_lines, 0, len(item_lines))
        items.append({"blocks": sub_blocks, "checked": checked})
    return {"type": "list", "ordered": ordered, "items": items}, i


def parse_blocks(lines, i, end):
    blocks = []
    while i < end:
        line = lines[i]
        if line.strip() == "":
            i += 1
            continue
        if FENCE_OPEN_RE.match(line):
            b, i = parse_fence(lines, i, end)
            blocks.append(b)
            continue
        m = HEADING_RE.match(line)
        if m:
            blocks.append({"type": "heading", "level": len(m.group(1)), "text": m.group(2).strip()})
            i += 1
            continue
        if HR_RE.match(line):
            blocks.append({"type": "hr"})
            i += 1
            continue
        if line.lstrip().startswith(">"):
            b, i = parse_blockquote(lines, i, end)
            blocks.append(b)
            continue
        if is_table_start(lines, i, end):
            b, i = parse_table(lines, i, end)
            blocks.append(b)
            continue
        if LIST_MARKER_RE.match(line.strip()):
            b, i = parse_list(lines, i, end)
            blocks.append(b)
            continue
        b, i = parse_paragraph(lines, i, end)
        blocks.append(b)
    return blocks


def extract_intro(lines):
    if not lines or not lines[0].lstrip().startswith(">"):
        return None, 0
    i = 0
    rows = []
    while i < len(lines) and lines[i].lstrip().startswith(">"):
        raw = lines[i].lstrip()[1:]
        if raw.startswith(" "):
            raw = raw[1:]
        rows.append(raw.rstrip())
        i += 1
    return rows, i


# ==========================================================================
# 3. 인라인 렌더링 (인라인 코드 보호 → 링크 → 굵게 → 이스케이프 복원 순서)
# ==========================================================================
INLINE_CODE_RE = re.compile(r"`([^`]+)`")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
BOLD_RE = re.compile(r"\*\*([^*]+)\*\*")


def render_inline(text):
    codes = []

    def stash_code(m):
        codes.append(m.group(1))
        return "\x00C%d\x00" % (len(codes) - 1)

    text = INLINE_CODE_RE.sub(stash_code, text)

    links = []

    def stash_link(m):
        links.append((m.group(1), m.group(2)))
        return "\x00L%d\x00" % (len(links) - 1)

    text = LINK_RE.sub(stash_link, text)

    text = html.escape(text, quote=False)
    text = BOLD_RE.sub(r"<strong>\1</strong>", text)

    def restore_link(m):
        idx = int(m.group(1))
        label, url = links[idx]
        label_html = html.escape(label, quote=False)
        label_html = BOLD_RE.sub(r"<strong>\1</strong>", label_html)
        target = ' target="_blank" rel="noopener"' if url.startswith("http") else ""
        return '<a href="%s"%s>%s</a>' % (html.escape(url, quote=True), target, label_html)

    text = re.sub(r"\x00L(\d+)\x00", restore_link, text)

    def restore_code(m):
        idx = int(m.group(1))
        return '<code class="inline-code">%s</code>' % html.escape(codes[idx], quote=False)

    text = re.sub(r"\x00C(\d+)\x00", restore_code, text)
    return text


def join_para_lines(lines):
    parts = []
    n = len(lines)
    for idx, raw in enumerate(lines):
        hard_break = raw.endswith("  ") and idx < n - 1
        parts.append(render_inline(raw.strip()))
        if hard_break:
            parts.append("<br>")
        elif idx < n - 1:
            parts.append(" ")
    return "".join(parts)


# ==========================================================================
# 4. 최소 syntax highlight (언어가 명시된 코드블록에만 적용, 나머지는 평문)
# ==========================================================================
HIGHLIGHT_RULES = {
    "bash": [
        (r"#.*$", "tok-comment"),
        (r'"[^"]*"', "tok-string"),
        (r"'[^']*'", "tok-string"),
        (r"\b(git|npm|pip|python|node|cd|ls|export|source|sudo|curl|gh)\b", "tok-keyword"),
    ],
    "python": [
        (r"#.*$", "tok-comment"),
        (r'"[^"]*"|\'[^\']*\'', "tok-string"),
        (r"\b(def|class|import|from|return|if|else|elif|for|while|as|with|try|except|in|is|not|and|or|None|True|False)\b", "tok-keyword"),
        (r"\b\d+\b", "tok-number"),
    ],
    "js": [
        (r"//.*$", "tok-comment"),
        (r'"[^"]*"|\'[^\']*\'|`[^`]*`', "tok-string"),
        (r"\b(const|let|var|function|return|if|else|for|while|import|from|export|default|async|await|class|new|extends|try|catch|null|undefined|true|false)\b", "tok-keyword"),
        (r"\b\d+\b", "tok-number"),
    ],
    "ts": [],  # js 규칙 재사용(아래에서 매핑)
    "jsx": [],
    "json": [
        (r'"[^"]*"\s*:', "tok-func"),
        (r'"[^"]*"', "tok-string"),
        (r"\b\d+\b", "tok-number"),
    ],
    "css": [
        (r"/\*.*?\*/", "tok-comment"),
        (r"[.#][\w-]+", "tok-func"),
        (r"\b\d+(px|em|rem|%)?\b", "tok-number"),
    ],
    "http": [
        (r"^(GET|POST|PUT|PATCH|DELETE)\b", "tok-keyword"),
    ],
}
HIGHLIGHT_RULES["ts"] = HIGHLIGHT_RULES["js"]
HIGHLIGHT_RULES["jsx"] = HIGHLIGHT_RULES["js"]
HIGHLIGHT_RULES["tsx"] = HIGHLIGHT_RULES["js"]


def highlight_code(code, lang):
    rules = HIGHLIGHT_RULES.get(lang.lower())
    escaped = html.escape(code)
    if not rules:
        return escaped

    # 이스케이프된 텍스트 위에서 토큰을 감싼다(겹치지 않게 순차 처리 + 플레이스홀더)
    placeholders = []

    def wrap(pattern, cls, text):
        def sub(m):
            placeholders.append('<span class="%s">%s</span>' % (cls, m.group(0)))
            return "\x00T%d\x00" % (len(placeholders) - 1)
        return re.sub(pattern, sub, text, flags=re.MULTILINE)

    text = escaped
    for pattern, cls in rules:
        text = wrap(pattern, cls, text)
    text = re.sub(r"\x00T(\d+)\x00", lambda m: placeholders[int(m.group(1))], text)
    return text


# ==========================================================================
# 5. 헤딩 메타데이터 부여 / 목차 / '기본 상식' 콜아웃 래핑
# ==========================================================================
def slugify(text, used):
    s = re.sub(r"[`*]", "", text)
    s = re.sub(r"[^0-9A-Za-z가-힣]+", "-", s)
    s = s.strip("-") or "section"
    base, n = s, 2
    while s in used:
        s = f"{base}-{n}"
        n += 1
    used.add(s)
    return s


TAG_BY_OFFSET = {0: "h2", 1: "h3", 2: "h4"}
CLS_BY_OFFSET = {0: "section-h1", 1: "section-h2", 2: "section-h3"}


def assign_heading_meta(blocks):
    levels = [b["level"] for b in blocks if b["type"] == "heading"]
    min_level = min(levels) if levels else 1
    used = set()
    for b in blocks:
        if b["type"] != "heading":
            continue
        offset = max(0, min(2, b["level"] - min_level))
        b["tag"] = TAG_BY_OFFSET[offset]
        b["cls"] = CLS_BY_OFFSET[offset]
        b["mapped"] = offset
        b["id"] = slugify(b["text"], used)


def build_toc(blocks):
    toc = []
    current = None
    for b in blocks:
        if b["type"] != "heading":
            continue
        if b["mapped"] == 0:
            current = {"id": b["id"], "text": b["text"], "children": []}
            toc.append(current)
        elif b["mapped"] == 1:
            entry = {"id": b["id"], "text": b["text"]}
            if current is not None:
                current["children"].append(entry)
            else:
                toc.append({"id": b["id"], "text": b["text"], "children": []})
    return toc


def normalize_heading_text(t):
    return t.replace(" ", "")


def wrap_concept_boxes(blocks):
    out = []
    i, n = 0, len(blocks)
    while i < n:
        b = blocks[i]
        if b["type"] == "heading" and b["mapped"] == 2 and normalize_heading_text(b["text"]) == "기본상식":
            j = i + 1
            while j < n and blocks[j]["type"] != "heading":
                j += 1
            out.append({"type": "concept_box", "inner": blocks[i:j]})
            i = j
        else:
            out.append(b)
            i += 1
    return out


# ==========================================================================
# 6. 블록 렌더링
# ==========================================================================
def render_item_inner(item_blocks):
    if len(item_blocks) == 1 and item_blocks[0]["type"] == "para":
        return join_para_lines(item_blocks[0]["lines"])
    return render_blocks(item_blocks)


def render_list(b):
    is_checklist = any(it.get("checked") is not None for it in b["items"])
    tag = "ul" if is_checklist else ("ol" if b["ordered"] else "ul")
    cls = ' class="checklist"' if is_checklist else ""
    parts = []
    for it in b["items"]:
        inner = render_item_inner(it["blocks"])
        if it.get("checked") is not None:
            checked_attr = " checked" if it["checked"] else ""
            li_cls = ' class="checked"' if it["checked"] else ""
            parts.append('<li%s><input type="checkbox" disabled%s><span>%s</span></li>' % (li_cls, checked_attr, inner))
        else:
            parts.append("<li>%s</li>" % inner)
    return "<%s%s>%s</%s>" % (tag, cls, "".join(parts), tag)


def render_table(b):
    thead = "<tr>" + "".join("<th>%s</th>" % render_inline(c) for c in b["header"]) + "</tr>"
    body_rows = []
    for r in b["rows"]:
        cells = "".join("<td>%s</td>" % render_inline(c) for c in r)
        body_rows.append("<tr>%s</tr>" % cells)
    return '<div class="table-scroll"><table><thead>%s</thead><tbody>%s</tbody></table></div>' % (thead, "".join(body_rows))


def render_code(b):
    lang = (b["lang"] or "").strip()
    label = lang if lang else "text"
    code_html = highlight_code(b["code"], lang) if lang else html.escape(b["code"])
    return (
        '<div class="code-block"><div class="code-block-header">'
        '<span class="code-lang">%s</span>'
        '<button class="copy-btn" type="button">복사</button></div>'
        "<pre><code>%s</code></pre></div>" % (html.escape(label), code_html)
    )


def render_heading(b):
    return '<%s class="%s" id="%s">%s<a class="heading-anchor" href="#%s" aria-label="이 섹션 링크">#</a></%s>' % (
        b["tag"], b["cls"], b["id"], render_inline(b["text"]), b["id"], b["tag"]
    )


def render_blocks(blocks):
    out = []
    for b in blocks:
        t = b["type"]
        if t == "heading":
            out.append(render_heading(b))
        elif t == "code":
            out.append(render_code(b))
        elif t == "table":
            out.append(render_table(b))
        elif t == "list":
            out.append(render_list(b))
        elif t == "blockquote":
            out.append("<blockquote>" + render_blocks(b["blocks"]) + "</blockquote>")
        elif t == "hr":
            out.append("<hr>")
        elif t == "para":
            if b["lines"]:
                out.append("<p>" + join_para_lines(b["lines"]) + "</p>")
        elif t == "concept_box":
            out.append(
                '<div class="callout callout-concept"><div class="callout-label">💡 핵심 개념</div>'
                + render_blocks(b["inner"])
                + "</div>"
            )
    return "\n".join(out)


def render_intro_box(rows):
    parts = []
    for row in rows:
        m = LABEL_RE.match(row)
        if m:
            parts.append(
                '<div class="intro-row"><strong>%s:</strong> %s</div>'
                % (html.escape(m.group(1)), render_inline(m.group(2)))
            )
        else:
            parts.append('<div class="intro-row">%s</div>' % render_inline(row))
    return '<div class="callout callout-intro"><div class="callout-label">📘 문서 소개</div>%s</div>' % "".join(parts)


def render_outline_box(toc):
    if not toc:
        return ""
    items = "".join("<li>%s</li>" % html.escape(t["text"]) for t in toc)
    return (
        '<div class="callout callout-outline"><div class="callout-label">🗂️ 이 문서의 구성</div>'
        "<ol>%s</ol></div>" % items
    )


# ==========================================================================
# 7. 페이지 조립 (공통 셸)
# ==========================================================================
def render_sidebar_toc(toc):
    items = []
    for t in toc:
        children = ""
        if t["children"]:
            children = '<ul class="toc-h2-list">' + "".join(
                '<li><a href="#%s">%s</a></li>' % (c["id"], html.escape(c["text"])) for c in t["children"]
            ) + "</ul>"
        items.append('<li class="toc-h1"><a href="#%s">%s</a>%s</li>' % (t["id"], html.escape(t["text"]), children))
    return '<ul class="toc">' + "".join(items) + "</ul>"


def render_breadcrumb(page):
    parts = ['<a href="%s">대시보드</a>' % rel_link(page["key"], "index")]
    if page.get("hub"):
        hub = PAGES_BY_KEY[page["hub"]]
        parts.append('<span>›</span><a href="%s">%s</a>' % (rel_link(page["key"], page["hub"]), html.escape(hub["title"])))
    parts.append('<span>›</span><span class="current">%s</span>' % html.escape(page["title"]))
    return " ".join(parts)


def render_prev_next(page_key):
    idx = STUDY_ORDER.index(page_key)
    prev_key = STUDY_ORDER[idx - 1] if idx > 0 else None
    next_key = STUDY_ORDER[idx + 1] if idx < len(STUDY_ORDER) - 1 else None

    def label(k):
        return "학습 대시보드" if k == "index" else PAGES_BY_KEY[k]["title"]

    left = ""
    right = ""
    if prev_key:
        left = '<a class="doc-nav-link prev" href="%s"><span class="doc-nav-dir">← 이전 학습</span><span class="doc-nav-title">%s</span></a>' % (
            rel_link(page_key, prev_key), html.escape(label(prev_key))
        )
    else:
        left = '<span class="doc-nav-spacer"></span>'
    if next_key:
        right = '<a class="doc-nav-link next" href="%s"><span class="doc-nav-dir">다음 학습 →</span><span class="doc-nav-title">%s</span></a>' % (
            rel_link(page_key, next_key), html.escape(label(next_key))
        )
    if not (prev_key or next_key):
        return ""
    return '<nav class="doc-nav">%s%s</nav>' % (left, right)


def render_hub_quicklinks(page):
    children = page.get("hub_children")
    if not children:
        return ""
    items = []
    for ck in children:
        c = PAGES_BY_KEY[ck]
        items.append(
            '<a class="hub-item" href="%s"><div><div class="hub-item-title">%s %s</div>'
            '<div class="hub-item-desc">%s</div></div><span class="hub-item-arrow">→</span></a>'
            % (rel_link(page["key"], ck), c["icon"], html.escape(c["title"]), html.escape(CAT_LABEL.get(c["cat"], "")))
        )
    return (
        '<div class="section-heading" style="margin-top:32px;">바로가기</div>'
        '<div class="hub-list">%s</div>' % "".join(items)
    )


PAGE_HTML_TMPL = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · 개발 학습·실전 노트</title>
<link rel="stylesheet" href="{prefix}assets/style.css">
<script src="{prefix}assets/search-index.js" defer></script>
</head>
<body data-root-prefix="{prefix}">
<div id="reading-progress"></div>
<header class="site-header">
  <div class="header-inner">
    <button class="menu-btn" type="button" aria-label="목차 열기">☰</button>
    <a class="brand" href="{prefix}index.html">개발 공부 가이드</a>
    <nav class="breadcrumb">{breadcrumb}</nav>
    <div class="header-actions">
      <div class="search-box-desktop"><span>🔍</span><input type="text" placeholder="검색 (Ctrl+K)" readonly></div>
      <button class="search-btn" type="button" aria-label="검색">🔍</button>
      <button class="theme-btn" type="button" aria-label="다크모드 전환">🌙</button>
    </div>
  </div>
</header>
<div class="sidebar-overlay"></div>
<div class="page-shell">
  <div class="layout">
    <aside class="sidebar">
      <div class="sidebar-title">목차</div>
      {sidebar}
      <a class="sidebar-footer-link" href="{prefix}index.html">← 학습 대시보드로</a>
    </aside>
    <main class="main-content">
      <div class="doc-inner" style="--card-accent: var(--cat-{cat});">
        <span class="page-kicker">{icon} {kicker}</span>
        <h1 class="page-title">{title}</h1>
        {intro}
        {outline}
        {hub_links}
        {body}
        {nav}
      </div>
    </main>
  </div>
</div>
<div class="search-overlay" id="search-overlay">
  <div class="search-panel">
    <input type="text" id="search-input" placeholder="키워드로 검색 (예: JWT, State, git commit)">
    <div class="search-results" id="search-results"></div>
  </div>
</div>
<script src="{prefix}assets/main.js" defer></script>
</body>
</html>
"""


def build_content_page(page):
    md_path = ROOT / page["src"]
    raw = md_path.read_text(encoding="utf-8")
    lines = raw.replace("\r\n", "\n").replace("\r", "\n").split("\n")

    intro_rows, start_idx = extract_intro(lines)
    blocks = parse_blocks(lines, start_idx, len(lines))
    assign_heading_meta(blocks)
    toc = build_toc(blocks)
    blocks = wrap_concept_boxes(blocks)
    body_html = render_blocks(blocks)

    intro_html = render_intro_box(intro_rows) if intro_rows else ""
    outline_html = render_outline_box(toc)
    hub_links_html = render_hub_quicklinks(page)
    sidebar_html = render_sidebar_toc(toc)
    nav_html = render_prev_next(page["key"])
    breadcrumb_html = render_breadcrumb(page)
    prefix = prefix_of(page["key"])

    html_out = PAGE_HTML_TMPL.format(
        title=html.escape(page["title"]),
        prefix=prefix,
        breadcrumb=breadcrumb_html,
        sidebar=sidebar_html,
        cat=page["cat"],
        icon=page["icon"],
        kicker=html.escape(page["kicker"]),
        intro=intro_html,
        outline=outline_html,
        hub_links=hub_links_html,
        body=body_html,
        nav=nav_html,
    )

    out_path = ROOT / (page["src"][:-3] + ".html")
    out_path.write_text(html_out, encoding="utf-8")

    # 검색 인덱스용 항목 수집
    search_entries = []
    for b in blocks_flatten_for_search(blocks):
        pass
    search_entries = collect_search_entries(page, blocks)
    return search_entries, toc


def blocks_flatten_for_search(blocks):
    return blocks


def block_text(b):
    """검색 스니펫용: 블록에서 순수 텍스트만 뽑는다."""
    t = b["type"]
    if t == "para":
        return " ".join(l.strip() for l in b["lines"])
    if t == "list":
        parts = []
        for it in b["items"]:
            for sub in it["blocks"]:
                parts.append(block_text(sub))
        return " ".join(parts)
    if t == "blockquote":
        return " ".join(block_text(sb) for sb in b["blocks"])
    if t == "table":
        return " ".join(" ".join(r) for r in b["rows"])
    if t == "concept_box":
        return " ".join(block_text(sb) for sb in b["inner"])
    return ""


def collect_search_entries(page, blocks):
    entries = []
    url = page["src"][:-3] + ".html"
    current_heading = None
    buffer_text = []

    def flush():
        if current_heading is not None:
            snippet = " ".join(buffer_text).strip()
            snippet = re.sub(r"\s+", " ", snippet)[:140]
            entries.append({
                "p": page["title"],
                "h": current_heading["text"],
                "u": url + "#" + current_heading["id"],
                "s": snippet,
            })

    def walk(blist):
        nonlocal current_heading, buffer_text
        for b in blist:
            if b["type"] == "heading":
                flush()
                current_heading = b
                buffer_text = []
            elif b["type"] == "concept_box":
                walk(b["inner"])
            else:
                txt = block_text(b)
                if txt:
                    buffer_text.append(txt)

    walk(blocks)
    flush()
    if not entries:
        entries.append({"p": page["title"], "h": page["title"], "u": url, "s": page["kicker"]})
    return entries


# ==========================================================================
# 8. 대시보드(index.html)
# ==========================================================================
DASHBOARD_INTRO = (
    "개발 분야별 기초를 따로 외우기보다, 프로젝트 전체 흐름 속에서 "
    "프론트엔드·백엔드·생성형 AI·Git이 어떻게 연결되는지 이해하기 위한 학습 자료입니다. "
    "원본 Markdown 내용을 그대로, 목차·핵심 개념 박스·코드 하이라이트가 있는 학습 화면으로 볼 수 있습니다."
)

OVERVIEW_ROWS = [
    ("team-start", "팀 개발 시작 가이드", "요구사항 확인, MVP 범위, 사용자 흐름, 기술·구조 결정, 구현, 테스트, 배포, 회고까지 전체 순서", "처음 팀 프로젝트를 시작할 때"),
    ("frontend", "프론트엔드 기초 가이드", "HTML·CSS·JavaScript부터 React, API 통신, 상태 관리, 인증, 배포까지 공통 기초", "프론트엔드를 처음 공부할 때"),
    ("backend", "백엔드 기초 가이드", "서버, HTTP/REST, DB, 인증·인가, 보안, 테스트, 운영·배포의 기본 원리", "백엔드를 처음 공부할 때"),
    ("ai", "생성형 AI 기능 개발 기초 가이드", "프롬프트, 구조화 출력, 평가, RAG, Tool Calling, Agent, 보안, 비용·지연시간", "AI 기능을 서비스에 붙이고 싶을 때"),
    ("git", "Git·GitHub 기초 가이드", "저장소, add/commit/push/pull, 브랜치, PR, 충돌, merge/rebase, 인증", "Git을 처음 사용할 때"),
    ("collab-method", "개발 협업 방식 선택 가이드", "브랜치 전략, 리뷰·머지 방식, 실시간 협업, 저장소 구조 비교", "팀 Git 협업 방식을 정할 때"),
    ("github-hub", "GitHub 팀 협업 가이드", "CONTRIBUTING, AGENTS, CLAUDE, PLANNING, Issue·PR 템플릿", "실제 팀 프로젝트를 진행할 때"),
]

DASHBOARD_CARDS = [
    "team-start", "frontend", "backend", "ai", "git", "collab-method", "github-hub",
]

STEP_FLOW = [
    {"title": "팀 개발 시작 가이드", "sub": "무엇을 확인하고 어떤 순서로 개발할지 먼저 파악", "key": "team-start"},
    {"title": "Git · GitHub 기초 가이드", "sub": "버전 관리와 협업의 공통 기초 익히기", "key": "git"},
    {"title": "원하는 개발 분야 선택", "sub": None, "branches": ["frontend", "backend", "ai"]},
    {"title": "개발 협업 방식 선택 가이드", "sub": "팀에 맞는 브랜치·리뷰 방식 정하기", "key": "collab-method"},
    {"title": "GitHub 팀 협업 가이드", "sub": "CONTRIBUTING·AGENTS 등 실전 협업 규칙 적용", "key": "github-hub"},
]


def render_overview_table():
    rows = []
    for key, name, learn, who in OVERVIEW_ROWS:
        url = url_of(key)
        rows.append(
            '<tr><td class="name-cell"><a href="%s">%s</a></td><td>%s</td><td>%s</td></tr>'
            % (url, html.escape(name), html.escape(learn), html.escape(who))
        )
    return (
        '<div class="overview-table-wrap"><table class="overview-table">'
        "<thead><tr><th>학습 자료</th><th>배우는 내용</th><th>추천 대상</th></tr></thead>"
        "<tbody>%s</tbody></table></div>" % "".join(rows)
    )


def render_step_flow():
    parts = ['<div class="step-flow">']
    for i, step in enumerate(STEP_FLOW, start=1):
        if step.get("key"):
            title_html = '<a href="%s">%s</a>' % (url_of(step["key"]), html.escape(step["title"]))
        else:
            title_html = html.escape(step["title"])
        sub_html = '<div class="step-sub">%s</div>' % html.escape(step["sub"]) if step.get("sub") else ""
        parts.append(
            '<div class="step-item"><div class="step-num">%d</div>'
            '<div class="step-body"><div class="step-title">%s</div>%s</div></div>' % (i, title_html, sub_html)
        )
        if step.get("branches"):
            branch_html = "".join(
                '<a class="step-branch" href="%s">%s %s</a>'
                % (url_of(bk), PAGES_BY_KEY[bk]["icon"], html.escape(PAGES_BY_KEY[bk]["title"]))
                for bk in step["branches"]
            )
            parts.append('<div class="step-branches">%s</div>' % branch_html)
        if i < len(STEP_FLOW):
            parts.append('<div class="step-arrow">↓</div>')
    parts.append("</div>")
    return "".join(parts)


def render_card_grid():
    cards = []
    for key in DASHBOARD_CARDS:
        p = PAGES_BY_KEY[key]
        desc = next((learn for k, _, learn, _ in OVERVIEW_ROWS if k == key), "")
        cards.append(
            '<a class="study-card" href="%s" style="--card-accent: var(--cat-%s);">'
            '<span class="study-card-icon">%s</span>'
            '<div class="study-card-title">%s</div>'
            '<div class="study-card-desc">%s</div>'
            '<span class="study-card-tag">%s →</span></a>'
            % (url_of(key), p["cat"], p["icon"], html.escape(p["title"]), html.escape(desc), html.escape(CAT_LABEL.get(p["cat"], "")))
        )
    return '<div class="card-grid">%s</div>' % "".join(cards)


DASHBOARD_TMPL = """<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>개발 공부 가이드 · 개발 학습·실전 노트</title>
<link rel="stylesheet" href="assets/style.css">
<script src="assets/search-index.js" defer></script>
</head>
<body data-root-prefix="">
<div id="reading-progress"></div>
<header class="site-header">
  <div class="header-inner">
    <button class="menu-btn" type="button" aria-label="메뉴" style="visibility:hidden;">☰</button>
    <a class="brand" href="index.html">개발 공부 가이드</a>
    <nav class="breadcrumb"><span class="current">학습 대시보드</span></nav>
    <div class="header-actions">
      <div class="search-box-desktop"><span>🔍</span><input type="text" placeholder="검색 (Ctrl+K)" readonly></div>
      <button class="search-btn" type="button" aria-label="검색">🔍</button>
      <button class="theme-btn" type="button" aria-label="다크모드 전환">🌙</button>
    </div>
  </div>
</header>
<div class="page-shell">
  <div class="dashboard-shell">
    <div class="dashboard-intro">
      <h1 class="dashboard-title">개발 공부 가이드</h1>
      <p class="dashboard-desc">{intro}</p>
    </div>

    <div class="section-heading">학습 자료 한눈에 보기</div>
    {overview_table}

    <div class="section-heading">처음 개발을 시작한다면 — 추천 학습 순서</div>
    {step_flow}

    <div class="section-heading">학습 자료</div>
    {card_grid}
  </div>
</div>
<div class="search-overlay" id="search-overlay">
  <div class="search-panel">
    <input type="text" id="search-input" placeholder="키워드로 검색 (예: JWT, State, git commit)">
    <div class="search-results" id="search-results"></div>
  </div>
</div>
<script src="assets/main.js" defer></script>
</body>
</html>
"""


def build_dashboard():
    html_out = DASHBOARD_TMPL.format(
        intro=html.escape(DASHBOARD_INTRO),
        overview_table=render_overview_table(),
        step_flow=render_step_flow(),
        card_grid=render_card_grid(),
    )
    (ROOT / "index.html").write_text(html_out, encoding="utf-8")


# ==========================================================================
# 9. 실행 진입점
# ==========================================================================
def main():
    all_search_entries = []
    for page in PAGES:
        entries, _toc = build_content_page(page)
        all_search_entries.extend(entries)
        print("생성:", page["src"][:-3] + ".html")

    build_dashboard()
    print("생성: index.html")

    assets_dir = ROOT / "assets"
    assets_dir.mkdir(exist_ok=True)
    search_js = "window.SEARCH_INDEX = " + json.dumps(all_search_entries, ensure_ascii=False) + ";\n"
    (assets_dir / "search-index.js").write_text(search_js, encoding="utf-8")
    print("생성: assets/search-index.js (%d개 항목)" % len(all_search_entries))

    print("\n총 %d개 HTML 생성 완료." % (len(PAGES) + 1))


if __name__ == "__main__":
    main()
