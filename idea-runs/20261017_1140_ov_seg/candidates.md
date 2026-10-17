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
