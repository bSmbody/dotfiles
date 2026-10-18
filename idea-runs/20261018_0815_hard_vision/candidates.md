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
