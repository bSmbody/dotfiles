# AC meta-review: C14 v3, "Keep the Attention Layers That Fix the Student's Own Mistakes"

Ratings: R1 4/conf 4, R2 3/conf 4, R3 3/conf 4. All three reviewers give p_core = 0.3.

## Decisive strengths
- **The question is the right one, and it is asked in the right units.** The paper puts the number of hybrid full-attention layers on the same growing-KV-bytes axis as FP8, INT4 and eviction. It also admits up front that FP8 on Opal 9/36 (4.5 L-eq) is already smaller than six bf16 layers. All three reviewers credit this framing, and none of the off-policy layer selectors they cite makes the comparison.
- **The specific signal looks novel.** Each reviewer ran separate recency searches. None found a paper that allocates a hybrid's full-attention layers from failure positions on the student's own long-CoT rollouts. The delta over KL-guided selection [2512.20569] (same restore-and-measure primitive, off-policy) and over LOOP [2610.25679] (same loop, depth pruning, aggregate scores) is narrow but real.
- **The experimental design is clearly above the norm for this subarea.** It uses:
  - a fresh 190-problem test pool, with AIME'24 kept for reproduction only;
  - avg@32 with 5 pipeline seeds, a hierarchical bootstrap and Holm correction;
  - an honest MDE of about 5 pp;
  - Opal-recipe baselines at matched GPU-hours, with a reproduction tolerance;
  - dev-only choice of B-dagger and of the compressor knobs;
  - G0/G1 kill gates aimed at the SWARR routing-around risk [2606.11634].

## Decisive weaknesses
1. **At threshold, the confirmed claims are the unsurprising ones, and the claim in the title is not confirmed.** All three reviewers raise this independently, and I agree. The Holm family is ours vs uniform-6, ours vs random commit order, and C2 vs Opal. The baselines that actually test "localize to failure positions" are left as 3-seed point estimates at ≥3 pp, below the 5 pp MDE and inside about one SE. Those baselines are greedy whole-trace on-policy KL, the LOOP score, DtR-style dev accuracy and the teacher-forced selectors. A NeurIPS reviewer who knows the 10+ hybrid-selector papers of the past year will read the result as "a greedy on-policy loop beats uniform and chance", which DtR, LightTransfer and Super Apriel already lead one to expect.
2. **The method may only tie cheap random search.** This is R2 W2 and R3 W2, and I accept it. The 90th percentile of 16 random layouts means one or two random layouts tie or beat ours-6. G1 already trains those 16 allocations, so best-of-G1 chosen on dev costs almost nothing extra. The event miner costs up to 1.5 shipping runs, and the paper makes no stated prediction against best-of-16. At threshold the practitioner takeaway is "run G1 and pick the best".
3. **C2, the stated headline, is narrow and confounded.** Three problems:
   - It is won at one budget of about 1 or 0.5 L-eq, chosen because Opal has already collapsed there. At the budgets practitioners use, it allows ours-6 to trail Opal by up to 3 pp.
   - It mixes "six layers" with "OFL's six layers", because uniform-6 plus a compressor is not in the confirmatory family (R2, R3).
   - It omits the direct continuous counterpart, training-free layer-adaptive compression of Opal 9/36 (R1 W1). That means ReasonAlloc per-layer and per-head decode budgets, KVTuner per-layer precision, or DuoAttention/LightTransfer-style sink+window on 3 of the 9 layers.

   I checked ReasonAlloc [2606.11164] with lit.py. It is a training-free, decode-time, per-layer budget allocator for long-CoT reasoning models, it beats uniform R-KV most at small budgets, and the proposal does not cite it. Setting three of Opal's layers to sink+window gives near-zero growing bytes at no training cost. If that matches ours-6 at B-dagger, the memory contribution disappears.
4. **There is an overlap the proposal does not address.** I checked LightTransfer [2410.13846] (TMLR 2025) with lit.py, and R1 and R2 are right. It turns a Transformer into a layer-level hybrid by replacing data-selected "lazy" layers with streaming attention. It reports o1-style AIME24 retention on QwQ-STILL with half the layers converted, and it shows that layer removal stacks with SnapKV. The report never cites it. It does not pre-empt the on-policy signal or the matched-bytes frontier. It does weaken both "data-driven layouts beat rule-based ones on long CoT" and the framing that "nobody has shown that cutting layers saves anything compression does not". As written, that framing is overstated.
5. **The byte metric can flatter one arm (R1 W4, R3 W4; I accept this).** Bytes per generated token, with eviction caps tuned at 16K and tested at 32K, is not matched at the realized trace length. Compressed or weaker arms tend to produce longer traces. C2 needs to be measured as peak or length-integrated KV per problem, with per-arm length distributions.

## Reviewer claims accepted or rejected
- **Accepted: localization not confirmatory (R1 W2, R2 W1, R3 W1).** This is the central problem.
- **Accepted: best-of-random (R2 W2, R3 W2).**
- **Accepted: C2 confound and missing uniform-6 frontier (R2 W3, R3 W3).**
- **Accepted, with the overlap verified: missing layer-adaptive compressors (R1 W1) and the uncited LightTransfer.**
- **Accepted, mostly: learned eviction on Opal 9/36 with the surplus GPU-hours (R1 W3).** DMS is cited but deferred. The matched-GPU-hours design makes it the natural use of the surplus, so I treat it as major but secondary to W1–W3.
- **Accepted: ours-9 vs Opal 9/36 (R1 W5).** This is the cleanest allocation-only test, and the paper drops it.
- **Partly accepted: R3 W5, that the breadth results read as mildly negative at threshold.** The LiveCodeBench margin of −2 pp, the 64K widening of 3 pp, the RULER margin of −3 pp and the non-significant MiMo result add up to a reasoning-only, math-tuned picture. I treat this as lowering enthusiasm, not as a separate major flaw.
- **Partly accepted: R3 W6, compute fit.** The constraints say compute is not binding (8×H200), so GPU count is not the issue. About 90 shipping runs plus the full compressor × budget sweep in 4–6 months is still tight for one student. The pre-stated cut order drops exactly the comparisons a skeptic wants (teacher-forced and head-level). This is a risk to execution, not a reason to reject the design.
- **Rejected as a separate weakness: R2 W4, "two stories, too many modules".** The complexity is real, but it follows from W1–W3. If localization and C2 were confirmed against strong alternatives, a three-part title would be acceptable.
- **Minor and accepted as stated:** weak proxy links (R1 W6, R2 W5, R3 W8; Spearman 0.5 frozen-to-shipped and 0.3 KL-to-answer), 1-seed ablations (R3 W7), and computed rather than measured memory (R1 W8, R3 W9).

## Calibration
The ratings are 4/3/3. Each weakness is major and answerable, and no reviewer raises a fatal flaw, so the starting band is 3–4. Two things push the paper toward the bottom of that band and slightly below it:
- All three reviewers independently find the same gap: the title claim is not confirmatory at threshold, and the method may only tie best-of-random.
- There are verified but unaddressed overlaps on both pillars: LightTransfer for layer-level conversion with stacking, and ReasonAlloc/KVTuner/DuoAttention for layer-adaptive compression.

These overlaps are partial, not pre-emptive, so I do not drop to the 1–2 anchor for strong overlap. Even with every prediction exactly at threshold, the paper shows:
- a 5 pp win over uniform;
- non-inferiority to Opal;
- one extreme-budget memory win, confounded with layer count and missing the strongest compressors.

That is a borderline-reject profile in a crowded subarea.

`p_core` concerns C1 together with G1: OFL-6 beats uniform-6 by a significant 5 pp after matched on-policy training. Every other claim depends on it. SWARR [2606.11634] and the convergence result [2606.15378] make routing-around likely, so I agree with the panel's 0.3. If it fails, the paper becomes a negative or analysis result, which problem.md puts out of scope as a main contribution; I give that version about 0.5.

odds_risk_adjusted ≈ 2.7 × 0.3 + 0.7 × 0.5 ≈ 1.2.

```json
{"odds": 2.7, "p_core": 0.3, "odds_risk_adjusted": 1.2,
 "decisive_weaknesses": [
  "The title claim (localizing to on-policy failure positions beats aggregate on-policy or teacher-forced signals) is not confirmatory: greedy whole-trace on-policy KL, LOOP score, DtR and KL-guided are 3-seed point estimates at >=3 pp, below the 5 pp MDE; the Holm family has only uniform-6, random commit order and Opal",
  "At threshold, ours-6 sits at the 90th percentile of the 16 G1 random allocations the pipeline already trains; there is no confirmatory test against best-of-N random at matched allocation compute, so 'ours is about best random' is the likely reading",
  "C2 is won at one extreme, dev-chosen budget (about 1 or 0.5 L-eq), allows trailing Opal by 3 pp elsewhere, does not separate K-reduction from OFL (uniform-6 plus compressor is outside the family), and omits training-free layer-adaptive compression of Opal 9/36 (ReasonAlloc [2606.11164], KVTuner [2502.04420], DuoAttention/LightTransfer-style sink+window on 3 of 9 layers) and learned eviction (DMS) using the surplus GPU-hours",
  "LightTransfer [2410.13846] (layer-level dense-to-streaming hybrid conversion on o1-style long CoT, data-selected layers beat fixed layouts, layer removal stacks with SnapKV) is uncited, and the 'nobody has shown' framing is overstated",
  "Bytes per generated token, with eviction knobs tuned at 16K and tested at 32K, is not matched at the realized trace length; C2 can favour whichever arm generates longer traces"
 ],
 "fixes_ranked": [
  "Rebuild the confirmatory Holm family around the strong alternatives at 5 seeds: greedy whole-trace on-policy KL with the same rounds, and best-of-N random (N set by the measured OFL cost) chosen on dev. Drop uniform-6 from the family if power requires; state a predicted margin for each",
  "Split C2 into a K-reduction part (uniform-6 plus best compressor vs Opal-9 plus best compressor) and an OFL part (ours-6 vs uniform-6 at B-dagger), and add training-free layer-adaptive compressors of Opal 9/36 (ReasonAlloc per-layer and per-head budgets, KVTuner per-layer precision, 3-of-9 sink+window chosen by DuoAttention gates or OFL's own coverage score) to the frontier and to the test",
  "Measure memory as peak or length-integrated KV bytes per problem at the realized length, report per-arm length and loop rates, tune knobs at the 32K test length, and claim the win at a practitioner budget (2 to 4.5 L-eq) rather than only at B-dagger",
  "Add ours-9 vs Opal 9/36 at 5 seeds as the clean allocation-only test, which also gives a direct 'better Opal' result",
  "Cite and position against LightTransfer [2410.13846], ReasonAlloc [2606.11164], KVTuner [2502.04420], DuoAttention [2410.10819] and MultiAlloc [2610.18642], restate the novelty as on-policy failure localization plus a matched-bytes test, and run a LightTransfer lazy-ratio selector on student rollouts as a baseline",
  "Add DMS-style learned eviction on Opal 9/36 trained with the matched surplus GPU-hours as a C2 competitor",
  "Cut the breadth scope (head-level, 64K, RULER) to protect the 5-seed strong-baseline comparisons within the 4 to 6 month budget, and make mixed math-and-code event mining a planned arm"
 ]}
```
