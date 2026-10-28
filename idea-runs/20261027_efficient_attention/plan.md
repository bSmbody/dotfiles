# Plan — efficient attention landscape (2026-10-27)

Goal of this run (user request): the user's senior labmate suggested a direction: standard attention pruning, variant attention pruning, hybrid attention architectures, memory matrices, and algorithms for variant attention. Map the current work and open problems so the user understands the area. Stop after MAP THE LANDSCAPE.

## Axes
1. KV cache and token pruning for standard softmax attention
2. Pruning and compression of variant attention mechanisms
3. Hybrid architectures mixing full attention with linear or recurrent layers
4. Memory matrix update rules in linear attention and fast-weight models
5. Hardware-efficient training and inference algorithms for linear and sparse attention

## Active direction
state: `forming`

## History
- `forming` at turn 1: wrote problem.md; spawning gap_finder on axes 1–5 in parallel (independent axes).
- `forming`: gap_finder axis 5 (hardware-efficient algorithms) returned, 2 gaps.
- `forming`: gap_finder axis 3 (hybrid architectures) returned, 2 gaps.
- `forming`: gap_finder axis 4 (memory matrix update rules) returned, 2 gaps.
- `forming`: gap_finder axis 2 (variant attention pruning) returned, 2 gaps.
- `forming`: gap_finder axis 1 (KV cache pruning) returned, 2 gaps. All 5 axes mapped (10 gaps); check_run passes. Wrote SURVEY_zh.md; ideation waits for the user to pick a direction.
- constraints updated: compute is now ~1 TB H200 (user, 2026-10-27).

## Round 2 — ideation (2026-10-28, user request)
User: run IdeaScientist on the directions discussed, find clear baselines, propose ideas with strong novelty, state the scope clearly. Compute is no longer binding (~1 TB H200). Scope and venue written into problem.md Constraints.

Lanes (one per item the senior labmate named; each lane runs innovator -> reviewer -> revise/commit -> report_writer -> panel, depth-first; lanes run in parallel):
| Lane | Senior's item | Gap (axis + gap) | Why the baselines are clear |
|---|---|---|---|
| L1 | standard attention pruning | KV cache and token pruning for standard softmax attention — gap 1: per-token additive ranking vs set-level coverage | H2O / SnapKV / R-KV / KVP / ForesightKV, plus the uniform-random null baseline and planted-fact probes of [2609.03430] |
| L2 | hybrid architecture + KV quantization / release timing | Hybrid architectures — gap 2 (attention-KV eviction ignores GDN state), possibly combined with a new axis on quantization/release timing (gap_finder pending) | GateSight, HeadWiseKV, SnapKV on public GDN hybrids; DAMP / lifetime-aware state quantization |
| L3 | memory matrix | Memory matrix update rules — gap 1: retention set at write time, not by read demand | GDN, GDN-2, EDA, KDN, VLA in flash-linear-attention; MQAR / RULER MK-NIAH |
| L4 | variant attention algorithms | Hardware-efficient algorithms — gap 2: sparse selector trained only on its own support | NSA, MSA, DashAttention, random-router control of [2603.02227] |
| L5 | variant attention pruning | Pruning and compression of variant attention — gap 1: static offline state mask vs content migration | DRRQR, JRNP, DASC, DAMP; same-window oracle of [2607.11796] |

Ids: L1 -> C1, L2 -> C2, L3 -> C3, L4 -> C4, L5 -> C5; revisions get the next free id.

## Active directions
- L1: `drilling` (C1)
- L2: `forming` (waiting for gap_finder on quantization/release timing)
- L3: `drilling` (C3)
- L4: `drilling` (C4)
- L5: `drilling` (C5)

## History (round 2)
- turn 1: constraints updated (venue, scope, team). Spawned gap_finder on "Quantization and release timing of KV cache and recurrent state in hybrid models"; spawned innovator C1, C3, C4, C5 in parallel (independent lanes).
