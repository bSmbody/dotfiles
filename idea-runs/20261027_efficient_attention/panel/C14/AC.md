# AC meta-review: C14, Verified Repair Sets for full-attention allocation in hybrid reasoning models

**Panel:** R1 3 (conf 4), R2 3 (conf 3), R3 3 (conf 4). Every reviewer gives p_core 0.25. No reviewer marks a weakness [fatal].

## What the paper would claim
Inside a teacher-anchored GDN supernet of Qwen3-4B, the paper picks which layers keep full attention, and how many, from the failures that mixer-only on-policy distillation leaves on the student's own long-CoT rollouts. Each failure event is shrunk by ddmin with PMA-gated skips to a 1-minimal "repair set" of layers. The method then greedily commits the layer or group that repairs the most events and stops when repairs stop being local.

## Decisive strengths
1. **The gap is real.** All three reviewers checked independently and agree. Published selectors score layers on teacher-forced text, synthetic probes or short benchmarks [2512.20569][2606.30562][2606.27791][2604.22050][2604.19877]. The strongest long-CoT conversion fixes allocation by rule [2609.31947]. Super Apriel names on-policy placement as future work. Nobody has chosen allocation from on-policy residual failures. I accept this.
2. **The all-exact configuration is exactly the teacher.** This gives every reduction a valid start and a deterministic predicate. It is a real improvement over Super Apriel's approximate all-FA placement.
3. **The controls are honest.** The paper runs the two cheap on-policy baselines (single-swap on-policy score and greedy whole-trace on-policy KL), has pilot kill criteria and an answer-flip filter, reports cost in GPU-hours, and gives every baseline the same finishing stage.

## Decisive weaknesses
1. **At threshold, the result in the shipped model is close to nothing (R2, R3; I accept).** The only prediction with a stated margin is #3, which only has to clear ±4.2 pp noise. It is measured in the frozen, mixer-only supernet, a model nobody ships. Prediction #6 only says the ranking is "preserved" after joint OPD, and #4 only says the long-bin results are "better". So the paper that results is "a few points in a frozen supernet, near zero after the training that actually ships". R2's outside evidence makes this more likely. SWARR [2606.11634] gets close to full attention on math with zero full-attention layers under RL. Opal's 9/36 rule already reaches 83–93% of the teacher. The proposal never shows that allocation matters at all after joint OPD; nobody has measured the spread across random allocations.
2. **The load-bearing comparison sits at the noise floor and the protocol is unspecified (all three; I accept).** MATH-500 is at 92–93.8% for Opal 9/36, so a gain of more than 4.2 pp at K=9 is nearly impossible there. AIME has 30 problems per year, and the proposal does not state avg@k or what counts as a seed. Even with the prediction met exactly, a reviewer can attribute the margin to run-to-run variance in a multi-day pipeline that is run once.
3. **No efficiency claim (R3; I accept, and I consider it the most damaging point given the scope).** KV memory depends only on K. Every prediction is stated at matched K, and the "minimize K at matched accuracy" goal has no prediction and no kill condition. The scope is "what history to keep", yet the predicted paper shows no memory saving over Opal 9/36, while costing several extra GPU-days next to selectors that take about 15 minutes.
4. **The machinery is heavier than the claimed delta, and the insight is buried under it (R1, R2, R3; I accept).** With at most 36 layers, ddmin plus revisit-to-fixpoint is backward elimination with caching. PMA, the unclear band and three orderings add knobs (kappa, tau, band, delta, k, s_min, m) and do not add insight. The proposal predicts no value for the monotonicity-violation rate, so nothing shows that joint, non-monotone repair sets matter. If they do not, greedy on-policy KL is the method people will adopt. Event-localized KL without ddmin is the missing separator (R1).
5. **The thresholds are internally inconsistent (R2; I checked this and it is correct).** The pilot passes as long as the median repair set is at most 12 of 36 layers. The loop stops once the median exceeds 4. So a pilot that only just passes produces a loop that stops in round 1. Either the kill criterion says nothing, or "K from data" rests on three hand-set knobs, and no sensitivity analysis is planned.
6. **Missing strong cheap baselines (R1, R3; I accept).** On-policy versions of FlashMorph, DASH or ConSA gates trained with the OPD reverse-KL objective are missing; they model interactions jointly. So is greedy allocation by long-CoT dev accuracy (DtR's criterion applied to the target task), and so is a total-GPU-hour-matched Opal.

## Claims I reject or downweight
- R3's feasibility concern (4–6 months for one student) is real but secondary. Under the conditional ("executed as written"), it does not lower odds.
- R1 and R2 say head-level allocation makes this look dated. I count that as minor: whole-layer allocation is still the standard unit in conversion papers.
- R1 argues that RAD [2505.22135] undermines the claim "every criterion is teacher-forced". That needs a narrower sentence, not a novelty downgrade. Its draft is the teacher, its generations are 128 tokens, and it selects once before distillation. All reviewers report no prior or concurrent work that kills novelty, and I found no disputed overlap that needed a bibliography check.
- I do not count the DAgger grounding as a weakness beyond R1's point that it is decorative. It costs clarity, not acceptance.

## Calibration
The ratings are 3/3/3. There is no strong-overlap kill, but several major weaknesses are well argued and agreed by all three reviewers. The worst of them is that the predicted evidence, met exactly at threshold, shows no memory gain and only a borderline accuracy gain, in a model that is not shipped. Rebuttal cannot fix this, because it comes from how the predictions are framed. The anchor is 1–2, and I put it at 1.8. The load-bearing prediction is #3: a clear win over greedy whole-trace on-policy KL. It depends on #1 (localized, recurring repair sets) and on that gain surviving into the shipped model. I share the reviewers' 0.25 and shade it to 0.2 because of MATH-500's ceiling and AIME's variance. If the prediction fails, the paper becomes a negative or diagnostic result ("residual long-CoT failures are diffuse after OPD"). Analysis as the main contribution is out of scope, so that version is worth about 0.5.

odds_risk_adjusted ≈ 1.8 × 0.2 + 0.8 × 0.5 = 0.76 → 0.8.

```json
{"odds": 1.8, "p_core": 0.2, "odds_risk_adjusted": 0.8,
 "decisive_weaknesses": [
  "At threshold, the only margin-bearing prediction (#3, just beyond +/-4.2 pp) is measured in the frozen mixer-only supernet; after joint OPD the ranking need only be 'preserved', so the shipped-model gain may be near zero, and the paper never shows that allocation matters at all after on-policy training (no random-allocation spread)",
  "No K-reduction / memory-saving prediction: every claim is at matched K, so the paper shows no KV saving over Opal 9/36, which contradicts the scope's object, while costing several extra GPU-days",
  "Statistical protocol unspecified (avg@k, what a seed is); MATH-500 at 92-93.8% leaves no room for >4.2 pp at K=9, and AIME pass@1 noise exceeds any plausible effect",
  "ddmin/PMA machinery is not shown to be necessary: no predicted monotonicity-violation rate, no event-localized-KL-without-ddmin ablation, and greedy whole-trace on-policy KL may carry everything",
  "Internally inconsistent thresholds (pilot passes at median <= 12/36, loop stops at median > 4), and 'K from data' swaps one knob for s_min, m, tau and the band, with no stability analysis",
  "Missing strong cheap baselines: on-policy differentiable gates (FlashMorph/DASH/ConSA with the OPD loss), greedy allocation by long-CoT dev accuracy, and a total-GPU-hour-matched Opal"
 ],
 "fixes_ranked": [
  "Make the headline a shipped-model K-reduction claim: after joint OPD, match Opal 9/36 on AIME avg@32 with K<=6 (>=33% smaller growing KV), with >=3 full pipeline seeds and paired bootstrap CIs, at matched total GPU-hours",
  "First establish that allocation matters after joint OPD: report the accuracy spread of >=5 random allocations at small K (4-6), and move the main comparisons to the K where that spread is large",
  "Add the strongest cheap on-policy competitors: FlashMorph/DASH-style gates trained with the OPD reverse-KL objective, and greedy allocation by long-CoT dev accuracy; pre-state a margin over them",
  "Cut the SE apparatus to what earns its keep: predict a monotonicity-violation rate, add event-localized KL without ddmin, and drop PMA/bands unless they change final accuracy",
  "Fix the threshold mismatch between the pilot kill and the stopping rule, show that K is stable across s_min, m and tau, and report how well KL repair agrees with answer repair"
 ]}
```
