# AC meta-review: C3 "Unwrapping the Dial" (CVPR 2027 main track)

Inputs read: report.json, the Constraints section of problem.md, and reviews R1 (area expert, 3/conf 4, p_core 0.30), R2 (generalist, 3/conf 3, p_core 0.30) and R3 (experimentalist, 4/conf 4, p_core 0.25). I used `lit.py biblio` only to settle disputed overlap claims: 2111.09162, 2604.22829 and 2609.04014.

Conditioning, as the protocol requires: the experiments run as written within budget, and every falsifiable prediction lands exactly at its threshold. That means +15 points value+unit over the best Astra configuration on 511 held-out MeasureBench real dials at no more than 1.2x default cost, +20 exact-minute on 1,000 TickTockVQA clocks, +8 over hybrid B, margin AUROC 0.80, and 75% selective accuracy at 50% coverage.

## Decisive strengths
- **The problem is real and timely.** Frontier VLMs read the unit (96.2%) but not the value (31.5%) on real dials, extra thinking does not help, and 2026 models still fail. All three reviewers accept this, and a CVPR audience will recognise it immediately.
- **The headline would be a decisive cost/performance change.** If it holds, it is a gain of +15 points over the best frontier configuration, xhigh effort with built-in Python/crop tools included, at about 1x default cost, with no training. This is the kind of result the venue's significance bar asks for, not a thin delta.
- **The evaluation design is unusually disciplined.** It has pre-registered gates with kill conditions, paired-bootstrap sizing, accuracy at 100% coverage with fallback, oracle splits (ground-truth needle and ground-truth labelling), measured cost, and the frontier's strongest own-tools baseline. All three reviewers credit this, and so do I. A paper with this design is hard to dismiss as cherry-picked.
- **The reliability signal is independent of the frontier.** Abstention uses a labelling margin built from local evidence and is tested on items where Astra's self-agreement is confidently wrong. This is a clean, testable claim that addresses a known weakness of VLM self-verification.

## Decisive weaknesses
1. **The insight is anticipated, and what remains is an assembly.** All three reviewers make this point. I checked [2604.22829] ("Lost in Motion", IEEE I&M Magazine 2026). It is a frontier-VLM gauge evaluation, and per both the proposal and the reviewers it recommends exactly the split of VLM for semantics and deterministic geometry for the needle. Each part of the pipeline also has a close ancestor:
   - polar unwrap and local interpolation: MeterFL;
   - numeral anchoring: Reitsma;
   - joint 720-state clock space: It's About Time;
   - frozen-DINOv2 render-and-compare: FoundPose.

   The authors' own limitations section concedes that the phase-unwrapping framing "mostly re-describes ordinary tick counting". The novelty that survives is a ±1-neighbourhood MAP search with a frontier-independent margin, plus a 2D silhouette sweep. The paper will therefore be judged almost entirely on its numbers. Using three analogies (structured light, phase unwrapping, render-and-compare) hurts rather than helps.
2. **There is no held-out benchmark, although generalisation is the paper's main selling point.** All three reviewers raise this, and R1 and R3 make it their one-point fix. Five weights and two thresholds are tuned on 200 MeasureBench dials and tested on 511 from the same collection. The argument against TriSCA, DialBench and Swap-DPO is that "training-free cannot overfit designs", and that is asserted, not shown. Candidate second test sets exist:
   - InSituMeasure analog categories (confirmed: 2,922 real industrial scenes, answerability labels; release status unknown);
   - MeterFL real test readings;
   - DialBench/RPM-10K test.
3. **The needle baselines are weak, and the DINOv2 sweep is suspect at patch scale.** All three reviewers raise this. Hybrid B uses a Hough needle. The sweep is not compared with:
   - a SAM-family mask prompted at the hub plus an axis fit;
   - a radial darkness or edge-energy profile;
   - a pixel-space version of paste-and-compare.

   A needle 2–4 px wide on a 32x32 grid of 14 px patches puts the precision in the loosely specified native-resolution tip refinement, not in DINOv2. Beating Hough by 8 points does not establish the third named contribution.
4. **The headline gain is relative to a baseline that has never been measured, and it is a mix of C3 answers and fallback answers.** R3 and R2 raise this, and I agree. The gain is Δ = coverage × (C3 selective accuracy − Astra accuracy on the covered items). At the thresholds, coverage is 50% at 75% selective accuracy, so +15 needs Astra-best at or below about 45% on the covered half. That half is probably the easy, crisp, well-ticked dials, where Astra is also stronger. The proposal commits to no absolute floor and no decomposition. This is the weakness a rebuttal would have to rescue.
5. **The scope is narrow.** R2 raises this, R1 notes it as minor, and I treat it as major for the main track. Every component is specific to dials. MeasureBench's linear, digital and composite items (561 of 1,272) are excluded, and nothing is shown to transfer to a second measurement task.

## Reviewer claims accepted or rejected
- **Accepted: R1/R2, "the split is anticipated by 2604.22829".** The bibliographic check confirms a 2026 frontier-VLM gauge evaluation. This is not novelty-killing, because it is design guidance from a three-instrument video study, not a method on a broad real-image benchmark. The paper must credit it and claim "first measured instantiation", not "insight".
- **Partly accepted: R2, "the clock pillar ignores It's About Time [2111.09162]".** The bibliographic check confirms a CVPR 2022 Sim2Real clock reader with COCO, OpenImages and Clock-movie benchmarks. The proposal does not cite it, and it must be a baseline and a citation. I reject R2's stronger inference that clocks are "already solved, so +20 says little". R1 reports that TickTockVQA lists this reader at 18.54% on its own test set [2603.08011], so it is not far above the frontier on this benchmark. The miss is a citation and baseline gap, not a significance kill. R1's other use of the paper stands: in the wild, its Sobel+Hough baseline gets 7.7–9.7%. That is strong prior evidence that training-free geometry often fails, and I count it in p_core, not in odds.
- **Accepted, downgraded to answerable-major: R1, "the frontier is asked for minors-per-major, a geometric quantity".** It contradicts the "frontier never reads geometry" claim. It is easily fixed: count minors locally and treat the frontier's M as a soft prior, then report component error rates.
- **Accepted: R2/R3, the DINOv2 resolution concern.** It is a real risk to G2. The proposal's fallback (hybrid B becomes the method) limits the damage to odds, but it removes a named contribution.
- **Accepted, minor: R3, statistical points.** These are the underpowered per-tag claims (about 30 images per tag on the pilot), component metrics measured on the tuning split, the TickTockVQA 1,000-subset protocol, Astra run-to-run variance, and the cost-ratio accounting for a two-image call. None of them is decisive alone.
- **Not adopted: R3's rating of 4.** R3's own analysis says the +15 is relative to an unmeasured Astra and is mechanically bounded by coverage. Under the threshold-exact conditioning that concern is partly resolved, which is why I land at the top of the 3/3/4 band rather than at its bottom. But the anticipated insight and the missing held-out test are not resolved by the predicted numbers.
- **No reviewer marked a [fatal] weakness, and I see none.** Every major weakness can be answered within the budget.

## Calibration
Ratings are 3/3/4. The weaknesses are major but answerable, and none is fatal, which puts this in the 3–4 band. Two things pull upward: the predicted effect is decisive (+15 over the frontier's own best configuration at default cost) and the evaluation design is the best I have seen in this area. Two things pull downward: the insight is anticipated and must be credited, and the scope is dial-only and tuned on the test benchmark. **Odds 3.2.**

**p_core 0.25.** The load-bearing prediction is G1: +15 over the best Astra configuration on held-out real dials. It needs four things at once:
- training-free rectification, lattice extraction and DBNet to cover at least 50% of uncurated dials;
- 75% selective accuracy on that half;
- Astra xhigh with Python/crop tools, which has never been measured on dials, to stay at or below about 45% on the covered items;
- all of this built in one week by a team whose stated strength is not classical geometry.

Prior training-free and modular pipelines collapsed on exactly these stages (Reitsma 8.5% on MeasureBench, Hough clocks below 10%). I take the reviewers' lower value.

**Odds if the paper is rewritten around a negative result: about 0.8.** If G1 fails, the run stops and the outcome is an oracle-split failure analysis, which is a workshop paper at CVPR. If only G2 fails, hybrid B carries the paper at roughly the same odds, so the negative-result branch is mainly G1.

**Risk-adjusted:** 3.2 × 0.25 + 0.75 × 0.8 = 1.4.

## Fixes, ranked, with estimated effect and combined ceiling
Effects are in tenths of odds on the 0–10 scale and are not additive (see the ceiling note).

1. **Second real-dial benchmark with frozen thresholds, plus an absolute floor and the gain decomposition. Adds about 0.7 to odds (3.2 to 3.9).**
   - What changes in proposal_evaluation: add an end-to-end reading benchmark on which every weight and threshold fixed on the MeasureBench pilot is applied unchanged. Use InSituMeasure's analog-dial categories if released; otherwise use MeterFL's held-out real images scored as readings rather than only as a component diagnostic, and the DialBench/RPM-10K test set.
   - Add a falsifiable prediction: C3 beats Astra-default by ≥10 points there with frozen thresholds.
   - Commit to an absolute held-out value+unit accuracy floor on the 511 dials, not only a delta.
   - Report Δ = coverage × (C3 selective accuracy − Astra accuracy on the same covered items), together with Astra's accuracy on the abstained items.
   - Cost: about 400–600 extra images. Run Astra-default and C3 on all of them, and xhigh with tools only on a subset, which fits the US$300 reserve.
   - This is R1's and R3's one-point fix, and it turns the paper's main argument from assertion into evidence.
2. **Strong training-free needle baselines, and a defined refinement step. Adds about 0.4 (G2 becomes credible).**
   - Replace the Hough-only hybrid B with three versions of it:
     - (a) a SAM-family mask prompted at the hub, plus a principal-axis or skeleton fit with an asymmetric tip rule;
     - (b) a radial needle-colour or edge-energy profile;
     - (c) a pixel- or gradient-space paste-and-compare, the same sweep without DINOv2.
   - Add the ablation "sweep only vs sweep + tip refinement", and define the refinement in the method.
   - Report peak sharpness per nuisance tag.
   - Restate G2 against the best of (a), (b) and (c), lowering the threshold to ≥5 points overall and ≥10 on the nuisance subsets if needed.
   - If DINOv2 does not beat (c), state that the contribution is the silhouette sweep, not the frozen features.
3. **Reposition around one transferable claim, demonstrated on a second measurement task. Adds about 0.5 (helps R2 most; higher engineering risk).**
   - Drop the structured-light and phase-unwrapping vocabulary from the title and the novelty section.
   - Credit [2604.22829] as the source of the semantics-versus-geometry split.
   - Make the claim "a frontier-independent labelling margin over locally measured geometry fixes frontier measurement failures and tells you when to trust it".
   - Show it on MeasureBench's linear subset (rulers, cylinders, thermometers), using the same lattice, labelling ranking and margin with a 1D unwrap instead of a polar one. That is about 361 more images.
   - This also removes the "narrow application paper" objection. Its effect on p_core is neutral to slightly negative because it adds engineering.
4. **Complete the clock pillar. Adds about 0.3 (mostly removes a sure downside).**
   - Cite It's About Time [2111.09162] and run its public checkpoint on the fixed and released 1,000-image TickTockVQA list, and on MeasureBench clocks.
   - Rerun the Swap-DPO checkpoint on the same list if it is public.
   - Report C3's local-only components on the full 5,247-image test set.
   - Report accuracy and coverage per clock type (numerals, Roman, no-numeral, illustrated).
   - State G3 against the best of Astra and the trained specialist, or explicitly as "training-free vs trained specialist".
5. **An Astra-with-better-views baseline. Adds about 0.2.**
   - Give Astra the rectified crop, the polar-unwrapped strip and an indexed-tick overlay, but not the computed answer.
   - This separates "local measurement" from "easier visual prompt", which is the first question from anyone who has read the visual-prompting work.
6. **A held-out annotated subset, per-family breakdowns, and the frontier's component error rates. Adds about 0.2.**
   - Annotate and tag 150 of the 511 test dials before any run, and report every per-tag and component claim there, not on the tuning pilot.
   - Give per-family accuracy, coverage and gain: gauges, clocks, multi-dial meters, linear and non-linear scales.
   - Make minors-per-major a locally counted quantity, with the frontier's M only as a soft prior.
   - Report the frontier's box-value accuracy as a function of box density, and its M accuracy.
   - Run 2 Astra samples on a subset to measure variance.
7. **Raise p_core without changing the odds definition (risk, not odds).**
   - Move the G0 component pilot (lattice coverage and numeral assignment on 50 tagged dials) and the Astra xhigh-with-tools measurement on those 50 dials to the first three days. Do this before building the needle sweep.
   - Commit to reusing the MeterFL-trained segmenter variant as the fallback lattice extractor if the training-free extractor fails G0.
   - This moves p_core from about 0.25 to about 0.30–0.35 without lowering the committed effect.

**Combined ceiling.** With fixes 1–4 all made, the reviews would plausibly move to about 4/4/4–5. The insight would still be partly anticipated, so I would not go to 7. That gives **odds ≈ 5.0**, and about 5.3 with fixes 5–6 as well. The gains overlap, because fixes 1 and 3 both answer the generality objection, so summing the tenths would overstate them. With fix 7, p_core is about 0.32, and the risk-adjusted ceiling is about 5.3 × 0.32 + 0.68 × 1.0 ≈ 2.4. The remaining risk is whether training-free geometry survives in-the-wild dials and whether Astra with tools stays at or below about 45%. No rewrite of the proposal removes that risk; only the first week of the pilot can.

```json
{"odds": 3.2, "p_core": 0.25, "odds_risk_adjusted": 1.4,
 "decisive_weaknesses": [
  "The central insight (VLM for semantics, deterministic geometry for the needle) is already recommended by 2604.22829, and each module has a close ancestor (MeterFL polar lattice, Reitsma numeral anchoring, It's About Time 720-state clocks, FoundPose render-and-compare). The authors concede the phase-unwrapping framing re-describes tick counting, so novelty reduces to a ±1-neighbourhood MAP search with a frontier-independent margin plus a 2D silhouette sweep, and the paper rests on its numbers.",
  "No held-out real-dial benchmark: five weights and two thresholds are tuned on 200 MeasureBench dials and tested on 511 from the same benchmark, so the paper's main argument against trained readers ('training-free cannot overfit designs') is asserted, not shown.",
  "The headline +15 is relative to an Astra that has never been measured on dials, has no absolute floor, and mixes C3 answers with Astra fallback; Δ = coverage × (C3 selective accuracy − Astra accuracy on covered items) is not reported, so the gain may come from C3 answering the easy half.",
  "The needle sweep, a named contribution, is compared only with Hough and a DINOv2 edge-map line fit, not with SAM-at-hub, a radial profile or pixel-space paste-and-compare. At 14 px patches a 2–4 px needle is sub-patch, so precision comes from an underspecified tip refinement.",
  "Scope is dial-specific with no second measurement task, and the clock pillar omits the uncited trained specialist It's About Time [2111.09162]."
 ],
 "fixes_ranked": [
  "+0.7: Add an end-to-end held-out real-dial benchmark with all pilot weights and thresholds frozen (InSituMeasure analog categories if released, else MeterFL held-out real images scored as readings plus DialBench/RPM-10K test, about 400–600 images, Astra-default plus C3 on all and xhigh with tools on a subset, within the US$300 reserve), with a new prediction of ≥10 points over Astra-default there. Also commit to an absolute value+unit floor on the 511 dials and report the coverage × (selective − Astra-on-covered) decomposition with Astra's accuracy on abstained items.",
  "+0.4: Replace the Hough-only hybrid B with three training-free needle baselines: (a) SAM-family mask prompted at the hub plus an axis or skeleton fit with an asymmetric tip rule, (b) a radial colour or edge-energy profile, (c) a pixel- or gradient-space paste-and-compare sweep. Define the native-resolution tip refinement and ablate sweep-only vs sweep + refinement. Report peak sharpness per nuisance tag and restate G2 against the best of (a)–(c) at ≥5 points overall and ≥10 on nuisance subsets.",
  "+0.5 (higher engineering risk): Drop the structured-light and phase-unwrapping framing, credit 2604.22829 for the semantics/geometry split, and centre the paper on one claim: a frontier-independent labelling margin over locally measured geometry fixes frontier measurement failures and says when to trust it. Demonstrate it on MeasureBench's linear subset (rulers, cylinders, thermometers, about 361 images) with a 1D unwrap and the same ranking and margin.",
  "+0.3: Cite It's About Time and run its public checkpoint (and Swap-DPO if public) on a fixed, released 1,000-image TickTockVQA list and on MeasureBench clocks. Run C3's local stages on the full 5,247-image test set. Report per clock type (numerals, Roman, no-numeral, illustrated) and state G3 against the best of Astra and the trained specialist.",
  "+0.2: Add an Astra-with-better-views baseline: rectified crop, polar strip and indexed-tick overlay, without the computed answer. This separates local measurement from visual prompting.",
  "+0.2: Annotate and tag 150 held-out test dials before any run and move all per-tag, component and oracle claims there. Add per-family breakdowns. Count minors locally with the frontier's M only as a soft prior, and report the frontier's box-value accuracy vs box density and its M accuracy. Run 2 Astra samples on a subset for variance.",
  "Risk, not odds (p_core about 0.25 → 0.32): Run the G0 component pilot and the Astra xhigh-with-tools measurement on 50 tagged dials in the first three days, before building the needle sweep, and pre-commit to the MeterFL-trained segmenter as the fallback lattice extractor if the training-free one fails G0.",
  "Combined ceiling: fixes 1–4 together take odds to about 5.0 (about 5.3 with fixes 5–6), not the naive sum, because fixes 1 and 3 overlap. With the risk fix, odds_risk_adjusted is about 5.3 × 0.32 + 0.68 × 1.0 ≈ 2.4. The gap that remains is the empirical risk that training-free geometry survives in-the-wild dials, which only the first pilot week can settle."
 ]}
```
