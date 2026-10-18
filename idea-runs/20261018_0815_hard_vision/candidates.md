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
