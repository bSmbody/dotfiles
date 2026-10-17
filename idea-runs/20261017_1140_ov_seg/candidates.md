### C1 — Distilled re-querying: eliminate the confidently absent, zoom on everything else

- **Intuition**: Treat thin and small structures as weak, sparse signals and apply Distilled Sensing's rule, "reject what is confidently null, re-measure the rest more precisely". After the first CLIP pass, drop only the (location, class) hypotheses whose score sits at that class's own background level in the image, then spend the remaining budget re-encoding just the surviving locations at progressively finer zoom against just their surviving classes. A pole then only has to survive elimination, not win a patch, to get a closer look.

- **Gap it attacks**: Axis "small objects and stuff classes in training-free open-vocabulary segmentation", Gap 1 (no stage re-queries the VLM where, and at the scale at which, evidence is ambiguous). The concrete failure is that every refiner redistributes one CLIP pass conditioned on its argmax:
  - LPOSS+ has a fidelity term to that prediction [2503.19777].
  - PixelUp takes a convex combination of neighbouring tokens [2608.02792].
  - PEARL's data term trusts low-peak nodes least [2603.21528].
  - Trident's SAM prompts come only from argmax components [2411.09219].

  A class that wins no patch therefore has nothing to propagate and no prompt. The one re-encoding path, FreeCP [2508.00557], re-queries only classes that survived an image-level redundancy test and already overlap another class's high response. Uniform upscaling is no fix either, because it costs context (ProxyCLIP VOC20 79.7→73.4 [2411.09219]).

  Closing this gap matters because it is exactly the problem's pole/sign failure, and patch quantization alone caps Cityscapes at 73.6 mIoU in the LPOSS oracle [2503.19777]. It would also tell a sampling bottleneck apart from a recognition bottleneck, through the gap's "recovery rate" of small segments that won no patch.

- **Source inspiration**: Distilled Sensing [1001.5311], from statistics and signal processing (multi-stage adaptive experimental design).
  - **The setting:** a sparse non-negative vector is observed in noise under a fixed total precision budget.
  - **The procedure:** DS measures every component crudely and keeps only those whose observation is above the null median (y > 0). It re-measures the survivors with the next budget slice spread over fewer components, and repeats about log log p times.
  - **Why it works:** the crude threshold almost never discards a true signal (Lemma IV.2) yet removes about half of the nulls per step (Lemma IV.1). Precision per survivor therefore grows geometrically while the total number of measurements stays near 2p.
  - **The payoff:** non-adaptive thresholding needs an amplitude of order sqrt(2 log p), because the largest of p null observations grows that fast (Thm II.3, Sec V). DS localizes signals whose amplitude grows arbitrarily slowly and detects constant-amplitude ones (Thm III.1). In simulation that is about a log p gain in SNR (Sec V–VI).
  - **No per-problem tuning:** a fixed schedule (each step gets 0.75 of the previous step's budget, and the first and last steps get equal shares) works across SNRs.

  Two near-domain papers support the visual half of the transfer:
  - AutoFocus [1812.01600]: coarse-to-fine zooming on selected chips keeps detection accuracy at 2.8× fewer pixels. Its "where to zoom" map, however, is a supervised, class-agnostic head.
  - FOCUS [2506.21710]: re-encoding a selected crop with a CLIP-based MLLM recovers details the global view misses (+42% average accuracy for LLaVA-1.5 on fine-grained VQA). It picks the crop by top relevance for one named object.

  Novelty type: recombination-of-distant-concepts.

- **How it maps to this problem**:
  - **Hypotheses:** DS's components become (location, class) pairs. Its "signal" is a class that covers only a sliver of a patch, and its "amplitude" is that class's share of the token's evidence.
  - **Measurement precision:** DS's precision becomes pixels-per-token at a location. Re-measuring means re-encoding a padded, zoomed crop around surviving locations with the same frozen CLIP and the base method's dense-attention modification, which raises the structure's share of each token. Zoom plays the role that averaging more samples plays in DS.
  - **Null level:** DS's null becomes the class's own background score in the image, i.e. how that class scores where it is clearly absent. Survival is judged per class across locations, not by argmax across classes at one location. The argmax plays the role of DS's non-adaptive max-threshold: to win, a weak class must beat the strongest of all competing classes, and that bar rises with vocabulary size. The survival bar does not rise with it.
  - **Class pruning:** elimination also prunes the class axis, so each zoomed crop is scored only against the classes still alive in it. That is the short-vocabulary regime where CLIP is far more accurate (a ground-truth-vocabulary oracle lifts ADE20K 15.6→37.5 [2508.00557]).
  - **Budget:** DS's fixed total budget becomes a token budget matched against uniform upscaling. Locations eliminated early (confident road, sky and wall interiors) keep their wide-context first-pass label and are never zoomed, so stuff keeps its context.
  - **Final decision:** DS's final threshold on last-step observations becomes the final label of each surviving location, read from its finest look, with AutoFocus-style discarding of crop-border predictions [1812.01600].
  - **Placement:** it plugs in after any first-pass method (SCLIP, NACLIP, ProxyCLIP, Trident) and before any refiner (LPOSS, PEARL), which can then propagate evidence that now exists.

- **Why it could work / feasibility**: DS relies on three conditions, and each plausibly holds here.
  - **(i) Sparsity.** Small structures occupy few hypotheses: small objects are 40% of COCO instances but 0.3% of area, and FocusPixels are about 4% of pixels at the finest scale [1812.01600].
  - **(ii) The first crude look shifts a true signal upward, even if it does not make it win.** This is the key assumption. A pole's score at its own patch must exceed the pole score of distant road or sky patches, not beat the building score. It is plausible because sub-patch coverage dilutes evidence rather than erasing it, and because the failure in the gap is losing the argmax, which is a stricter test than this one.
  - **(iii) Re-measurement raises effective SNR.** FOCUS shows that CLIP-based encoders recover small details once the crop is re-encoded [2506.21710]. AutoFocus shows that objects too small to detect at a coarse scale can be localised there with high recall and recognised after zooming [1812.01600].

  Compute: DS's total cost is about twice that of one pass when roughly half of the hypotheses drop at each step. A frozen ViT-B/16 forward on a crop takes milliseconds on one 24 GB GPU. The method is training-free and fits easily in the 40 GPU-day budget across eight benchmarks and ablations. DS's dataset-agnostic schedule also sidesteps the per-dataset knobs criticised in the gap (FreeCP thresholds [2508.00557], PEARL grid [2603.21528]).

- **Novelty vs. closest in-domain work**: The closest is FreeCP [2508.00557]. It re-encodes one fixed-size 112×112 crop per ambiguity group, only among classes that passed an image-level redundancy test and already overlap, and assigns one label per crop. C1 instead:
  - triggers per location when a hypothesis is merely not eliminated;
  - escalates zoom over several stages;
  - labels each token densely;
  - shrinks the local vocabulary as it goes.

  The near-domain work differs in other ways:
  - AutoFocus [1812.01600] learns where to zoom from box labels.
  - FOCUS [2506.21710] zooms on the top region for one named object.
  - The concurrent digital-foveation pipeline [2609.04088] fixates by class-agnostic saliency, with a trained closed-set segmenter, for efficiency.

- **Main risk**: If CLIP's evidence for a sub-patch structure is erased rather than diluted, the survival test fails. The pole's score at its own patch would then be no higher than its background level, so stage 1 eliminates it and it is never re-queried. DS's guarantee rests on the signal shifting the first measurement upward, which must be confirmed empirically before anything else.

### C2 — Zoom as pooled testing: split only the crops where the model recognises a concept the map is missing

- **Intuition**: Treat every crop as a pooled test, as in adaptive group testing. Ask the frozen model's own crop-level recognition (SAM 3's presence head, or CLIP's image-level score for the crop) whether it sees a concept that the current label map does not explain inside that crop. Retire every crop that answers no, together with all its locations, and split and zoom only the crops that answer yes, until the concept is either segmented in a view where it fits or rejected. The looks are then fused coarse-first: a zoomed view may only add a concept its parent flagged, and only on segments it both resolves and fully contains. Zoom can thus add thin structures but never relabels large objects or stuff from a context-poor view.

- **Gap it attacks**: Axis "small objects and stuff classes in training-free open-vocabulary segmentation", Gap 1 (no stage re-queries the vision-language model where, and at the scale at which, evidence is ambiguous). The concrete failure appears in both pipeline families.
  - **CLIP pipelines:** every refiner redistributes one pass conditioned on its argmax: LPOSS+ [2503.19777], PixelUp [2608.02792], PEARL [2603.21528] and Trident [2411.09219]. FreeCP's single crop re-encoding is gated by an image-level redundancy test [2508.00557].
  - **SAM 3 pipelines, the training-free state of the art** (ActiveSAM: 66.0 average mIoU, 73.0 on Cityscapes [2606.16996]):
    - They squeeze every image into one 1008×1008 input regardless of aspect ratio [2511.16719, 2606.16996, 2512.08730], so a 2048×1024 Cityscapes frame loses half its horizontal resolution before the model sees a thin pole.
    - SegEarth-OV3 says the semantic head "blurs the boundaries of small targets or misses them entirely" [2512.08730].
    - ActiveSAM concedes that prompt filtering "can also omit small or occluded objects" [2606.16996].
    - ProC-SAM3's small-object fix only re-aggregates the prompt responses of the same single pass [2606.21863].
    - Presence is used once per image to drop classes (ActiveSAM) or per uniform window to suppress hallucinations (SegEarth-OV3), never to decide where to look closer.

  Closing the gap matters for three reasons:
  - A stage that re-acquires evidence can plug into the strongest pipelines, not only into the CLIP ones that score 34–51 on Cityscapes.
  - It attacks the problem's pole/sign failure where that failure is structural (sampling).
  - The gap's recovery rate then separates a sampling bottleneck from a recognition bottleneck on SAM 3 as well as on CLIP.

- **If improving prior candidate**: This improves C1 (distilled re-querying). It keeps two ideas: a hidden concept only has to beat its own null, not win the argmax, and only unresolved evidence is re-measured. It changes four things, following the C1 verdict.
  - **(a) Measurement unit and retirement.** C1 tested (location, class) pairs, but a crop measures all classes at once, so a location retired only if all of its 18–149 competitors were eliminated. C2 makes the crop the unit, as a pool is in group testing.
    - Each concept gets one pooled recognition decision per crop.
    - A crop stays alive only for a concept that is both recognised there and unexplained by the map. The large classes that already hold the crop are explained and never keep it alive.
    - The recognised set is small: SAM 3 presence at image level admits 7.3 of 81 COCO-Object prompts and 30.8 of 150 ADE20K prompts [2606.16996].
    - A negative crop retires all its locations at once.
  - **Cost of (a).** Each tested crop costs one frozen pass. A positive crop spawns children only where the flagged concept's own dense evidence lies. Cost therefore grows with the number of separate unexplained structures times the zoom depth, not with image area. In the worst case, when every crop is positive, it equals uniform tiling at the depth cap, which is the matched baseline.
  - **(b) Fusion.** "The finest look wins" becomes "the coarsest valid view decides" (see the mapping below).
  - **(c) Positioning.** MagNet, CaR and ActiveSAM are positioned explicitly (see Novelty).
  - **(d) SAM 3 relevance.** The primary instantiation is on SAM 3 pipelines (ActiveSAM, SegEarth-OV3), whose presence head is a native pooled test. CLIP pipelines are the second instantiation.

- **Source inspiration**: Adaptive group testing, from information theory and medical screening.
  - **The mechanism** [2106.12193]: a test pools many items and reports whether any defective is among them. Hwang's binary splitting tests partitions of the items and discards in one step every partition that tests negative. It then binary-searches the positive partitions. This needs k·log2(n/k) + O(k) tests instead of n, which is optimal when defectives are sparse (k = o(n)). Noisy tests are handled by noisy binary search and by certifying candidate defectives with repeated tests.
  - **Dilution** [2008.06642]: in pooled PCR a positive sample is diluted by the pool size, so a pool's sensitivity falls as the pool grows. The pool size is chosen to balance the number of tests against false negatives. False negatives from weak samples are correlated across pools: a sample too weak to detect is missed by every pool that holds it.
  - **Lineage:** Distilled Sensing [1001.5311] supplied C1's lenient "beat your own null" test, but it assumes one measurement per component. Group testing is the variant built for the crop's real situation, where one measurement covers many hypotheses.
  - **Sources for the fusion rule:**
    - SNIP keeps a detection at each pyramid scale only if the object's size falls in that scale's valid range, because large objects are hard to classify at high resolution and small ones at low resolution [1711.08189].
    - AutoFocus drops detections that touch chip borders [1812.01600].
    - Concurrent theory [2610.09313] proves that splitting an image into crops cannot lower the expected accuracy of per-pixel labelling if no crop zooms out and each crop contains the support an item needs (Thm 4). Without that containment, nothing is guaranteed (Prop 4).

  Novelty type: recombination-of-distant-concepts.

- **How it maps to this problem**:
  - **Items and defectives:** the items are image locations. A "defective" is a location where a concept is present but missing from the current label map, such as a pole absorbed into building.
  - **Pool and test:** a pool is a crop. The test is the frozen model's own crop-level recognition of each concept.
    - With SAM 3 this is the presence head, which is "solely responsible" for whether a concept is in its input [2511.16719].
    - With CLIP it is CLIP's image-level score for the crop, the task CLIP was trained for.
  - **When a crop tests positive:** only if some concept is both recognised above its own null and unexplained in that crop. "Unexplained" means it holds none of the pixels where its own dense evidence peaks inside that crop.
  - **The null:** for SAM 3 it is the shared presence threshold, which ActiveSAM already uses unchanged across eight benchmarks [2606.16996]. For CLIP it is the concept's score on crops of the same image where it is clearly absent (C1's null).
  - **Negative pool:** a negative crop retires with all its locations, which keep the coarse, context-rich label.
  - **Splitting means zooming:** children of a positive crop are placed where the parent's dense evidence for the flagged concept is strongest, so the parent localises and the child recognises. Each child is encoded at higher zoom and tested again, so zoom both narrows the location and reduces dilution.
  - **Dilution and pool size:** a thin structure's share of a crop plays the role of a diluted viral load. The root pool is the base pipeline's own view, and the depth cap is the largest zoom.
  - **Certification:** a concept is written only when a zoomed child confirms it with a valid segment. If its recognition drops to its null in every child, it is rejected as a false alarm.
  - **Correlated misses:** a structure the model cannot recognise at any zoom is missed in every crop. That is the recognition bottleneck, and the gap's recovery rate exposes it instead of hiding it.
  - **Fusion: the coarsest valid view decides.**
    - A view is authoritative only for segments that it resolves (enough tokens across the segment's narrow side) and fully contains with a margin. This combines SNIP's valid range, AutoFocus's border rule and the containment condition of [2610.09313].
    - A zoomed view may write only the concept its parent flagged.
    - Everything else keeps the label from the coarsest view, so road, sky, wall and the interiors of large objects are never relabelled from a context-poor crop.
  - **Placement:** on top of ActiveSAM or SegEarth-OV3, or of CLIP first-pass methods, and before any refiner.

- **Why it could work / feasibility**:
  - **Defectives are sparse.** Group testing pays off only when k ≪ n. Small objects are 40% of COCO instances but 0.3% of image area, and FocusPixels are about 4% of pixels at the finest scale [1812.01600].
  - **Pooled recognition is what these models do best.** SAM 3 deliberately separates recognition, which needs global context, from localisation, which is local [2511.16719]. After ActiveSAM's presence filtering, 93.9% of the image–class pairs from components smaller than 1,024 px remain admissible [2606.16996], so recognition of small structures usually survives at image level. C2 asks the same head the same question on smaller pools.
  - **The key assumption is now formally necessary and has near-domain support.**
    - [2610.09313] proves that if a view below some token count reveals nothing about a target, any adaptive zoom policy must pay roughly the cost of uniform tiling. Saving cost requires coarse views to carry graded evidence about sub-token targets (Prop 8–9).
    - Its measurements show recall rising gradually with tokens per object side. Half-recall comes at or below 0.54 tokens per side for all but one of the models tested.
    - These are multimodal LLMs, not SAM 3 or CLIP, so the evidence supports C1's "the first look shifts the signal" assumption rather than proving it. The assumption is now stated as a requirement that any adaptive scheme must meet.
  - **Zooming helps, and gating the fusion matters.** Training-free selective crops beat uniform slicing (SAHI) on small-object AP at higher speed [2604.26806]. Crops beyond the useful number add false positives: going from 5 to 7 crops drops mAP50 from 38.9 to 34.1 [2604.26806]. That is why a zoomed view may only add flagged concepts on valid segments.
  - **Compute.** The method is training-free and runs on one GPU. SAM 3 has about 850M parameters [2511.16719] and runs on one RTX 4090 [2606.21863]. Per-image cost is the base pass plus one pass per tested crop, capped by uniform tiling at the depth cap. By my estimate, eight benchmarks plus ablations fit the 40 GPU-day budget with a wide margin.

- **Novelty vs. closest in-domain work**: The closest is ActiveSAM [2606.16996]. It uses SAM 3 presence once per image, at two resolutions, to drop classes for speed, with no crop and no zoom. C2 uses presence per crop to find concepts the map is missing, to decide where to zoom, and to limit what a zoomed view may add. Other near work differs as follows:
  - MagNet [2104.03778] is trained, selects locations by the top-1 minus top-2 margin (so it cannot see a hidden class outside the top two), and fuses scales with a trained module.
  - CaR [2312.07661] recurrently drops text queries at image level using visual prompts, without zoom.
  - SegEarth-OV3 [2512.08730] applies presence per uniform window, only to suppress categories.
  - ViCrop-Det [2604.26806] crops once, by class-agnostic attention entropy, for closed-set detection, and fuses by NMS.
  - FreeCP [2508.00557] re-encodes one crop per ambiguity group and assigns it a single label.
  - The concurrent theory [2610.09313] gives a uniform safe tiling rule for VLM enumeration and proposes no dense open-vocabulary method.

- **Main risk**: The remaining thin-class error of SAM 3 pipelines may be a recognition limit rather than a sampling one. If zoomed crops do not make SAM 3 segment the poles, signs and lights that the squeezed 1008 px view missed (recovery rate near zero), C2 has nothing to add, and if crop-level presence also hallucinates in context-poor crops, its cost drifts toward uniform tiling with no accuracy gain.
