# AC meta-review: C3v2, "Read the Labels, Measure the Ticks" (CVPR 2027 main track)

Inputs read: report.json, the Constraints section of problem.md, R1 (area expert, 4/conf 4, p_core 0.25),
R2 (generalist, 3/conf 3, p_core 0.25) and R3 (experimentalist, 4/conf 4, p_core 0.20). I used
`lit.py biblio` only to confirm the three uncited overlaps the reviewers raised (2512.23454, 2512.15327,
2609.29073). All three exist and say what the reviewers said they say.

## What the paper would be
It is a training-free analog-instrument reader. One GPT-6 Astra call supplies the symbols: numeral
values for letter-marked DBNet boxes, the unit, the scale type and the indicator roles. Ticks, numeral
positions and pointer angles are measured locally. A small MAP search over neighbouring scale
labellings picks the reading, and the score margin to the best rival that would change the answer
decides between answering and falling back to Astra. Taking every prediction at its threshold, the
paper reports these results:
- ≥50% value+unit on 511 held-out MeasureBench real dials and ≥ Astra-best + 15 at ≤1.3x API cost;
- with thresholds frozen, +10 over Astra-default on MeterFL and on RPM-10K, +20 over Astra-best on
  TickTockVQA and +8 on linear scales;
- margin AUROC 0.80, against ≤0.60 for Astra's own confidence signals;
- a better-views control that recovers at most a third of the gain.

## Decisive strengths (accepted from all three reviewers)
- **The problem is real, current and documented.** Frontier VLMs read the unit (96%) and the value
  badly (31.5% on real dials), and trained readers transfer poorly. A fix that works for a model
  available only through an API matters to the CVPR audience.
- **The controls are unusually good.** The better-views baseline separates measuring the answer from
  giving Astra a better image. Astra-best is selected on the pilot and then fixed. There is a gain
  decomposition, oracle splits on 150 geometry-annotated test dials, and a go/no-go gate after three
  days. Thresholds, code hash and image lists are committed publicly before any test run. All three
  reviewers credit this, and I agree it is the paper's strongest asset with a skeptical committee.
- **The numbers are large at threshold.** 50% on MeasureBench real dials is about 19 points above the
  best published model and 21 points above TriSCA, with no weight changes. Frozen-threshold transfer
  to three further public sets would be a first in this sub-area.
- **Prior work is credited honestly** (Lost in Motion for the split, MeterFL, Reitsma, It's About
  Time). The limitations section says the paper "stands or falls on its numbers."

## Decisive weaknesses
1. **[major, accepted; all three reviewers] The conceptual delta is thin.** The split comes from
   [2604.22829]. Unwrap and interpolation come from MeterFL, numeral anchoring from Reitsma's RANSAC
   fit, and the numeral-consistency vote from the uncited [2512.15327]. A local-geometry-to-LLM hybrid
   already exists in the uncited [2512.23454], and the general "VLM names, tools measure" pattern of
   2026 appears in the uncited [2609.29073]. The authors call the margin "ordinary MAP-with-margin."
   What remains is a careful, well-measured integration whose acceptance rests on its numbers. R2 asks
   what transfers beyond instruments, and the paper has no answer. I do not treat this as fatal:
   none of the overlaps builds the system on public single-image benchmarks, ranks labellings or
   abstains. It does cap the paper below the 5–6 band no matter how the numbers land.
2. **[major, accepted with a correction; R2 and R3] The headline and its decomposition thresholds do
   not line up.** R2 and R3 say the predictions are contradictory at threshold. Strictly they are
   not: the decomposition entries are bounds, not point values. With coverage 0.50, selective accuracy
   0.75, Astra-best 45% on covered items, 25% on abstained items and a zero fallback cost, all of G1
   holds and gives +15 at 50% absolute. However, every prediction exactly at threshold (Astra-best 55%
   on covered items, fallback cost 3) gives only +7. G1 therefore implicitly commits to two numbers
   the paper never states: Astra-best ≈35% overall and ≤45% on covered items. The G0 gate allows
   Astra-best up to 50%, which is far too lax for that. This is a real presentation and pre-registration
   flaw. A committee member would read it as a headline built on an unmeasured baseline: Astra has
   never been measured on dials. It can be fixed in the proposal.
3. **[major, accepted; R3] The strongest geometry baseline is not rerun.** The MeterFL U-Net pipeline
   is already the pre-committed fallback, so running it is almost free. Yet it is never run on
   MeasureBench with Astra-supplied v_min/Δv, which is the row that separates "the ranked labelling and
   margin help" from "any explicit tick geometry plus frontier semantics helps." The abstention claim
   has a related gap. The margin is compared only with Astra's own confidence signals, which are known
   to fail, and not with a trivial quality-feature gate. Without both rows the paper's named mechanism
   is not isolated.
4. **[major, accepted; R1 and R2] The significance case leaves out the result the Constraints reward
   most.** The Constraints ask the work "to need the frontier model less" and favour a "decisive
   cost/performance change." The fully local Qwen3-VL-4B variant is called a headline row but has no
   threshold. As written, the paper is about helping one closed model, and only one frontier family is
   tested.
5. **[major, accepted; R1, R2 and R3] Scope relative to calendar and team.** The paper has nine
   prediction pillars and two independent "novel" mechanisms; the DINOv2 needle sweep is a third story
   that dilutes the margin thesis. Six build days and 350 hand-annotated dials must all fit before a
   10-28 freeze, for a team whose experience is diffusion and RL rather than geometric pipelines. I
   judge the paper conditional on execution, as the panel rules require. Even at threshold, nine
   barely-met claims give reviewers nine things to argue with, and R2 is right that the paper has no
   single figure a reader will remember.
6. **[minor→major on the reliability claim; R1 and R2] "Frontier-independent" overclaims.** The margin
   does not use Astra's reading, but it depends entirely on Astra's semantics. A consistent misread
   (wrong numeral ring on a dual-unit gauge, a dropped ×10 multiplier, a decimal) satisfies the
   arithmetic prior and produces a confident wrong answer. The paper has no error taxonomy that would
   bound how often this happens. Together with R2's point that 75% selective accuracy is not a "trust"
   operating point, the reliability half of the title is weaker than the accuracy half.

## Reviewer claims I set aside or discount
- R2 and R3's word "inconsistent" is too strong (see weakness 2). The thresholds are under-specified
  and not mutually contradictory. The fix is the same either way.
- R1's composition of G0 into a ~38% end-to-end ceiling multiplies gates that do not measure
  independent stages (oracle-geometry reading conditions on ground-truth geometry). It is a fair
  warning about p_core, not about the conditional paper, and I use it only in p_core.
- R3's engineering-scope argument bears on whether the paper exists, not on how the executed paper
  would be judged. I count it toward p_core and toward the "too many pillars" weakness, not toward
  odds directly.
- None of the uncited works ([2512.23454] abstract-level, [2512.15327] one syringe, [2609.29073]
  metric 3D) kills novelty. All must be cited, and [2512.23454] makes the hand-back row (Astra composes
  the answer from the evidence JSON) a required G5 baseline rather than an ablation.

## Calibration
The ratings are 4/3/4 with several major weaknesses, and every one of them can be answered by
changing the proposal; none is fatal. That puts the paper in the 3–4 anchor band. Within the band it
moves up for the large absolute number, real controls and frozen-threshold transfer. It moves down
for a delta that all three reviewers independently call thin, and for a headline that rests on an
unmeasured and possibly much stronger Astra. **Odds 3.5/10.**

p_core: the reviewers give 0.25, 0.25 and 0.20. The load-bearing claim (≥50% absolute and +15 over
Astra-best on real dials) needs training-free lattice, attachment and pointer stages to be jointly
right on about 40% or more of web dials. Every earlier training-free or modular reader has collapsed
on such images. It also needs Astra-best ≤35% on dials in late 2026 at xhigh with tools. **p_core
0.22.** If the result is negative, the paper becomes a measurement paper: Astra configurations on
dials, oracle splits and component failure rates. At CVPR that is worth about 0.8.
Risk-adjusted ≈ 3.5 × 0.22 + 0.78 × 0.8 ≈ **1.4/10**.

## Fixes, ranked by odds added (conditional odds; overlapping effects not double-counted)
1. **+0.5 Make G1 arithmetically explicit and gate on the real baseline.** Commit coverage ≥60%,
   selective accuracy ≥80% and Astra-best ≤45% on covered items, so that the decomposition implies
   +15 on its own. State that Astra-best is ≈35% overall and tighten G0(c) to "Astra-best ≤38% on
   the 50 pilot dials," with a pre-stated pivot below +15 if it fails. Add an end-to-end G1 pilot gate
   on the 200 pilot dials before the freeze. This removes the R2/R3 headline objection. It lowers
   p_core slightly (≈0.20), because the bar becomes explicit.
2. **+0.5 Isolate the mechanism with three cheap rows on the 511 test dials.**
   (a) MeterFL U-Net + Astra v_min/Δv + count-from-start.
   (b) The same extractor with the labelling search.
   (c) A logistic-regression quality-feature abstention gate fitted on the pilot (number of numerals,
       tick-spacing CV, M_L = M_F, peak sharpness, q) as the AUROC baseline, plus a RANSAC/mode-of-slopes
       numeral fit as a second joint-ranking ablation.
   These rows turn "a geometry pipeline helps" into "ranked labelling and the margin help," and they
   answer R3's main objection.
3. **+0.4 Commit the zero-API headline.** For example: "Qwen3-VL-4B semantics + local geometry ≥
   Astra-best + 5 on the 511 test dials at zero API cost." Also add one open 7–8B semantic reader.
   This is the decisive cost/performance claim the Constraints ask for, and it answers the
   single-model objection (R1's one-point fix).
4. **+0.3 Cut to one story.** Demote the DINOv2 sweep (G2) to an ablation, and drop or shrink the
   linear-scale pillar to a short transfer note. Use the freed build days to commit a high-precision
   operating point: selective accuracy ≥90% at ≥35% coverage on the test dials, reused frozen on
   MeterFL and RPM-10K. The reliability half of the title then means something (R2's one-point fix),
   and the scope risk drops.
5. **+0.2 Honest framing and citations.**
   - Rename the signal "independent of the frontier's visual reading."
   - Add a per-cause error table (semantic: ring, multiplier, decimal, unit / attachment / lattice /
     pointer) on the 150 annotated dials, with margin AUROC on dual-scale and multiplier gauges.
   - Cite [2512.23454], [2512.15327] and [2609.29073].
   - Promote the evidence-JSON hand-back to a G5 baseline row with its cost.
   - Shorten the title to the thesis line.
6. **+0.1 Budget hygiene.** Budget three Astra samples on the 511 dials and the hand-back calls inside
   the US$1,000. State the exact image list on which every Astra-best comparison is made, with the CI
   at that n. Report a harm rate (items Astra-best gets right that the method answers wrong) and
   per-family pilot n with a leave-one-family-out threshold check.

**Combined ceiling: about 5.0/10.** The raw sum is +2.0 → 5.5, but fixes 1, 4 and 6 overlap in
tightening the headline, and the thin conceptual delta keeps the paper at "4/4/4, clear and
well-controlled, no new idea" rather than the 7–8 band. Risk-adjusted with all fixes: about
5.0 × 0.22 + 0.78 × 0.9 ≈ **1.8/10**. The fixes raise the value of a positive result far more than
the chance of getting one. p_core can only move with pilot evidence: a measured Astra-best ≤35% and
end-to-end G0 numbers on 50 dials.

```json
{
  "odds": 3.5,
  "p_core": 0.22,
  "odds_risk_adjusted": 1.4,
  "decisive_weaknesses": [
    "Thin conceptual delta: split from Lost in Motion [2604.22829], unwrap/interpolation from MeterFL, numeral anchoring from Reitsma, numeral-consistency vote from uncited [2512.15327], local-geometry-to-LLM hybrid in uncited [2512.23454], general 'VLM names, tools measure' pattern in uncited [2609.29073]; the margin is self-described as ordinary MAP-with-margin, so acceptance rests entirely on the numbers",
    "Headline +15 over Astra-best is not implied by the G1 decomposition thresholds (all-at-threshold gives about +7); it silently requires Astra-best about 35% overall and <=45% on covered items, while G0 tolerates Astra-best up to 50% and Astra has never been measured on dials",
    "Mechanism not isolated: MeterFL's trained tick pipeline with Astra-supplied metadata is not rerun on MeasureBench, and the margin is compared only with Astra self-confidence, not with a trivial quality-feature abstention gate",
    "Significance under the Constraints is under-claimed: the zero-API Qwen3-VL-4B variant has no committed prediction and only one frontier family is tested",
    "Too many pillars (nine predictions, a separate DINOv2 needle-sweep story) for a 3-week build by a non-geometry team; the 'frontier-independent' margin still trusts frontier semantics (ring, multiplier, decimal) and its 75% selective accuracy is not a trust-grade operating point"
  ],
  "fixes_ranked": [
    "+0.5: Restate G1 so the decomposition alone implies +15 (coverage >=60%, selective accuracy >=80%, Astra-best <=45% on covered items, Astra-best about 35% overall stated), tighten G0(c) to Astra-best <=38% on the 50 pilot dials with a pre-stated pivot, and add an end-to-end G1 gate on the 200 pilot dials before the freeze (p_core drops slightly to about 0.20)",
    "+0.5: Add three rows on the 511 test dials: MeterFL U-Net + Astra v_min/delta_v + count-from-start; the same extractor + labelling search; and a pilot-fitted logistic quality-feature abstention gate as the AUROC baseline, plus a RANSAC/mode-of-slopes numeral fit as a second joint-ranking ablation",
    "+0.4: Commit a zero-API headline prediction (Qwen3-VL-4B semantics + local geometry >= Astra-best + 5 on the 511 test dials at zero API cost) and add one open 7-8B semantic reader, making the decisive cost/performance claim the Constraints reward",
    "+0.3: Cut to one story: demote the DINOv2 sweep (G2) to an ablation, shrink the linear pillar to a transfer note, and use the freed days to commit a high-precision operating point (>=90% selective accuracy at >=35% coverage, frozen across MeterFL and RPM-10K)",
    "+0.2: Rename to 'independent of the frontier's visual reading', add a per-cause error table (semantic ring/multiplier/decimal vs attachment vs lattice vs pointer) with margin AUROC on dual-scale and multiplier gauges, cite 2512.23454 / 2512.15327 / 2609.29073, and promote the evidence-JSON hand-back to a G5 baseline row with cost",
    "+0.1: Budget three Astra samples on the 511 dials and the hand-back calls, state the exact image list behind every Astra-best comparison with its CI, and report the harm rate and a leave-one-family-out threshold check",
    "Combined ceiling: about 5.0/10 conditional odds (raw sum 5.5, minus overlap among fixes 1, 4 and 6; capped by the thin conceptual delta); risk-adjusted ceiling about 1.8/10, since p_core moves only with pilot evidence (measured Astra-best <=35% and end-to-end G0 numbers)"
  ]
}
```
