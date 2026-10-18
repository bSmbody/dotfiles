# AC meta-review: C3, "Unsticking the Subject" (UnStick-CFG), CVPR 2027 main track

**Recommendation: reject.** Odds 1.5/10, risk-adjusted 0.6/10.
- Reviews: R1 3 (confidence 4), R2 3 (confidence 3), R3 3 (confidence 4).
- Reviewer p_core: 0.30 / 0.25 / 0.25.
- No reviewer tagged a weakness [fatal], and no reviewer argues for acceptance.

## The paper that would result at threshold

If every prediction lands exactly at its stated threshold, the paper shows six things:
- **The method.** An exact, zero-extra-NFE guidance rule that is formally an instance of FDG's linear-transform rule [2506.19713]: a temporal-DC split of the coarse band, gated to steps 1–5. It gives a just-detectable gain in RAFT flow and dynamic degree over CFG and over the whole-coarse-band control ("FDG along time") on Wan2.1-T2V-1.3B.
- **A motion knob.** Flow rises monotonically with w, where CFG's stays flat.
- **Targeted gains.** The gains fall on high-dynamics, fixed-camera prompts.
- **Guards.** Alignment and identity costs stay within an unstated "small margin".
- **Three mechanism results.** Lower same-position MC, sub-additivity with RoPE-λ, and a smaller gain on CogVideoX-2B.
- **No effect sizes.** No prediction carries a number, so "at threshold" means the smallest effect the planned sample can resolve. That is about ±4 dynamic-degree points at 95% with one seed per prompt (R1 and R3 compute this independently and agree).

## Decisive strengths

- **A clean causal handle at zero cost.** The change from CFG, Δ = −(w − g_s)·M L D, is identical in every frame. The guided estimate's inter-frame differences therefore equal CFG's exactly, and with all gains at w the rule reduces to CFG. It needs one subtraction, no hooks and no extra pass, and it composes with per-token rules. All three reviewers credit this, and so do I.
- **Honest framing with a pre-committed control.**
  - The proposal concedes the FDG and DyMoS overlap.
  - It names FDG along time and guidance-off-in-window as the controls that decide the paper.
  - It writes kill conditions for every pillar and sets a pilot stop rule.
- **Evaluation design that avoids the field's usual trap.**
  - It reads quality at matched dynamics.
  - It uses DEVIL grades 1–2 as a negative control and D_control.
  - It uses a camera-split set to separate sticking from tracking.
  - It borrows StyleGAN3's averaged-frame sharpness test.
- **A memorable practical claim, which the reviews underweight.** If pillars (v) and (vi) hold, the guidance scale becomes a prompt-appropriate motion knob at CFG cost. Readers would remember that figure, and it is the strongest result the paper could show at threshold.
- **A realistic budget.** About 23 of 40 GPU-days, on tooling the team already runs (R3 re-derived the 11.4 GPU-day main study).

## Decisive weaknesses

1. **The contribution is the causal account, and at threshold none of its tests discriminates.** The method delta over FDG is conceded, so the paper must win on mechanism. All three reviewers, independently, show that each mechanism pillar passes whether or not the account is true:
   - **(ii) The probe.** In [2609.23658] the per-frame "winner" is read off the final trajectory, so "the winner lies away from the earliest-committed frame" mostly restates "the subject moved" (R1). I add a second point: removing a frame-identical component from the clean estimate lowers same-position cross-frame agreement by construction. A drop in same-position MC is therefore partly mechanical as well.
   - **(iii) Sub-additivity with RoPE-λ.** Saturation alone produces it on a bounded metric over the same near-static seeds (R1, R2, R3), and no reference pair is run.
   - **(iv) The CogVideoX-2B contrast.** It confounds positional encoding with model size, data, window and headroom. CogVideoX-2B is already the most dynamic small model [2502.02492], and the contrast rests on one model per side (R1, R2, R3).
   - **The pilot.** It is selected on the outcome (the bottom ~8% of CFG flow), so the gain over CFG on that set is regression to the mean (R1, R3).
2. **Two predictions pull against each other, and the dose is tiny.**
   - **The tension.** UnStick and FDG along time differ only by (w − 1)·(I − M)·L·D. The larger the frame-identical share ρ_k that pillar (viii) predicts, the smaller this difference, in exactly the window where it must decide pillar (i) (R1, R2, R3).
   - **The dose.** Under Wan's shift-5 schedule, steps 1–5 move σ only from 1 to about 0.978. I re-derived this: σ' = 5·0.9 / (1 + 4·0.9) ≈ 0.978. The guided estimate therefore enters x_t with only about 2% weight.
   - **The priors.** The in-domain evidence points the other way. Switching guidance off early lowered FLOW from 4.10 to 3.76 on this model [2603.14073]. Ablating the condition-induced static content changed object size, not trajectory [2609.23658].
   - **The missing control.** No norm- or energy-matched control and no random frame-identical perturbation separate "this cell" from "any early perturbation of near-static seeds".
3. **Directional-only predictions and an underpowered design leave the threshold result mid-table.**
   - **No primary endpoint or multiplicity control.** The design has one seed per prompt, so the "seed-bootstrap" CIs in kill condition (i) cannot be computed. It names no primary endpoint and applies no multiplicity correction.
   - **A human study that cannot show non-inferiority.** It uses 50 pairs × 3 raters against CFG only, so it cannot support "identity not worse than CFG".
   - **A gain that may trail the competitors.** A barely-detectable gain can sit below the same-model competitors already in the table: TrajCFG adds +5.55 dynamic degree at 0 NFE [2610.14153], and MotionCFG adds about +16% FLOW on 1.3B [2603.14073]. Nothing is predicted against either, nor for the UnStick + TrajCFG composition arm.
4. **The headline metrics do not measure the claimed phenomenon** (R3).
   - **Dynamic degree and mean flow.** The motivating video ("trots in place while the sand slides") already counts as dynamic under both.
   - **Subject travel.** It is measured only on the 80-prompt camera-split set, with a mask taken from the generator's own cross-attention, which the method perturbs.
   - **Consequence.** A flow gain could come from background motion, camera motion or flicker rather than unsticking.
5. **Scope and parity.**
   - **Backbones.** All primary evidence comes from Wan2.1-1.3B, an early-2025 model; transfer uses 2024 models. The concurrent competitors already evaluate Wan2.2: TrajCFG on Wan2.2-5B [2610.14153], and SpecLoR's abstract states "Experiments on Wan2.2" [2606.11969].
   - **Baseline tuning.** The baselines run at single settings:
     - RoPE-λ = 0.70, although its authors needed 0.50–0.85 per seed;
     - TrajCFG off its native 40-step setup;
     - MotionCFG at one τ, despite its non-monotone response to τ.
   - **Own tuning.** UnStick's own window, J and g_s are tuned on pilot prompts that are not stated to be disjoint from the evaluation prompts (R3).

## Reviewer claims: accepted, down-weighted, rejected

- **Accepted (decisive).** The FDG instance relation, which kills method novelty but is conceded (R1, R2, R3). The viii-versus-i tension (R1, R2, R3). Saturation in the λ test and confounding in the CogVideoX-2B contrast (R1, R2, R3). The outcome-selected pilot (R1, R3). The circular probe (R1), to which I add the by-construction MC drop. The underpowered, directional-only design (R1, R3). The metric mismatch (R3). The dated backbones (R2, R3, R1). Tuning parity (R3).
- **Accepted (minor).**
  - The σ-span window: state it in σ and report ‖Δx_t‖ (R1, R2, R3).
  - The negative-prompt confound: the proposal never states its negative prompt (R2, R3). R2 and R3 both recall that Wan's default negative prompt contains "static/still" terms. I share that recollection, but nobody on the panel verified it in a paper. An empty-negative-prompt arm settles it either way.
  - The ambiguous dog example, which is a tracking shot (R2).
  - The "five times the gap" sentence, which is just w − 1 and holds for every cell (R2).
  - The long title (R1, R2).
  - R3's Q7. The design claims that raising the frame-varying gain barely changes dynamics, yet pillar (v) needs flow to rise with w when only the frame-varying and fine gains grow. The two are reconcilable: under CFG the shared push cancels the frame-varying gain. But then the "C1-style raise" ablation should also add motion, and the proposal must say so.
- **Down-weighted.**
  - R2's ALG / History Guidance "band tension". This is a fair question, but the fine-band (HG-literal) arm already in the plan answers it if it is given a stated prediction. Minor.
  - R2's "under-animation is a tail" (dynamic degree 65–83). Dynamic degree cannot see screen-space sticking (R3's point), so these numbers do not show that sticking is rare. They do show that the proposal never measures how often it occurs. I accept the request for a prevalence number, not the conclusion that the problem is unimportant.
- **Rejected as a bar.** R1 uses MotionCFG's roughly 2× FLOW on Wan2.1-14B as the effect-size bar. The relevant same-model bars are about +16% FLOW (MotionCFG, 1.3B) and +5.55 dynamic degree (TrajCFG). The reviewers' numbers are mutually consistent; only the 1.3B figures belong in a 1.3B table.

## Overlap claims settled with `lit.py biblio`

- **[2504.03072] How I Warped Your Noise** (ICLR 2024 oral). The abstract confirms R1: noise sampling that ignores frame correlations "produces high-frequency flickering, or texture-sticking artifacts". This is in-domain diffusion precedent for screen-fixed inputs causing sticking, at fine scale. It is missing from the related work and should replace StyleGAN3 as the lead analogy. It does not kill novelty.
- **[2405.14864] MOFT** (NeurIPS 2024). The abstract confirms R2: motion features are obtained by "eliminating content correlation information". The frame-mean / residual split is therefore a known tool, and the decomposition itself is not novel. Its use in the CFG rule is new. It does not kill novelty.
- **[2606.11969] SpecLoR.**
  - The abstract describes early 3D amplitude rectification for "motion coherence" on Wan2.2, at 4 extra NFE.
  - R1's MovieGen-Bench dynamic-degree numbers cannot be confirmed from the abstract.
  - The proposal's blanket "keeps or lowers motion" is at least imprecise; its own text says only that SpecLoR-stochastic lowers dynamic degree.
  - Minor. Cite it accurately and add it as a reference arm that is not NFE-matched.
- **[2605.19398] DyMoS** (accepted to NeurIPS 2026, so published prior work by submission time). The abstract also frames the method as "a single scalar parameter for continuous control over motion strength". DyMoS therefore anticipates, in I2V, both the principle and the "motion knob" selling point of pillar (v). This is partial overlap and does not kill the T2V-CFG instance, but the knob claim must be positioned against it.

## Calibration

- **Band.** Ratings of 3/3/3 put the paper in the 1–2 band.
- **No cap.** I agree with no [fatal] weakness, so the 1.5 cap does not bind.
- **Where in the band.**
  - The three reviews converge independently on the same four defects: the viii/i tension, the confounded positional-encoding contrast, the saturation reading of the λ test, and the selected pilot.
  - The method novelty is conceded.
  - At threshold, no result is both discriminating and large enough to carry a rebuttal.
  - That places the paper in the lower half of the band: **odds 1.5**.
- **p_core 0.25.** I side with R2 and R3 over R1's 0.30. The ~2% σ span, the Interval Guidance FLOW drop on this model and the size-not-trajectory ablation all point against the premise. The I2V shared-content evidence [2605.19398][2506.08456][2502.06764] keeps it from being lower.
- **Negative-result rewrite.** A paper titled "CFG's frame-identical term does not drive anchoring" would have odds of about 0.3.
- **Risk-adjusted odds.** 1.5 × 0.25 + 0.75 × 0.3 ≈ **0.6**.

## Fixes, ranked by the odds they add

Each delta is on the x/10 scale, from the current 1.5. The deltas are sub-additive:
- fixes 1–6 together would bring the paper to about 3.5, the 4/3/3 band;
- the ceiling stays there because the method remains an FDG instance with 1.3B-centred evidence.

Fixes 1, 2 and 4 together cost about 13–15 GPU-days. That fits the ~17 GPU-day reserve if the CogVideoX-2B/5B transfer (2.3 GPU-days) is dropped and the w-sweep is cut to {3, 6, 9}. On 2 GPUs the calendar becomes tight, so run in the order listed.

1. **Replace the confounded mechanism tests with a discriminating causal design: about +1.0 (to 2.5).**
   - **New arms.** On 150 unselected prompts × 2 seeds (≈0.83 GPU-days per arm), add:
     - **(a) Two-sided dose.** Extend the g_s dose past CFG to g_s = 2w − 1, which adds back exactly what UnStick removes.
     - **(b) Random control.** Add a random frame-identical coarse perturbation matched to M L D in per-step norm and spectrum.
     - **(c) Energy-matched scalar.** Add a scalar w_early per step that removes the same energy as UnStick.
     - **(d) Within-Wan λ dose-response.** Run UnStick against CFG at RoPE-λ ∈ {1.0, 0.85, 0.70, 0.55}. This becomes the primary positional-encoding test, and CogVideoX-2B is demoted.
     - **(e) Reference pair.** Run TrajCFG + RoPE-λ, so that sub-additivity is judged against a reference, using log RAFT flow and a per-seed interaction model rather than dynamic degree.
   - **Probe.** Run the probe on (a)–(c) as well, with the winner defined at step 5 (argmax candidate) rather than from the final trajectory.
   - **Restated predictions.**
     - Stasis rises monotonically for g_s > w.
     - The random and energy-matched controls give no gain.
     - UnStick's gain shrinks monotonically toward 0 as λ falls.
     - Only UnStick lowers same-position MC at matched flow.
   - **Cost.** About 8 arms, roughly 6.7 GPU-days.
2. **Pre-register quantitative thresholds and a powered primary endpoint on unselected seeds: about +0.7 (to 2.2).**
   - **Primary endpoint.** Paired log RAFT flow on fixed-camera motion prompts. Use ≥3 seeds × ≥150 prompts for CFG, FDG along time and UnStick, analysed with a mixed model that has prompt as a random effect.
   - **Thresholds.**
     - At least +15% flow and +5 dynamic-degree points over CFG, i.e. at the level of TrajCFG and MotionCFG on 1.3B.
     - At least +8% flow over FDG along time.
     - Non-inferiority margins: at most a 1% relative drop in VideoAlign TA and at most 0.005 on ViCLIP.
   - **Statistics.** Apply Holm correction across the secondary pillars. Report the selected-seed pilot only as a diagnostic, and tune on prompts disjoint from evaluation.
   - **Cost.** About 2.5 GPU-days.
   - **Trade-off.** Raising the threshold lowers p_core to about 0.2, so the risk-adjusted gain is only about +0.2.
3. **Make the composition arm the practical headline and level the baselines: about +0.5 (to 2.0).**
   - **Composition prediction.** Predict that UnStick + TrajCFG, with TrajCFG's gains confined to the three gain-w cells, beats TrajCFG alone by at least +3 dynamic-degree points at 0 extra NFE, with no TA loss. This turns "mid-table" into the best row.
   - **Baseline sweeps.** Sweep RoPE-λ ∈ {0.55, 0.70, 0.85}, which is shared with fix 1(d). Run TrajCFG at its native 40-step configuration and MotionCFG at two values of τ.
   - **Reporting.** Show flow against TA/VQ Pareto fronts for CFG over w, UnStick, MotionCFG and TrajCFG.
   - **Cost.** About 1.2 GPU-days.
4. **Add one current backbone: about +0.5 (to 2.0).**
   - **The run.** Wan2.2-TI2V-5B in T2V mode, which has a base dynamic degree of 55.56 and therefore more headroom [2610.14153] and fits on a 24 GB GPU. Run 150 prompts × {CFG, FDG along time, UnStick, TrajCFG}.
   - **Cost.** About 3.75 GPU-days at ~9 min per clip, paid for by dropping CogVideoX-2B/5B.
5. **Measure the claimed phenomenon on every benchmark: about +0.4 (to 1.9).**
   - **Subject metrics.** Add screen-space subject travel and the ratio of subject to background flow, from an external segmenter and point tracker rather than the generator's own cross-attention, as co-primary metrics next to RAFT flow and dynamic degree.
   - **Prevalence.** Report how often CFG sticks on the fixed-camera prompts.
   - **Headline example.** Replace the dog example, which is a tracking shot, with a fixed-camera prompt.
   - **Cost.** Metric compute only.
6. **Resolve the viii-versus-i tension with day-1 dose diagnostics: about +0.3 (to 1.8).**
   - **Diagnostics.** Before any headline result, report per window step:
     - ‖(I − M)LD‖ / ‖LD‖ and ‖(I − M)LD‖ / ‖MLD‖;
     - ‖Δx_t‖ / ‖x_t‖;
     - the window's σ span.
   - **Window and stated ranges.** Define the window in σ, not step index. State the predicted ρ_k range and the minimum residual share that pillar (i) needs.
   - **Explanation.** Explain why full gain on the small residual decides the competition. Use these diagnostics as an explicit go/no-go.
   - **Cost.** Essentially free.
7. **Re-allocate the ~150 human judgements: about +0.15.**
   - Split them as 25 pairs against CFG and 25 against TrajCFG, with 3 raters each.
   - Pre-state a non-inferiority margin for identity breaks and include a power note.
8. **Fix presentation and citations: about +0.1.**
   - Use a short title, e.g. "Unsticking the Subject in Text-to-Video Guidance".
   - Cite [2504.03072] and MOFT [2405.14864].
   - Correct the SpecLoR characterisation and position the motion-knob claim against DyMoS's scalar slider.
   - State the negative prompt and add an empty-negative-prompt arm.
   - Drop the "five times the gap" sentence, and present StyleGAN3 as intuition, not evidence.

```json
{
  "odds": 1.5,
  "p_core": 0.25,
  "odds_risk_adjusted": 0.6,
  "decisive_weaknesses": [
    "The method is a conceded instance of FDG's linear-transform rule [2506.19713], so the paper rests on its causal account, yet at threshold no mechanism pillar discriminates. The probe's winner is read off the final trajectory, and removing frame-identical content lowers same-position MC by construction. Sub-additivity with RoPE-λ follows from saturation alone. The CogVideoX-2B contrast confounds positional encoding with size, data and headroom. The pilot is selected on the outcome (regression to the mean).",
    "Pillars (viii) and (i) pull against each other: a large frame-identical share ρ_k shrinks the only UnStick-versus-FDG-along-time difference, (w−1)(I−M)LD. Steps 1–5 span σ 1→0.978, so the change enters x_t with about 2% weight. In-domain priors point the other way (early guidance-off lowered FLOW 4.10→3.76 [2603.14073]; ablating condition-induced static content changed object size, not trajectory [2609.23658]). No norm-, energy- or random-matched control is run.",
    "Every prediction is directional only, with one seed per prompt (about ±4 dynamic-degree points at 95%), no primary endpoint, no multiplicity correction, and a 50×3 human study against CFG only. At threshold the gain can sit below TrajCFG (+5.55 dynamic degree at 0 NFE) and MotionCFG (about +16% FLOW) on the same model, and nothing is predicted against them.",
    "Dynamic degree and mean RAFT flow do not measure subject sticking: the motivating 'trots in place' video already counts as dynamic. Subject travel is measured only on 80 prompts, with a mask from the generator's own cross-attention.",
    "All primary evidence is on Wan2.1-1.3B, with transfer only to 2024 models, while competitors evaluate Wan2.2. Baselines run at single, partly off-native settings (λ=0.70, TrajCFG at 50 steps, MotionCFG at one τ), while UnStick is tuned on pilot prompts not stated to be disjoint from evaluation."
  ],
  "fixes_ranked": [
    "+1.0 (1.5→2.5) Discriminating causal design. On 150 unselected prompts × 2 seeds, add: g_s extended to 2w−1; a random frame-identical coarse perturbation matched in norm and spectrum; an energy-matched scalar w_early; UnStick vs CFG across RoPE-λ ∈ {1.0, 0.85, 0.70, 0.55} as the primary positional-encoding test, with CogVideoX-2B demoted; and a TrajCFG+λ reference pair, judged on log flow. Run the MC probe on these arms with the winner defined at step 5. Restate predictions as: stasis rises for g_s>w; the controls give no gain; UnStick's gain shrinks monotonically as λ falls; only UnStick lowers MC at matched flow. Cost about 6.7 GPU-days.",
    "+0.7 (to 2.2) Pre-register quantitative thresholds. Primary endpoint: paired log RAFT flow on fixed-camera prompts, unselected, ≥3 seeds × ≥150 prompts for CFG / FDG along time / UnStick, in a mixed model. Thresholds: ≥+15% flow and ≥+5 dynamic-degree points over CFG; ≥+8% flow over FDG along time; at most a 1% TA drop and 0.005 on ViCLIP. Apply Holm correction to secondary pillars, treat the pilot as a diagnostic only, and use disjoint tuning prompts. Cost about 2.5 GPU-days. p_core falls to about 0.2, so the risk-adjusted gain is only about +0.2.",
    "+0.5 (to 2.0) Composition headline and baseline parity. Predict that UnStick+TrajCFG (TrajCFG's gains confined to the three gain-w cells) beats TrajCFG alone by ≥3 dynamic-degree points at 0 extra NFE with no TA loss. Sweep λ, run TrajCFG at its native 40 steps and MotionCFG at two τ values, and report flow against TA/VQ Pareto fronts. Cost about 1.2 GPU-days.",
    "+0.5 (to 2.0) Add Wan2.2-TI2V-5B in T2V mode (base dynamic degree 55.56, fits in 24 GB): 150 prompts × {CFG, FDG along time, UnStick, TrajCFG}, about 3.75 GPU-days, paid for by dropping CogVideoX-2B/5B.",
    "+0.4 (to 1.9) Measure subject screen-space travel and the subject/background flow ratio with an external segmenter and point tracker on every benchmark, as co-primary metrics. Report how often CFG sticks on fixed-camera prompts, and replace the tracking-shot dog example with a fixed-camera one.",
    "+0.3 (to 1.8) Day-1 dose diagnostics as a go/no-go. Report per step ‖(I−M)LD‖/‖LD‖, ‖Δx_t‖/‖x_t‖ and the window's σ span; define the window in σ. State the predicted ρ_k range and the minimum residual share pillar (i) needs, and explain why full gain on that residual decides the competition.",
    "+0.15 Split the ~150 human judgements as 25 pairs vs CFG and 25 vs TrajCFG (3 raters each), with a pre-stated non-inferiority margin for identity breaks.",
    "+0.1 Presentation and citations: a short title; cite [2504.03072] (diffusion texture sticking) and MOFT [2405.14864]; correct SpecLoR; position the motion-knob claim against DyMoS's scalar slider [2605.19398]; state the negative prompt and add an empty-negative-prompt arm; drop the 'five times' sentence."
  ]
}
```
