#!/usr/bin/env python3
"""IdeaScientist 的文献工具：用 arXiv 代替原版的 Svalbard Idea Vault。

只用标准库，任何机器上都能直接跑。论文 id 统一用不带版本号的 arXiv id（如 2210.09461），
正文里引用写成 [2210.09461]。

子命令：
  search  "q1" "q2" ... [-k 10] [--sort relevance|date] [--since 2025-01-01] [--cat cs.CV] [--abs]
          对应原版 keyword_search。每条 query 单独检索，结果按 id 去重。
  biblio  <id> [<id> ...]
          对应原版 get_paper_biblio：标题、作者、日期、分类、comment（常写着录用会议）、摘要。
  fulltext <id> [--print] [--max-chars N]
          抓正文（arXiv HTML → ar5iv → PDF），缓存成纯文本，打印缓存路径和带行号的章节目录。
          之后用 sed -n 'a,bp' 或 grep -n 读需要的段落，不要整篇塞进上下文。
  append  <file>
          从 stdin 读内容，加文件锁后追加到 <file> 末尾。多个子 agent 并行写同一个
          gaps.md / papers/<id>.md 时必须用它，否则会互相覆盖。

arXiv API 要求两次请求间隔 3 秒。这里用全局文件锁排队，多个 agent 同时调用也不会被封。
"""

from __future__ import annotations

import argparse
import fcntl
import html
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

CACHE = Path(os.environ.get("LIT_CACHE", Path.home() / ".cache" / "idea-scientist"))
API = "https://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"
UA = "idea-scientist-lit/1.0 (research ideation; polite, rate-limited)"
API_GAP = 3.1  # 秒，arXiv API 的礼貌间隔

ID_RE = re.compile(r"^(\d{4}\.\d{4,5}|[a-z\-]+(\.[A-Z]{2})?/\d{7})(v\d+)?$")


def norm_id(raw: str) -> str:
    s = raw.strip().strip("[]")
    s = re.sub(r"^(https?://)?(www\.)?(arxiv\.org|ar5iv\.labs\.arxiv\.org)/(abs|pdf|html)/", "", s)
    s = re.sub(r"^arxiv:", "", s, flags=re.I).removesuffix(".pdf")
    m = ID_RE.match(s)
    if not m:
        sys.exit(f"不是合法的 arXiv id：{raw}")
    return m.group(1)


# ---------------------------------------------------------------- 网络

def _throttle() -> None:
    """全局排队：所有进程共用一个时间戳文件，保证两次 API 请求至少间隔 API_GAP 秒。"""
    CACHE.mkdir(parents=True, exist_ok=True)
    with open(CACHE / "arxiv_api.lock", "a+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.seek(0)
        try:
            last = float(f.read().strip() or 0)
        except ValueError:
            last = 0.0
        wait = last + API_GAP - time.time()
        if wait > 0:
            time.sleep(wait)
        f.seek(0)
        f.truncate()
        f.write(str(time.time()))


def fetch(url: str, *, api: bool = False, timeout: int = 60, tries: int = 4) -> bytes:
    for attempt in range(tries):
        if api:
            _throttle()
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise
            if attempt == tries - 1:
                raise
            time.sleep(5 * (attempt + 1))  # 429 / 503：退避后重试
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            if attempt == tries - 1:
                raise
            time.sleep(5 * (attempt + 1))
    raise RuntimeError("unreachable")


# ---------------------------------------------------------------- arXiv API

def _parse_feed(xml: bytes) -> list[dict]:
    root = ET.fromstring(xml)
    out = []
    for e in root.findall(f"{ATOM}entry"):
        url = e.findtext(f"{ATOM}id") or ""
        if "/abs/" not in url:
            continue  # API 出错时会返回一条没有 id 的 entry
        pid = norm_id(url.split("/abs/")[1])
        txt = lambda tag: re.sub(r"\s+", " ", e.findtext(tag) or "").strip()
        out.append({
            "id": pid,
            "title": txt(f"{ATOM}title"),
            "published": txt(f"{ATOM}published")[:10],
            "updated": txt(f"{ATOM}updated")[:10],
            "authors": [a.findtext(f"{ATOM}name") for a in e.findall(f"{ATOM}author")],
            "categories": [c.get("term") for c in e.findall(f"{ATOM}category")],
            "comment": txt(f"{ARXIV_NS}comment"),
            "abstract": txt(f"{ATOM}summary"),
        })
    return out


def _to_search_query(q: str, cat: str | None) -> str:
    """把自然的关键词串变成 arXiv 检索式：引号里的短语整体匹配，其余词用 AND 连接。"""
    phrases = re.findall(r'"([^"]+)"', q)
    rest = re.sub(r'"[^"]+"', " ", q)
    words = [w for w in re.findall(r"[\w\-\+]+", rest) if len(w) > 1]
    parts = [f'all:"{p}"' for p in phrases] + [f"all:{w}" for w in words]
    expr = " AND ".join(parts) or "all:*"
    if cat:
        expr = f"({expr}) AND cat:{cat}"
    return expr


def cmd_search(a: argparse.Namespace) -> None:
    seen: dict[str, dict] = {}
    for q in a.queries:
        params = {
            "search_query": _to_search_query(q, a.cat),
            "start": 0,
            "max_results": a.k * (5 if a.since else 1),
            "sortBy": "submittedDate" if a.sort == "date" else "relevance",
            "sortOrder": "descending",
        }
        try:
            hits = _parse_feed(fetch(f"{API}?{urllib.parse.urlencode(params)}", api=True))
        except Exception as e:  # noqa: BLE001 — 单条 query 失败不影响其余
            print(f"## query: {q}\n  (检索失败: {e})\n")
            continue
        if a.since:
            hits = [h for h in hits if h["published"] >= a.since][: a.k]
        print(f"## query: {q}  ({len(hits)} hits)")
        for h in hits:
            mark = "" if h["id"] not in seen else "  (重复)"
            seen.setdefault(h["id"], h)
            venue = f"  [{h['comment'][:80]}]" if h["comment"] else ""
            print(f"- [{h['id']}] {h['published']}  {h['title']}{venue}{mark}")
            if a.abs:
                print(f"    {h['abstract'][:400]}")
        print()


def cmd_biblio(a: argparse.Namespace) -> None:
    ids = [norm_id(i) for i in a.ids]
    params = {"id_list": ",".join(ids), "max_results": len(ids)}
    for h in _parse_feed(fetch(f"{API}?{urllib.parse.urlencode(params)}", api=True)):
        print(f"[{h['id']}] {h['title']}")
        print(f"  published {h['published']} (updated {h['updated']}); "
              f"{', '.join(h['categories'][:4])}")
        print(f"  authors: {', '.join(h['authors'][:8])}{' …' if len(h['authors']) > 8 else ''}")
        if h["comment"]:
            print(f"  comment: {h['comment']}")
        print(f"  abstract: {h['abstract']}\n")


# ---------------------------------------------------------------- 正文

class _HTML2Text(HTMLParser):
    """把 arXiv / ar5iv 的 LaTeXML HTML 转成带章节标题的纯文本。公式用 alttext 里的 TeX 代替。"""

    SKIP = {"script", "style", "nav", "header", "footer", "button", "svg"}
    BLOCK = {"p", "div", "section", "li", "tr", "figcaption", "table", "br", "dd", "dt", "blockquote"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.out: list[str] = []
        self.skip = 0
        self.math = 0
        self.heading: str | None = None

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag in self.SKIP:
            self.skip += 1
            return
        if self.skip:
            return
        if tag == "math":
            self.math += 1
            if self.math == 1:
                tex = d.get("alttext") or ""
                self.out.append(f" ${tex}$ ")
            return
        if re.fullmatch(r"h[1-6]", tag):
            self.heading = tag
            self.out.append("\n\n" + "#" * min(int(tag[1]) + 0, 4) + " ")
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag == "math":
            self.math = max(0, self.math - 1)
            return
        if tag == self.heading:
            self.heading = None
            self.out.append("\n")
        elif tag in self.BLOCK:
            self.out.append("\n")

    def handle_data(self, data):
        if self.skip or self.math:
            return
        self.out.append(data)

    def text(self) -> str:
        t = "".join(self.out)
        t = re.sub(r"[ \t ]+", " ", t)
        t = re.sub(r" *\n *", "\n", t)
        t = re.sub(r"\n{3,}", "\n\n", t)
        return t.strip()


def _from_html(url: str) -> str | None:
    try:
        raw = fetch(url, timeout=90, tries=2).decode("utf-8", "replace")
    except Exception:  # noqa: BLE001
        return None
    m = re.search(r"<article[^>]*>(.*)</article>", raw, flags=re.S)
    body = m.group(1) if m else raw
    p = _HTML2Text()
    p.feed(body)
    t = p.text()
    return t if len(t) > 5000 else None  # 太短说明是"HTML 未生成"之类的占位页


def _from_pdf(pid: str) -> str | None:
    try:
        pdf = fetch(f"https://arxiv.org/pdf/{pid}", timeout=120, tries=2)
    except Exception:  # noqa: BLE001
        return None
    with tempfile.NamedTemporaryFile(suffix=".pdf") as f:
        f.write(pdf)
        f.flush()
        try:
            r = subprocess.run(["pdftotext", "-layout", f.name, "-"], capture_output=True,
                               timeout=120, check=True)
        except (OSError, subprocess.SubprocessError):
            return None
    t = r.stdout.decode("utf-8", "replace")
    return t if len(t) > 5000 else None


def get_fulltext(pid: str) -> tuple[Path, str]:
    path = CACHE / "fulltext" / f"{pid.replace('/', '_')}.txt"
    if path.exists() and path.stat().st_size > 5000:
        return path, "cache"
    for src, getter in (
        ("arxiv-html", lambda: _from_html(f"https://arxiv.org/html/{pid}")),
        ("ar5iv", lambda: _from_html(f"https://ar5iv.labs.arxiv.org/html/{pid}")),
        ("pdf", lambda: _from_pdf(pid)),
    ):
        t = getter()
        if t:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(t)
            return path, src
    sys.exit(f"[{pid}] 拿不到正文（HTML、ar5iv、PDF 都失败）。只能用 biblio 的摘要，不能引用细节。")


def cmd_fulltext(a: argparse.Namespace) -> None:
    pid = norm_id(a.id)
    path, src = get_fulltext(pid)
    text = path.read_text()
    lines = text.splitlines()
    print(f"[{pid}] 正文缓存：{path}  （来源 {src}，{len(lines)} 行，{len(text)} 字符）")
    if a.print:
        print(text[: a.max_chars])
        if len(text) > a.max_chars:
            print(f"\n…（截断，剩余 {len(text) - a.max_chars} 字符；用 sed -n 读后面的行）")
        return
    print("章节目录（行号: 标题）：")
    for i, ln in enumerate(lines, 1):
        if ln.startswith("#"):
            print(f"  {i}: {ln[:110]}")
    if not any(ln.startswith("#") for ln in lines):  # PDF 来源没有标题标记
        for i, ln in enumerate(lines, 1):
            if re.match(r"^\s*(\d+(\.\d+)*\.?|[A-Z]\.)\s+[A-Z][A-Za-z].{2,60}$", ln):
                print(f"  {i}: {ln.strip()[:110]}")
    print(f"\n读法：sed -n '120,220p' {path}   或   grep -n -i 'keyword' {path}")


# ---------------------------------------------------------------- 加锁追加

def cmd_append(a: argparse.Namespace) -> None:
    content = sys.stdin.read()
    if not content.strip():
        sys.exit("stdin 为空，什么都没写。")
    target = Path(a.file)
    target.parent.mkdir(parents=True, exist_ok=True)
    with open(str(target) + ".lock", "a") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        prefix = ""
        if target.exists() and target.stat().st_size:
            prefix = "" if target.read_text().endswith("\n\n") else "\n" if target.read_text().endswith("\n") else "\n\n"
        with open(target, "a") as f:
            f.write(prefix + content.rstrip("\n") + "\n")
    print(f"已追加 {len(content)} 字符到 {target}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search")
    s.add_argument("queries", nargs="+")
    s.add_argument("-k", type=int, default=10)
    s.add_argument("--sort", choices=["relevance", "date"], default="relevance")
    s.add_argument("--since", help="只保留此日期（YYYY-MM-DD）之后发表的")
    s.add_argument("--cat", help="限定 arXiv 分类，如 cs.CV")
    s.add_argument("--abs", action="store_true", help="同时打印摘要前 400 字符")
    s.set_defaults(fn=cmd_search)

    b = sub.add_parser("biblio")
    b.add_argument("ids", nargs="+")
    b.set_defaults(fn=cmd_biblio)

    f = sub.add_parser("fulltext")
    f.add_argument("id")
    f.add_argument("--print", action="store_true")
    f.add_argument("--max-chars", type=int, default=60000)
    f.set_defaults(fn=cmd_fulltext)

    p = sub.add_parser("append")
    p.add_argument("file")
    p.set_defaults(fn=cmd_append)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
