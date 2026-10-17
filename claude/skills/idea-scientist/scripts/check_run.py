#!/usr/bin/env python3
"""IdeaScientist 运行目录的确定性检查，对应原版 reward 里的 validity checks。

用法：python3 check_run.py <run_dir> [--quiet]

检查项：
  - gaps.md：每个 '## Axis:' 段有两个小节；每条 gap 五个字段齐全；每个轴最多 2 条 gap。
  - candidates.md：每个 '### C<n> —' 段的必填字段齐全。
  - scores.md：每个 '### C<n> verdict' 段有合法 verdict。
  - report.json：是一个合法 JSON 对象，schema 的顶层字段全部存在且非空，没有 TODO。
  - 引用：上面四个文件里引用的每个 [arXiv id] 都必须有 papers/<id>.md 摘要，
    也就是这次运行里真的读过。方括号里只有全部是 id 时才算引用，
    所以 "[full text, Section 3]" 这类定位标注不会被误判。
有问题时退出码为 1。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
ID = r"(?:\d{4}\.\d{4,5}|[a-z\-]+(?:\.[A-Z]{2})?/\d{7})"
BRACKET = re.compile(r"\[([^\[\]]{1,200})\]")
ID_FULL = re.compile(rf"^{ID}(?:v\d+)?$")

GAP_FIELDS = ["**Gap:**", "**Near-miss methods and coverage:**", "**Methodological deficiency:**",
              "**Why it matters:**", "**Evidence route:**"]
CAND_FIELDS = ["**Intuition**", "**Gap it attacks**", "**Source inspiration**",
               "**How it maps to this problem**", "**Why it could work / feasibility**",
               "**Novelty vs. closest in-domain work**", "**Main risk**"]
VERDICT = re.compile(r"\*\*Verdict\*\*\s*:?\s*`?(survive|revise\(focus=\w+\)|reject\(reason=[^)]*\))`?")


def citations(text: str) -> set[str]:
    out: set[str] = set()
    for inner in BRACKET.findall(text):
        toks = [t.strip() for t in re.split(r"[,;]", inner) if t.strip()]
        if toks and all(ID_FULL.match(t) for t in toks):
            out.update(re.sub(r"v\d+$", "", t) for t in toks)
    return out


def sections(text: str, header: str) -> list[tuple[str, str]]:
    parts = re.split(rf"(?m)^({re.escape(header)}.*)$", text)
    return [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts) - 1, 2)]


def check_gaps(text: str, issues: list[str]) -> None:
    for head, body in sections(text, "## Axis:"):
        if "### What has been done" not in body:
            issues.append(f"gaps.md {head}：缺 '### What has been done'")
        if "### Open gaps on this axis" not in body:
            issues.append(f"gaps.md {head}：缺 '### Open gaps on this axis'")
            continue
        gaps_part = body.split("### Open gaps on this axis", 1)[1]
        blocks = [b for b in re.split(r"(?m)^\s*- \*\*Gap:\*\*", gaps_part)[1:]]
        if len(blocks) > 2:
            issues.append(f"gaps.md {head}：{len(blocks)} 条 gap，超过上限 2")
        for i, b in enumerate(blocks, 1):
            b = "- **Gap:**" + b
            miss = [f for f in GAP_FIELDS if f not in b]
            if miss:
                issues.append(f"gaps.md {head} gap#{i}：缺字段 {miss}")


def check_candidates(text: str, issues: list[str]) -> None:
    for head, body in sections(text, "### C"):
        if not re.match(r"### C\d+\s+[—-]", head):
            continue
        miss = [f for f in CAND_FIELDS if f not in body]
        if miss:
            issues.append(f"candidates.md {head[:40]}：缺字段 {miss}")


def check_scores(text: str, issues: list[str]) -> None:
    for head, body in sections(text, "### C"):
        if "verdict" in head and not VERDICT.search(body):
            issues.append(f"scores.md {head}：没有合法的 **Verdict**")


def _empty(v) -> bool:
    return v in (None, "", [], {}) or (isinstance(v, str) and not v.strip())


def check_report(path: Path, issues: list[str]) -> str:
    raw = path.read_text()
    try:
        rep = json.loads(raw)
    except json.JSONDecodeError as e:
        issues.append(f"{path.name}：不是合法 JSON（{e}）")
        return raw
    if not isinstance(rep, dict):
        issues.append(f"{path.name}：顶层不是 JSON 对象")
        return raw
    schema = json.loads((SKILL / "report_schema.json").read_text())
    for k in schema:
        if k not in rep:
            issues.append(f"{path.name}：缺顶层字段 {k}")
        elif _empty(rep[k]):
            issues.append(f"{path.name}：字段 {k} 为空")
    if re.search(r"\bTODO\b|\bTBD\b", raw):
        issues.append(f"{path.name}：含 TODO/TBD 占位")
    return raw


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    run = Path(sys.argv[1])
    quiet = "--quiet" in sys.argv
    issues: list[str] = []
    cited: dict[str, set[str]] = {}

    for name, checker in (("gaps.md", check_gaps), ("candidates.md", check_candidates),
                          ("scores.md", check_scores)):
        p = run / name
        if p.exists():
            t = p.read_text()
            checker(t, issues)
            cited[name] = citations(t)
    for p in sorted(run.glob("report*.json")):
        cited[p.name] = citations(check_report(p, issues))

    digests = {re.sub(r"^(.+?)\.md$", r"\1", f.name).replace("_", "/") for f in (run / "papers").glob("*.md")} \
        if (run / "papers").exists() else set()
    for name, ids in cited.items():
        missing = sorted(i for i in ids if i not in digests)
        if missing:
            issues.append(f"{name}：引用了没有 papers/<id>.md 摘要的论文 {missing}")

    if not quiet:
        for name, ids in cited.items():
            print(f"{name}: 引用 {len(ids)} 篇")
        print(f"papers/: {len(digests)} 篇摘要")
    if issues:
        print("问题：")
        for i in issues:
            print(f"  - {i}")
        return 1
    print("全部检查通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
