### C1 — Simulate-then-infer: the frontier model writes the simulator, a frozen small encoder reads the quantity in context

- **Intuition**: The frontier model cannot see how many teeth a gear has, but it can write a short program that draws gears with any number of teeth in the style of the query image. Render a few hundred such labelled images, embed them and the real image with a frozen small encoder, and let a pretrained in-context posterior estimator infer the quantity for the real image in one forward pass. This is simulation-based inference with the frozen encoder supplying the summary statistics, and the resulting calibrated posterior is handed back to the frontier model as answer-bearing evidence.

- **Gap it attacks**: Axis "perceptual blind spots of frontier VLMs that more reasoning does not fix", Gap 1. Every black-box remedy still ends with the frontier model reading the quantity off pixels: hints, ICL and reasoning effort [2407.06581, 2610.12942, 2605.16410], and task-wise visual prompts that stay near 52% on OverlappingShapes [2603.16250]. The readouts that do recover the quantity are fixed per task: a logistic probe fit on 4.4k–8.9k images from the benchmark's own generator [2407.06581], task-specific heads or LoRA [2506.08008], or a hand-derived kernel for directed noun-pair relations [2610.06324]. Closing the gap would turn one question into a working measurement readout, with no per-task design or training. The frontier model would then get an answer plus a reliability signal that does not come from its own lossy visual pathway.

- **Source inspiration**: Simulation-based inference with a tabular foundation model, NPE-PFN [2504.17660]. When a likelihood is intractable but a simulator exists, sample parameters from a prior and simulate observations. Then place the (observation, parameter) pairs in TabPFN's context; TabPFN was pretrained only on synthetic tabular tasks. It returns the posterior for a real observation without training any network ("bypasses model fitting entirely"). It works in this setting for three reasons. First, TabPFN is a strong in-context density estimator at small budgets: with 10^2 simulations it beats trained flow-based NPE/NLE on all but one SBI benchmark task, and its posteriors are calibrated. Second, keeping only the simulations nearest the observation leaves the posterior unbiased. Third, it degrades more gracefully than NPE when the simulator is misspecified, including on real Hodgkin–Huxley recordings [2504.17660, Sec 2.2–3.3]. Its stated limit is high-dimensional observations, which need a summary or embedding network [2504.17660, App B.3/D.4]. Novelty type: **recombination-of-distant-concepts** (SBI in the physical and neural sciences × black-box VLM perception).

- **How it maps to this problem**:
  - The *scientist's simulator* is a parametric renderer that the frontier model writes for the question. The queried quantity (intersection count, teeth count, which line is longer, overlap or not) is the parameter of interest. Line width, colours, positions and background are nuisance parameters, which the frontier model sets from its own coarse description of the image. It perceives style and layout well; the exact quantity is what it loses.
  - The *prior* is the answer range the question admits.
  - The *summary statistic / embedding net* is a frozen ≤3B vision encoder's (SigLIP/DINOv2-class) pooled patch features, reduced to a few dozen dimensions.
  - The *posterior estimator* is TabPFN run in context on (feature, quantity) pairs from the renders.
  - NPE-PFN's *nearest-simulation filtering* and *sequential truncation* become two steps: keep the renders closest to the real image, then render a second batch concentrated near the first posterior's mode. That concentrates simulations on the hard, near-boundary cases, which are the ones that make frozen-feature readouts robust [2407.06581].
  - The *misspecification check* becomes a distance test. If the real image sits far from every render in feature space, the readout abstains and the frontier answers alone.
  - The frontier model receives the answer distribution, not pixels, and composes the final answer.

- **Why it could work / feasibility**: Each link has a published precedent.
  - The signal is in small frozen encoders and is linearly decodable from average-pooled features: CLIP/SigLIP probes reach ≥99.47% on two-circles and line intersections, where their VLMs fail [2407.06581, Sec 6]. Hidden-in-plain-sight confirms the information survives encoder and LLM layers [2506.08008].
  - TabPFN works as a training-free head on frozen image embeddings after z-norm + PCA. It has the best NLL/ECE of nine heads across 22,820 episodes. Its accuracy is competitive or better at about ≥50 examples per class and d≈8–32, which is a few hundred renders [2607.11007, Exp 1–2]. That matches NPE-PFN's efficiency at 10^2–10^3 simulations [2504.17660].
  - LLMs can write *parametrised* drawing functions and vary them to produce diverse instances of one concept [2401.01862, Sec 4.1], and today's frontier models code far better than the GPT-4 tested there.
  - Cost per question:
    - one frontier call to write the renderer, cacheable per question template;
    - local rendering and encoder passes on a few hundred small images, seconds on one consumer GPU;
    - one TabPFN pass;
    - the final frontier call.

    This is within the "≤ one extra call" bar in gaps.md and the US$1k / 40 GPU-day budget. Nothing is trained.
  - Key assumption: for the targeted families, a short program can render images whose frozen-encoder features vary with the quantity the same way the real images' features do. The quantity's direction in feature space must transfer from renders to the test image, even when pixel styles differ.

- **Novelty vs. closest in-domain work**:
  - Closest is [2407.06581]. Its probes are fit per task on thousands of images from the benchmark's own hand-written generator, as a diagnostic. C1 writes a new simulator per question at test time and reads it in context with no fitting, so a new primitive needs no human design.
  - [2608.00726] has a question-conditioned readout, but it is trained per task over a fixed label space.
  - In [2601.11109] the VLM itself compares renders to the target over up to 10 rounds, so the comparator is the blind pathway.
  - [2604.09531] uses LLM-synthesised data only to fine-tune open VLM weights, so it does not apply to an API model.

- **Main risk**: The gap between simulated and real images. On natural photos (gears, crowds), or on benchmark images whose style the frontier-written renderer does not match, the real image's features may fall off the simulated manifold. The in-context posterior would then be confidently wrong, or the abstain rule would fire so often that coverage collapses. LLM drawing is weakest exactly on "sets of shapes with a specific spatial organisation" [2401.01862], and pooled features dilute localized evidence under clutter [2608.00726].


### C2 — Counterfactual render-and-compare for dial reading: the frontier writes this dial's renderer, frozen DINOv2 patches pick the needle

- **Intuition**: A frontier model can read a gauge's or clock's units, numerals, range and look, but it cannot place the needle to within one minor tick. So let it write a short program that redraws *this* dial with the needle free. A small frozen encoder then compares the photo, patch by patch, against a sweep of renders that differ *only* in the needle. The best-matching needle position is the reading, and the sharpness of the match is its reliability. This is training-free render-and-compare from unseen-object pose estimation, with the needle angle as the "pose" and the frontier-written program as the "CAD model".

- **Gap it attacks**: Axis "perceptual blind spots of frontier VLMs that more reasoning does not fix", Gap 1. The family is now fixed to dial-based measurement reading: pointer gauges, meters and analog clocks. Here the frontier failure is exactly what the gap describes.
  - On MeasureBench's real images the best model reads only 31.5% of dials correctly while getting units right 96.2% of the time. Thinking budgets of up to 10k tokens give "very little improvement". The errors are "one minor tick left/right" in pointer localisation [2510.26865, Sec 3.1–3.4].
  - 2026 frontier models still fail. GPT-5.4 Thinking, Gemini 3 Pro and Gemini 3 Flash fail real gauge reading in nearly every configuration of the dynamic-gauge test [2604.22829]. Gemini-3.1-Pro is within one minute on only 22% of clean clocks [2604.26614, Tab 4]. This sits in the "metrically precise output / small structures" tier that the GPT-6 Astra evaluation leaves open [2609.35718].
  - The readouts that do work are trained. TriSCA retrains a 4B VLM's vision tower and weights on 600K synthetic samples plus real-image GRPO to reach 28.5% on real dials [2604.26614]. The best gauge specialist is trained per family on 12k Blender renders [2308.14583]. Earlier specialist pipelines score 8.5% on MeasureBench real images [2510.26865, Tab 7].
  - Nothing reads the needle *for a black-box API model, on an unseen dial design, without training*. Closing this would turn a 20–30% task into a usable one and give the frontier a reliability signal that does not come from its own lossy visual pathway.

- **If improving prior candidate**: C1's feasibility weaknesses, and what changed:
  - *Task family.* C1 was task-generic and leaned on BlindTest. C2 commits to one family where (i) frontier models still fail in 2026, (ii) the main test images are real photos with no generator to copy (MeasureBench real dials, TickTockVQA real clocks), and (iii) render→real transfer of needle geometry is documented. Gauge readers trained only on Blender renders reach 2–7° error on real gauges [2308.14583]. Spatially exact OpenCV clock renders transfer better than photorealistic diffusion restyles [2603.08011, Sec 5.4.2].
  - *Readout.* C1 used pooled features, reduced with PCA to a few dozen dimensions, as input to TabPFN. C2 uses a quantity-preserving comparison. The renders in a sweep share every nuisance (style, colour, numerals, dial layout) and differ only in the needle. The comparison is therefore confined to the patches the sweep changes, and style mismatch shifts every candidate's score equally and drops out of the ranking.
  - *Evidence for the readout change.* Global descriptors carry "limited information about the object pose" [2311.18809, Sec 4.3]. Pooled MLLM visual features are organised by appearance, not dial state [2604.26614, Sec 3.4]. That is exactly C1's failure, and a within-sweep comparison sidesteps it.
  - *What is kept from C1.* The frontier writes the simulator. Nearest-simulation filtering survives as fitting the dial's layout first [2504.17660]. The answer distribution goes back to the frontier as evidence, and there is an abstain rule.

- **Source inspiration**: FoundPose [2311.18809] (6D pose estimation of unseen objects, robotics/BOP), supported by MegaPose-style render-and-compare as described there.
  - *Mechanism.* Given only a 3D model of a new object, render templates and describe both the templates and the real crop with frozen DINOv2 intermediate-layer patch descriptors. Retrieve the closest templates by bag-of-words, match patches by nearest neighbour, then refine by aligning features on the same frozen descriptors. No object- or task-specific training is needed, and it beats trained RGB methods on seven real BOP datasets [Sec 3–4.2].
  - *Why it works there.* Intermediate-layer descriptors (layer 18 of 23) carry positional as well as semantic information. They therefore give geometrically consistent synthetic-to-real correspondences even on texture-less, symmetric objects. Last-layer, CLIP, SAM and SIFT descriptors do much worse, and a global cls descriptor barely encodes pose [Sec 3.3, 4.3].
  - *Novelty type.* **Recombination-of-distant-concepts**: training-free model-based pose estimation × black-box VLM measurement reading, with the frontier model supplying the "CAD model". It is also positioned as SuS-X/RECOUNT-style test-time synthesis [2211.16198, 2608.20621] extended from categories to a measured quantity.
  - *Acknowledged prior work.* LLM-written simulators feeding simulation-based inference already exist, with trained estimators and scientific simulators; counts there were "only weakly identified" at pixel scale [2607.17540].

- **How it maps to this problem**:
  - *The CAD model* becomes a parametric dial program the frontier writes from the photo. The frontier fills in what it sees reliably: instrument type, unit, printed numerals and range, face and needle colours, needle shape, number of hands. It leaves free the things it reads poorly, namely the scale's arc span and zero position, the needle angle(s), and the dial's tilt.
  - *The object mask and perspective crop* become a dial crop from a small open-vocabulary detector, rectified to a canonical view.
  - *Template retrieval* becomes the first stage: render layout variants with the needle masked out (arc span, zero offset, tilt) and keep those whose patches best match the photo. This is NPE-PFN's "keep the nearest simulations" step [2504.17660].
  - *Pose hypotheses* become the second stage, a counterfactual sweep. Hold the fitted layout fixed and render the needle (for clocks, both hands jointly) at every candidate reading. Score each render against the photo only on the patches whose descriptors the sweep changes.
  - *Featuremetric refinement* becomes a finer local sweep around the best candidate, to get below the 14-px patch grid.
  - *The pose estimate* becomes a distribution over readings built from the sweep's similarity profile. A sharp single peak means a confident reading. A flat or multi-peaked profile, or a weak best match, means abstain, and the frontier answers alone.
  - *The final answer.* The frontier gets back the reading distribution in its own units and composes the answer. It never has to re-read the needle.

- **Why it could work / feasibility**:
  - *The needed transfer is documented for exactly this geometry.*
    - Frozen DINOv2 intermediate patches match renders to real photos well enough for 6D pose without training [2311.18809].
    - Needle angle learned only from rendered gauges transfers to real photos at about 2–5° error under natural light, distance, dim light and glass reflection [2308.14583, Tab 2].
    - For clocks, spatially exact simple renders transfer better than photorealistic ones [2603.08011]. A frontier-written program gives spatial exactness, not photorealism, which is the property that matters.
  - *The division of labour matches what frontier models can and cannot do.* Units are read correctly at >90%, and in-band digits are read near-perfectly [2510.26865, 2604.22829]. The dynamic-gauge authors themselves recommend VLMs for "instrument type recognition, context-aware calibration" and deterministic geometry for the needle [2604.22829].
  - *The comparison does not need appearance-invariant state features.* TriSCA's diagnosis says off-the-shelf features fail to cluster the same state *across appearances* [2604.26614]. The sweep never asks for that. It only asks which of several renders, all in one appearance, best matches the photo at the needle's patches. That is the within-template matching FoundPose relies on.
  - *Cost and compute.*
    - Frontier side: one call to write the renderer and at most one call to compose the answer.
    - Local side: a few hundred 448-px renders through DINOv2-L, seconds on one RTX 4090. Nothing is trained.
    - Budget: about 700 MeasureBench real dials plus a TickTockVQA subset fit within the US$1k and 40 GPU-day limits.
  - *Committed effect.* On MeasureBench real dials (711 images), raise the frontier from about 31% (best published) to ≥50% accuracy, above the trained TriSCA's 28.5%. On TickTockVQA, gain ≥15 points over the frontier alone.
  - *Cross-generator check.* Renderers are written blind to every benchmark generator. Results are reported on real photos (no generator), on MeasureBench's own synthetic dials (a different, LLM-drafted generator [2510.26865, Sec 2.4]) and on real clocks.
  - *Key assumption.* A frontier-written dial program puts the scale arc and needle shape close enough to the photo that, after layout fitting, the needle's patches dominate the sweep's score differences.

- **Novelty vs. closest in-domain work**:
  - Closest is TriSCA [2604.26614]. It retrains a VLM's vision tower and weights so its features become organised by dial state. C2 trains nothing, works through a black-box API model, and avoids needing state-invariant features by comparing counterfactual renders of the same dial.
  - [2308.14583] trains a reader per instrument family on 12k Blender renders.
  - VIGA [2601.11109] uses render-and-compare, but the comparator is the VLM itself over many rounds.
  - [2607.17540] uses trained estimators on scientific simulators.
  - SuS-X and RECOUNT synthesise categories, not quantities [2211.16198, 2608.20621].

- **Main risk**: The needle is a few pixels wide inside 14-px patches. When the real dial has glare, a shadowed needle, or a layout that the frontier-written renderer gets wrong (for example the arc's zero position or a non-linear scale), the sweep profile may come out flat or peak on the shadow. The abstain rule would then fire on many images, and coverage, not accuracy, would cap the gain.


### C3 — Unwrap the dial: frontier-read numerals as the coarse code, the photo's own ticks as the fine phase, and a needle-only counterfactual sweep

- **Intuition**: A dial is a multi-frequency phase measurement. Its numerals, and the frontier model's own rough reading, are coarse but unambiguous. Its tick ring is precise but periodic. On a clock, the hour hand is the coarse phase for the minute hand. Structured-light scanners read such signals hierarchically: the coarse signal only picks *which period*, and the fine signal, measured directly, gives the value. C3 reads a dial the same way:
  - the frontier supplies only the coarse code (numeral values, unit, scale type, which hand is which);
  - the photo's own tick lattice supplies every measured angle;
  - a needle-only render-and-compare sweep places the pointer between its two neighbouring ticks.

- **Gap it attacks**: Axis "perceptual blind spots of frontier VLMs that more reasoning does not fix", Gap 1, restricted to dial-based measurement reading.
  - *Concrete failure.* On MeasureBench real dials the best model is right 31.5% of the time while getting the unit right 96.2% of the time. The errors are "one minor tick left/right", and thinking does not help [2510.26865]. The quantity is lost in the frontier's encoder-to-language readout.
  - *What prior approaches miss.* Pipelines that measure geometry are trained and break on unseen designs: 8.5% on MeasureBench real images [2510.26865]. DialBench's trained reader "struggles to predict well on meter images it has never seen before" [2511.21982]. Nothing gives a black-box frontier model an answer-bearing reading of an unseen dial without training.
  - *Why closing it matters.* A training-free reader that turns a 30% task into a usable one shows that a "hard vision" failure is a readout failure, not missing knowledge. It also hands the frontier a reliability signal that does not come through its own lossy visual pathway.

- **If improving prior candidate**: Improves C2, which fitted the scale by matching an approximate frontier-written render against periodic tick rings and so invited the very one-tick aliasing that defines the failure.
  - *Scale.* The scale is no longer fitted by render matching. It is measured from the photo. The frontier gives values; local geometry gives angles.
  - *Aliasing.* Aliasing becomes a rounding problem with a margin. Each level of the scale hierarchy (numerals → major ticks → minor ticks) only has to choose the right period of the level below, and each level is measured directly.
  - *Locality.* The reading is local: the needle's fraction of the interval between its two neighbouring measured ticks. An error in arc span or zero position therefore no longer shifts the whole scale. Values attach to tick indices rather than to a global linear angle model, so non-linear scales need no special case.
  - *Needle.* The render-and-compare sweep is kept for the needle only. Its "model" is now a 2D silhouette with a handful of parameters (taper, tail or counterweight, hub, colour). Shape variants are enumerated as nuisance templates, so no exact CAD model is assumed.
  - *Evaluation.* C3 names the frontier + classical needle-line hybrid as the key baseline, measures the GPT-6-class baseline before claiming any delta, and replaces the unsupported "≥50%" with a pilot-gated commitment.

- **Source inspiration**:
  - *Multi-frequency temporal phase unwrapping from optical 3D metrology* [1903.09836].
    - A high-frequency fringe gives precise but 2π-ambiguous phase. A low-frequency one gives unambiguous but imprecise phase. The integer period index comes from rounding the scaled difference between the two.
    - Rounding is exact as long as the combined error stays below half a period. The admissible error shrinks as the coarse-to-fine ratio grows, so practitioners unwrap hierarchically, step by step through intermediate frequencies. The precision of the result always comes from the fine phase [Sec II-B].
    - Errors appear as whole-period jumps, the analogue of the one-tick reading error.
  - *Joint multi-hypothesis unwrapping* [1608.05209] (time-of-flight depth).
    - Sequential CRT unwrapping "propagates" early errors. Enumerating every plausible unwrapping near the wrap-around points and ranking them jointly guarantees that the true maximum is checked.
    - The winning hypothesis's density then doubles as a single confidence threshold for outlier rejection, which gave 52% more valid measurements [Sec 2.2, 3.2, 4.5].
  - *Needle sweep* (in-domain, kept from C2): frozen DINOv2 intermediate patch descriptors give render-to-real correspondences on texture-less shapes without training [2311.18809].
  - *Novelty type*: **recombination-of-distant-concepts** (optical-metrology phase unwrapping × black-box VLM dial reading), plus a reinforced in-domain link (render-and-compare restricted to a low-parameter needle).

- **How it maps to this problem**:
  - *The coarse unambiguous phase* is supplied in one frontier call: numeral values with their rough clock positions, unit, scale direction and type (linear, non-linear, multiple scales), the pointers and their roles, and the frontier's own reading. Frontier models read these reliably: units 96.2% [2510.26865], in-band digits near-perfectly [2604.22829]. Its own reading errs by about one minor tick, far inside half a major interval, so it is a valid coarse code even when it is a wrong answer.
  - *The fine periodic phase* is the photo's tick lattice. After dial detection and rectification, unwrap the annulus around the pivot into a strip, as MeterFL does [2609.31998]. Measure every tick's angle there, and tell major from minor ticks by length.
  - *The hierarchy of frequencies* is the dial's own hierarchy:
    - numeral → which major tick (margin: half a major interval);
    - major tick → which minor tick (counted locally between two measured majors, not from the scale start, so a missed tick corrupts one interval rather than every later index, unlike MeterFL);
    - minor tick → the needle's fraction of its interval.
    - For multi-dial electricity meters, each dial is the next decade. For clocks, the hour hand is the coarse phase of the minute hand, with a fixed ratio of 12.
  - *Joint hypothesis ranking*. C3 does not round level by level. It enumerates the few neighbouring unwrappings at each ambiguous step, including tick-count ±1, numeral-to-tick assignment ±1 and hand-role swap. It scores them jointly by agreement among the numerals, the lattice, the needle and the frontier's coarse reading. The margin of the winner over the runner-up is the reliability; a low margin means abstain.
  - *The needle*. Render the needle silhouette alone, in a small set of shape variants, at candidate angles within a window around the frontier's coarse reading. Compare each render with the photo on the frozen-feature patches the sweep changes, as in C2. Then refine the winner at native resolution against the two flanking ticks.
    - What the sweep handles that a frontier + Hough/line-fit hybrid cannot:
      - *Shadows and glare.* A line fit takes the strongest straight edge. The silhouette score needs the hub, tail and tip shape, so it rejects a shadow offset from the pivot and bridges glare gaps. Reitsma's segmentation breaks on needle shadows and on white-on-white needles (IoU 0) [2404.08785].
      - *Counterweights.* A line is 180°-symmetric, and Reitsma settles tip versus tail by a "closer end" heuristic [2404.08785]. The silhouette is asymmetric.
      - *Tapered, spade or hollow hands.* Edge-based line fits lock onto one flank or onto the cut-out. The silhouette is centred on the needle's axis.
      - *Multi-hand clocks.* Hough returns unlabelled lines. The joint sweep labels hands by length and width and checks that the hour hand sits where the minute hand implies, using the angle coupling [2603.08011]. This rejects the hour/minute swaps that TickTockVQA needed Swap-DPO training to suppress.
    - *What the sweep does not handle.* Non-linear scales are handled by the scale module, not the sweep. On crisp, high-contrast single needles the hybrid should match C3, and the claimed delta lives in the nuisance subsets.
  - *The answer*. The frontier receives the reading in its own units, plus the margin and the abstention flag.

- **Why it could work / feasibility**:
  - *Each half of C3 already works in prior systems; what was missing is having both halves together.*
    - With a 2-gauge reader that anchors the scale on the photo's own numerals, the error is 0.77–1.15% of the range whenever its OCR reads at least two numerals. OCR, however, fails on 40–57.5% of images and is what made it collapse (444% error over all images) [2404.08785]. MeasureBench shows the frontier reads units at 96.2% versus 17.8% for that OCR [2510.26865]. In C3 the frontier takes exactly the role that broke.
    - Explicit tick geometry with known metadata reaches 87.2% within two minor divisions and beats fine-tuned 7B VLMs [2609.31998]. In C3 the frontier supplies the metadata that MeterFL assumed.
    - Reitsma's interpolation between numeral anchors (about 1–2% of range, roughly one minor division) is not enough. Snapping to the measured minor-tick lattice is what C3 adds.
  - *The unwrapping condition is plausible here.* The source's condition is that the coarse error stays below half the next period [1903.09836].
    - Dial scales step by small ratios (2, 5 or 10 minor per major), unlike the 16–64 fringe ratios that strain MF-TPU.
    - Numeral positions sit beside their major ticks. The frontier's coarse reading is off by about one minor tick, well under half a major interval.
    - Joint ranking guards against the residual error propagation [1608.05209].
  - *The needle sweep's model is now small.*
    - A 2D needle needs a few shape parameters. Enumerating a few variants is FoundPose's template retrieval over a tiny, near-exact model space [2311.18809].
    - The window around the frontier's reading removes distant aliases (scale marks, bezel edges).
    - Rendered needle geometry carries a transferable signal of about 2–5° on real gauges, though that was shown with a trained reader [2308.14583].
  - *Cost.*
    - One frontier call per image, plus an optional compose call.
    - Locally: a detector, a polar unwrap and about 100 needle renders through DINOv2-L, about a second on one RTX 4090.
    - No training is needed. Optionally, a 30M tick segmenter can be trained on MeterFL's public masks in GPU-hours [2609.31998].
  - *Baselines.* All are measured on the same images:
    - GPT-6 Astra alone at default and high reasoning effort, with per-call cost measured;
    - **key hybrid A**: frontier semantics + numeral-anchored linear fit + Hough/line needle (Reitsma with the frontier replacing OCR);
    - **key hybrid B**: frontier semantics + C3's unwrapped tick lattice + Hough/line needle, which isolates the sweep;
    - TriSCA's published 28.5% for reference [2604.26614].
  - *Pilot-gated commitment.* No delta is claimed before the pilot.
    - Pilot set: 100 stratified MeasureBench real dials held out of the final test (single needles, clocks, multi-dial meters, glare, shadows), at a few hundred API calls, done by about 2026-10-26.
    - Gate: the full study goes ahead only if C3 beats Astra by ≥15 points and hybrid B by ≥8 points, with bootstrap lower bounds above zero.
    - Committed number: the pilot's lower bound, reported on the remaining ~611 real dials and on TickTockVQA, together with an oracle split (ground-truth needle → scale-only accuracy, and the reverse).
    - If the sweep fails the hybrid-B gate, the paper reports hybrid B as the method, still a training-free frontier-plus-geometry reader, and states the needle result as negative.
  - *Key assumption.* On most real MeasureBench dials the tick lattice is resolvable after rectification at the available resolution. Where it is not, C3 must abstain rather than guess.

- **Novelty vs. closest in-domain work**: The closest prior systems are Reitsma et al. [2404.08785] and MeterFL [2609.31998].
  - Reitsma anchors the scale on OCR'd numerals, interpolates linearly between them, and fits a line to a segmented needle.
  - MeterFL counts a trained tick segmentation from the scale start with metadata supplied.
  - C3 uses numerals only as the coarse code of a hierarchical, jointly ranked unwrapping onto the measured tick lattice. The frontier reads the code, and a needle-silhouette sweep with clock-hand coupling locates the pointer. Nothing in the pipeline is trained.
  - Searches found no dial or gauge reader that uses phase unwrapping: "phase unwrapping gauge", "gauge reading", "pointer meter", "clock hands hour minute", "scale tick detection" and "gauge VLM", with `--since` 2025-10 recency runs.
  - Recent readers are trained: DialBench [2511.21982], TriSCA [2604.26614] and Swap-DPO [2603.08011].

- **Main risk**: On low-resolution web photos the minor ticks may not be resolvable after rectification. The fine phase is then missing, and C3 either abstains often (coverage caps the gain) or falls back to numeral interpolation, which sits at the one-tick tolerance.
