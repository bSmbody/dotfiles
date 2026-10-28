# AC meta-review: C14 v2, "Fewer Full-Attention Layers from the Failures On-Policy Training Leaves Behind"

Ratings: R1 4 (conf 4), R2 4 (conf 3), R3 3 (conf 4). Reviewer p_core: 0.2 / 0.3 / 0.3.

## What the paper would show (every prediction exactly at threshold)
The paper converts Qwen3-4B (thinking) to a GDN hybrid. It first gates on whether allocation still matters after joint OPD: across 5 random allocations the spread is 5 pp, at least twice the seed range. Under default stopping knobs it lands at K_stop in {4,5,6}. The shipped model is non-inferior to a re-run Opal 9/36 at matched GPU-hours (CI lower bound just above -2 pp, so the point estimate is about parity). It beats uniform-at-K and three on-policy allocators by 3 pp each, with CIs just clear of zero, and beats event-localized KL by 2 pp. The predicted non-monotonicity rate is 5%. 32K retrieval may be up to 5 pp worse. The growing KV cache is at least 33% smaller. All of this is on one 60-problem benchmark and one primary model.

## Decisive strengths
- **A real, unclaimed angle.** All three reviewers' searches, including recency searches, found no prior work that picks hybrid full-attention layers from the trained student's own long-CoT failures. I accept this. The overlaps raised do not threaten it:
  - HydraHead [2606.20097] works at head level, off-policy, with NIAH patching only.
  - LOOP [2610.25679] is depth pruning. I checked its record (`lit.py biblio`): it removes one layer per shot with short OPD and reuses recovery trajectories to score layers. It does not do hybrid allocation and does not localize failures.
- **The allocation-matters gate runs first and has a stated kill.** It takes SWARR [2606.11634] seriously and would be a citable finding on its own. All three reviewers value it.
- **Comparison discipline is better than usual for this sub-area:**
  - the headline is measured on the shipped, jointly trained model;
  - every method gets matched total GPU-hours, with the allocation run charged to the method;
  - the strong baselines are on-policy versions of the competitors (OPD-trained gates with an exact-K Lagrangian, DtR-style greedy dev accuracy, greedy on-policy KL);
  - the kill conditions are honest, including "uniform at the same K is already non-inferior".

## Decisive weaknesses
1. **The significance of the memory claim is unanchored (all three reviewers; I accept it, and it is the decisive issue).** The deliverable is one third less growing KV on 9 layers. Existing methods already cut those same layers' cache by 2-10x with little reasoning loss: FP8/INT4 KV [2505.18610], long-CoT eviction [2505.24133][2506.05345], and hybrid-specific KV compression [2610.14754][2609.02029]. The proposal never puts Opal 9/36 plus compression at K=6's byte budget and never shows the two compose. "They are orthogonal" is the obvious answer, but proposed_evaluation does not test it, so under the conditioning it stays unanswered. Throughput gains will also be below 33%, because weights and GDN state do not shrink. Answerable, but not answered.
2. **Every pillar is marginal at threshold, and the statistics are not set up to carry marginal effects (R1, R2, R3; I accept).**
   - Parity with a -2 pp lower bound, 3 pp superiority claims on 60 AIME problems, and no multiplicity control across at least six pairwise claims.
   - The primary CI pools seeds into problem means, which leaves out pipeline-seed variance. The hierarchical bootstrap should be primary.
   - R3's point about the gate is correct. Under the null, the ratio of a 5-draw range to a 3-draw range is about 1.4 in expectation and has high variance, so the "at least 2x" condition passes by chance fairly often. With 5 single-seed random draws, the paper cannot say where its allocation falls in the random distribution, and the 3 pp gain is smaller than the 5 pp random spread.
3. **"K from data" does not hold at threshold (R1, R3; I accept).** The stability prediction allows K_stop to move by plus or minus 2 layers across knobs and seeds, with Jaccard 0.6. With a default of 6, some settings give 7 or 8, so "K <= 6" holds only at the default knobs. The defensible claim is the smaller "a better allocation at a hand-chosen K".
4. **The name-giving machinery is barely separated from the simpler idea (R2; I accept).** The predicted margin over event-localized KL is 2 pp, and the non-monotonicity rate is 5%. At threshold, the paper's real message is "on-policy failure positions pick better layers". The title, ddmin and verified coverage overclaim that. LOOP's ablation, where iteration carries about 7 pp and the score about 2 pp, adds to this. A "same rounds, random or LOOP-style commit order" control is missing.
5. **Narrow scope for a memory paper (R1, R2, R3; I accept, as major-minus).** One primary model with 3 seeds and MiMo with 1 seed, math only, 32K generation, and AIME'24/'25 (possibly contaminated) as the only load-bearing metric. Up to 5 pp of 32K retrieval loss at threshold will be read against the memory claim.

## Claims I accept with qualification, or downgrade
- **Search regime differs from shipping regime (R1, R2).** Valid as an explanatory gap. Because headline claims sit on the shipped model, it does not undermine validity at threshold. I downgrade it to minor. Reporting the Spearman correlation between frozen and shipped accuracy over the gate's random allocations would cover it.
- **K\* chosen from AIME spread and then tested on AIME (R3).** Real, but mild and fixable in one line by choosing K\* on the dev pool. I count it under weakness 2.
- **The Opal reproduction needs a tolerance, and uniform-at-K needs Opal's dedicated recipe (R2, R3).** Correct and answerable. Without both, "non-inferior to Opal" and "beats uniform" could reflect a weak reproduction or a weaker supernet route to uniform. I fold it into the fixes. It is not decisive by itself.
- **Diagnosis cost may exceed the shipping stage (R2, R3).** Plausible, since the 8-vs-8 continuations on prefixes up to 32K are expensive. The odds are conditioned on the plan running as written, so this matters for feasibility and adoption more than for acceptance. Kept as minor.
- **"Mechanism is standard activation patching plus set cover" (R1, R2).** Partly rejected. The tools are standard, but applying them on-policy to hybrid allocation, after first testing whether allocation matters at all, is new as far as all three searches show. The problem is the framing, not the novelty.
- **R1: going below 1:3 is not new in itself** (Jet-Nemotron, KL-guided, FlashMorph). Accepted as a framing correction. The new part is long-CoT after OPD.
- **R2: building on a one-month-old preprint is fragile.** Minor, and it applies to any follow-up work.

## Calibration
The ratings are 4/4/3, with several well-argued major weaknesses that could be answered but that the proposal as written does not answer. No weakness is fatal. The most important one, significance against KV compression at matched bytes, is shared by all three reviewers, and none of them would move above borderline without it. At threshold every result is marginal and nothing is decisive. That places the paper in the 3-4 band at its lower end: **odds 3.2**.

p_core is the load-bearing headline: the shipped K <= 6 model is non-inferior to Opal 9/36 and beats uniform at the same K by at least 3 pp. That needs the gate to pass (about 0.5) and a narrow window in which uniform-6 falls clearly short of Opal while the selected 6 does not. I put it at **0.25**, between R1's estimate, which also includes beating all three baselines, and the 0.3 from R2 and R3. If the core fails, the rewrite is an analysis paper ("allocation does or does not matter after OPD", or "Opal's ratio is overprovisioned"), and new analyses are out of scope as a main contribution. I put that at about 1.0. Risk-adjusted: 3.2 x 0.25 + 0.75 x 1.0 = 1.55, so **1.6**.

```json
{"odds": 3.2, "p_core": 0.25, "odds_risk_adjusted": 1.6,
 "decisive_weaknesses": [
  "No matched-growing-KV-bytes comparison or composition: Opal 9/36 with FP8/INT4 KV or long-CoT/hybrid eviction [2505.18610][2505.24133][2506.05345][2610.14754] at K=6's byte budget, so a one-third cut of 9 layers' cache is not shown to beat or add to near-free compression; throughput gain is below 33%",
  "At threshold every claim is marginal (parity with -2 pp lower bound, +3 pp on 60 AIME problems, CIs just above 0); the primary CI leaves out seed variance, there is no multiplicity control, the 5-vs-3-draw range-ratio gate passes by chance fairly often, K* is chosen on the test set, and the method's position in the random-allocation distribution is never established",
  "'K from data' does not hold at threshold: K_stop moves by 2 layers across knobs and seeds (Jaccard 0.6), so K <= 6 holds only at default settings",
  "The repair-set machinery is only 2 pp ahead of event-localized KL with 5% non-monotonicity, and there is no rounds-only control (LOOP [2610.25679] suggests iteration carries most of the gain), so the title and ddmin/verified-coverage framing overclaim relative to 'on-policy failure positions pick better layers'",
  "Narrow scope for a memory claim: one primary model, math-only allocation and evaluation, 32K generation, possibly contaminated AIME'24/'25 as the only load-bearing metric, and up to 5 pp loss on 32K retrieval"
 ],
 "fixes_ranked": [
  "Make the headline an accuracy-versus-growing-KV-bytes Pareto: Opal 9/36 + FP8/INT4 KV + one long-CoT or hybrid eviction method at the bytes of K=4 and K=6, and ours at K_stop + the same compressor, showing K-reduction beats or composes with compression",
  "Rebuild the statistics: 10-20 random allocations at K* (2 seeds for some) with ours reported as a percentile; hierarchical seed bootstrap as the primary CI with Holm correction; K* chosen on the dev pool; add AIME 2026/HMMT to enlarge and decontaminate the evaluation; include a power analysis for 3 pp",
  "Add a rounds-only control (same diagnose-free rounds with random or LOOP-style commit order) and heuristic layouts (contiguous middle block, skip first/last); discuss LOOP; reframe the title and story around on-policy failure localization, moving ddmin and monotonicity to the appendix unless they change the chosen layers",
  "Train uniform at K* and K_stop through Opal's dedicated recipe at matched GPU-hours, and require the Opal 9/36 reproduction to come within a stated tolerance of the published 52.5/40.4 before the non-inferiority margin counts",
  "Commit to a fixed-K headline (K=6), or predict K_stop <= 6 across the whole knob grid; report frozen-vs-shipped Spearman over the gate allocations",
  "Broaden: MiMo-7B or Qwen3-8B at 3 seeds, one out-of-domain long-thinking task (LiveCodeBench), generation beyond 32K, and a head-level allocation comparison (ConSA head-wise / HydraHead-style) at matched KV bytes; tighten the retrieval bound",
  "Pilot-measure event-mining and diagnosis GPU-hours per round and report the diagnosis share of the matched budget; cut the 8-vs-8 filter cost if it exceeds the shipping stage"
 ]}
```
