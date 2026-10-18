# Meta-review (AC), submission C3, CVPR 2027 main track

**"Remove the Found, Ask Again: Residual Presence Tests Tell a Frozen Segmenter Where to Zoom"**

Reviews: R1 (area expert) 3 / conf 4 / p_core 0.55; R2 (generalist) 3 / conf 3 / p_core 0.40; R3 (experimentalist) 3 / conf 4 / p_core 0.40.

**Recommendation at the stated thresholds: reject (weak), odds 1.8/10, risk-adjusted 1.0/10.**

## What the paper would be

C3 wraps an unchanged frozen-SAM 3 OVSS pipeline (ActiveSAM). It masks each minority class's already-labelled tokens as attention keys after the shared backbone pass and re-reads SAM 3's presence on aspect-preserving root tiles. It then zooms best-first in a depth-2 quadtree only on (view, class) pairs whose residual presence stays at or above τ = 0.1. Zoomed views may only add small, contained, certified segments of flagged classes, and the coarsest valid view keeps authority. The predictions are all directional. Exactly at threshold, the paper shows four things. Residual presence beats unmasked presence in AUROC. C3's recovery-versus-passes curve beats presence-ranked search (iii) and uniform tiling (ii) at some budget. Stuff IoU stays "within noise". mIoU does not fall on any base.

## Decisive strengths

- **A crisp, memorable, apparently new trigger.** None of the three reviewers found prior or concurrent work that asks a frozen open-vocabulary recogniser "is c still here?" after hiding c's found segments, and uses the answer to gate zoom. I checked the two overlap claims raised against the novelty sentence (below), and neither touches the zoom gate. The failure it targets is real and well documented: presence on unedited crops cannot stop once any instance is visible, which is why ZoomEye's all-instance mode visits every node [2411.16044].
- **Well-controlled matched baselines.** Baselines (ii)–(vi) share C3's child geometry, certification, write rules and fusion, so (iii) isolates the removal step. All three reviewers credit this. The anytime search gives the whole budget curve from one logged run.
- **Honest design.** There is a pre-registered go/no-go pilot with a stated negative-result branch, a context-answering rate as a reported metric, fixed hyperparameters, and limitations that name the failure modes the reviewers then attack.
- **Cheap by construction**, as long as removal after the backbone does not leak. The per-prompt key mask rides on SAM 3's prompt-independent backbone pass.

## Decisive weaknesses

1. **At threshold, the paper has no committed gain on any standard metric.** All three reviewers raise this, and I weigh it most heavily, because the odds are judged with every prediction landing exactly at its threshold. At that point the evidence is:
   - a recovery rate the authors define themselves;
   - mIoU that is flat across eight benchmarks, some near saturation;
   - unquantified pole, sign and light IoU;
   - up to 43–64 view passes per image against ActiveSAM's single pass.

   The limitations already concede that "the paper has to lead with recovery rate". A CVPR OVSS reviewer reads the mIoU table first and finds ±0 at 10–60× the cost.
2. **The load-bearing comparison is against the weakest alternative gate.** R1 and R3 independently make the same argument, and it is the best-argued point in the reviews. The pilot and prediction 2 compare residual presence only with unmasked presence, which by the proposal's own argument fires on every view holding any instance. Beating it is nearly guaranteed by construction. The base pass and the same view pass already supply class-specific "present but unlabelled" evidence at no extra cost:
   - the presence-gated semantic score S_c outside the dilated F_c;
   - sub-threshold SAM 3 query boxes of c that lie outside F_c;
   - "decode-and-diff": decode c unmasked in the view and expand if c-evidence appears outside F_c.

   Without these arms the paper cannot show that *removal* adds information, and the novelty claim "no zoom criterion separates present from present-but-unlabelled" holds only for the triggers the authors chose to list.
3. **The benchmarks do not match the thesis.** All three reviewers raise this. Cityscapes is the only one of the eight benchmarks where zooming adds real pixels. On VOC, Context and COCO a depth-2 view is upsampled about 7.5×, and on ADE20K about 5×, so the eight-benchmark table will mostly show zeros. No high-resolution thin-structure set (Mapillary Vistas, or SegEarth-OV3's remote-sensing domain) is included.
4. **On the one testbed that matters, the gate's selective regime barely exists.** R2 argues this and R1 agrees. Misses on Cityscapes are dense: TAG reports that vanilla SAM 3 fails about 41% of Cityscapes val components, roughly 38 per image [2610.14651]. Nearly every root and most depth-1 children therefore legitimately hold a missed component of some tested class. The ideal residual test is positive almost everywhere, and C3 tends toward (ii), as the proposal concedes for cost. ActiveSAM is stronger than vanilla SAM 3, but the burden of showing sparsity is on the authors.
5. **The write rule excludes the headline targets.** R3 rates this major and R1 minor. I checked the arithmetic and side with R3. SAM 3 tokens are 14 px at 1008, so a view token covers about 14, 8.5 and 5.1 native Cityscapes px at depths 0, 1 and 2. With r_min = 2 tokens, a pole must be at least 28, 17 or 10 px wide to be written at all. Box-plus-half-size containment also caps a depth-2 pole's length at about 185–245 px. The motivating "three distant poles" therefore fall largely outside the reachable set. Expect pole recovery near zero, with compact signs and lights carrying the result.

The main risk to p_core rather than to odds is that removal after the backbone leaks and the model answers from context. All three reviewers raise it, citing the backbone's four global-attention layers [2511.16719], context answering [1703.08448] and token-dropped ViTs that keep their predictions [2204.08945]. The odds condition on the predictions holding, so a passed pilot would neutralise most of this objection. The objection still bites in two ways. First, the pilot's bar ("AUROC above unmasked") is low, so reviewers will doubt a pass. Second, the stated fallback, token dropping inside the backbone per class at 10–18 backbone passes on Cityscapes, would undo the compute story.

## Reviewer claims: accepted, discounted, verified

**Accepted.**
- All three on weakness 1, R1 and R3 on weakness 2, all three on weakness 3, R2 (with R1) on weakness 4, and R3 (with R1) on weakness 5.
- R3, pilot on evaluation labels. The pilot and the choice of removal variant run on Cityscapes val and ADE20K val with GT-derived labels. That contradicts the proposal's own claim that "no hyperparameter is set on evaluation labels" and ActiveSAM's protocol. It is a major issue with a trivial fix (use the train splits).
- R2, prediction 2 is incoherent at the depth-cap budget. There C3 visits a subset of (ii)'s views with the same decode and fusion, so it cannot recover more than (ii). The prediction should be "equal recovery at ≤ X% of (ii)'s cost".
- R1, aspect-preserving overlapping windows are the standard sliding-window protocol of training-free OVSS: ProxyCLIP falls from 36.0 to 13.6 on Cityscapes without them [2503.19777]. Listing them as a novel architectural element is overclaiming, and every gain must be reported over (i).
- R1, "view passes" undercounts cost, because the fusion encoder and decoder scale with the prompt count. Seconds on one 4090 should be the primary x-axis.
- R1 and R3, ordinary multi-scale or sliding-window TTA with score averaging is the baseline a segmentation reviewer expects.
- R3, statistics: "CIs overlap at every budget" allows a win at any one of about 10 budgets × 2 datasets × 2 comparators. A single pre-registered summary with a paired bootstrap is needed.
- R1 and R3, writes bypass ActiveSAM's Exclusive Concept Decoding, which is worth 3.3 mIoU on Cityscapes through rider/person [2606.16996]. Minor, but it must be specified.

**Accepted in part.**
- R3, budget. R3's own worst-case estimate (about 4.7 4090-days per method) agrees with the proposal's. The real problems are that "the three matched baselines" counts three of the six listed, that the D = 3 ablation costs 4× the worst case, and that the SegEarth-OV3 base has no admitted set. R3's total of about 33 GPU-days still fits within 40 on 4090s but not on 3090s. I treat this as a feasibility risk with an obvious trim, not as a decisive weakness.
- R2, "too many moving parts". Matched baseline (iii) shares every other component and already isolates the gate. This is a presentation problem (one clean decomposition figure), not a major weakness.
- R2, "the group-testing frame is decoration". This is true for the rate argument, which the proposal itself disclaims. It is a framing issue only.

**Discounted.**
- R2, "the case rests on recent preprints". The vanilla SAM 3 and SegEarth-OV3 rows hedge it, and a CVPR 2027 reviewer will know ActiveSAM.
- R3's use of [2607.09583] as evidence that presence behaves like a scene prior. Its abstract is a remote-sensing evaluation that repurposes the presence head as a classifier and reports ground-level textual bias. It is indirect and domain-shifted, so I give it little weight. The context-answering risk stands on [1703.08448] and [2204.08945] alone.

**Overlap claims verified with `lit.py biblio`.**
- [2602.04053] Seeing Through Clutter (3DV 2026). Its abstract confirms an iterative object-removal loop orchestrated by frozen VLMs, with "no task-specific training". This refutes the sentence "erase-and-re-ask exists only with a retrained second look". It is class-agnostic, works in pixel space and does not gate zoom, so it is **not a novelty kill**, but it must be cited and the sentence corrected.
- [2303.16891] Mask-free OVIS (CVPR 2023). Its abstract confirms pseudo-masks generated from a frozen pre-trained VLM for offline supervision. It is the same erase-and-re-query principle in a different use, **not a kill**, and it is a second reason to soften the claim.
- [2604.19648] CoCo-SAM3 (Apr 2026) is confirmed as a training-free SAM 3 OVSS method on the same eight benchmarks. It is a missing comparison row and a natural third base, not an overlap.
- [2610.14651] TAG (Oct 2026, under review) is confirmed as diagnosing concept recognition and presence, not mask quality, as SAM 3's bottleneck, and as fixing it with a trained adapter. There is no mechanism overlap. It does challenge the "sampling bottleneck" framing and should be discussed.

## Calibration

The panel rated 3/3/3 with confidences 4/3/4. No [fatal] weakness was raised and I see none. The core idea survives every overlap check, and every decisive weakness can be answered by changing the proposal. The weaknesses are consistent across reviewers and well argued, however. In particular, the paper at threshold has no standard-metric headline, its gate is never compared against the free residual evidence the base pass already has, and its testbed is a single 500-image benchmark on which the gate is unlikely to be selective. That places it in the 1–2 band. I put it at the top of that band, **1.8**, for the crisp trigger and the unusually clean matched-baseline design.

**p_core = 0.45.** I take the load-bearing prediction to be the pilot's second clause together with prediction 2: residual presence falls below τ on enough fully explained views to retire pairs at 90% recall, and C3 then beats (iii) at matched passes. The AUROC clause is near-certain by construction. Context answering through a context-pooling presence token, leakage after the backbone, a τ borrowed from unmasked whole images and dense Cityscapes misses all push against the rest. The lenient "any budget" kill condition partly offsets them. I sit between R1's 0.55 and R2's and R3's 0.40.

If the pilot fails, the paper becomes a negative result plus a matched-tiling study, at about 0.4/10. Risk-adjusted: 1.8 × 0.45 + 0.55 × 0.4 ≈ **1.0**.

## Fixes, ranked by odds gained

Each gain below is in tenths of odds, i.e. points on the 0–10 scale, measured from the current 1.8. The gains overlap and are not additive. Fixes 1–4 together would plausibly lift odds to about 3.5, and all eight to about 3.8–4.0, the "4/3/3, answerable majors" band. Fixes 1 and 2 raise the bar the predictions must clear, so they lower p_core (to about 0.35 with both), and the risk-adjusted odds rise less, to about 1.5.

1. **Commit to magnitudes on standard metrics, tested once, with non-inferiority margins (+1.0, 1.8 → 2.8).**
   - *Change:* rewrite predictions 2, 3 and 7. On Cityscapes, ActiveSAM + C3 beats aspect-preserving tiling (i) by at least +3.0 mean IoU over pole, traffic sign and traffic light, and by at least +0.5 mIoU. It beats ActiveSAM by at least +1.0 mIoU. It reaches the recovery of (ii) at no more than 50% of (ii)'s seconds per image on one 4090.
   - *Margins:* −0.3 mIoU on every other benchmark, and −0.5 stuff and large-object IoU on ADE20K and COCO-Stuff.
   - *Test:* replace "CIs overlap at every budget" with one pre-registered summary, the area under the recovery-versus-seconds curve, compared by a paired bootstrap over images on Cityscapes.
   - *Effect:* the paper at threshold then has a table headline instead of an analysis profile.
2. **Add the free alternative gates as baseline (vii) and as arms of the pilot (+0.8, 1.8 → 2.6).**
   - *Arms:* (a) residual dense score, the maximum of the base-pass S_c outside the dilated F_c; (b) sub-threshold query boxes, SAM 3 instance queries of c with scores in [0.05, 0.3) whose boxes lie outside F_c, cropped SAHI-style; (c) decode-and-diff on the same view pass.
   - *Setup:* identical budget, certification and fusion, with no extra passes, since all three come from passes already run.
   - *Prediction:* residual presence AUROC is at least 0.03 above the best of (a)–(c), and C3's recovery-AUC is above (vii)'s.
   - *Effect:* this is the only experiment that shows removal itself adds information.
   - *Fallback:* if (a)–(c) match residual presence, the paper can be reframed honestly as "residual-evidence-gated zoom with authority fusion" around the cheapest trigger, which keeps the negative branch above 0.4.
3. **Move the evaluation to where zoom adds pixels (+0.5, 1.8 → 2.3).**
   - *Change:* add Mapillary Vistas val (2,000 high-resolution street images, about 0.5–1 GPU-day at the depth-2 worst case) as a primary benchmark next to Cityscapes. Optionally add one SegEarth-OV3 remote-sensing set (iSAID or UAVid).
   - *Demote:* move VOC, Context and COCO-Object to a no-regression table.
   - *Report:* the sparsity statistics R2 asks for, i.e. the fraction of root and depth-1 views with no missed component of any tested class, on Cityscapes, ADE20K and Mapillary. This shows how much the gate can retire.
4. **Make thin structures writable, and show the ceiling (+0.5, 1.8 → 2.3).**
   - *Change the write rule:* replace r_min = 2 view tokens with r_min = 1 token at the view's depth (about 5 native px at depth 2). For elongated segments, replace box-plus-half-size containment with cross-section containment, and stitch partial segments of one class across overlapping children.
   - *Add analyses:* (a) the reachable set, i.e. the fraction of base-missed components writable at some depth ≤ D, binned by narrow-side width and aspect ratio; (b) a GT-guided oracle gate that zooms exactly on missed components, with the same decode, certification and fusion, so readers see where C3 sits between (ii) and the ceiling.
   - *Effect:* without this, pole recovery at threshold is about zero and the title example visibly fails.
5. **Clean up the protocol (+0.3).**
   - *Pilot:* run the pilot, the choice of removal variant and the sensitivity sweeps on Cityscapes train and ADE20K train, not val.
   - *τ:* calibrate a residual-specific τ on the unlabeled COCO train images ActiveSAM already uses for signatures, and report it against the borrowed τ = 0.1.
   - *Leakage:* add R1's diagnostic, comparing presence after key masking with presence after the found instance is inpainted out, on the same views.
   - *Reporting:* give the pilot's positive base rates and AUROC CIs per depth and per class.
6. **Add the baselines a segmentation reviewer expects (+0.3).**
   - *TTA:* standard SAM 3 multi-scale and sliding-window test-time inference with score averaging (scales 1.0, 1.5 and 2.0; 1008 windows at stride 2/3), at matched seconds.
   - *CoCo-SAM3 [2604.19648]:* as a comparison row, and as a third base if time allows.
   - *Pareto plot:* mIoU and small-class IoU against seconds per image on one 4090 as the main efficiency figure.
7. **Fix the claims (+0.2).**
   - *Novelty:* drop aspect-preserving roots from the novelty list and report every gain over (i). Correct the "only with retraining" sentence, citing [2602.04053] and [2303.16891].
   - *Prediction 2:* restate it as equal recovery at a stated fraction of (ii)'s cost.
   - *Framing:* discuss TAG [2610.14651] against the sampling-bottleneck framing, and demote group testing to motivation.
   - *ECD:* specify how writes interact with Exclusive Concept Decoding, e.g. re-score rider/person and bicycle/motorcycle writes with ActiveSAM's class signatures.
8. **Re-budget the plan honestly (+0.1 to odds, large for feasibility).**
   - *Count:* include all six baselines in the budget.
   - *Drop:* the D = 3 ablation, and the CLIP instantiation (or move it to an appendix, Cityscapes only).
   - *Restrict:* the SegEarth-OV3 base to Cityscapes and ADE20K, using ActiveSAM's admitted set.
   - *Contingency:* state a plan in case the cluster assigns 3090s.

```json
{"odds": 1.8, "p_core": 0.45, "odds_risk_adjusted": 1.0,
 "decisive_weaknesses": [
  "At the stated thresholds the paper has no committed gain on any standard metric: a self-defined recovery rate, flat mIoU across eight benchmarks and unquantified pole/sign/light IoU, at up to 43-64 view passes per image against ActiveSAM's single pass.",
  "The residual pooled test is compared only with unmasked presence, which loses by construction. The free same-cost alternatives (base-pass S_c outside the dilated found set, sub-threshold SAM 3 query boxes, decode-and-diff in the same view) are missing, so the paper cannot show that removal itself adds information.",
  "The benchmarks do not match the thesis: Cityscapes is the only set where zoom adds real pixels (depth-2 views are upsampled about 5-7.5x on VOC, Context, COCO and ADE20K), and no high-resolution thin-structure benchmark is included.",
  "On Cityscapes misses are dense (about 41% of components, about 38 per image, fail under vanilla SAM 3), so most views legitimately stay positive, the gate retires little, and C3 tends toward uniform tiling. The regime where the gate is selective and the regime where zoom helps barely overlap.",
  "The write rule (r_min = 2 view tokens plus box-plus-half-size containment) needs at least 10 native px of width at depth 2, so the motivating thin distant poles are largely unwritable at any depth, and pole recovery at threshold will be near zero."
 ],
 "fixes_ranked": [
  "+1.0 (1.8->2.8): Rewrite predictions 2, 3 and 7 with magnitudes. On Cityscapes, require at least +3.0 mean IoU over pole/sign/light and +0.5 mIoU over aspect-preserving tiling (i), at least +1.0 mIoU over ActiveSAM, and (ii)'s recovery at no more than 50% of (ii)'s seconds per image on one 4090. Set non-inferiority margins of -0.3 mIoU on the other benchmarks and -0.5 stuff/large-object IoU. Replace 'CIs overlap at every budget' with one pre-registered recovery-vs-seconds AUC and a paired bootstrap over images.",
  "+0.8 (1.8->2.6): Add baseline (vii) and pilot arms for the free alternative gates: (a) max base-pass S_c outside the dilated F_c, (b) SAM 3 queries of c scoring in [0.05, 0.3) with boxes outside F_c, cropped SAHI-style, and (c) decode-and-diff on the same view pass, all at the same budget, certification and fusion. Predict residual-presence AUROC at least 0.03 above the best of them and a higher recovery AUC. If they tie, reframe around the cheapest trigger.",
  "+0.5 (1.8->2.3): Add Mapillary Vistas val (about 0.5-1 GPU-day at the depth-2 worst case), and optionally one SegEarth-OV3 remote-sensing set, as a primary benchmark next to Cityscapes. Move VOC, Context and COCO-Object to a no-regression table. Report the fraction of root and depth-1 views with no missed component of any tested class.",
  "+0.5 (1.8->2.3): Change the write rule to r_min = 1 token at the view's depth (about 5 native px at depth 2), with cross-section containment and stitching across overlapping children for elongated segments. Report the reachable set of missed components by width and aspect ratio, and a GT-guided oracle gate as the ceiling between (ii) and perfect gating.",
  "+0.3: Run the pilot, the removal-variant choice and the sensitivity sweeps on Cityscapes train and ADE20K train, not val. Calibrate a residual-specific tau on unlabeled COCO train against the borrowed tau = 0.1. Add a leakage diagnostic (key-masked versus inpainted-out presence on the same views), and report the pilot's base rates and AUROC CIs per depth and class.",
  "+0.3: Add standard SAM 3 multi-scale and sliding-window TTA with score averaging at matched seconds, add CoCo-SAM3 [2604.19648] as a comparison row (and a base if time allows), and make mIoU and small-class IoU against seconds per image on one 4090 the main efficiency figure.",
  "+0.2: Drop aspect-preserving roots from the novelty list and report every gain over (i). Restate prediction 2 as equal recovery at a stated fraction of (ii)'s cost, since C3 visits a subset of (ii)'s views. Correct the 'erase-and-re-ask only with retraining' sentence, citing [2602.04053] and [2303.16891]. Discuss TAG [2610.14651], demote group testing to motivation, and specify how writes interact with ActiveSAM's Exclusive Concept Decoding.",
  "+0.1 (larger for feasibility): Re-budget with all six baselines, drop the D = 3 ablation and the CLIP instantiation (or keep CLIP in an appendix, Cityscapes only), restrict SegEarth-OV3 to Cityscapes and ADE20K with ActiveSAM's admitted set, and state a plan in case the cluster assigns 3090s."
 ]}
```
