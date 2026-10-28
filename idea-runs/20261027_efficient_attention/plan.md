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
- turn 2: user allowed the orchestrator to redraw the scope. Re-scoped around one question: memory management for long-generation (long-CoT) inference in standard and hybrid models. Re-prioritized: core L1, L2, L3, new L6; secondary L4; L5 demoted (GDN state is ~1/42 of attention KV at 100K tokens [2610.14754], so state compression is weakly motivated for memory; it finishes its current innovator/review but goes to report/panel only if it survives clearly). Added L6 = Hybrid architectures gap 1 (layer allocation chosen off-policy on teacher-forced text, while long-CoT failure is on the student's own rollouts); now feasible with H200 compute; baselines [2512.20569], [2606.30562], [2605.20936], [2603.26556], Opal [2609.31947]. Spawned innovator C6.
- turn 3: gap_finder on quantization/release timing returned 2 gaps. L2 state -> `drilling`: spawned innovator C2 on that axis's gap 2 (two memories compressed independently, split fixed per request). Correction to the L5 demotion: [2610.36950] reports the GDN state is about three quarters of a stored request at 4K-11K tokens, so state compression does matter at short-to-mid length and for prefix checkpoints; L5 stays secondary rather than demoted.
- turn 4: C5 created (new): recurrent-state units as cache lines with a learned replacement policy imitating the future-aware oracle of [2607.11796], Parrot/Belady-style [2006.16239]. L5 -> `under_review`; spawned reviewer C5.
- turn 5: C4 created (new): exploration block slots sampled outside top-K with known probabilities, importance-weighted sparse-only selector feedback (off-policy top-K correction from recommender systems [1812.02353]); closest prior SAS [2609.13141]. L4 -> `under_review`; spawned reviewer C4.
- turn 6: C1 created (new): k-coverage sleep scheduling from sensor networks [0710.3918] for KV eviction (evict only while each fact keeps a quorum of carrier copies); closest prior CORE [2610.02235]. L1 -> `under_review`; spawned reviewer C1.
- turn 7: C3 created (new): usage record of read key directions, decay/overwrite aimed at least-read directions (LRUA from memory-augmented networks [1605.06065]; optional Belady-style labels [2006.16239]); closest prior CARVE [2606.27229]. L3 -> `under_review`; spawned reviewer C3.
- turn 8: C6 created (new): targeted-observation layer selection from ensemble weather forecasting [2606.27267] plus DAgger re-collection [1011.0686]: score layers by reduction of student-teacher divergence along the hybrid's own rollouts, greedy picks with re-sampling, budget K set by when drift stops compounding. L6 -> `under_review`; spawned reviewer C6.
- turn 9: C5 verdict revise(focus=mapping): oracle is a read mask, irreversible eviction has no backing store, dense writes leave no miss/admission, GDN units coupled, in-scope hybrid payoff weak. L5 -> `drilling`: spawned innovator C7 BUILD_ON C5 (one revise cycle only; secondary lane, drop if not survive).
- turn 10: C1 verdict revise(focus=mapping): CGS assumes surplus coverage, budget cannot keep all units at quorum; coverage should be token-head mass, not copy count; residual failure is once-stated facts. L1 -> `drilling`: spawned innovator C8 BUILD_ON C1.
- turn 11: C3 verdict revise(focus=mapping): LRUA slot unit has no counterpart in a superposed delta-rule state; write half breaks retrieval keys; low initial usage evicts unread needles first; RDN [2106.06295] is a read-feedback prior. L3 -> `drilling`: spawned innovator C9 BUILD_ON C3.
- turn 11: C4 verdict revise(focus=novelty): exact off-support signal cheaply available from a short dense teacher [2606.22874] or dense sampled rows; SAS [2609.13141] blames selector capacity. L4 (secondary) -> `drilling`: spawned innovator C10 BUILD_ON C4 (one revise cycle).
- turn 11: C6 verdict revise(focus=novelty): PostNAS [2508.15884] and DtR [2601.11667] already do outcome-based greedy placement with data-driven K; surrogate mapping unspecified. L6 -> `drilling`: spawned innovator C11 BUILD_ON C6.
