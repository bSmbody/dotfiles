# Paper access and tool mapping (Claude Code)

Every first-tier role (gap_finder, innovator, reviewer, report_writer) reads this file together
with its own role file. The role prompts are upstream text and name upstream tools; this file says
how to carry each one out here. Where the two disagree on mechanics, this file wins; on what to
produce and how to judge, the role file wins.

`$LIT` below means `python3 <skill>/scripts/lit.py`, where `<skill>` is the directory this file
sits in, one level up. `$RUN` is the run directory named in your task.

## Upstream paper-access rule, adapted

You read a paper's body only through the reading procedure below, which plays the role of
`read_paper`. Do NOT guess a paper's mechanism, equations, numbers or limitations from its title or
abstract, and do NOT fabricate. Read only the papers you actually need.

## Tool mapping

| Upstream tool | Do this instead |
|---|---|
| `keyword_search(queries, k)` | `$LIT search "q1" "q2" ... -k 10` (add `--cat cs.CV`, `--abs`, or `--since 2026-01-01` as needed). One query per quoted string; `"exact phrase"` inside a query is matched as a phrase. |
| `get_paper_biblio(id)` | `$LIT biblio <id> [<id> ...]` — title, authors, date, comment (often the venue), abstract. |
| `read_paper(id, goals)` | The reading procedure below. You are your own paper reader. |
| `edit_doc view <file>` | The Read tool on `$RUN/<file>`. |
| `edit_doc insert ... insert_line=999999` (append) | Write the block to a temp file in your scratchpad, then `$LIT append $RUN/<file> < tmpfile`. **Never** use Write or Edit on gaps.md, candidates.md, scores.md or papers/*.md: other sub-agents may be appending to the same file at the same moment, and `append` is the only locked write. |
| `edit_doc create report.json` | The Write tool on `$RUN/report.json` (only the report_writer, and only that file). |

## Reading procedure (= read_paper)

Paper ids are arXiv ids without version, e.g. `2210.09461`. Cite them as `[2210.09461]`.

1. Write down 1–5 concrete reading goals (questions) before you open the paper.
2. If `$RUN/papers/<id>.md` exists, Read it first. Goals already answered there are reused, not
   re-read. If every goal is answered, skip to step 5.
3. `$LIT fulltext <id>` downloads and caches the body and prints a numbered section outline.
   Read only the sections your goals need with `sed -n 'a,bp' <cache path>` or
   `grep -n -i '<term>' <cache path>` — at most ~400 lines per read, never the whole paper.
   Read the body; do not stop at the abstract.
4. Append the digest with `$LIT append $RUN/papers/<id>.md`:
   - If the file did not exist, start the appended block with
     `# <title>`, then `## What this paper does` (one paragraph, ≤120 words),
     then `## Goal-by-goal answers`.
   - Then one block per new goal: `### Goal: <verbatim question>` followed by a focused answer
     (≤300 words) that grounds specifics as `[full text, Section X / Eq Y]`. If the body cannot
     answer it, say so.
5. Use the answers. A paper counts as "read this run" only once `$RUN/papers/<id>.md` exists;
   the deterministic check (`scripts/check_run.py`) rejects any cited id without a digest.

Batch for speed: when several papers are independent, run their `fulltext` downloads in one
Bash call (`for id in A B C; do $LIT fulltext $id; done`), then read and digest them.

## Retrieval scope

- There is no cutoff unless the task names one: search up to today. Work from the last 12
  months counts as prior or concurrent work for novelty, so for every novelty claim also run a
  recency search (`--since` one year back).
- The search backend is arXiv. If a load-bearing paper is not on arXiv (e.g. a CVF-only paper),
  you may use WebSearch to find an arXiv version; a paper with no arXiv version cannot be cited,
  only mentioned by name with "(not on arXiv, not read)".
- Do not use WebFetch to read paper bodies; use `$LIT fulltext`, which handles HTML, ar5iv and PDF.

## Reply

Your final message to the orchestrator is the one-line status your role file asks for — nothing
else. The orchestrator reads your output files, not your reply.
