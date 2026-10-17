
### C1 verdict

- **Verdict**: `revise(focus=mapping)`
- **Evidence**:
  - **Source grounding is accurate, but it shows where the transfer breaks.** [1001.5311]: C1 states DS correctly: keep a component if y > 0 (Alg 1), Lemma IV.1 removes about half the nulls per step, Lemma IV.2 keeps nearly all signals, about log2 log p + 2 steps, a 0.75 budget ratio, and about 2p total measurements. DS's gain, however, comes from Eq 1. Each component gets its own precision γ_{i,j}, and each step's budget R_j is spread only over the shrinking survivor set, so precision per survivor grows geometrically.
  - **The mapping breaks at the measurement unit.** In C1 the costly measurement is a re-encoded crop. It is paid per location and scores every class at that location at once, while text-side scoring of extra classes costs almost nothing. Budget therefore concentrates only if whole locations are retired, and C1 never says when a location retires.
    - Under DS's own rule, each competing class at a location survives a stage with probability about ½.
    - With independent competitors (my back-of-envelope estimate), a Cityscapes location with 18 competitors is cleared after stage 1 with probability 2^−18. After stage 3 it is (7/8)^18 ≈ 0.09. An ADE20K location with 149 competitors is cleared after six stages only with probability (63/64)^149 ≈ 0.10.
    - So the early stages re-encode almost every location at rising zoom. That is uniform multi-scale inference, the very baseline C1 claims to beat at matched compute, and the "about twice one pass" cost does not carry over.
    - Retiring "confident road, sky and wall interiors" early needs a stricter, location-level threshold. Such a threshold drops the null-median cut on which Lemma IV.2's "almost never discards a true signal" rests.
  - **"Read the final label from the finest look" assumes later looks are strictly more precise, and zoom is not.** DS's last step is the most precise, fresh-noise measurement of the same x_i (Eq 1). Zooming instead raises a thin structure's token share but removes context, and CLIP's errors are systematic, not i.i.d. C1's own sources show the cost:
    - ProxyCLIP's VOC20 score falls from 79.7 to 73.4 when the input grows from 336 to 576 px [2411.09219].
    - LaVG finds that crops suffer part-whole ambiguity, while whole-image recognition lowers accuracy on small-resolution images [2408.04961].

    Surviving locations inside large objects, or on stuff edges, would be relabelled from their worst-context view. C1 needs a cross-scale fusion rule, and DS does not supply one.
  - **Novelty: the supervised precedent for multi-stage magnification is not cited.** MagNet [2104.03778] already zooms progressively through four scales on Cityscapes. It updates only uncertain locations, using a top-1 minus top-2 margin and Q = F(Y_u ⊙ (1−R_u)), and MagNet-Fast processes only the most uncertain patches. C1's "escalate zoom over several stages only where unresolved" is that design made training-free. What C1 genuinely adds is the trigger: per-class survival above that class's own background instead of a margin. That trigger is exactly the part whose mapping is unspecified.
  - **Novelty: training-free class elimination followed by re-measurement already exists, at image level.**
    - CaR [2312.07661] re-encodes the image with CLIP and visual prompts, drops queries with P_ii < θ, and repeats until the set stops changing. It uses no zoom and does not prune per location.
    - ActiveSAM [2606.16996] (2026-06) drops classes using a 336 px presence preview, re-checks the survivors at 1008 px with the same τ, and decodes only those survivors. This is effectively two-stage distilled sensing on the class axis, with resolution as the precision knob, at image level.

    Neither paper zooms per location, so C1's delta (dense, per-location, progressive) is real. It is narrower than "FreeCP [2508.00557] is the closest", and C1 cites none of these three papers.
  - **Positioning: a much stronger training-free baseline exists.** With frozen SAM 3, the same eight benchmarks and no per-dataset tuning, ActiveSAM reaches 73.0 on Cityscapes, 40.0 on ADE20K and 66.0 on average [2606.16996]. In the same table, the CLIP first-pass methods C1 plugs into score 33.9 (ProxyCLIP), 42.9 (Trident) and 51.1 (CorrCLIP) on Cityscapes. ActiveSAM does concede that "prompt filtering can also omit small or occluded objects" and keeps 93.9% of components smaller than 1,024 px. So the gap "re-query where evidence is ambiguous" might still be worth posing on SAM 3 pipelines. As written, though, C1 is a CLIP-patch-score plug-in and will be judged against a 66-mIoU training-free state of the art.
  - **Transfer assumption (ii) is named, and at a median cut it is plausible, but its cited support is off-target.** The evidence that small objects are "localisable at a coarse scale with high recall" comes from AutoFocus's supervised, class-agnostic FocusPixel head, trained on boxes [1812.01600], not from frozen per-class scores. FOCUS [2506.21710] supports (iii) only for one named target in an MLLM.
  - **Contribution type and feasibility pass.** C1 is an inference-time algorithm, so it counts as methodological. It fits the 40 GPU-day budget even if it falls back to full multi-scale inference.
- **Strongest objection in 1 sentence**: DS gains by concentrating a per-component budget on a shrinking survivor set, but in C1 the cost unit is a crop that measures all classes at a location at once, and under DS's median rule almost no location is ever retired (each of its 18–149 competitors survives a stage with probability ½), so elimination does not shrink what must be re-encoded and the method collapses into uniform progressive zoom with class pruning, which sits close to MagNet's uncertainty-gated magnification [2104.03778] and ActiveSAM's two-resolution class elimination [2606.16996].
- **What a revision must specify**:
  - A location-level retirement statistic and its cost accounting. One option is DS run over locations on "max over non-argmax classes of (score − that class's own background quantile)". Another is image-level class elimination first, so that per-location competitor sets shrink before zooming.
  - A cross-scale fusion rule to replace "finest look wins".
  - Explicit positioning against MagNet, CaR and ActiveSAM, and a stated reason to target CLIP pipelines rather than SAM 3 ones, or a demonstration on both.


### C2 verdict

- **Verdict**: `revise(focus=mapping)`
- **Evidence**:
  - **Source grounding is accurate.**
    - [2106.12193]: a test returns the OR of its items' defectiveness. Hwang's binary splitting discards every negative partition in one step and binary-searches the positive ones, using k·log2(n/k) + O(k) tests when k = o(n). Noise is handled by noisy binary search and by repeated tests that certify defectives. C2 states all of this correctly.
    - [2008.06642]: dilution lowers a pool's sensitivity as the pool grows, and false negatives from weak samples are correlated across pools. Also stated correctly.
    - The fusion sources are quoted correctly:
      - SNIP's valid range per scale [1711.08189];
      - AutoFocus's pruning of detections at chip borders [1812.01600];
      - Thm 4 of [2610.09313] (no zoom-out, each crop contains the item's support) and its Prop 8–9 (adaptive zoom saves cost only if coarse views carry graded evidence below one token). Half-recall falls at or below 0.54 tokens per side for all but one of the MLLMs tested.
    - The SAM 3 facts check out:
      - The presence token is "solely responsible" for presence and is kept apart from local localisation. The input is a fixed 1008 square that ignores aspect ratio [2511.16719].
      - ActiveSAM, SegEarth-OV3 and ProC-SAM3 all resize to 1008×1008, and none of them re-encodes a region [2606.16996, 2512.08730, 2606.21863].
  - **The mapping breaks at the test, which is not an OR over defectives.**
    - In group testing a pool is positive if and only if it holds at least one defective [2106.12193]. C2's defective is "the concept is present here but missing from the map". Its test, however, is "the presence head fires AND the concept holds none of the pixels where its own dense evidence peaks in the crop".
    - The presence head fires for any instance of the concept, found or missed [2511.16719]. So one correctly labelled instance of the same class inside the pool makes the concept "explained". The crop then tests negative, and every missed instance in it is retired with the coarse label.
    - This masking effect grows with pool size and with the number of instances per class. That is not the dilution trade-off C2 borrows from [2008.06642]; it is a separate failure that the source does not model.
    - At the root (the base pipeline's whole view) this bites hardest. Poles, traffic signs, traffic lights and people usually appear several times in a street scene, and the base map usually labels at least the most salient one. (This is my estimate; no paper read here reports per-image instance counts.) The root test is therefore negative for exactly the classes and images the gap targets. C2 then fires only when a recognised class wins nothing anywhere in the view.
    - If "unexplained" is read per peak instead ("some evidence peak is not held"), the decision no longer uses the pooled test at all. It becomes a location-level check on the dense map, which is C1's per-location trigger plus a presence confirmation.
  - **On SAM 3, presence at the root carries almost no information about where to look.**
    - Even from a 336 px preview, ActiveSAM's image-level presence admits 93.9% of the ground-truth image–class pairs from components smaller than 1,024 px. Raising the preview to 672 px moves mean mIoU by at most 0.04 [2606.16996].
    - A test that is positive for nearly every present class, whatever the pool size, cannot narrow down the location. C2's children are in fact placed by the parent's dense evidence, as in AutoFocus [1812.01600] and ViCrop-Det [2604.26806], not by splitting the pool.
    - So group testing contributes only a stop rule and a certification rule. The efficiency argument (one negative clears many items) rests entirely on the "explained" clause criticised above.
  - **Novelty: using crop-level recognition of "is the concept in this view?" to decide where to zoom already exists, training-free.**
    - ZoomEye [2411.16044] builds a quadtree over the image. It ranks each sub-patch by the model's own Yes/No confidence for "Is there a o in the sub-patch?", plus "could it be found by zooming further?". For all-instance cues it searches the whole tree and keeps every node with enough existing confidence. It has no per-pixel output, no notion of what a current map already explains, and no rule for which view is authoritative. C2 does not cite it.
    - Against ZoomEye and the in-domain work, C2's real delta is two things: (i) the map-residual trigger and (ii) the "coarsest valid view decides" fusion. The in-domain work differs as follows:
      - ActiveSAM: presence once per image, no crops [2606.16996].
      - SegEarth-OV3: presence per uniform window, used only to suppress categories [2512.08730].
      - ViCrop-Det: one class-agnostic crop stage, fused by NMS [2604.26806].
    - This delta is real. My searches (SAM 3 OVSS, and zoom, crop or tiling for open-vocabulary segmentation, with a 2025-06 recency pass) found no SAM 3 pipeline that re-encodes selected regions. But (i) is exactly the part whose mapping is wrong.
  - **The fusion rule is well grounded and fixes C1's "finest look wins".**
    - Three sources together justify "a zoom may only add its parent's flagged concept, on segments it resolves and contains": SNIP's valid range [1711.08189], AutoFocus's border pruning [1812.01600] and the containment condition of Thm 4 [2610.09313].
    - One consequence should be stated. The rule cannot widen or complete a thin instance that the coarse map already labels, because the concept is "explained" there. Gains are therefore limited to wholly missed segments. The gap's recovery rate measures exactly that, but Cityscapes pole and sign IoU also depends on found instances that are under-segmented.
  - **The transfer assumption is named but supported only indirectly.**
    - C2 states the condition it needs: coarse views carry graded evidence about targets smaller than a token. It supports this with Prop 8–9 and MLLM recall curves from [2610.09313], but no measurement exists for SAM 3.
    - On the hallucination side, partial support comes from SegEarth-OV3. On very large remote-sensing images, its per-window presence filtering "effectively eliminates localized false positives" [2512.08730].
  - **The cheapest competitor is missing from the baselines.**
    - Aspect-preserving uniform tiling with two 1024×1024 tiles undoes Cityscapes' 2× horizontal squeeze for one extra pass.
    - C2's worst case equals uniform tiling at the depth cap, and its fusion rule can be added to uniform tiling as well. The ablations must therefore show that the gate buys the gain, not the zoom or the fusion rule. Two needed ablations: uniform tiling with the same fusion rule, and presence-ranked search (ZoomEye-style) without the residual gate.
  - **Contribution type and feasibility pass.**
    - C2 is an inference-time algorithm on frozen SAM 3. SAM 3 has about 850M parameters [2511.16719] and runs on one 24 GB RTX 4090 [2606.21863].
    - A crop test needs presence only for the flagged concepts, and the worst case is bounded by uniform tiling. The method fits the 40 GPU-day budget.
- **Strongest objection in 1 sentence**: C2's pooled test ("the presence head fires and the concept holds none of its evidence peaks in the crop") is not the OR over defectives that group testing needs, because one correctly labelled pole in a crop makes the class "explained" and retires every missed pole in that crop; so on street scenes with several poles, signs or people the root test is negative exactly where the gap lives, while the presence head, which already admits about 94% of small components at image level [2606.16996], adds no localisation of its own.
- **What a revision must specify**:
  - **A residual pooled test** whose positive means "at least one unexplained instance of the concept is in this crop". Two options:
    - Query presence on the crop with that concept's already-labelled segments masked out, using a visual-prompt edit such as CaR's gray-background prompt [2312.07661]. This restores the OR-over-defectives mapping. The cost of the masked context must be checked.
    - Compare SAM 3's per-query instance hypotheses against the map and flag the uncovered ones. This turns C2 into detection-guided zoom, which must then be positioned against ViCrop-Det [2604.26806] and AutoFocus [1812.01600].
  - **Positioning against ZoomEye** [2411.16044]: say that crop-level recognition as the zoom criterion is borrowed, and that the contribution is the residual trigger plus per-pixel authority fusion for dense OVSS.
  - **The matched baselines**:
    - aspect-preserving uniform tiling;
    - uniform tiling at the depth cap with the same fusion rule;
    - presence-ranked search without the residual gate.
