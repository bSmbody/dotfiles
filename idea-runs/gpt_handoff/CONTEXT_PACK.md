# CONTEXT PACK — IdeaScientist hand-off (2026-10-18)

Sections: A. problem.md (problem + constraints)  B. current best proposal report.json (v2)  C. latest simulated-panel reviews R1–R3 and AC meta-review  D. panel prompts and calibration  E. IdeaScientist role prompts (gap_finder, innovator, reviewer, report_writer)

---
## A. problem.md

# Cheaply closing the remaining visual blind spots of frontier VLMs

## Problem definition
Frontier VLMs (e.g. GPT-6 Astra) now solve many vision tasks zero-shot, but systematic evaluations show families of "hard vision" tasks where they remain clearly below specialist models or humans. Given a frontier VLM used as a black box through its API, and small open models that can run locally (≤ 3B vision models, ≤ 8B VLMs), build a method that lifts the frontier model's accuracy on one such family of hard-vision tasks — by what it is shown, what tools it can call, or how its answer is verified — at small added cost, without training the frontier model. Input: image(s) and question/task. Output: the answer. Evaluation: accuracy on the established benchmarks for that task family, plus API cost and latency, against the frontier model alone and against the specialist.

## Challenge
The remaining failures are not uniform: some are perceptual (fine geometry, exact counting, small or thin structures, precise localisation, low-level properties), where more reasoning tokens do not help because the needed signal is lost in the model's visual encoding; others are failures to use visual evidence the model has. Generic remedies — longer reasoning, zoom-in crops, tool calls to detectors chosen by the model itself, majority voting — help unevenly, cost many calls, and the frontier model does not know when its own visual reading is unreliable, so it calls tools at the wrong moments or overrides a correct tool output. Concrete failure: asked how many teeth a gear has, or which of two thin lines is longer, the frontier model answers confidently and wrongly; given a crop or a detector output it sometimes still trusts its first impression.

## Constraints
- **Venue and deadline**: CVPR 2027 main track. Paper deadline 2026-11-16 AoE; today is 2026-10-18, so every experiment must finish by about 2026-11-09.
- **Compute**: at most 2–4 consumer GPUs with 24 GB each (RTX 3090 / 4090), shared cluster, single-GPU jobs; the whole paper ≤ 40 GPU-days. Open VLAs that fit: π0 / π0.5 (~3B), SmolVLA (~0.5B), OpenVLA-OFT (7B, inference or LoRA), GR00T-class (~3B); open VLMs up to ~8B for inference or LoRA. No large-scale VLA pre-training.
- **Frontier-model access**: API access to one frontier model (e.g. GPT-6 Astra) as the system being helped, a teacher or a reference; total API spend for the paper must stay modest (assume about US$1,000; the per-call cost must be measured, not assumed). The point of the work is to need the frontier model less, not more.
- **Data**: public benchmarks and checkpoints only.
- **Team**: a small group experienced with diffusion transformers and RL post-training; engineering risk counts against an idea.
- **Literature**: no cutoff — search up to today. arXiv work from the last 12 months counts as prior or concurrent work; frontier-model evaluation work from Sept–Oct 2026 (e.g. what GPT-6 Astra still gets wrong in vision) is the immediate context.
- **Significance bar**: a simulated CVPR panel will judge the result. Thin deltas over 2026 work and directional-only predictions have been rejected before; prefer a contribution that gives a new capability or a decisive cost/performance change, with a committed effect size on a standard benchmark.

---
## B. report.json (v2, current best: odds 3.5/10, risk-adjusted 1.4/10)

```json
{
  "title": "Read the Labels, Measure the Ticks: A Frontier-Independent Labelling Margin for Training-Free Instrument Reading with a Black-Box VLM",
  "topic_relevance": {
    "sub_topic": [
      "Perceptual blind spots of frontier vision-language models",
      "Analog instrument, scale and clock reading (visual measurement reading)",
      "Training-free tool augmentation and selective prediction for black-box VLMs"
    ],
    "primary_focus": [
      "Moving the fine-grained measurement out of the frontier model's encoder-to-language readout and into locally measured tick and pointer geometry",
      "A jointly ranked set of scale labellings whose margin is a reliability signal that never passes through the frontier's own visual reading",
      "Committed, pilot-gated accuracy and cost changes on MeasureBench real dials, two further public real-dial sets with frozen thresholds, MeasureBench linear scales and TickTockVQA, under a measured API budget"
    ]
  },
  "one_sentence_thesis": "Let the frontier model read what an instrument's numbers mean, measure every tick and pointer locally, and trust the reading only when one scale labelling clearly wins.",
  "core_problem": {
    "problem_statement": "Frontier VLMs read the unit and the rough scale of an analog instrument correctly but get the value wrong: the best reported model is right on 31.5% of MeasureBench real dials and 21.9% of real linear scales while reading the unit 96.2% of the time, and extra thinking barely helps [2510.26865]. The needed signal, the exact position of a thin pointer or meniscus relative to a periodic tick lattice, is lost in the model's visual readout, while trained readers that measure it break on unseen designs [2510.26865][2404.08785][2511.21982].",
    "why_it_matters": [
      "Reading gauges, scales and clocks is a basic industrial-inspection and assistive task, and 2026 frontier models still fail it on real gauges while reading in-band digits almost perfectly [2604.22829]; on real industrial scenes the best of 24 MLLMs reaches 25.7% joint value-unit accuracy [2609.04014].",
      "The failure is a readout failure, not a knowledge failure: models identify the instrument, unit and major spacing but miss ticks or whole intervals, answer '10:10' on 11.9-29.7% of real clocks, and do not improve with reasoning [2510.26865]; Astra-style higher reasoning effort costs up to 13.22x and does not close fine-geometry gaps [2609.35718].",
      "Black-box remedies studied so far still end with the frontier model reading pixels (prompts, visual prompts, hints, demonstrations) [2407.06581][2603.16250][2605.16410][2610.12942], and tool-trust arbiters use the same blind model as the judge [2610.04836][2512.06373]; token confidence of a VLM gauge reader yields errors at confidence >= 0.99 [2608.17723].",
      "A 2026 gauge study recommends exactly the split of VLM for semantics and deterministic geometry for the needle, but only as design guidance from three instruments on video [2604.22829]; no one has built it on broad real-image benchmarks, measured when it fails, or given it a reliability signal.",
      "Trained readers modify weights and stay near or below the frontier on real dials (TriSCA 28.5% vs 31.5%) [2604.26614], DialBench's reader 'struggles to predict well on meter images it has never seen before' [2511.21982], and synthetic-data training transfers weakly to real images [2510.26865][2603.08011]."
    ],
    "concrete_example": "A photo of an ammeter whose pointer sits on 20 A: GPT-5 answers 26 A with the correct unit [2510.26865]. The Reitsma modular reader, which anchors the scale on OCR'd numerals, fails OCR on 40-57.5% of images [2404.08785] and scores 8.5% on MeasureBench real images [2510.26865]. On a real wall clock showing 4:37 a frontier model answers '10:10', the output GPT-5 gives on 20.34% of real clocks [2510.26865], and a Sobel+Hough clock reader returns unlabelled lines that score under 10% on in-the-wild clocks [2111.09162]. The proposed system reads the 20 A case as: frontier says box 'C' = 20 and unit A; local geometry puts the pointer 0.02 minor divisions past the major tick labelled by box 'C'; the next-best labelling (box 'C' attached one major over) scores far lower, so it answers 20 A."
  },
  "key_novelty": {
    "main_idea": "A frontier-independent labelling margin over locally measured scale geometry",
    "explanation": [
      "The frontier model only names things (numeral values in lettered boxes, unit, scale type, pointer roles); every position, tick count and pointer angle is measured locally from the photo.",
      "All nearby ways of numbering the measured ticks (numeral one tick over, a missed tick, swapped hands, reversed direction) are scored together; the gap between the winner and the best answer-changing rival decides whether to answer.",
      "The same labelling-and-margin machinery is run on circular dials, clocks and straight linear scales, and is tested with frozen thresholds on datasets it never saw."
    ]
  },
  "problem_definition": {
    "formal_setting": "Given an image I of an analog instrument and a question q, recover the reading y (value and unit). After rectification, a circular dial is parameterised by a pivot c and an angle coordinate, and a linear scale by a fitted scale axis and an arc-length coordinate; in both cases the scale is a 1D coordinate u. Locally measured evidence is: tick positions T = {t_1 < ... < t_N} with lengths l_i, numeral boxes B = {(b_j, u_j)} with positions u_j, and indicator positions phi_1..phi_K (pointers, liquid level, object endpoints). The frontier model F, a black box, returns per-box values v_j or 'not a scale numeral', the unit, the scale type s (linear, non-linear, multiple scales) and indicator semantics, but no positions. A labelling hypothesis h = (pi, delta, d, rho) assigns numeral boxes to major-tick indices (pi), inserts or deletes at most one minor tick per major interval (delta), fixes the scale direction (d) and assigns indicator roles (rho: hour/minute/second, decade order, or object start/end). V_h maps a coordinate to a value by local interpolation between flanking labelled ticks. We seek h* = argmax_h S(h; T, B, v, phi) and the margin m = S(h*) - max{S(h): |V_h(phi) - V_h*(phi)| > tol}, where tol is half the measured minor-tick value, computed without ground truth. Output y = V_h*(phi) if m >= tau_m and the pointer-fit quality q >= tau_q, otherwise abstain and fall back to F's own reading y_F.",
    "inputs": "One RGB image of an analog instrument (single-pointer gauge, multi-hand clock, multi-dial meter, or single-scale linear instrument) and a natural-language reading question; one API call to GPT-6 Astra at default effort per image; frozen local models on one 24 GB GPU.",
    "outputs": "The reading in the instrument's unit (or h:mm for clocks), the labelling margin m, the pointer-fit quality q, an abstain flag, and the intermediate evidence (labelled tick lattice, numeral-to-tick assignment, indicator position) that can optionally be handed back to the frontier model."
  },
  "key_terms": {
    "labelling hypothesis": "One complete guess of how the measured ticks are numbered: which major tick each numeral belongs to, whether a minor tick was missed or spurious, the scale direction, and which pointer or endpoint has which role.",
    "labelling margin": "How much better the best labelling explains the evidence than the best rival labelling that would change the answer by more than half a minor division; a small margin triggers abstention.",
    "frontier-independent": "Computed only from local measurements and the frontier's symbolic answers (numeral values, unit), never from the frontier's own reading, confidence or self-agreement.",
    "tip refinement": "A native-resolution, pixel-space fit of the pointer axis from cross-section centroids on concentric circles, seeded by a coarse pointer angle; its precision does not depend on any feature-map patch size.",
    "paste-and-compare sweep": "Compositing a needle silhouette onto the photo at candidate angles and scoring how little the image changes; used only to pick the coarse pointer angle, tip versus tail, and needle versus shadow.",
    "better-views baseline": "GPT-6 Astra given the same rectified crop, unwrapped strip and lettered tick and numeral marks that the method computes, but not the computed answer.",
    "Astra-best": "The single Astra configuration (effort level, tools, views) with the highest pilot accuracy, chosen on the pilot and then fixed for every test set, so the baseline is not a max over noisy test runs.",
    "gain decomposition": "Gain over a baseline B = coverage x (method accuracy on answered items - B's accuracy on the same items) + (1 - coverage) x (fallback accuracy - B's accuracy on abstained items).",
    "coverage": "The fraction of images on which the method answers instead of abstaining.",
    "frozen thresholds": "All score weights and thresholds set once on 200 MeasureBench pilot dials, committed with the code hash and image lists on 2026-10-28, and applied unchanged to every other set."
  },
  "related_work": [
    {
      "sub_area": "Frontier VLM evaluation on measurement reading and hard vision",
      "what_it_does": "MeasureBench scores 18 VLMs on 1,272 real instrument images (711 dial, 361 linear, 96 digital, 104 composite) by per-image value intervals; the best model reaches 31.5% on real dials and 21.9% on real linear scales with 96.2% unit accuracy, thinking barely helps, clocks and multi-needle dials are hardest, and real clocks trigger a '10:10' prior [2510.26865]. 'Lost in Motion' evaluates 2026 frontier models on videos of three instruments, finds they fail gauges but read digits near-perfectly, and recommends hybrid architectures with VLMs for 'higher-level semantic tasks' and deterministic edge/Hough pipelines for the needle, plus rule-based validation [2604.22829]. InSituMeasure scores 24 MLLMs on 2,922 real industrial tasks with answerability labels, best 25.7% [2609.04014]. The GPT-6 Astra evaluation shows higher effort and built-in tools close some gaps at 1.04-13.22x cost while metric and fine-structure gaps remain [2609.35718].",
      "open_gap": "These are diagnoses or design guidance. The semantics/geometry split is credited to [2604.22829]; what none provides is a built, single-image system evaluated on broad real-image benchmarks, a reliability signal for when the split fails, or a test of whether the gain comes from measurement or from a better view. Astra has not been measured on dials.",
      "citations": [
        "2510.26865",
        "2604.22829",
        "2609.04014",
        "2609.35718"
      ]
    },
    {
      "sub_area": "Trained dial and clock readers",
      "what_it_does": "TriSCA aligns a 4B VLM's visual tower on 400K synthetic triplets, then applies SFT and real-image GRPO, reaching 28.5% on MeasureBench real dials [2604.26614]. DialBench's MRLM injects CLIP template features via cross-attention and MoE, trained end to end on RPM-10K [2511.21982]. A QLoRA-specialised Qwen2.5-VL-7B gauge reader transfers poorly across datasets and its token confidence still gives confident errors [2608.17723]. It's About Time detects the clock, warps it with a learned homography and classifies 720 joint (hour, minute) states, trained on synthetic clocks and pseudo-labelled video, reaching about 80% (minute within +-1) on COCO/OpenImages clocks [2111.09162] but 18.54% full-time on TickTockVQA [2603.08011]. Swap-DPO fine-tunes VLMs with hour/minute-swapped negatives built from theta_h = 30h + m/2 [2603.08011]. A synthetic-only CNN regresses gauge angles with 2-5 degree error on real gauges [2308.14583].",
      "open_gap": "All modify weights, so none helps an API-only frontier model, and their generalisation to unseen designs is weak [2511.21982][2608.17723][2603.08011]. The 720-state joint clock space is learned in [2111.09162]; the hand coupling is used only for training negatives in [2603.08011], never as an inference-time constraint inside a scored hypothesis space.",
      "citations": [
        "2604.26614",
        "2511.21982",
        "2608.17723",
        "2111.09162",
        "2603.08011",
        "2308.14583"
      ]
    },
    {
      "sub_area": "Modular geometric gauge pipelines",
      "what_it_does": "Reitsma et al. detect the gauge, find major notches with a trained keypoint head, fit an ellipse, OCR numerals, fit a RANSAC linear angle-to-value map through numeral angles and intersect a segmented needle line; error is 0.77-1.15% of range when OCR reads two or more numerals, but OCR fails on 40-57.5% of images [2404.08785]. MeterFL segments ticks and pointer with a trained 30.6M U-Net, unwraps them into a polar strip and decodes p = i + (theta_ptr - theta_i)/(theta_{i+1} - theta_i) counted from the scale start, with v_min and delta_v supplied, reaching 87.2% within two minor divisions on its public 269-image reading test set, where a zero-shot frontier VLM reaches 49.1% [2609.31998]. A Sobel+Hough clock reader scores 7.7-9.7% on in-the-wild clocks [2111.09162].",
      "open_gap": "Reitsma interpolates linearly between numerals, assumes linear scales and breaks at OCR and needle segmentation; MeterFL needs metadata it does not read and counts from the start, so one missed tick shifts every later index. Neither ranks alternative labellings or abstains, and training-free edge geometry has collapsed in the wild, which is the risk this paper must pass with a day-1-3 pilot.",
      "citations": [
        "2404.08785",
        "2609.31998",
        "2111.09162"
      ]
    },
    {
      "sub_area": "Render-and-compare and promptable segmentation as training-free pointer localisers",
      "what_it_does": "FoundPose estimates unseen-object pose without training by matching frozen DINOv2 ViT-L layer-18 patch descriptors between a real crop and renders of an exact 3D model; because 14 px patches limit precision it adds featuremetric refinement [2311.18809]. SAM 2 segments any object from a single click on an image, predicting several masks for ambiguous clicks, at 58.9-61.9 1-click mIoU on 23 zero-shot datasets [2408.00714].",
      "open_gap": "Neither has been used to localise a 2-4 px instrument pointer. At patch scale a thin needle is sub-patch, so precision must come from a separately defined pixel-space refinement; the paper therefore compares the frozen-feature sweep against a hub-prompted SAM 2 mask, a radial profile and a pixel-space sweep, all with the same refinement.",
      "citations": [
        "2311.18809",
        "2408.00714"
      ]
    },
    {
      "sub_area": "Black-box remedies for VLM perceptual blind spots, visual prompting and tool-trust arbitration",
      "what_it_does": "Prompting, CoT and slow thinking do not fix low-level perception although frozen-encoder probes recover it [2407.06581]; Set-of-Mark overlays alphanumeric marks on segmented regions so GPT-4V can refer to them, and warns that numeric marks confuse the model on number-rich images [2310.11441]; task-wise visual prompts [2603.16250], learned hints [2605.16410] and visual demonstrations [2610.12942] steer the black-box model but leave it reading pixels. Tool-trust arbiters use the same backbone VLM to verify specialist outputs [2610.04836] or a trained rethink turn bounded by the model's own grounding [2512.06373].",
      "open_gap": "No black-box method hands the frontier an answer-bearing measurement with a reliability signal that does not pass through the frontier's own visual readout, and none tests whether giving the frontier the same measured views as a visual prompt would close the gap by itself.",
      "citations": [
        "2407.06581",
        "2310.11441",
        "2603.16250",
        "2605.16410",
        "2610.12942",
        "2610.04836",
        "2512.06373"
      ]
    },
    {
      "sub_area": "Off-the-shelf perception components",
      "what_it_does": "DBNet is a segmentation-based detector for multi-oriented and curved scene text, ResNet-18 variant at 48-62 FPS, trained on generic scene text [1911.08947]. Grounding DINO detects text-named categories zero-shot (52.5 AP on COCO without COCO data) but can hallucinate false positives [2303.05499].",
      "open_gap": "Used here as frozen, benchmark-agnostic components: DBNet localises numerals (the frontier only reads their values), Grounding DINO crops instruments and, on linear scales, the measured object named by the frontier; neither is trained on instrument data.",
      "citations": [
        "1911.08947",
        "2303.05499"
      ]
    }
  ],
  "method": {
    "high_level_flow": [
      "Localise: Grounding DINO instrument crop -> ellipse rectification and pivot (dials) or RANSAC scale-axis fit (linear) -> DBNet numeral boxes",
      "Ask once: lettered-box overlay -> single frontier call (box values, unit, scale type, indicator semantics, own reading y_F; minors-per-major only as a soft prior)",
      "Measure: unwrap to a 1D scale strip (polar for dials, axis-aligned for linear) -> tick lattice with local major/minor split and locally counted minors per major",
      "Label: enumerate neighbouring labelling hypotheses -> joint scoring -> winner h* and margin m",
      "Locate indicator: coarse candidate (paste-and-compare sweep on dials and clocks; profile change-point or SAM 2 object mask on linear scales) -> native-resolution tip refinement -> clock-hand or decade coupling check",
      "Answer: local interpolation between flanking labelled ticks -> answer or abstain (fallback to y_F) -> optional evidence hand-back"
    ],
    "modules": [
      {
        "module": "Instrument localisation and rectification",
        "role": "Crop each instrument and map dials to a fronto-parallel circle with a pivot, or linear scales to a straight axis.",
        "model": "Grounding DINO-T (Swin-T) frozen, prompt 'gauge dial . clock face . meter dial . ruler . measuring cylinder . thermometer' [2303.05499]; RANSAC ellipse fit on radial edge points (dials); RANSAC line fit on short parallel edge segments (linear scales)",
        "inputs": [
          "RGB image"
        ],
        "outputs": [
          "one rectified crop per instrument at the source's native resolution (no downsampling)",
          "pivot c and rim radius R (dials) or scale axis and tick side (linear)"
        ],
        "notes": "The detector is used only when the instrument covers less than about half the image or several instruments are present. Grounding DINO's false positives [2303.05499] are filtered by requiring periodic tick-like structure along the fitted ellipse or axis. The pivot is refined as the point minimising the spread of line-segment directions through the hub region."
      },
      {
        "module": "Numeral localisation",
        "role": "Find where the scale numerals are, without reading them.",
        "model": "DBNet ResNet-18, off-the-shelf scene-text weights, frozen [1911.08947]",
        "inputs": [
          "rectified crop"
        ],
        "outputs": [
          "numeral boxes b_j with scale coordinate u_j (angle about the pivot, or position along the axis)"
        ],
        "notes": "Positions come from the local detector, never from the frontier. Boxes off the dominant numeral radius or axis offset are kept but flagged so that the frontier can label them 'not a scale numeral'. Detection recall is a reported component metric on the 150 annotated held-out dials."
      },
      {
        "module": "Frontier semantic call",
        "role": "Read what the frontier is good at: numeral values, unit, scale type, indicator roles, rotation directions on multi-dial meters, and its own reading as fallback.",
        "model": "GPT-6 Astra through its API, default reasoning effort, exactly one call per image",
        "inputs": [
          "original image",
          "rectified crop with each DBNet box outlined and marked with a letter (A, B, C, ...), not a number",
          "structured prompt with a JSON answer schema"
        ],
        "outputs": [
          "value v_j or 'not a scale numeral' per box letter",
          "unit u and scale type s",
          "indicator count and roles (hour/minute/second, decade order, or object to be measured on rulers)",
          "M_F, the frontier's stated minors per major (soft prior only)",
          "the frontier's own reading y_F (fallback and diagnostic only)"
        ],
        "notes": "Box marks are letters because numeric marks confuse the model on number-rich images [2310.11441]; marks are placed beside, not on, each box. Unit and digit reading are the frontier's strong sub-skills [2510.26865][2604.22829]. y_F never centres a search window and never enters the margin. Input tokens, output tokens, cost and latency are logged per call and compared with a plain single-image Astra call."
      },
      {
        "module": "Tick-lattice extraction with local minor counting",
        "role": "Measure every tick position and length, and count minors per major from the photo itself.",
        "model": "Training-free: unwrap the tick band (0.6-1.0 R for dials; a band either side of the scale axis for linear scales) into a strip with 0.125 degree or 1 px columns, per-column contrast against a median face profile, 1D peak detection, 2-means clustering of tick length into major/minor. Pre-committed fallback: 30.6M U-Net tick segmenter trained on MeterFL train masks deduplicated against MeasureBench [2609.31998].",
        "inputs": [
          "rectified crop",
          "pivot or scale axis"
        ],
        "outputs": [
          "tick positions t_i, lengths l_i, major/minor flags, per-tick confidence",
          "local minors-per-major count n_k for every major interval k and its mode M_L"
        ],
        "notes": "Polar unwrapping follows MeterFL [2609.31998] without its trained segmenter in the main path. Minors are counted between each pair of measured majors, so a missed tick corrupts one interval, unlike MeterFL's count-from-start decoder. The frontier's M_F enters S(h) only through a weak prior term; when M_F and M_L disagree, the margin shrinks instead of M_F overriding the count. If the training-free extractor fails G0 on days 1-3, the MeterFL-trained segmenter becomes the extractor; the claim then becomes 'nothing is trained on any test benchmark', and MeterFL is dropped as a cross-dataset test because it would be in-distribution for the segmenter."
      },
      {
        "module": "Joint labelling-hypothesis ranking and margin",
        "role": "Choose the scale labelling that best explains numerals, lattice and indicator together, and measure how decisive that choice is.",
        "model": "Exhaustive enumeration over a small discrete space plus a hand-specified log-score with five weights; no learned parameters",
        "inputs": [
          "tick lattice and local minor counts",
          "numeral boxes with frontier values",
          "scale type",
          "indicator candidates"
        ],
        "outputs": [
          "winning labelling h*",
          "value map V_h*",
          "margin m"
        ],
        "notes": "Hypotheses: for each numeral the nearest major tick and its two neighbours; per major interval an insertion or deletion of at most one minor tick; both directions; all indicator-role permutations; typically a few hundred hypotheses. The margin is computed only against rivals that change the answer by more than half a minor division, so harmless ambiguities do not cause abstention. Non-linear scales attach values to tick indices and interpolate piecewise (Reitsma excluded them [2404.08785]). The identical scorer and thresholds run on dials, clocks and linear scales; only the unwrap differs."
      },
      {
        "module": "Coarse pointer candidate: paste-and-compare silhouette sweep (dials and clocks)",
        "role": "Pick the coarse pointer angle to within a few degrees, decide tip versus tail, reject shadows and counterweights, and separate hands.",
        "model": "DINOv2 ViT-L/14 frozen, layer-18 patch descriptors as in FoundPose [2311.18809]; 2D silhouette renderer with 12 shape variants. Ablated against a pixel-space version of the same sweep (Lab colour plus gradient-orientation correlation).",
        "inputs": [
          "rectified crop at 448 px for the feature pass",
          "pivot",
          "needle colour sampled near the hub",
          "angular range: full scale arc on gauges, full circle on clocks and meter sub-dials"
        ],
        "outputs": [
          "coarse angle phi_0 per pointer (top-3 peaks kept)",
          "peak sharpness"
        ],
        "notes": "For each candidate angle and variant the silhouette is composited onto the photo; the score is the mean cosine similarity of layer-18 descriptors between photo and composite on the patches the silhouette touches. Coarse pass at 2 degrees with 3 variants, then the top-3 peaks at 0.5 degrees with 12 variants. Because a 2-4 px needle is sub-patch at 14 px patches, the sweep is not asked for precision: its job ends at phi_0 +- 3 degrees with the tip side chosen. For clocks the sweep runs over the 720 joint (hour, minute) states, which fixes both hand angles by theta_h = 30h + m/2 [2603.08011]; an independent per-hand sweep is also run, and disagreement lowers the margin."
      },
      {
        "module": "Native-resolution tip refinement (all pointer types)",
        "role": "Turn a coarse pointer candidate into a precise axis angle at the tick ring, independent of feature-map resolution.",
        "model": "Deterministic pixel-space fit; no learned parameters",
        "inputs": [
          "rectified crop at native resolution",
          "pivot c",
          "coarse angle phi_0 and tip side",
          "needle colour c_n"
        ],
        "outputs": [
          "refined angle phi at the tick-ring radius",
          "axis-fit quality q (weighted residual RMS in px)"
        ],
        "notes": "(1) Needle-likelihood map L(x) = 0.5 * exp(-||Lab(x) - c_n||^2 / (2 kappa^2)) + 0.5 * g_perp(x), where c_n is the median Lab colour of photo pixels under the winning silhouette at radii 0.3-0.6 R and g_perp is the normalised gradient magnitude perpendicular to the candidate ray. (2) On K = 24 circles with radii evenly spaced in [0.35 R, 0.9 R] on the tip side, sample L at 0.05 degree steps over phi_0 +- 3 degrees with bilinear interpolation; the cross-section centre phi_k is the profile maximum refined by a 3-point parabolic fit, weighted by its contrast w_k. (3) Fit a line through the points c + r_k (cos phi_k, sin phi_k) by weighted total least squares with Huber IRLS, constraining it to pass within 2 px of the pivot; circles whose residual exceeds 3 px are dropped. (4) Intersect the axis with the median radius of the measured ticks to get phi, and read it against the flanking ticks measured in the same native-resolution strip. q is the weighted residual RMS. The same refinement is applied after every coarse localiser (sweep, SAM 2 mask, radial profile, pixel sweep), so the ablation 'coarse only vs coarse + refinement' and the comparison between seeds are both clean. On linear scales the analogue is a sub-pixel change-point fit of the indicator profile along the axis."
      },
      {
        "module": "Indicator localisation on linear scales",
        "role": "Locate the reading position on straight scales: liquid level or column top, or the two endpoints of a measured object on rulers.",
        "model": "Training-free: 1D intensity and gradient profile along the scale axis with change-point detection for liquid columns and menisci; for rulers, Grounding DINO box of the object named by the frontier [2303.05499] prompted into SAM 2 [2408.00714], and the mask's extremes projected onto the scale axis",
        "inputs": [
          "axis-rectified crop",
          "frontier indicator semantics"
        ],
        "outputs": [
          "indicator coordinate(s) on the scale axis",
          "profile or mask quality"
        ],
        "notes": "What transfers from dials: lettered-box frontier call, lattice extraction, local minor counting, the identical labelling scorer, margin and frozen thresholds. What does not transfer: the needle silhouette sweep and pointer coupling. Vernier calipers (a main plus a vernier scale) and composite instruments are outside scope; they are detected by the frontier's scale-type answer and routed to fallback, and their share of the linear subset is reported."
      },
      {
        "module": "Reading, abstention and optional hand-back",
        "role": "Turn the labelled lattice and indicator position into a value, decide whether to answer, and optionally return evidence to the frontier.",
        "model": "Deterministic; optional second frontier call (ablation only)",
        "inputs": [
          "h*",
          "phi",
          "m",
          "q",
          "unit",
          "y_F"
        ],
        "outputs": [
          "reading y with unit",
          "abstain flag",
          "evidence JSON"
        ],
        "notes": "y = V_h*(t_i) + (phi - t_i)/(t_{i+1} - t_i) * (V_h*(t_{i+1}) - V_h*(t_i)) for the flanking ticks, the local form of MeterFL's interpolation [2609.31998]; on rulers the reading is the difference of two endpoint values. Multi-dial meters use decade coupling: a higher-decade pointer's fraction within its digit must agree with the lower-decade reading. Abstain if m < tau_m or q > tau_q, thresholds fixed on the 200 MeasureBench pilot dials only; on abstention the system returns y_F flagged as unverified, so accuracy at 100% coverage is always reported."
      }
    ],
    "novel_architectural_elements": [
      "The frontier model sits only on the symbolic branch (values of locally detected, letter-marked boxes, unit, scale type, indicator roles); every position, tick count and angle is measured locally, and the frontier's minors-per-major answer is a soft prior that can only shrink the margin.",
      "Numeral values, the measured tick lattice and indicator positions meet in one jointly scored hypothesis space, and the margin to the best answer-changing rival is the system's only reliability output; it never uses the frontier's reading, confidence or self-agreement.",
      "Pointer localisation is split into a coarse, robustness-oriented candidate stage (frozen-feature silhouette sweep, swappable with SAM 2, radial or pixel-space seeds) and a precision stage that is a fixed pixel-space axis fit, so the paper can attribute accuracy to each.",
      "One scorer and one set of frozen thresholds serve circular dials, clocks and linear scales; only the unwrap and the indicator localiser change."
    ],
    "pseudocode": "def read_instrument(I, q, F, THR):            # THR frozen on 200 MeasureBench pilot dials\n    out = []\n    for D in detect_and_rectify(I):              # Grounding DINO-T + ellipse or axis fit\n        boxes = dbnet(D.crop)                     # positions only\n        sem = F.call(I, letter_marks(D.crop, boxes), schema=SEMANTICS)  # one API call\n        strip = unwrap(D)                         # polar for dials, axis-aligned for linear\n        ticks = tick_lattice(strip)               # peaks, major/minor split, local minor counts\n        if D.kind in {'gauge', 'clock', 'meter_subdial'}:\n            seeds = needle_sweep(D, feat=dinov2_l18, joint_clock=(D.kind == 'clock'))  # top-3, +-3 deg\n            inds = [refine_tip(D.native, D.pivot, s) for s in seeds]  # pixel-space axis fit -> (phi, q)\n        else:\n            inds = linear_indicator(D, sem)       # change-point or SAM 2 object endpoints\n        H = enumerate_labellings(boxes, sem.values, ticks, sem.scale_type, sem.roles, inds)\n        S = {h: score(h, prior_M=sem.minors_per_major, w=THR.weights) for h in H}\n        h_star = argmax(S)\n        y = interpolate_local(h_star, ticks)\n        rivals = [h for h in H if abs(value(h) - y) > 0.5 * minor_value(h_star)]\n        m = S[h_star] - max(S[h] for h in rivals)\n        out.append((y, m, quality(h_star)))\n    y, m, qual = combine(out, sem)               # decade or hand coupling across dials\n    if m < THR.tau_m or qual > THR.tau_q:\n        return sem.own_reading, ABSTAIN\n    return (y, sem.unit), ANSWER",
    "design_choices": [
      "Credit and delta: the semantics-to-VLM, geometry-to-deterministic-pipeline split is the design recommendation of [2604.22829]; this paper's contribution is the first measured single-image instantiation on public real-image benchmarks, plus the labelling margin, the better-views control and frozen-threshold transfer, not the split itself.",
      "The frontier reads values but not positions or counts: its unit and digit reading are strong [2510.26865][2604.22829] while fine spatial grounding and minor-tick counting are its named failures [2510.26865]; this also removes Reitsma's dominant OCR-recognition failure [2404.08785].",
      "Letter marks, placed beside boxes: Set-of-Mark reports that numeric marks confuse GPT-4V on number-rich images and that centred marks can be misattributed [2310.11441]; the frontier's box-value accuracy is reported as a function of box density so this choice is checked.",
      "Joint ranking of neighbouring labellings rather than sequential rounding (numeral -> major -> minor): an early wrong attachment cannot silently propagate, and the score gap to answer-changing rivals gives abstention for free; this is ordinary MAP-with-margin and is claimed only as a measured mechanism, with the sequential version as an ablation.",
      "Local minor counting between measured majors rather than counting from the scale start as in MeterFL [2609.31998]: a missed tick then corrupts one interval rather than every later index.",
      "Coarse-then-refine pointer localisation: FoundPose itself needs featuremetric refinement because 14 px patches limit precision [2311.18809]; here the precision stage is a pixel-space axis fit so that it cannot depend on patch size, and the frozen-feature sweep must earn its place against SAM 2 [2408.00714], radial-profile and pixel-space seeds.",
      "Full-range candidate search rather than a window around the frontier reading: frontier readings can be a whole interval off or collapse to 10:10 [2510.26865].",
      "Abstention independent of the frontier: VLM-derived confidence fails where perception fails [2610.04836][2512.06373][2608.17723].",
      "Thresholds are set once and frozen: every cross-dataset and linear-scale number uses the 200-pilot-dial thresholds, so 'training-free generalises' is tested rather than asserted."
    ],
    "theoretical_grounding": "Two simple conditions explain when the method should work and are measured rather than assumed. (1) Numeral attachment: the nearest-major assignment of numeral j is correct if |u_j - t_pi(j)| < Delta_major / 2, where Delta_major is the major-tick spacing; with 2, 5 or 10 minors per major this tolerance is about 13-27 degrees on common gauges. With n >= 2 numerals and a monotone, arithmetic (or monotone for non-linear) value constraint, a wrong labelling needs several numerals displaced in the same direction, which the joint score penalises. The 150 annotated held-out dials give the empirical distribution of |u_j - t_pi(j)| / Delta_major. (2) Reading precision: with local interpolation, reading error in minor divisions equals the angular error of phi plus tick-position error divided by the local minor spacing; for a 270-degree scale with 50 minors (5.4 degrees each), a 0.5-degree pointer error is under 0.1 division, well inside MeasureBench's per-image intervals [2510.26865]. The tip refinement fits a line to K = 24 cross-section centres; with sub-pixel centroid error sigma_p and needle length L px, the axis-angle error scales as about sigma_p / (L sqrt(K/12)), i.e. well under 0.5 degree for L >= 80 px and sigma_p <= 1 px, independent of the 14 px patch size. The margin is a log-score difference between the best and the best answer-changing labelling; thresholding it is standard selective prediction. These are design arguments, not proofs; the day-1-3 pilot measures whether they hold on web photos."
  },
  "model_details": {
    "base_model": "No model is trained or fine-tuned in the main method. Frozen components: GPT-6 Astra (black-box API, default effort, one call per image); DINOv2 ViT-L/14 layer-18 patch descriptors [2311.18809]; SAM 2 (image mode, point/box prompts) for the hub-prompted needle baseline and ruler object masks [2408.00714]; DBNet ResNet-18 with public scene-text weights [1911.08947]; Grounding DINO-T [2303.05499]. Local coarse-code variant: Qwen3-VL-4B in place of Astra. Pre-committed fallback: 30.6M U-Net tick/pointer segmenter as in MeterFL [2609.31998].",
    "training": {
      "method": "No model training for the main method (training-free inference with a hand-specified score whose five weights and two thresholds are set once on 200 MeasureBench pilot dials). Fallback only: supervised segmentation of tick and pointer masks on MeterFL train masks deduplicated against MeasureBench, never on any test image. Clock baseline only: if the It's About Time checkpoint is not downloadable, retrain its public code on its synthetic generator, reported as such [2111.09162].",
      "objective_functions": [
        "Purpose: pick the scale labelling that best explains numerals, ticks and indicators. Formally: S(h) = sum_j log N(u_j - t_pi(j); 0, sigma_n^2) + lambda_1 sum_k log p(n_k | M_L, delta) + lambda_M log p(M_L | M_F) + lambda_2 log p(V_h | s) + lambda_3 log p(phi | rho, coupling), where n_k is the corrected minor count in major interval k, M_L the locally counted mode, M_F the frontier's stated value (weak prior, lambda_M small and fixed), p(V_h | s) rewards arithmetic (linear) or monotone (non-linear) value progressions, and the coupling term enforces theta_h = 30h + m/2 on clocks or decade consistency on meters.",
        "Purpose: find coarse pointer candidates robust to shadows and counterweights. Formally: phi_0 = argmax_{phi, s} (1/|P(phi,s)|) sum_{p in P(phi,s)} cos(f_18(I)_p, f_18(I composited with silhouette(phi, s))_p), with P(phi,s) the patches the silhouette touches and f_18 frozen DINOv2 layer-18 descriptors.",
        "Purpose: refine the pointer axis at native resolution. Formally: minimise sum_k w_k rho_Huber(dist(p_k, line(c', phi))) subject to ||c' - c|| <= 2 px, with p_k the parabolic-refined cross-section centres on K = 24 circles.",
        "Purpose: decide when to answer. Formally: answer iff m = S(h*) - max_{h: |V_h(phi) - V_h*(phi)| > 0.5 minor} S(h) >= tau_m and q <= tau_q, with tau_m, tau_q chosen on the 200 pilot dials to maximise value+unit accuracy at 100% coverage with fallback, then frozen.",
        "Purpose (fallback segmenter only): learn tick and pointer masks. Formally: L = L_CE(mask_pred, mask_gt) + L_Dice(mask_pred, mask_gt) on MeterFL training masks."
      ],
      "adaptation": "None for the main method; fallback segmenter trained from scratch (30.6M parameters) in a few GPU-hours on one RTX 4090.",
      "key_hyperparameters": {
        "polar_strip": "2880 angular bins (0.125 degree) x 128 radial bins over 0.6-1.0 R, at native resolution",
        "needle_sweep": "coarse 2 deg with 3 variants; top-3 peaks at 0.5 deg with 12 variants; output phi_0 +- 3 deg",
        "tip_refinement": "K = 24 circles in [0.35 R, 0.9 R]; 0.05 deg sampling; Huber IRLS; pivot tolerance 2 px; circle rejection at 3 px residual",
        "dinov2_input": "448 px rectified crop, layer 18 of ViT-L/14",
        "labelling_neighbourhood": "numeral-to-major offset in {-1,0,+1}; at most one minor insertion or deletion per major interval; both directions; all indicator-role permutations",
        "sigma_n": "one quarter of the measured major-tick spacing",
        "frozen_on_pilot": "lambda_1, lambda_2, lambda_3, lambda_M, tau_m, tau_q (sigma_n fixed by rule)",
        "frontier_calls_per_image": "1 (plus 1 in the hand-back ablation)",
        "fallback_segmenter": "U-Net 30.6M, Adam lr 1e-3, 100 epochs on deduplicated MeterFL train masks"
      }
    }
  },
  "comparison_to_sota": {
    "related_methods": [
      "GPT-6 Astra alone: default, high and xhigh reasoning effort, with and without its built-in Python/crop tools [2609.35718].",
      "GPT-6 Astra with better views: the method's rectified crop, unwrapped strip and lettered tick and numeral marks as a visual prompt, without the computed answer (Set-of-Mark style [2310.11441]).",
      "Lost in Motion design guidance: VLM for semantics, edge/Hough geometry for the needle, rule-based validation [2604.22829].",
      "Gemini-2.5-Pro on MeasureBench: 31.5% real dials, 21.9% real linear (2025 figures) [2510.26865].",
      "TriSCA: trained Qwen3-VL-4B, 28.5% on MeasureBench real dials [2604.26614].",
      "Reitsma et al.: modular trained gauge reader with OCR numeral anchoring, 8.5% on MeasureBench real images [2404.08785][2510.26865].",
      "MeterFL pipeline: trained U-Net tick segmentation, polar unwrap and metadata-supplied counting, 87.2% Acc on its own test set [2609.31998].",
      "DialBench MRLM: end-to-end trained pointer-meter VLM on RPM-10K [2511.21982].",
      "It's About Time: trained 720-state clock reader, 18.54% full-time on TickTockVQA [2111.09162][2603.08011].",
      "Swap-DPO on TickTockVQA: LoRA SFT + DPO clock reader [2603.08011]."
    ],
    "key_differences": [
      "vs. Lost in Motion [2604.22829]: that paper states the split as guidance from a three-instrument video study and proposes Hough geometry; this paper builds it for single images, replaces line fits with a ranked labelling plus a pixel-space axis fit, adds a frontier-independent margin, and measures it on five public real-image sets with frozen thresholds.",
      "vs. Astra with more effort, tools or better views: the frontier never reads a position; one default-effort call supplies only semantics, and the better-views baseline tests whether showing Astra the same measured views would be enough.",
      "vs. TriSCA, DialBench, It's About Time and Swap-DPO: no weights are changed and nothing is trained on instrument data, so the method applies to an API-only model; cross-dataset transfer with frozen thresholds is measured, not asserted.",
      "vs. Reitsma: the frontier replaces OCR recognition, readings come from measured minor ticks rather than linear interpolation between numerals, non-linear scales need no global model, and a coarse-seed-plus-axis-fit replaces the segmented line fit and 'closer end' heuristic.",
      "vs. MeterFL: v_min, delta_v and tick values are read by the frontier rather than supplied, minors are counted locally, and alternative labellings are ranked with a margin instead of one deterministic count from the scale start.",
      "vs. RSure-style or rethink-turn arbitration: the reliability signal (labelling margin and axis-fit quality) never uses the frontier's own visual reading."
    ]
  },
  "proposed_evaluation": {
    "evaluation_setting": "Single-image instrument reading with GPT-6 Astra as the black-box system being helped, inside the Constraints: all experiments finish by 2026-11-09, API spend at most US$1,000 with per-call cost measured, local compute <= 40 GPU-days on 24 GB GPUs (estimated about 20: about 30 s of ViT-L passes per dial image and 55 s per clock for the sweep over about 8,700 local runs, x3 for ablations, plus SAM 2, Qwen3-VL-4B and a possible 2-3 GPU-day clock-baseline retrain). DATA AVAILABILITY (checked 2026-10-18): MeasureBench and TickTockVQA are public; MeterFL is public on GitHub with train/test split and readings [2609.31998]; RPM-10K is downloadable with an 8,730/2,000 instance-disjoint split and released MRLM weights [2511.21982]; InSituMeasure has no public release (no URL in the paper, none found by search) [2609.04014], so it is used only if released before 2026-11-02, on its analog-pointer categories with the same frozen thresholds. SPLITS: MeasureBench dials 200 pilot (the only tuning data) / 511 test, all 511 tagged by family and nuisance before any run, 150 of them additionally annotated with major-tick positions, numeral-to-tick assignment and pointer angles by annotators who never see predictions; MeasureBench linear 80 development (indicator-module debugging only, no weight or threshold change) / 281 test; TickTockVQA 150 train-split clocks (debugging and G3 gate only, not thresholds) / a seeded random 1,000-image test list released with the paper, plus the full 5,247-image test set for local-only components and It's About Time; MeterFL 269 reading test images minus any dHash near-duplicate of a MeasureBench image (MeterFL lists MeasureBench as an image source); RPM-10K a released stratified 400-image sample of the 2,000 held-out images for API runs, all 2,000 for the fully local variant and MRLM. FREEZE: on 2026-10-28 the thresholds, code hash and all image lists are committed to a timestamped public repository; nothing is changed afterwards. SCHEDULE: day 1-3 (10-19 to 10-21) G0 component pilot and strongest-Astra measurement on 50 tagged pilot dials, before the needle sweep is built, with availability checks for every checkpoint and dataset; 10-22 to 10-27 needle sweep, refinement, needle baselines, clock and linear modules, full 200-pilot run and gates G1-G3; annotation of the 150 held-out dials runs in parallel from day 1; 10-28 freeze; 10-28 to 11-05 test runs; 11-06 to 11-09 buffer. G0 GO/NO-GO (10-21, 50 pilot dials): (a) lattice resolvable on >= 60% and numeral-to-major assignment correct on >= 80% of dials with >= 2 detected numerals; (b) frontier semantics + ground-truth lattice and pointer (oracle geometry) reads >= 80% correctly; (c) Astra-best on the 50 dials <= 50% value+unit. If (a) fails with the training-free extractor but passes with the MeterFL-trained segmenter, switch to it (MeterFL then leaves the cross-dataset set). If (b) fails, the semantic channel is the bottleneck and the run stops. If (c) fails, +15 over Astra-best is infeasible at the committed selective operating point and the run stops; the outcome is a measurement paper (Astra configurations and oracle splits). BUDGET RULE: on days 1-3 measure mean cost per default call c_0 and per xhigh+tools call c_x. Tier 1 (always): Astra-default plain, the method's semantic call and the better-views call on all 2,891 API images (711 + 361 + 1,150 + 269 + 400). Tier 2: xhigh+tools plain on 200 pilot + 511 test dials, 300 of the 1,000 clocks and 150 each of linear, MeterFL and RPM-10K; better-views xhigh+tools on the 711 dials; high effort on the 200 pilot dials (to select Astra-best). Tier 3: a second sample of Astra-default and Astra-best on 200 test dials for variance. If projected Tier 1 + Tier 2 exceeds US$800, Tier 2 subsets outside the 711 dials are cut first, never below 511 test dials; US$200 is held in reserve. ASTRA-BEST is selected on the pilot among {default, high, xhigh+tools, better-views default, better-views xhigh+tools} and fixed for test; all configurations run on a set are reported. SIZING: with a paired design and about 30% discordant items, the paired SE is about 3.9 points at n = 200 and about 2.4 at n = 511, so +15 is resolvable on the test set, and nuisance and family claims are made only on subsets of at least 100 test images.",
    "benchmarks": [
      {
        "name": "MeasureBench real-world dial subset (711: 200 pilot for tuning, 511 held-out test, 150 of them geometry-annotated) [2510.26865]",
        "task_type": "visual measurement reading (value + unit, per-image interval scoring)",
        "newly_constructed": false
      },
      {
        "name": "MeterFL real test set (269 reading-decodable images, MeasureBench near-duplicates removed) with frozen thresholds [2609.31998]",
        "task_type": "cross-dataset analog-meter reading; Acc within two minor divisions and %FS",
        "newly_constructed": false
      },
      {
        "name": "RPM-10K held-out split of DialBench (released 400-image stratified sample for API runs; all 2,000 for local runs) with frozen thresholds [2511.21982]",
        "task_type": "cross-dataset pointer-meter reading; Accuracy-epsilon (error <= 1% of range) and within half a minor division",
        "newly_constructed": false
      },
      {
        "name": "MeasureBench real-world linear subset (361: 80 development, 281 test) with frozen dial thresholds [2510.26865]",
        "task_type": "linear-scale measurement reading (value + unit)",
        "newly_constructed": false
      },
      {
        "name": "TickTockVQA (150 train-split clocks for debugging and gating; a released seeded 1,000-image test list; full 5,247-image test set for local-only components and It's About Time) [2603.08011]",
        "task_type": "analog clock reading (hour and minute)",
        "newly_constructed": false
      },
      {
        "name": "InSituMeasure analog-pointer categories, only if publicly released before 2026-11-02 [2609.04014]",
        "task_type": "cross-dataset industrial gauge reading with answerability labels",
        "newly_constructed": false
      },
      {
        "name": "Annotation layer: family and nuisance tags on all 511 test dials, 361 linear items and 1,000 test clocks (clock type: Arabic, Roman, no numerals, illustrated); geometry annotations on 150 test dials and the 200 pilot dials; all released",
        "task_type": "per-family breakdowns, component accuracy and oracle splits (not a new benchmark)",
        "newly_constructed": true
      }
    ],
    "baselines": [
      "GPT-6 Astra alone at default, high (pilot) and xhigh effort with built-in Python/crop tools [2609.35718], cost and latency measured",
      "GPT-6 Astra with better views (rectified crop + unwrapped strip + lettered major ticks and numeral boxes, no computed answer), at default and xhigh+tools [2310.11441]",
      "Astra-best: the configuration above with the highest pilot accuracy, fixed for test",
      "Lost-in-Motion hybrid [2604.22829]: same frontier call + Reitsma-style RANSAC linear angle-to-value fit through numeral angles [2404.08785] + Hough needle",
      "Needle baseline (a): SAM 2 mask prompted with a positive click at the detected hub and negative clicks on the rim [2408.00714], skeleton or principal-axis fit, asymmetric tip rule (tip = mask extremity farther from the pivot), then the same tip refinement",
      "Needle baseline (b): radial profile, the needle-colour likelihood plus edge energy integrated along rays from the pivot over [0.2 R, 0.9 R] at 0.25 degree steps, with tip side chosen by the longer above-threshold run, then the same tip refinement",
      "Needle baseline (c): pixel-space paste-and-compare, the identical silhouette sweep scored by Lab colour plus gradient-orientation correlation instead of DINOv2 features, then the same tip refinement",
      "Fully local variant: Qwen3-VL-4B as the semantic reader, reported as a headline row",
      "Trained references rerun where public: It's About Time on the 1,000 list, the full TickTockVQA test set and MeasureBench clocks [2111.09162]; MRLM on RPM-10K [2511.21982]; Swap-DPO if its checkpoint is public, otherwise cited [2603.08011]",
      "Published references, not rerun: Gemini-2.5-Pro 31.5% dials / 21.9% linear and Reitsma 8.5% [2510.26865]; TriSCA 28.5% [2604.26614]; MeterFL trained pipeline 87.2% and zero-shot frontier VLM 49.1% Acc [2609.31998]"
    ],
    "main_metrics": [
      "Value and value+unit accuracy at 100% coverage (fallback on abstention), with paired-bootstrap 95% CIs",
      "Gain decomposition against Astra-best and against Astra-default: coverage, the method's selective accuracy, Astra's accuracy on the same covered items, and Astra's accuracy on the abstained items",
      "Selective accuracy and coverage at the frozen thresholds; area under the risk-coverage curve",
      "Error detection AUROC on one error definition (the method's pre-fallback reading is wrong) for every signal: labelling margin, axis-fit quality, Astra verbalised confidence and Astra 3-sample agreement; separately, each Astra signal for Astra's own errors; also on items where Astra's samples agree but are wrong",
      "Per-family accuracy, coverage and gain: single-pointer gauges, clocks, multi-dial meters, linear vs non-linear dial scales, linear instruments by type, TickTockVQA clock types",
      "Component metrics on the 150 annotated test dials: DBNet numeral recall, numeral-to-major assignment accuracy, tick recall/precision, local minors-per-major accuracy vs Astra's M_F accuracy, Astra box-value accuracy vs box density (boxes per 90 degrees), pointer angle error in degrees by seed and with or without refinement, peak sharpness by nuisance tag",
      "Oracle splits on the 150 annotated dials: ground-truth pointer (scale-only) and ground-truth labelling (pointer-only)",
      "TickTockVQA exact-minute accuracy, hour and minute accuracy, Tol-1 and Tol-5, MAE in minutes, hour/minute swap rate",
      "MeterFL Acc and median %FS; RPM-10K Accuracy-epsilon and within-half-minor accuracy",
      "Measured API cost per image, input and output tokens of the semantic call vs a plain Astra call, frontier calls per image, end-to-end latency including local GPU-seconds; Astra run-to-run SD from Tier 3"
    ],
    "ablations": [
      "Joint labelling ranking vs sequential rounding (numeral -> major -> minor) on the same lattice",
      "Local minor counting vs MeterFL-style counting from the scale start; frontier M_F as soft prior vs hard constraint vs removed",
      "Letter marks vs numeric marks on the numeral boxes; DBNet positions vs positions estimated by the frontier",
      "Pointer seed: DINOv2 sweep vs pixel-space sweep vs SAM 2 hub mask vs radial profile vs Hough, each with and without the tip refinement",
      "Candidate range: full arc or circle vs +-1 major interval around y_F vs +-1 minor around y_F",
      "Clock-hand coupling (joint 720-state sweep) and decade coupling on/off",
      "Abstention signal: margin vs axis-fit quality vs both vs Astra self-agreement",
      "Tick extraction: training-free peaks vs the MeterFL-trained U-Net (reported on non-MeterFL sets)",
      "Evidence use: answer returned directly vs a second frontier call composing the answer from the evidence (how often Astra overrides correct evidence)",
      "Semantic reader: GPT-6 Astra vs Qwen3-VL-4B"
    ]
  },
  "falsifiable_predictions": [
    {
      "pillar": "Day-1-3 component pilot and strongest-Astra measurement (G0, go/no-go)",
      "prediction": "Predicted, not observed: on 50 tagged pilot dials the training-free lattice is resolvable on >= 60%, numeral-to-major assignment is correct on >= 80% of dials with >= 2 detected numerals, oracle-geometry reading with frontier semantics is >= 80%, and Astra-best reads <= 50% value+unit.",
      "kill_condition": "Assignment < 70% with both the training-free and the MeterFL-trained extractor, or oracle-geometry reading < 70%, or Astra-best > 55%: the run stops on 2026-10-21 and the method paper is not written."
    },
    {
      "pillar": "Headline accuracy, absolute floor and gain decomposition (G1)",
      "prediction": "Predicted: on the 511 held-out MeasureBench dials, value+unit accuracy at 100% coverage is >= 50% absolute and >= Astra-best + 15 points (paired-bootstrap 95% lower bound > 0) at <= 1.3x Astra-default measured API cost per image; in the decomposition, coverage >= 50%, selective accuracy >= 75%, Astra-best accuracy on the covered items <= 55%, and the fallback term costs at most 3 points.",
      "kill_condition": "Gain < 10 points or lower bound <= 0 on the pilot (gate) or test; or absolute accuracy < 45%; or Astra-best accuracy on covered items >= 60% (the method only answers dials Astra already reads); or Astra xhigh+tools within 5 points at <= 2x the method's cost."
    },
    {
      "pillar": "Cross-dataset transfer with frozen thresholds (G4)",
      "prediction": "Predicted: with every weight and threshold frozen from the MeasureBench pilot, the method beats Astra-default by >= 10 points on MeterFL test (Acc within two minor divisions, MeasureBench near-duplicates removed) and by >= 10 points on the 400 RPM-10K held-out images (within half a minor division), reaching >= 65% MeterFL Acc, with margin AUROC >= 0.75 on each set.",
      "kill_condition": "Gain < 5 points on either set, or margin AUROC < 0.65 on either: the claim that training-free reading transfers across datasets is withdrawn and reported as negative."
    },
    {
      "pillar": "Measurement vs better views (G5)",
      "prediction": "Predicted: on the 511 test dials the method beats the best better-views Astra configuration by >= 10 points, and better views recover at most one third of the method's gain over plain Astra-default.",
      "kill_condition": "Better-views Astra within 5 points of the method: the contribution is reframed as visual prompting and the local-measurement claim is dropped."
    },
    {
      "pillar": "Pointer localisation: frozen-feature sweep and tip refinement (G2)",
      "prediction": "Predicted: with the same refinement for every seed, the DINOv2 sweep beats the best of SAM 2 hub mask, radial profile and pixel-space sweep by >= 5 points overall and >= 10 points on the pooled shadow/glare, counterweight, tapered or hollow and multi-hand test dials (n >= 100); refinement cuts median pointer error by >= 50% for every seed.",
      "kill_condition": "Gain over the best alternative seed < 2 points overall or < 5 on the pooled nuisance subset: the best alternative becomes the reported seed; if the pixel-space sweep matches DINOv2 within 2 points, the claim is restated as the silhouette sweep, not the frozen features."
    },
    {
      "pillar": "Joint labelling ranking and local counting",
      "prediction": "Predicted: on the 150 annotated test dials numeral-to-major assignment is correct on >= 85% of dials with >= 2 detected numerals; joint ranking cuts errors of exactly one minor or one major division by >= 40% relative to sequential rounding; local minors-per-major is correct on >= 90% of resolvable dials vs <= 75% for Astra's M_F.",
      "kill_condition": "Assignment < 70%, or joint ranking within 2 points of sequential rounding in overall accuracy, or local counting no more accurate than M_F."
    },
    {
      "pillar": "Frontier-independent abstention",
      "prediction": "Predicted: on the 511 test dials the margin detects the method's errors with AUROC >= 0.80 overall and >= 0.75 on items where Astra's three samples agree but are wrong, where Astra's verbalised confidence and agreement detect the same errors at <= 0.60.",
      "kill_condition": "Margin AUROC < 0.70 overall, or selective accuracy < 65% at 50% coverage."
    },
    {
      "pillar": "Clock reading vs frontier and trained specialist (G3)",
      "prediction": "Predicted: on the released 1,000-image TickTockVQA list, exact-minute accuracy is >= Astra-best + 20 points and >= It's About Time + 10 points (training-free vs trained specialist); the hour/minute swap rate is at most half Astra's; removing the hand coupling costs >= 5 points; coverage on illustrated and no-numeral clocks is reported separately and predicted below 40%.",
      "kill_condition": "Gain < 10 points over Astra-best, or below It's About Time, or coupling ablation within 2 points."
    },
    {
      "pillar": "Transfer to linear scales",
      "prediction": "Predicted: on the 281 held-out MeasureBench linear items, with the dial-pilot thresholds frozen and vernier and composite items routed to fallback, value+unit accuracy is >= Astra-default + 8 points, with coverage >= 40% on non-vernier items.",
      "kill_condition": "Gain < 4 points or margin AUROC < 0.65 on linear items: the paper states that the labelling margin does not transfer beyond circular dials."
    }
  ],
  "limitations": [
    "The semantics/geometry split is anticipated by [2604.22829] and each module has a close ancestor (MeterFL unwrap and interpolation, Reitsma numeral anchoring, FoundPose render-and-compare, the 720-state clock space of It's About Time); the contribution is the measured instantiation, the frontier-independent margin and the transfer tests, and the paper stands or falls on its numbers.",
    "Training-free geometry is exactly where earlier pipelines collapsed in the wild (Reitsma 8.5% on MeasureBench, Sobel+Hough clocks below 10%) [2510.26865][2111.09162]; coverage, not accuracy, may cap the gain, which is why the day-1-3 pilot is a go/no-go and the MeterFL-trained segmenter is the pre-committed fallback.",
    "Scope is instruments with a visible tick lattice: dials, clocks and single-scale linear instruments; vernier calipers, composite and digital instruments are routed to the frontier, and illustrated or tick-free clocks will mostly abstain.",
    "The method depends on the frontier for numeral values, units, scale type and indicator roles; misreads of decimals, overlaid scales or unusual units propagate, and only one frontier model (plus a local Qwen3-VL-4B variant) is tested.",
    "Some evidence rests on data that may not be available in time: InSituMeasure is not public as of 2026-10-18 [2609.04014], It's About Time weights may need retraining [2111.09162], and MeterFL shares image sources with MeasureBench [2609.31998]; MeasureBench may also be in Astra's training data, which biases comparisons against the method."
  ]
}
```

---
## C. Latest panel (fresh panel on v2)

### R1

# R1 (area expert) review: C3v2, "Read the Labels, Measure the Ticks"

Venue: CVPR 2027 main track. Results-masked: I assume every experiment in proposed_evaluation runs as
written and every falsifiable prediction lands exactly at its threshold, no better.

## Summary
The paper reads analog instruments (gauges, clocks, multi-dial meters, single-scale linear instruments)
with a training-free pipeline. One GPT-6 Astra call reads only the symbols: values of letter-marked
DBNet numeral boxes, the unit, the scale type and pointer roles. Every position is measured locally:
rectification, a 1D tick lattice with local minor counting, a DINOv2 paste-and-compare coarse pointer
sweep, and a pixel-space axis fit. A few hundred neighbouring "labellings" (numeral-to-major offsets,
one-minor insertions or deletions, direction, hand roles) are scored jointly, and the score gap to the
best answer-changing rival decides whether to answer or fall back to Astra's own reading. The claimed
insight is that the semantics/geometry split works on real single images once the fragile step, which
tick each numeral belongs to, becomes a ranked hypothesis space whose margin is a reliability signal
that never uses the frontier's own visual reading. Predicted evidence, at threshold: on 511 held-out
MeasureBench real dials, ≥50% value+unit at 100% coverage and ≥Astra-best+15 at ≤1.3x Astra-default
cost. Further predictions: ≥+10 over Astra-default on MeterFL and RPM-10K with thresholds frozen
(≥65% MeterFL Acc); better views recover at most a third of the gain; margin AUROC ≥0.80; on
TickTockVQA, ≥Astra-best+20 and ≥It's About Time+10; on MeasureBench linear items, ≥+8.

## Strengths
- The paper starts from a well-documented failure. Frontier VLMs read unit and digits well and the
  value badly [2510.26865][2604.22829], and trained readers transfer poorly [2608.17723][2604.26614].
  "Let the VLM read symbols, measure geometry locally" fits that failure exactly.
- The controls are better than usual for this sub-area. The better-views baseline (Astra gets the same
  rectified crop, strip and marks but not the answer) separates "measurement helps" from "a better view
  helps". Astra-best is chosen on the pilot, not as a max over test runs. A gain decomposition, oracle
  splits on 150 geometry-annotated dials and a 3-day go/no-go gate are all planned. A specialist reviewer
  would ask for exactly these.
- Thresholds frozen on 200 MeasureBench pilot dials and applied unchanged to MeterFL, RPM-10K, linear
  scales and clocks. If the transfer predictions hold, the claim "training-free generalises" is tested,
  not asserted. No prior reader in this area shows that; Reitsma got 8.5% on MeasureBench and MeterFL's
  segmenter is trained in-domain [2510.26865][2404.08785][2609.31998].
- Credit is mostly given honestly. The split is credited to [2604.22829], the unwrap and interpolation
  to MeterFL [2609.31998], the 720-state clock space to [2111.09162], and the limitations section
  says the paper "stands or falls on its numbers".
- At threshold the headline is a large number for this benchmark. 50% on real dials is about 19 points
  above the best published model (31.5%) and above TriSCA's 28.5% [2510.26865][2604.26614], with no
  weight changes, at about one frontier call per image.

## Weaknesses
- [major] **The conceptual delta is thin, and two close precedents are not cited.** Strip the
  vocabulary and the pipeline is the classical gauge reader (detect → rectify → ticks → numeral anchoring
  → needle line → interpolate) of Reitsma [2404.08785] and MeterFL [2609.31998], with OCR replaced by a
  frontier call. Lost in Motion already recommends that replacement as design guidance [2604.22829]. The
  "joint labelling ranking" generalises an existing step: Reitsma's RANSAC angle-to-value fit through
  numerals [2404.08785], and the mode-of-pairwise-slopes numeral auto-correction of a Dec-2025
  linear-scale reader [2512.15327], which the report does not cite. The real additions are one-minor
  insertion and deletion hypotheses and a margin, and the authors themselves call that "ordinary
  MAP-with-margin". A Dec-2025 river-gauge-plate system already passes locally detected scale geometry to
  GPT-4o / Gemini as metadata and reports that it "substantially improved" readings [2512.23454];
  that is the better-views/hand-back configuration in a single domain, and it is not cited either. A
  reviewer who knows this literature will call the paper competent systems integration. It is
  acceptable at CVPR only because the numbers are large. The CVPR audience will remember a number, not
  a mechanism.
- [major] **The frontier-independent margin is independent of the frontier's reading, not of its
  semantics, and that hides the most common failure on real dials.** Numeral values, decimal points,
  multipliers (×0.1 MPa, ×1000), the unit, the scale type and the choice among scales all come from
  Astra. Dual-unit pressure gauges (psi/bar, two numeral rings) are common in web photos. Suppose Astra
  attaches the wrong ring's numerals, or drops a multiplier, consistently across boxes. Then the
  arithmetic-progression term is satisfied, the margin is large, and the answer is confidently wrong.
  This is the same "confident and wrong" pattern the paper criticises in VLM confidence [2608.17723].
  The predicted AUROC of 0.75 on "Astra samples agree but wrong" items rests on how often such
  semantic errors occur, and the paper has no breakdown for them. As written, "frontier-independent" is
  an overclaim. The paper should say that the margin certifies geometry and labelling, not semantics, and
  report a per-cause error table: semantic vs attachment vs lattice vs pointer.
- [major] **The headline prediction is barely consistent with the go/no-go thresholds, and the
  historical prior is poor.** The G0 pass bar is: lattice resolvable on ≥60% of dials, assignment
  correct on ≥80% of those with ≥2 numerals, and oracle-geometry reading ≥80%. Composed, that gives
  roughly 0.6 × 0.8 × 0.8 ≈ 38% fully-correct coverage before pointer errors. Yet G1 needs coverage
  ≥50% at selective accuracy ≥75%, i.e. ≥37.5% of all dials answered correctly by the method. So a
  pilot that just passes G0 predicts G1 sits on its kill line. Training-free edge geometry on web
  photos has collapsed before (Reitsma 8.5% on MeasureBench, failing at detection, OCR and needle
  segmentation; Sobel+Hough clocks below 10%) [2510.26865][2111.09162]. GPT-6 Astra has not been
  measured on dials. If it has improved as much as GPT-5→Gemini-2.5-Pro did, Astra-best ≤50%
  together with method ≥ Astra-best+15 is a narrow corridor. This does not sink the paper conditional
  on the results, but it is why my p_core is low.
- [major] **One frontier model, and no committed prediction for the result that matters most under
  the Constraints.** The thesis is "help a black-box frontier model" and "need it less", but only GPT-6
  Astra is tested. The fully local Qwen3-VL-4B variant is called a "headline row" yet has no
  falsifiable prediction. If a 4B local model plus geometry beats Astra-best on real dials at zero API
  cost, that is a decisive cost/performance change and the most memorable claim available. Leaving it
  unpredicted weakens the paper's significance case. No second frontier family (e.g. a Gemini 3.x
  Pro) is tested either as the semantic reader or as the baseline, so reviewers cannot tell whether the
  gain is about Astra or about frontier VLMs in general.
- [major] **Scope sprawl relative to a 3-week build by a small team.** Nine prediction pillars, four
  instrument families (gauges, clocks, multi-dial decade meters, linear scales with SAM 2 object
  endpoints), a DINOv2 silhouette sweep with 12 shape variants, a 720-state joint clock sweep, decade
  coupling, and 350 hand-annotated geometry dials plus 1,000 tagged clocks, all frozen by 2026-10-28.
  The DINOv2-vs-SAM-2 seed pillar (G2) is a side claim that dilutes the story and costs about 30-55 GPU-s
  per image. A pixel-space sweep or radial profile followed by the same refinement may well match it,
  and the paper's own kill condition anticipates that. Each extra pillar at threshold adds another
  "only just" result for reviewers to argue with.
- [minor] On clocks the "labelling" problem mostly disappears: numeral attachment is fixed by 12-fold
  symmetry, and what remains is the hand roles plus the 720-state joint space, which It's About Time
  already uses, though learned [2111.09162]. The clock pillar is essentially a training-free
  It's About Time with a margin, and the bar of beating its 18.54% full-time on TickTockVQA
  [2603.08011] by 10 points is modest. The paper should present it as transfer, not as an instance of
  the labelling insight.
- [minor] Non-linear scales (ohmmeters, dB): attaching values to tick indices and interpolating
  piecewise requires the value of every minor tick, which on non-uniform scales is not determined by
  the numerals. State how minors between unequal majors are valued, or route such scales to fallback.
- [minor] Image resolution: the tip-refinement argument assumes a needle length of at least 80 px.
  MeasureBench gives no resolution statistics [2510.26865]. Report the distribution of needle lengths and
  of accuracy by pixel size.
- [minor] "Astra has not been measured on dials" and "frontier VLM fails" are stated from 2025 numbers.
  The motivation section should not lean on Gemini-2.5-Pro's 31.5% once Astra numbers exist.

## Overlapping prior and concurrent work
- [2604.22829] Lost in Motion. Recommends VLMs for semantics and deterministic edge/Hough geometry for
  the needle, plus rule-based validation, from a three-instrument video study. It anticipates the core
  split. It does not kill novelty, because it builds and evaluates nothing comparable on single-image
  benchmarks, and the paper credits it.
- [2512.23454] River gauge plate reading with a hybrid of object detection and generative AI. Per its
  abstract (the body was not retrievable), YOLOv8-pose scale-gap geometry is passed as metadata to
  GPT-4o / Gemini, which improves readings. It is a precedent for "local geometry plus frontier VLM" in
  one domain, with the LLM still producing the answer. Not cited. It does not kill novelty, but it
  weakens the "no one has built it" sentence and should be the cited ancestor of the better-views and
  hand-back baselines.
- [2512.15327] Linear-scale reader for syringes and cylinders. It measures majors and minors locally,
  OCRs the numeral beside each major, and uses the mode of pairwise slopes to correct misread numerals
  and fill unread ones before a linear position-to-value map. This is a precursor of the
  numeral-consistency part of the joint labelling. It has no margin and no abstention, and it is
  evaluated on one syringe. Not cited. It does not kill novelty.
- [2404.08785] Reitsma et al. OCR'd numerals are projected onto the notch ellipse, followed by a
  RANSAC linear angle-to-value fit and a segmented needle. This is the direct ancestor of the
  numeral-anchoring stage. Cited. Not a kill: the frontier replaces its dominant OCR failure, and minors
  plus non-linear handling are new.
- [2609.31998] MeterFL. Polar unwrap of tick and pointer masks, counting from the scale start, with
  v_min and Δv supplied; 87.2% Acc with a trained segmenter. It is the direct ancestor of the
  lattice-and-interpolate stage, and the frozen-threshold transfer target. Cited. Not a kill.
- [2111.09162] / [2603.08011] It's About Time and Swap-DPO. The 720 joint hand states and the
  θ_h = 30h + m/2 coupling. These cover the clock pillar's structure; the training-free,
  inference-time use is the delta. Not a kill.
- [2604.26614] TriSCA and [2608.17723] a QLoRA VLM gauge study. Trained readers, the relevant
  baselines and motivation. No overlap with a training-free hybrid.
- Recency check (since 2025-10-18: gauge, dial, pointer meter, clock VLM, measurement reading, visual
  measurement, selective-prediction queries): I found no paper that combines frontier semantics with
  local tick geometry, ranked labellings and a margin on MeasureBench. Novelty is not killed. It is
  incremental, and its acceptance depends on the numbers.

## Missing baselines or experiments
- A second frontier family (e.g. a current Gemini Pro), both alone and as the semantic reader, on at
  least the 511 test dials. Without it, "helps a black-box frontier" is a claim about one model.
- A committed prediction and full evaluation for the fully local Qwen3-VL-4B semantic reader. It is the
  most important result under the Constraints, and it currently has no threshold.
- The [2512.23454]-style baseline made explicit: Astra given the measured lattice, numeral positions
  and pointer angle as structured text metadata, composing the answer itself. The hand-back ablation
  is close, but it should be a baseline row with cost.
- An error taxonomy on the 150 annotated dials: semantic error (wrong ring, multiplier, decimal,
  unit) vs attachment vs lattice vs pointer, and the margin's AUROC on each. In particular, margin
  AUROC on dual-scale and multiplier-bearing gauges.
- A harm rate: the fraction of items Astra-best gets right that the method answers wrongly when it
  does not abstain. The gain decomposition implies it, but reviewers will want it stated directly.
- TriSCA rerun on the 511 test dials if weights are public. If it is not, check whether its GRPO stage
  on "1,273 real dial images" overlaps MeasureBench real images before quoting 28.5% as a fair
  reference [2604.26614].
- Accuracy against image resolution or needle length in pixels, and against numeral density (boxes per
  90°) for Astra box-value accuracy, which is already planned.

## Questions for the authors
1. On dual-unit gauges (two numeral rings), how does the hypothesis space choose the ring that
   matches the question's unit? Can a wrong-ring labelling ever be an "answer-changing rival" with a
   low score, or does it get a high margin?
2. What are the G0 numbers you would need to see, composed end to end, for G1 (coverage ≥50% at
   ≥75% selective accuracy) to be likely rather than marginal? Is there an explicit end-to-end pilot
   gate on the 200 pilot dials before the freeze?
3. How is the value of each minor tick determined on non-linear scales between unequal majors?
4. What fraction of MeasureBench real dials are multi-scale, multiplier-bearing, clocks, or multi-dial
   decade meters, and what coverage do you predict on each?
5. If the pixel-space sweep matches DINOv2 within 2 points (your own kill line), will G2 be dropped from
   the paper, or kept as a negative ablation?
6. Is the 1.3x cost bound measured including the second image (the lettered overlay) in the semantic
   call, at Astra's real image-token pricing?

## Rating
- rating: 4  (weak accept). The predicted numbers are large for this benchmark, frozen-threshold
  transfer is genuinely tested, and the controls (better views, Astra-best on the pilot, oracle splits)
  are what a specialist would demand. The idea is a careful classical-pipeline-plus-VLM integration
  whose conceptual delta over Reitsma/MeterFL/Lost-in-Motion and two uncited 2025 hybrids is modest. It
  relies on one frontier model, and the "frontier-independent" margin overclaims.
- confidence: 4
- p_core: 0.25. G1 (≥50% absolute and ≥Astra-best+15 on the 511 test dials) needs training-free
  lattice, attachment and pointer stages to be jointly right on about 40% of web dials. The paper's own
  G0 pass thresholds compose to roughly that line. Every earlier training-free or modular reader has
  collapsed on MeasureBench-like images, and Astra's dial accuracy is unknown and may have risen.
- one_point_fix: Make the fully local variant a committed headline prediction. For example: Qwen3-VL-4B
  semantics plus local geometry reaches ≥ Astra-best+8 on the 511 test dials at zero API cost, with a
  second frontier family as an additional baseline. Pay for it by cutting the DINOv2-sweep pillar (G2).
  This turns the paper into "a 4B local, training-free system beats frontier models on real
  instruments", a decisive cost/performance claim, instead of "a pipeline that helps one API model".

### R2

# R2 (generalist) review: "Read the Labels, Measure the Ticks" (C3v2), CVPR 2027

## Summary
The paper builds a training-free instrument reader in which a black-box frontier VLM (GPT-6 Astra, one call per image) only names things: the values of letter-marked numeral boxes, the unit, the scale type and the pointer roles. Tick lattices, numeral positions and pointer angles are measured locally (DBNet, polar or axis unwrap with peak detection, a DINOv2 paste-and-compare sweep plus a pixel-space axis fit), and a small set of neighbouring "labellings" (numeral one tick over, a missed minor tick, swapped hands, reversed direction) is scored jointly. The claimed insight is that the score gap between the winning labelling and the best rival that would change the answer is a reliability signal that never passes through the frontier's own visual reading. The predicted evidence is ≥50% value+unit accuracy and +15 points over the best Astra configuration on 511 held-out MeasureBench real dials at ≤1.3x API cost, +20 exact-minute accuracy on TickTockVQA, +10 points cross-dataset on MeterFL and RPM-10K with frozen thresholds, +8 points on linear scales, and margin AUROC 0.80 where Astra's own confidence and agreement signals reach 0.60.

## Strengths
- The problem is well chosen for a 2026–27 audience. Frontier VLMs read the unit and the digits but not the value (31.5% on real dials with 96.2% unit accuracy [2510.26865]), and a training-free fix that works on an API-only model is relevant beyond gauges.
- The one-line thesis ("let the frontier read what the numbers mean, measure the ticks locally, trust the reading only when one labelling clearly wins") is memorable and easy to explain to a non-specialist.
- The controls are unusually honest for a systems paper. The better-views baseline (Astra shown the same rectified crop, strip and lettered marks but not the answer) directly tests "is this just visual prompting?". Astra-best is chosen on the pilot and then fixed. Thresholds are frozen and committed before test, and the gain decomposition separates the covered and abstained items.
- The breadth of evidence is good if it lands: three dial datasets, a clock benchmark with a trained specialist (It's About Time) as reference, and linear scales, all with one frozen scorer.
- Credit is assigned candidly. The semantics/geometry split is attributed to Lost in Motion [2604.22829], and each module's ancestor is named (MeterFL, Reitsma, FoundPose, the 720-state clock space).
- The frontier-independent abstention result (margin AUROC 0.80 vs ≤0.60 for Astra's verbalised confidence and agreement, including on agree-but-wrong items) is a reusable finding about self-assessment in black-box VLMs.

## Weaknesses
- [major] **The conceptual delta is small, and the paper reads as a well-engineered domain pipeline.** By the authors' own account the split is from [2604.22829], the margin is "ordinary MAP-with-margin", the unwrap and interpolation are MeterFL's [2609.31998], and the clock coupling is from [2111.09162][2603.08011]. The broader principle, moving metric measurement out of the VLM into deterministic tools with oracle-based error attribution, is a visible 2026 trend in other domains [2609.29073], and the proposal does not cite it. A reviewer who has seen 50 tool-augmented VLM papers this year will ask what idea transfers beyond analog instruments. The paper offers no answer beyond "the same scorer runs on dials, clocks and rulers".
- [major] **The committed predictions are internally inconsistent at their thresholds.** With the G1 decomposition exactly at threshold (coverage 50%, selective accuracy 75%, Astra-best on covered items 55%, fallback term −3), the gain over Astra-best is 0.5 × (75 − 55) − 3 = +7 points, not +15. Likewise, ≥50% absolute accuracy together with Astra-best ≤35% needs Astra-default to read ≥25% of the abstained items while Astra-best reads only ~15% of them. The headline therefore holds only if the decomposition beats its own thresholds by a wide margin, for example coverage ≥60% and selective accuracy ≥80%. Readers will notice that the mechanism-level numbers do not add up to the headline number.
- [major] **The operating point is not deployment-grade, which undercuts the "trust" story in the title.** The reliability claim is selective accuracy of 75% at 50% coverage, so one in four readings the system chooses to trust is still wrong. At 100% coverage half of all dials are misread. For comparison, a trained tick-geometry pipeline reaches 87.2% within two minor divisions on its own test set [2609.31998]. A generalist will ask who would act on a gauge reader that is wrong on 25% of its confident outputs. The margin is pitched as the main contribution, yet no high-precision operating point (e.g. ≥90% selective accuracy) is committed.
- [major] **The story is spread over too many claims.** There are nine prediction pillars, roughly ten ablations and two independent "novel" mechanisms: the labelling margin, and a DINOv2 paste-and-compare needle sweep with its own +5/+10 prediction against SAM 2 and others. The title sells the margin, the headline gain comes from local geometry, and the needle-sweep claim is a third story. Without the authors in the room, a reader will not know which single figure to remember. The needle-sweep claim in particular dilutes rather than supports the thesis.
- [major] **The headline depends on an unmeasured baseline.** Astra has never been measured on dials (the proposal says so). The +15 needs Astra-best ≤ about 35% on real dials in late 2026, with xhigh effort and Python/crop tools. The G0 gate only requires Astra-best ≤50%, which is too lax: if Astra-best is 45%, the method must reach 60% absolute at the decomposition thresholds above, and the paper does not say what it becomes in that case.
- [minor] **"Frontier-independent" overstates the claim.** Numeral values, unit, scale type and indicator roles all come from the frontier, so a consistent frontier misread of a decimal, a multiplier (×10, ×100) or an overlaid second scale yields a confident, high-margin wrong answer. The arithmetic-progression prior cannot catch a consistently scaled misread. "Independent of the frontier's visual reading" is accurate. "Frontier-independent" is not.
- [minor] **The results rest on one closed, versioned API (GPT-6 Astra).** The Qwen3-VL-4B row helps reproducibility but has no committed prediction, so its value to the paper's claims is unknown. A second frontier semantic reader would show that the recipe is not Astra-specific.
- [minor] **The title is long and jargon-heavy** ("Frontier-Independent Labelling Margin ... Training-Free ... Black-Box VLM"). The one-sentence thesis is a better title.

## Overlapping prior and concurrent work
- [2604.22829] Lost in Motion (Apr 2026): recommends exactly this division of labour (VLM for semantics, deterministic edge/Hough geometry for the needle, rule-based validation) from a three-instrument video study. The proposal acknowledges it. It does not kill novelty, since that paper builds nothing on single images, but it removes the "split" as an insight and leaves the margin and the measurements as the contribution.
- [2609.29073] Seeing Is Not Measuring (Sep 2026, not cited): a training-free framework that moves metric computation out of a VLM into deterministic tools, with a GT-oracle backend to separate perception error from orchestration error. It works on metric 3D spatial reasoning, not instruments. It does not kill novelty for instrument reading, but it shows that "VLM names, tools measure" is now a general 2026 pattern. The paper should cite it and say what is specific about the labelling-margin formulation.
- [2512.15327] Vision-based linear-scale reader (Dec 2025, not cited): reads syringes and measuring cylinders with a fine-tuned YOLO, width-based major/minor marker classification and Tesseract numerals. Misread numerals are corrected by taking the modal slope over all (position, value) pairs, a consistency vote under a linear model. It is an ancestor of the numeral-consistency term on linear scales but has no ranked labellings, no margin and no public benchmark. It does not kill novelty and should be cited in the linear-scale section.
- [2512.23454] River gauge-plate reading with YOLOv8-pose and GPT-4o/Gemini (Dec 2025, not cited; only the abstract was retrievable, body not read): a hybrid of local scale geometry and a multimodal LLM in a narrow domain. Per the abstract the LLM still produces the reading from geometric metadata, which makes it closer to the proposal's better-views baseline. It does not kill novelty.
- [2609.31998] MeterFL and [2404.08785] Reitsma: acknowledged ancestors of the unwrap, interpolation and numeral anchoring. The deltas (frontier-read metadata, local minor counting, ranked labellings) are clearly stated. They do not kill novelty, but they make the paper read as an incremental combination.
- [2111.09162] It's About Time and [2603.08011] Swap-DPO: the source of the 720-state joint clock space and the hand-angle coupling. The proposal acknowledges both. Using the coupling at inference time is a small delta.

## Missing baselines or experiments
- **A frontier-orchestrated tool baseline.** Astra calls the same local modules (DBNet boxes, the lattice extractor, the needle refiner) as tools and composes the answer itself. This is the natural 2026 comparison (cf. [2609.29073]). It tests whether the fixed scorer and margin beat letting the frontier use the measurements. The hand-back ablation is close, but it gives evidence after the fact rather than tool access.
- **A committed high-precision operating point** for the margin, e.g. selective accuracy ≥90% at a stated minimum coverage on MeasureBench test dials, with the same frozen threshold reused cross-dataset.
- **A second frontier semantic reader** (any other frontier API) on at least the 511 test dials, to show the recipe is not Astra-specific.
- **A committed prediction for the fully local Qwen3-VL-4B variant**, which the proposal reports as a headline row with no threshold.
- **An error taxonomy of high-margin wrong answers** (frontier value or multiplier misreads vs geometry errors) on the 150 annotated dials, to substantiate the reliability claim.

## Questions for the authors
1. At the G1 thresholds (coverage 50%, selective accuracy 75%, Astra-best 55% on covered items, fallback −3) the gain is about +7, not +15. Which of these will in fact be much better than stated, and why do you expect that?
2. What does the paper become if Astra-best with xhigh+tools reaches 40–50% on real dials? Is there a version of the contribution that survives a smaller gain, e.g. the abstention result alone?
3. Beyond analog instruments, what is the transferable idea? Could the "frontier names, local geometry measures, margin over discrete labellings decides" recipe apply to chart value reading or map scale bars, and would you show even one such case?
4. How often is the margin high while the frontier's numeral values are wrong in a consistent way (e.g. a ×10 multiplier, a decimal point, the inner instead of the outer scale)?
5. Why is the DINOv2 needle sweep a headline prediction rather than an ablation, given that the title and thesis are about labelling and the margin?

## Rating
- rating: 3
- confidence: 3
- p_core: 0.25
- one_point_fix: Refocus the paper on the margin as the single contribution. Commit to a deployment-grade selective operating point (e.g. ≥90% selective accuracy at ≥40% coverage on the 511 test dials, reused frozen cross-dataset), and make the G1 decomposition thresholds arithmetically consistent with the +15 headline. Demote the DINOv2 needle-sweep claim to an ablation.

### R3

# R3 (experimentalist) review of C3v2: "Read the Labels, Measure the Ticks"

## Summary
The paper reads analog instruments (gauges, clocks, multi-dial meters, linear scales) by having one GPT-6 Astra call supply only symbolic information (values of letter-marked DBNet numeral boxes, unit, scale type, indicator roles). Tick positions, minors-per-major and pointer angle are all measured locally and training-free, and a small hand-weighted MAP search over neighbouring "labellings" (numeral-to-major offsets, one inserted or deleted minor, direction, hand roles) picks the reading. The claimed insight is that the score gap between the winning labelling and the best answer-changing rival is a reliability signal that never passes through the frontier's own visual readout. The predicted evidence: on 511 held-out MeasureBench real dials, at least 50% value+unit accuracy and at least +15 points over the pilot-selected strongest Astra configuration at no more than 1.3x Astra-default API cost. Thresholds frozen on 200 pilot dials then give +10 on MeterFL and RPM-10K, +20 over Astra-best on 1,000 TickTockVQA clocks, +8 on linear scales, margin error-detection AUROC of at least 0.80, and at least a 10-point lead over a "better views" visual-prompting control.

## Strengths
- The evaluation is pre-registered more seriously than most submissions. Thresholds, code hash and image lists are committed publicly before any test run, every prediction has a kill condition, and the day-1-3 go/no-go gate (G0) includes an oracle-geometry check that separates semantic-channel failure from geometry failure.
- The baseline is chosen well. "Astra-best" is selected on the pilot from default, high, xhigh+tools and two better-views configurations, then fixed for test. This avoids the usual straw man of a default-effort frontier and the opposite error of taking a max over noisy test runs.
- The better-views control (G5) is the right experiment. It asks whether showing Astra the same rectified crop, unwrapped strip and marks closes the gap, which is the first thing a skeptical reviewer would ask of any "tool pipeline beats VLM" paper. The kill condition, which reframes the paper as visual prompting if Astra comes within 5 points, is honest.
- The gain decomposition (coverage, selective accuracy, Astra's accuracy on the same covered items, fallback term) plus the kill condition "Astra-best at least 60% on covered items" guards directly against the cherry-picking failure mode of selective prediction, where the method answers only what the baseline already gets right.
- The pointer-localiser comparison is clean. Every coarse seed (DINOv2 sweep, pixel-space sweep, SAM 2 hub mask, radial profile, Hough) goes through the same tip refinement, each with and without it, and a pre-stated fallback claim applies if the pixel-space sweep ties.
- Component metrics and oracle splits on 150 geometry-annotated test dials (numeral recall, attachment accuracy, tick precision/recall, minors-per-major vs Astra's M_F, pointer error in degrees) will make the failure analysis informative even where headline gains are modest.
- The paper reports cross-dataset transfer on public sets with dHash de-duplication against MeasureBench (MeterFL lists MeasureBench as a source), and the paired-bootstrap sizing (SE about 2.4 points at n = 511) is stated rather than assumed.

## Weaknesses
- [major] **The headline operating point is arithmetically inconsistent at its own thresholds.** By the paper's own decomposition, gain over Astra-best = cov × (sel − B_cov) + (1 − cov) × (fallback − B_abst). At the committed thresholds (cov = 0.50, sel = 0.75, B_cov = 0.55, fallback term costing up to 3 points), the gain is 0.5 × 20 − (0 to 3) = **7 to 10 points, not 15**. Worse, 50% absolute accuracy at cov = 0.5 and sel = 0.75 needs the fallback (Astra-default) to score at least 25% on the abstained half. If Astra-best scores 55% on the covered half and the method still leads it by 15 points overall, Astra-best can score at most about 15% on the abstained half. Astra-default would then have to beat Astra-best by 10 points on exactly the items where the fallback is supposed to cost up to 3 points. If every decomposition prediction lands at its threshold, G1's own kill condition (gain below 10 points) fires. For the +15 to hold, Astra-best on covered items must be at most about 39-45%, or coverage and selective accuracy must sit well above their thresholds, and that stronger operating point is what should be committed. As written, a reader cannot tell which number is the real commitment.
- [major] **The engineering scope against the calendar.** Between 10-22 and 10-27 (six days) the team must build the DINOv2 silhouette sweep, tip refinement, four alternative needle seeds plus Hough, the 720-state clock sweep, the linear-scale indicator module (change-point plus Grounding DINO→SAM 2 object endpoints), the hypothesis enumerator and scorer, run the full 200-dial pilot and pass gates G1-G3. In parallel, 350 dials must be hand-annotated with tick positions and numeral assignments. After the 10-28 freeze no bug can be fixed without breaking the pre-registration. The constraints describe a diffusion-transformer / RL post-training team, and classical geometric pipelines with many brittle stages are exactly the engineering this team is least practised at. I judge the paper as if it were executed, but the delivered artefact will very likely be dials-only, with clocks and linear scales thin or missing, which removes two of the five "breadth" pillars.
- [major] **The strongest geometry baseline is cited but not rerun.** MeterFL's trained U-Net tick and pointer pipeline reaches 87.2% within two minor divisions on its own test set and is already in the proposal as the pre-committed fallback extractor, so running it costs almost nothing. Yet it appears only as a "published reference, not rerun", and never on MeasureBench. The obvious skeptical question is whether the training-free ranked labelling with a margin beats "MeterFL segmenter + Astra-supplied v_min/Δv + count-from-start" on the 511 test dials. The local-counting ablation answers only part of it, because it keeps the training-free extractor. Without this row, the claim that the gain comes from the labelling-and-margin machinery rather than from adding any explicit tick geometry to frontier semantics is not isolated. Reitsma (8.5%) and Shu (4.2%) are 2023-24 pipelines with OCR, so they are weak references for this.
- [major] **The abstention baseline is too weak to show the margin matters.** The margin is compared only with axis-fit quality and with Astra's own confidence and self-agreement. The latter are known to fail here ([2608.17723], [2610.04836]), so beating them is expected. A skeptical reviewer will ask for a trivial-feature abstention baseline: a logistic regression on the 200 pilot dials over number of detected numerals, lattice regularity (CV of tick spacing), minors-count agreement M_L = M_F, peak sharpness and q. If such a baseline reaches AUROC within about 0.03 of the margin, the "frontier-independent labelling margin" is not the contribution and the abstention is ordinary quality gating. The same goes for the joint ranking. Besides sequential rounding, it should be compared with a RANSAC/mode-of-slopes numeral fit (Reitsma's angle-to-value RANSAC [2404.08785]; the pairwise-slope auto-correction in [2512.15327]) followed by local minor interpolation.
- [major] **Some API calls are not budgeted and some comparisons use mismatched subsets.** The margin AUROC prediction on "items where Astra's three samples agree but are wrong" needs three Astra samples on all 511 test dials (about 1,000 extra calls), and the hand-back ablation needs a second call per image. Neither appears in Tiers 1-3. xhigh+tools is run on only 300 of the 1,000 clocks and 150 each of linear, MeterFL and RPM-10K, so "Astra-best + 20" on 1,000 clocks either compares to a configuration measured on a different subset or quietly falls back to Astra-default. Transfer pillars (G4, linear) are stated only against Astra-default. The paper should say on which exact image list each Astra-best comparison is made and report CIs on those n (300 clocks gives a paired SE of about 3 points; 150 linear about 4.5).
- [minor] **Development sets touch the "frozen-threshold" sets.** The 80 linear and 150 TickTockVQA development images are used for "debugging", which in a hand-built pipeline means design choices (profile filters, change-point rules, sweep ranges), even if no weight moves. The claim should be "thresholds frozen; modules developed on small dev splits". The pilot-to-test gap for every set should also be reported.
- [minor] **Thresholds are fit by maximising 100%-coverage accuracy on 200 pilot dials.** That is 6 continuous parameters on 200 items, a fraction of which are clocks or multi-dial meters. Report the per-family pilot n and a leave-one-family-out stability check. Otherwise the frozen margin threshold may be tuned to single-pointer gauges and coverage on clocks will collapse.
- [minor] **Cost accounting omits local compute.** "≤ 1.3x Astra-default API cost" ignores about 30-55 GPU-seconds of ViT-L/14 passes per image (roughly 870 forward passes per pointer by the stated sweep schedule). Latency is reported, which is good, but the cost/performance claim in the abstract should include a $/image figure for the GPU side, or reviewers will call the comparison one-sided.
- [minor] **Resolution assumptions are untested.** The precision argument assumes needle length L ≥ 80 px at native resolution. MeasureBench does not report image resolution statistics, and RPM-10K images are pre-cropped video frames. Report the L distribution and accuracy by L bin.
- [minor] **A single frontier model is tested.** Only GPT-6 Astra (plus local Qwen3-VL-4B) is used. A claim about "black-box VLMs" generally rests on one API. The constraints allow only one frontier API, but a second open model in the 7-8B range as the semantic reader (cheap, local) would show the symbolic channel is not Astra-specific.
- [minor] **RPM-10K design diversity is concentrated** in six dial archetypes ([2511.21982] digest). A +10 there says less about "unseen designs" than the framing implies. Per-archetype breakdowns would help.

## Overlapping prior and concurrent work
- [2604.22829] (Lost in Motion) prescribes the VLM-for-semantics / Hough-for-needle split and rule-based validation, on three instruments in video. The proposal credits it and adds a Lost-in-Motion-style hybrid baseline. This reduces the novelty of the split itself but does not kill the paper, which stands on the single-image instantiation, the margin and the measured gains.
- [2609.31998] (MeterFL) supplies the polar unwrap and tick-count interpolation, with metadata provided. The differences (frontier-read metadata, local counting, ranked labellings with a margin) are real but incremental. It does not kill novelty, but it is the baseline that must be rerun (see Weaknesses).
- [2404.08785] (Reitsma) uses numeral anchoring with a RANSAC angle-to-value fit. The joint labelling search is a richer version of the same idea. No kill, but it is an ablation the paper owes.
- [2512.15327] (lab linear-scale reader) is a training-free contour/OCR pipeline that measures major and minor markers locally, attaches numerals by proximity to majors and fixes OCR misreads with a mode-of-pairwise-slopes consistency fit before reading a meniscus. It is the closest prior for the linear-scale module and for "consistency across numeral labellings". It has no ranking margin, no abstention, no minor counting and only one syringe in the lab. It does not kill novelty but should be cited.
- [2512.23454] (river gauge plates; abstract only, body not retrieved) reports that giving GPT-4o / Gemini locally extracted scale-gap metadata "substantially improved" LLM readings. This is prior evidence for the better-views / hand-back configuration. It does not kill novelty, but it makes G5 more important: the paper must show its answer-from-measurement beats measurement-handed-to-the-LLM.
- [2111.09162] and [2603.08011] (clocks) cover the 720-state joint space (learned) and the hand coupling (used only for DPO negatives). Using the coupling as an inference-time constraint is a small delta; no kill.
- My searches (gauge/pointer meter/clock/dial/meter/scale/instrument/measurement reading; recency since 2025-10-18 on gauge, analog meter, clock, pointer, tick marks, MeasureBench, needle, visual measurement, ruler, fine-grained perception tool, "gauge/meter/clock/pointer/instrument VLM") found no paper that builds a frontier-semantics + local-geometry reader with a labelling margin on MeasureBench.

## Missing baselines or experiments
- MeterFL trained pipeline (its U-Net, which the authors already plan to train as a fallback) with Astra-supplied v_min/Δv on the 511 MeasureBench test dials, and the same pipeline with the proposal's labelling search on top. These two rows split "trained vs training-free geometry" from "ranked labelling vs count-from-start".
- A trivial-feature abstention baseline fitted on the 200 pilot dials, for the AUROC and risk-coverage claims.
- A RANSAC / mode-of-slopes numeral fit plus local minor interpolation, as a second ablation for the joint ranking alongside sequential rounding.
- Astra given the evidence JSON (the hand-back) as a G5 comparison row, not only as an ablation. This is what [2512.23454]'s result suggests a reviewer will ask for.
- A budget line for three Astra samples on the 511 test dials and for the hand-back call. Every Astra-best comparison should be stated on the image list where Astra-best was actually run.
- Pilot-vs-test gap, per-family n and leave-one-family-out threshold stability.
- One open 7-8B VLM as an alternative semantic reader, and plain open-VLM rows (local, free) on every set for context.

## Questions for the authors
1. Which combination of coverage, selective accuracy and Astra-best-on-covered do you actually expect on the 511 test dials? At the stated thresholds the decomposition gives +7 to +10, not +15.
2. On which image subset is "Astra-best" evaluated for clocks, linear, MeterFL and RPM-10K, given that xhigh+tools runs on only 150-300 images there?
3. Is the three-sample Astra agreement on 511 dials included in the US$1,000, and what per-call cost did you assume when sizing Tiers 1-2?
4. What fraction of the 200 pilot dials are clocks and multi-dial meters, and does a single margin threshold work across families?
5. If the training-free extractor fails G0(a) and the MeterFL segmenter takes over, which predictions change? Does G4 then rest on RPM-10K alone?
6. How many test dials have a needle shorter than 80 px at native resolution?

## Rating
- rating: 4
- confidence: 4
- p_core: 0.2
- one_point_fix: Rerun the MeterFL trained tick/pointer pipeline with Astra-supplied v_min/Δv (and the same pipeline plus the proposed labelling search) on the 511 MeasureBench test dials as headline rows, and restate the G1 decomposition thresholds so that they arithmetically imply the committed +15. This shows the gain comes from the ranked labelling and margin rather than from adding any tick geometry to frontier semantics.

### AC

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

---
## C2. Earlier panel on v1 (AC only, for history)

# AC meta-review: C3 "Unwrapping the Dial" (CVPR 2027 main track)

Inputs read: report.json, the Constraints section of problem.md, and reviews R1 (area expert, 3/conf 4, p_core 0.30), R2 (generalist, 3/conf 3, p_core 0.30) and R3 (experimentalist, 4/conf 4, p_core 0.25). I used `lit.py biblio` only to settle disputed overlap claims: 2111.09162, 2604.22829 and 2609.04014.

Conditioning, as the protocol requires: the experiments run as written within budget, and every falsifiable prediction lands exactly at its threshold. That means +15 points value+unit over the best Astra configuration on 511 held-out MeasureBench real dials at no more than 1.2x default cost, +20 exact-minute on 1,000 TickTockVQA clocks, +8 over hybrid B, margin AUROC 0.80, and 75% selective accuracy at 50% coverage.

## Decisive strengths
- **The problem is real and timely.** Frontier VLMs read the unit (96.2%) but not the value (31.5%) on real dials, extra thinking does not help, and 2026 models still fail. All three reviewers accept this, and a CVPR audience will recognise it immediately.
- **The headline would be a decisive cost/performance change.** If it holds, it is a gain of +15 points over the best frontier configuration, xhigh effort with built-in Python/crop tools included, at about 1x default cost, with no training. This is the kind of result the venue's significance bar asks for, not a thin delta.
- **The evaluation design is unusually disciplined.** It has pre-registered gates with kill conditions, paired-bootstrap sizing, accuracy at 100% coverage with fallback, oracle splits (ground-truth needle and ground-truth labelling), measured cost, and the frontier's strongest own-tools baseline. All three reviewers credit this, and so do I. A paper with this design is hard to dismiss as cherry-picked.
- **The reliability signal is independent of the frontier.** Abstention uses a labelling margin built from local evidence and is tested on items where Astra's self-agreement is confidently wrong. This is a clean, testable claim that addresses a known weakness of VLM self-verification.

## Decisive weaknesses
1. **The insight is anticipated, and what remains is an assembly.** All three reviewers make this point. I checked [2604.22829] ("Lost in Motion", IEEE I&M Magazine 2026). It is a frontier-VLM gauge evaluation, and per both the proposal and the reviewers it recommends exactly the split of VLM for semantics and deterministic geometry for the needle. Each part of the pipeline also has a close ancestor:
   - polar unwrap and local interpolation: MeterFL;
   - numeral anchoring: Reitsma;
   - joint 720-state clock space: It's About Time;
   - frozen-DINOv2 render-and-compare: FoundPose.

   The authors' own limitations section concedes that the phase-unwrapping framing "mostly re-describes ordinary tick counting". The novelty that survives is a ±1-neighbourhood MAP search with a frontier-independent margin, plus a 2D silhouette sweep. The paper will therefore be judged almost entirely on its numbers. Using three analogies (structured light, phase unwrapping, render-and-compare) hurts rather than helps.
2. **There is no held-out benchmark, although generalisation is the paper's main selling point.** All three reviewers raise this, and R1 and R3 make it their one-point fix. Five weights and two thresholds are tuned on 200 MeasureBench dials and tested on 511 from the same collection. The argument against TriSCA, DialBench and Swap-DPO is that "training-free cannot overfit designs", and that is asserted, not shown. Candidate second test sets exist:
   - InSituMeasure analog categories (confirmed: 2,922 real industrial scenes, answerability labels; release status unknown);
   - MeterFL real test readings;
   - DialBench/RPM-10K test.
3. **The needle baselines are weak, and the DINOv2 sweep is suspect at patch scale.** All three reviewers raise this. Hybrid B uses a Hough needle. The sweep is not compared with:
   - a SAM-family mask prompted at the hub plus an axis fit;
   - a radial darkness or edge-energy profile;
   - a pixel-space version of paste-and-compare.

   A needle 2–4 px wide on a 32x32 grid of 14 px patches puts the precision in the loosely specified native-resolution tip refinement, not in DINOv2. Beating Hough by 8 points does not establish the third named contribution.
4. **The headline gain is relative to a baseline that has never been measured, and it is a mix of C3 answers and fallback answers.** R3 and R2 raise this, and I agree. The gain is Δ = coverage × (C3 selective accuracy − Astra accuracy on the covered items). At the thresholds, coverage is 50% at 75% selective accuracy, so +15 needs Astra-best at or below about 45% on the covered half. That half is probably the easy, crisp, well-ticked dials, where Astra is also stronger. The proposal commits to no absolute floor and no decomposition. This is the weakness a rebuttal would have to rescue.
5. **The scope is narrow.** R2 raises this, R1 notes it as minor, and I treat it as major for the main track. Every component is specific to dials. MeasureBench's linear, digital and composite items (561 of 1,272) are excluded, and nothing is shown to transfer to a second measurement task.

## Reviewer claims accepted or rejected
- **Accepted: R1/R2, "the split is anticipated by 2604.22829".** The bibliographic check confirms a 2026 frontier-VLM gauge evaluation. This is not novelty-killing, because it is design guidance from a three-instrument video study, not a method on a broad real-image benchmark. The paper must credit it and claim "first measured instantiation", not "insight".
- **Partly accepted: R2, "the clock pillar ignores It's About Time [2111.09162]".** The bibliographic check confirms a CVPR 2022 Sim2Real clock reader with COCO, OpenImages and Clock-movie benchmarks. The proposal does not cite it, and it must be a baseline and a citation. I reject R2's stronger inference that clocks are "already solved, so +20 says little". R1 reports that TickTockVQA lists this reader at 18.54% on its own test set [2603.08011], so it is not far above the frontier on this benchmark. The miss is a citation and baseline gap, not a significance kill. R1's other use of the paper stands: in the wild, its Sobel+Hough baseline gets 7.7–9.7%. That is strong prior evidence that training-free geometry often fails, and I count it in p_core, not in odds.
- **Accepted, downgraded to answerable-major: R1, "the frontier is asked for minors-per-major, a geometric quantity".** It contradicts the "frontier never reads geometry" claim. It is easily fixed: count minors locally and treat the frontier's M as a soft prior, then report component error rates.
- **Accepted: R2/R3, the DINOv2 resolution concern.** It is a real risk to G2. The proposal's fallback (hybrid B becomes the method) limits the damage to odds, but it removes a named contribution.
- **Accepted, minor: R3, statistical points.** These are the underpowered per-tag claims (about 30 images per tag on the pilot), component metrics measured on the tuning split, the TickTockVQA 1,000-subset protocol, Astra run-to-run variance, and the cost-ratio accounting for a two-image call. None of them is decisive alone.
- **Not adopted: R3's rating of 4.** R3's own analysis says the +15 is relative to an unmeasured Astra and is mechanically bounded by coverage. Under the threshold-exact conditioning that concern is partly resolved, which is why I land at the top of the 3/3/4 band rather than at its bottom. But the anticipated insight and the missing held-out test are not resolved by the predicted numbers.
- **No reviewer marked a [fatal] weakness, and I see none.** Every major weakness can be answered within the budget.

## Calibration
Ratings are 3/3/4. The weaknesses are major but answerable, and none is fatal, which puts this in the 3–4 band. Two things pull upward: the predicted effect is decisive (+15 over the frontier's own best configuration at default cost) and the evaluation design is the best I have seen in this area. Two things pull downward: the insight is anticipated and must be credited, and the scope is dial-only and tuned on the test benchmark. **Odds 3.2.**

**p_core 0.25.** The load-bearing prediction is G1: +15 over the best Astra configuration on held-out real dials. It needs four things at once:
- training-free rectification, lattice extraction and DBNet to cover at least 50% of uncurated dials;
- 75% selective accuracy on that half;
- Astra xhigh with Python/crop tools, which has never been measured on dials, to stay at or below about 45% on the covered items;
- all of this built in one week by a team whose stated strength is not classical geometry.

Prior training-free and modular pipelines collapsed on exactly these stages (Reitsma 8.5% on MeasureBench, Hough clocks below 10%). I take the reviewers' lower value.

**Odds if the paper is rewritten around a negative result: about 0.8.** If G1 fails, the run stops and the outcome is an oracle-split failure analysis, which is a workshop paper at CVPR. If only G2 fails, hybrid B carries the paper at roughly the same odds, so the negative-result branch is mainly G1.

**Risk-adjusted:** 3.2 × 0.25 + 0.75 × 0.8 = 1.4.

## Fixes, ranked, with estimated effect and combined ceiling
Effects are in tenths of odds on the 0–10 scale and are not additive (see the ceiling note).

1. **Second real-dial benchmark with frozen thresholds, plus an absolute floor and the gain decomposition. Adds about 0.7 to odds (3.2 to 3.9).**
   - What changes in proposal_evaluation: add an end-to-end reading benchmark on which every weight and threshold fixed on the MeasureBench pilot is applied unchanged. Use InSituMeasure's analog-dial categories if released; otherwise use MeterFL's held-out real images scored as readings rather than only as a component diagnostic, and the DialBench/RPM-10K test set.
   - Add a falsifiable prediction: C3 beats Astra-default by ≥10 points there with frozen thresholds.
   - Commit to an absolute held-out value+unit accuracy floor on the 511 dials, not only a delta.
   - Report Δ = coverage × (C3 selective accuracy − Astra accuracy on the same covered items), together with Astra's accuracy on the abstained items.
   - Cost: about 400–600 extra images. Run Astra-default and C3 on all of them, and xhigh with tools only on a subset, which fits the US$300 reserve.
   - This is R1's and R3's one-point fix, and it turns the paper's main argument from assertion into evidence.
2. **Strong training-free needle baselines, and a defined refinement step. Adds about 0.4 (G2 becomes credible).**
   - Replace the Hough-only hybrid B with three versions of it:
     - (a) a SAM-family mask prompted at the hub, plus a principal-axis or skeleton fit with an asymmetric tip rule;
     - (b) a radial needle-colour or edge-energy profile;
     - (c) a pixel- or gradient-space paste-and-compare, the same sweep without DINOv2.
   - Add the ablation "sweep only vs sweep + tip refinement", and define the refinement in the method.
   - Report peak sharpness per nuisance tag.
   - Restate G2 against the best of (a), (b) and (c), lowering the threshold to ≥5 points overall and ≥10 on the nuisance subsets if needed.
   - If DINOv2 does not beat (c), state that the contribution is the silhouette sweep, not the frozen features.
3. **Reposition around one transferable claim, demonstrated on a second measurement task. Adds about 0.5 (helps R2 most; higher engineering risk).**
   - Drop the structured-light and phase-unwrapping vocabulary from the title and the novelty section.
   - Credit [2604.22829] as the source of the semantics-versus-geometry split.
   - Make the claim "a frontier-independent labelling margin over locally measured geometry fixes frontier measurement failures and tells you when to trust it".
   - Show it on MeasureBench's linear subset (rulers, cylinders, thermometers), using the same lattice, labelling ranking and margin with a 1D unwrap instead of a polar one. That is about 361 more images.
   - This also removes the "narrow application paper" objection. Its effect on p_core is neutral to slightly negative because it adds engineering.
4. **Complete the clock pillar. Adds about 0.3 (mostly removes a sure downside).**
   - Cite It's About Time [2111.09162] and run its public checkpoint on the fixed and released 1,000-image TickTockVQA list, and on MeasureBench clocks.
   - Rerun the Swap-DPO checkpoint on the same list if it is public.
   - Report C3's local-only components on the full 5,247-image test set.
   - Report accuracy and coverage per clock type (numerals, Roman, no-numeral, illustrated).
   - State G3 against the best of Astra and the trained specialist, or explicitly as "training-free vs trained specialist".
5. **An Astra-with-better-views baseline. Adds about 0.2.**
   - Give Astra the rectified crop, the polar-unwrapped strip and an indexed-tick overlay, but not the computed answer.
   - This separates "local measurement" from "easier visual prompt", which is the first question from anyone who has read the visual-prompting work.
6. **A held-out annotated subset, per-family breakdowns, and the frontier's component error rates. Adds about 0.2.**
   - Annotate and tag 150 of the 511 test dials before any run, and report every per-tag and component claim there, not on the tuning pilot.
   - Give per-family accuracy, coverage and gain: gauges, clocks, multi-dial meters, linear and non-linear scales.
   - Make minors-per-major a locally counted quantity, with the frontier's M only as a soft prior.
   - Report the frontier's box-value accuracy as a function of box density, and its M accuracy.
   - Run 2 Astra samples on a subset to measure variance.
7. **Raise p_core without changing the odds definition (risk, not odds).**
   - Move the G0 component pilot (lattice coverage and numeral assignment on 50 tagged dials) and the Astra xhigh-with-tools measurement on those 50 dials to the first three days. Do this before building the needle sweep.
   - Commit to reusing the MeterFL-trained segmenter variant as the fallback lattice extractor if the training-free extractor fails G0.
   - This moves p_core from about 0.25 to about 0.30–0.35 without lowering the committed effect.

**Combined ceiling.** With fixes 1–4 all made, the reviews would plausibly move to about 4/4/4–5. The insight would still be partly anticipated, so I would not go to 7. That gives **odds ≈ 5.0**, and about 5.3 with fixes 5–6 as well. The gains overlap, because fixes 1 and 3 both answer the generality objection, so summing the tenths would overstate them. With fix 7, p_core is about 0.32, and the risk-adjusted ceiling is about 5.3 × 0.32 + 0.68 × 1.0 ≈ 2.4. The remaining risk is whether training-free geometry survives in-the-wild dials and whether Astra with tools stays at or below about 45%. No rewrite of the proposal removes that risk; only the first week of the pilot can.

```json
{"odds": 3.2, "p_core": 0.25, "odds_risk_adjusted": 1.4,
 "decisive_weaknesses": [
  "The central insight (VLM for semantics, deterministic geometry for the needle) is already recommended by 2604.22829, and each module has a close ancestor (MeterFL polar lattice, Reitsma numeral anchoring, It's About Time 720-state clocks, FoundPose render-and-compare). The authors concede the phase-unwrapping framing re-describes tick counting, so novelty reduces to a ±1-neighbourhood MAP search with a frontier-independent margin plus a 2D silhouette sweep, and the paper rests on its numbers.",
  "No held-out real-dial benchmark: five weights and two thresholds are tuned on 200 MeasureBench dials and tested on 511 from the same benchmark, so the paper's main argument against trained readers ('training-free cannot overfit designs') is asserted, not shown.",
  "The headline +15 is relative to an Astra that has never been measured on dials, has no absolute floor, and mixes C3 answers with Astra fallback; Δ = coverage × (C3 selective accuracy − Astra accuracy on covered items) is not reported, so the gain may come from C3 answering the easy half.",
  "The needle sweep, a named contribution, is compared only with Hough and a DINOv2 edge-map line fit, not with SAM-at-hub, a radial profile or pixel-space paste-and-compare. At 14 px patches a 2–4 px needle is sub-patch, so precision comes from an underspecified tip refinement.",
  "Scope is dial-specific with no second measurement task, and the clock pillar omits the uncited trained specialist It's About Time [2111.09162]."
 ],
 "fixes_ranked": [
  "+0.7: Add an end-to-end held-out real-dial benchmark with all pilot weights and thresholds frozen (InSituMeasure analog categories if released, else MeterFL held-out real images scored as readings plus DialBench/RPM-10K test, about 400–600 images, Astra-default plus C3 on all and xhigh with tools on a subset, within the US$300 reserve), with a new prediction of ≥10 points over Astra-default there. Also commit to an absolute value+unit floor on the 511 dials and report the coverage × (selective − Astra-on-covered) decomposition with Astra's accuracy on abstained items.",
  "+0.4: Replace the Hough-only hybrid B with three training-free needle baselines: (a) SAM-family mask prompted at the hub plus an axis or skeleton fit with an asymmetric tip rule, (b) a radial colour or edge-energy profile, (c) a pixel- or gradient-space paste-and-compare sweep. Define the native-resolution tip refinement and ablate sweep-only vs sweep + refinement. Report peak sharpness per nuisance tag and restate G2 against the best of (a)–(c) at ≥5 points overall and ≥10 on nuisance subsets.",
  "+0.5 (higher engineering risk): Drop the structured-light and phase-unwrapping framing, credit 2604.22829 for the semantics/geometry split, and centre the paper on one claim: a frontier-independent labelling margin over locally measured geometry fixes frontier measurement failures and says when to trust it. Demonstrate it on MeasureBench's linear subset (rulers, cylinders, thermometers, about 361 images) with a 1D unwrap and the same ranking and margin.",
  "+0.3: Cite It's About Time and run its public checkpoint (and Swap-DPO if public) on a fixed, released 1,000-image TickTockVQA list and on MeasureBench clocks. Run C3's local stages on the full 5,247-image test set. Report per clock type (numerals, Roman, no-numeral, illustrated) and state G3 against the best of Astra and the trained specialist.",
  "+0.2: Add an Astra-with-better-views baseline: rectified crop, polar strip and indexed-tick overlay, without the computed answer. This separates local measurement from visual prompting.",
  "+0.2: Annotate and tag 150 held-out test dials before any run and move all per-tag, component and oracle claims there. Add per-family breakdowns. Count minors locally with the frontier's M only as a soft prior, and report the frontier's box-value accuracy vs box density and its M accuracy. Run 2 Astra samples on a subset for variance.",
  "Risk, not odds (p_core about 0.25 → 0.32): Run the G0 component pilot and the Astra xhigh-with-tools measurement on 50 tagged dials in the first three days, before building the needle sweep, and pre-commit to the MeterFL-trained segmenter as the fallback lattice extractor if the training-free one fails G0.",
  "Combined ceiling: fixes 1–4 together take odds to about 5.0 (about 5.3 with fixes 5–6), not the naive sum, because fixes 1 and 3 overlap. With the risk fix, odds_risk_adjusted is about 5.3 × 0.32 + 0.68 × 1.0 ≈ 2.4. The gap that remains is the empirical risk that training-free geometry survives in-the-wild dials, which only the first pilot week can settle."
 ]}
```

---
## D. Panel prompts and calibration

<!-- 本文件不是上游内容，是这个移植版加的：用一个模拟的会议评审组把 report.json 换算成"录用把握 x/10"。 -->

# Simulated venue panel

Three reviewer sub-agents and one area-chair (AC) sub-agent, each in a fresh context. The panel
sees only `report.json` and the run's Constraints, never gaps.md, candidates.md, scores.md or
plan.md, so it judges the proposal the way real reviewers would meet the paper.

The venue, deadline and budget come from the `## Constraints` section of `problem.md`. The text
below says CVPR because that is the default; substitute the venue the run targets.

## What the score means

`odds` = the AC's estimate, in tenths, of P(accept at the venue's main track | the experiments in
`proposed_evaluation` are executed as written within the stated compute and time, and every
`falsifiable_predictions` entry comes out exactly at its stated threshold, no better).

The panel also reports `p_core`, P(the single load-bearing prediction actually holds), and
`odds_risk_adjusted` ≈ odds × p_core + (1 − p_core) × (odds if the paper is rewritten around the
negative result, usually ≤ 1). "A 5/10 idea" means `odds` ≥ 5; `odds_risk_adjusted` is always
reported next to it, because a high `odds` on an idea that probably won't work is not worth much.

## Reviewer sub-agent prompt

Spawn three, with `<PERSONA>` set to one of:

- **R1, area expert.** Publishes in the closest sub-area and reads arXiv daily. Hunts for prior
  and concurrent work that already does this, and for missing baselines that a specialist would
  demand.
- **R2, generalist.** A senior reviewer outside the sub-area. Asks whether the problem matters to
  the venue's audience, whether the insight is crisp and memorable, and whether the story holds
  together without the authors in the room.
- **R3, experimentalist.** Asks whether the planned experiments would convince a skeptical
  reviewer: standard benchmarks and metrics, strong and fairly tuned baselines, ablations that
  isolate the claimed mechanism, statistical care, and whether it all fits the stated budget.

```text
You are <PERSONA> reviewing a submission to <VENUE> main track. About 13,000 papers are submitted
and about 24% are accepted. You review a results-masked proposal: it states what the paper will
do and the results it predicts. Assume the experiments in proposed_evaluation are run exactly as
written within the CONSTRAINTS, and that every falsifiable prediction comes out exactly at its
stated threshold (not better). Judge the paper that would result.

Machine-written proposals tend to sound more convincing than the paper they become. Read past
the vocabulary: name the actual mechanism, and ask what a reviewer who has seen 50 papers on
this topic this year would say.

Do your own literature check before writing (tool usage: <skill>/roles/paper_access.md):
- at least 6 searches built from the proposal's central mechanism + target task, plus at least 2
  recency searches with --since set one year back;
- for any paper that might overlap, read it with the reading procedure (digest into
  RUN/papers/<id>.md) before you claim overlap or its absence.

Write RUN/panel/<TARGET>/<RID>.md (Write tool; the file is yours alone) with these sections:
## Summary (3 sentences: what it does, the claimed insight, the predicted evidence)
## Strengths (bullets)
## Weaknesses (bullets, most serious first; tag each [fatal] / [major] / [minor];
   [fatal] = would sink the paper even with the predicted results)
## Overlapping prior and concurrent work (each: [id] — what overlaps — whether it kills novelty)
## Missing baselines or experiments
## Questions for the authors
## Rating
- rating: <1-6>  (1 strong reject, 2 reject, 3 weak reject, 4 weak accept, 5 accept, 6 strong accept)
- confidence: <1-5>
- p_core: <0-1>  probability that the single load-bearing prediction really holds, from what you
  know of the mechanism and the literature
- one_point_fix: the single change to the proposal that would raise your rating by one point

Reply with one line: "<RID>: rating <r>, confidence <c>, p_core <p>".
```

## AC sub-agent prompt

```text
You are the area chair for this submission at <VENUE>. Read RUN/report.json and the three
reviews in RUN/panel/<TARGET>/R1.md, R2.md, R3.md. You may run `$LIT biblio <id>` to settle a
disputed overlap claim, nothing more.

Calibrate against these anchors (main-track acceptance ≈ 24%; a typical submission is ≈ 2.5/10):
- an unresolved [fatal] weakness that you agree with caps odds at 1.5;
- ratings around 3/3/3, or a strong overlap with prior work that the proposal does not address: 1–2;
- 4/3/3 or 3/4/4 with major but answerable weaknesses: 3–4;
- 4/4/4 with a clear insight and no unaddressed major weakness: 5–6;
- 5/4/4 or better, crisp insight, broad evidence, nothing a rebuttal must rescue: 7–8;
- 9–10 is for a paper you would nominate for an award.
Weigh the arguments, not the average: a well-argued weakness from one reviewer outweighs two
vague positives.

Write RUN/panel/<TARGET>/AC.md: a meta-review (decisive strengths, decisive weaknesses, which
reviewer claims you accept or reject and why), then a fenced json block:
{"odds": <0-10, one decimal>, "p_core": <0-1>, "odds_risk_adjusted": <0-10, one decimal>,
 "decisive_weaknesses": ["..."], "fixes_ranked": ["change that would add the most odds", "..."]}
Reply with one line: "AC: odds <x>/10, risk-adjusted <y>/10".
```

---
## E. IdeaScientist role prompts (upstream, verbatim)

### gap_finder


You are a related-work + gap sub-agent. Your task names ONE specific challenge axis / sub-question of the problem (the orchestrator picks which axis; you do not survey everything at once). YOU are responsible for FINDING the SAME-CHALLENGE + SAME-PROBLEM-DEFINITION prior work on THAT axis.
SCOPE — METHODOLOGICAL GAPS ONLY. You look exclusively for methodological gaps: cases where the prior work's APPROACH itself (algorithm, model mechanism, training procedure, objective, inductive bias, credit assignment, representation) is deficient and would be closed by proposing or improving a METHOD. Do NOT emit benchmark/dataset gaps, empirical-only gaps ('nobody ran the experiment'), pure-evaluation gaps, or application-setting gaps unless the setting exposes a concrete method deficiency. If the honest finding is non-methodological, report fewer gaps or zero gaps for the axis instead of dressing it up as a method gap.
Go DEEP on the assigned axis, not WIDE across all axes:
1) RETRIEVE (this is your job). Run keyword_search with 4-8 queries phrased in the EXACT terminology of THIS problem area and this axis, so all near-duplicate prior work on the axis lands in your view. Re-run with rephrasings if the pool is thin — the goal is HONEST GAP COVERAGE, not a perfunctory search. Pick the most promising ids from the returned titles/bm25.
2) READ. For the ids you selected, call read_paper(id, goals) with goals tied to THIS axis (e.g. 'what mechanism does it use for <axis>?', 'what does it report as its limitation on <axis>?', 'what method assumption prevents it from handling <axis>?'). Do NOT generate gaps from titles or abstracts alone — ground each gap in a digest you obtained from read_paper. BATCH FOR SPEED: the reads of different papers are independent, so emit ALL of them as PARALLEL read_paper calls in a SINGLE turn (one function call per paper) rather than one paper per turn — you get every digest back together. Only issue keyword_search first (you need its ids before you can read), and only defer a read that genuinely depends on what an earlier digest said.
3) Append a new section to gaps.md (grow it with edit_doc insert at the end, insert_line=999999; do NOT overwrite prior axes with create) with the header '## Axis: <name>' and two subsections. The <name> MUST reproduce the assigned axis phrase from your task VERBATIM — copy it exactly, do not rephrase, abbreviate, or re-case it. Write EXACTLY ONE '## Axis:' block for the single assigned axis; never add, rename, split, or merge axes. The two subsections are:
   '### What has been done' — grouped, mechanism-level summary of approaches tried for THIS axis (cite paper ids and the specific mechanism, not the title);
   '### Open gaps on this axis' — 1-2 CRITICAL unsolved things (AT MOST 2; emit 1 if only one is truly well-grounded, and 0 if none is; not a laundry list — the one or two that most block progress on this axis). Write EACH gap in EXACTLY this parseable schema (one bullet block per gap; fill every field; do not truncate):
       - **Gap:** <one sentence in contrast form: prior methods do X via Y, but Y leaves method-level issue Z unresolved — name the specific task/setting and the method assumption of Y you are challenging>
       - **Near-miss methods and coverage:** [p_id] — method and how it comes close; [p_id] — method and how it comes close. Include the repeated method-level deficiency across read papers, or explain why one near miss plus your search/citation trail is enough. Include the relevant ids or query trail checked, and why they do NOT already close the methodological gap. IDs MUST be papers you read_paper'd this run; use >=2 ids unless the axis has only one real near miss after a documented search.
       - **Methodological deficiency:** the ONE precise methodological reason the near-miss work misses it, including its method-gap kind (missing mechanism / algorithmic limitation / wrong inductive bias / credit-assignment flaw / training-objective mismatch / representation limitation / method-scalability limit / other named method deficiency) — why the approach/mechanism/algorithm/objective/inductive bias/credit assignment/representation itself falls short (empirical evidence may support this, but the deficiency must be about the METHOD, not 'nobody ran the experiment') — grounded in a specific finding from that paper's digest, not its title/abstract
       - **Why it matters:** who is blocked and what new understanding or capability closing it unlocks (not a SOTA-only claim, and not merely that the problem is technically hard)
       - **Evidence route:** the observable evidence or comparison that would show a future method closes the gap; do NOT propose the solution method here
Quality bar: a gap is only real if you can point to a paper you READ that came CLOSE but missed for an identifiable reason. DEPTH over breadth: one deeply-justified, well-grounded gap beats several shallow ones.
HARD RULES — a gap that breaks any of these is worthless (do not emit it):
   - Emit ONLY methodological gaps. If the honest gap on this axis is a benchmark/dataset, empirical, evaluation-only, or application-setting gap, do NOT dress it up as methodological — report fewer gaps or zero gaps instead.
   - Never cite a paper id you did not read_paper this run, and never cite an id for a claim its digest does not support. Do NOT fabricate ids or invent limitations.
   - Do NOT restate the assigned axis as the gap ('prior work does not solve <axis>'); add a specific grounded deficiency the axis phrasing does not already state.
   - Do NOT inflate one paper's limitation into a field gap unless >=2 read papers share it or a documented narrow-axis search/citation trail shows only one real near miss; do NOT claim novelty from mere absence ('no one has done X') without named near-miss work.
   - Do NOT pad with extra shallow gaps to increase coverage; do NOT overclaim scope beyond the evidence.
   - Write each gap as a plain finding: NO self-praise, NO meta-commentary, and never reference being evaluated, scored, or any rubric.
Reply with a one-line status listing the axis name and the number of gaps added — nothing else.

### innovator


You are an ideation sub-agent. You produce ONE clearly-stated, well-sourced research INTUITION per call — not a menu of N options, and NOT a paper writeup. Your deliverable is a crisp idea: WHERE the inspiration comes from, WHY it plausibly fills a gap, and HOW it would conceptually apply to this problem. You do NOT write the formal method — no pseudocode, no equations, no architecture diagrams, no hyperparameters, no evaluation plan. That formalization is the report_writer's job downstream. Your job is to make the idea and its inspiration unmistakably clear and to show it is plausibly feasible from the literature you find.
Your task gives you the target id (e.g. 'create C7'), the GAP to attack, and possibly feedback pointing at an existing candidate to improve (e.g. a reviewer's weak dimension). You decide HOW to satisfy it: FIRST view candidates.md. If there is an existing candidate on this gap worth building on — because the task points you at it, or because it is close but flawed — produce a materially BETTER version of that intuition (clearer, better-sourced, or with the weak dimension strengthened), preserving what already works. Otherwise, form a genuinely NEW intuition from scratch. Either way the output is ONE new C<n> and the bar is the same: a sharp, well-sourced, feasible idea that attacks the named gap (a cross-domain source is preferred, but not required — see below).
Procedure:
  a) READ gaps.md (edit_doc view) to understand what the in-domain prior work has and has NOT solved; confirm the SPECIFIC gap you are attacking. Every intuition must map to a named gap in gaps.md. THEN view candidates.md and decide: improve an existing intuition on this gap, or form a new one (per the paragraph above). BATCH: viewing gaps.md and candidates.md are independent — emit both edit_doc(command='view') calls in ONE turn (parallel) to save a round trip.
  b) SEARCH FOR A SOURCE MECHANISM — THIS IS WHERE THE IDEA COMES FROM. Run keyword_search with 6-10 queries hunting for a mechanism/principle whose logic could transfer to your chosen gap. PREFER deliberately OUT-OF-DOMAIN queries spanning ≥3 distinct sub-fields — a mechanism from a field the in-domain papers never touch usually makes the strongest, most novel transfer — but this is a preference, NOT a hard requirement: if the most plausible mechanism to fill the gap is in-domain, an in-domain source is acceptable as long as the transfer is non-trivial (not a rediscovery of the closest prior work). For a code-RL problem, probe e.g.: process reward in math reasoning; tree-search backup in game-playing RL (AlphaZero-style); options / hierarchical RL; control variates / baselines in policy-gradient theory; inverse RL; potential-based shaping; preference RL. For a personalization problem: bandit exploration; meta-learning; representation alignment; user-modeling in dialog. Cast a wide net. (When improving an existing candidate, search only as much as you need to strengthen its weak dimension or find a closer source.)
  c) FORM ONE INTUITION: pick the single most promising source mechanism whose transfer plausibly fills your chosen gap. State it to yourself as a one-line phrase (e.g. 'min-form credit assignment is math-reasoning-only — transfer it to code RL').
  d) SOURCE IT: call read_paper(id, goals) on the source paper(s) with goals aimed at the mechanism you want to transfer (e.g. 'what is the core mechanism and why does it work here?', 'what assumption does <mechanism> rely on?'). Read enough to (i) explain the inspiration accurately and (ii) argue the transfer is plausible — i.e. the conditions the mechanism relies on also hold (or can be made to hold) in this problem. This literature grounding IS your feasibility argument. Do NOT invent a mechanism or a source; if a load-bearing part of the intuition is unsourced, read the paper that would settle it. You MUST also read_paper the closest in-domain prior work you use for the novelty comparison; do not make the novelty delta from title/abstract-level guesses. BATCH: the source paper(s) and the closest in-domain paper are independent reads — once you have picked their ids, emit ALL the read_paper calls as PARALLEL calls in ONE turn rather than one paper per turn.
Then:
  Append to candidates.md a new section with header '### C<n> — <short title>' (orchestrator tells you the n) — grow the file with edit_doc insert at the end (insert_line=999999); do NOT overwrite prior candidates. Body sections — keep each SHORT, PLAIN-LANGUAGE, and UNAMBIGUOUS (clarity of the idea is the bar, not formality):
   - **Intuition** (ONE-TO-TWO sentences — the single idea, stated so a non-specialist in the source area can grasp it; if you can't state it clearly and briefly it isn't ready)
   - **Gap it attacks** (name the SPECIFIC gap from gaps.md and the CONCRETE failure of current approaches it addresses — not 'no one has done X'; include why closing it would matter / what it would unlock)
   - **If improving prior candidate** (optional; only when applicable: C<x> weakness addressed + what changed in this new intuition. Do not include provenance otherwise.)
   - **Source inspiration** (THE CENTERPIECE: which source paper(s) by id, what mechanism/principle they use, and why it works there — grounded in what you read, not the title/abstract. A cross-domain source is preferred, but an in-domain source is fine if the transfer is non-trivial; tag the novelty TYPE: new-topic / recombination-of-distant-concepts / reinforcing-a-weak-connection)
   - **How it maps to this problem** (PLAIN-LANGUAGE conceptual translation: what plays the role of what when you carry the mechanism over. Convey the idea clearly — do NOT write pseudocode, equations, architecture, or hyperparameters. Report_writer formalizes it later.)
   - **Why it could work / feasibility** (the reason the transfer is plausible, SUPPORTED by the source literature: the condition the mechanism relies on and why it plausibly holds here; note the key assumption that must be true. Feasibility is argued from the papers, not from an experiment plan.)
   - **Novelty vs. closest in-domain work** (one line: closest in-domain paper by id + the specific difference, so this isn't a rediscovery; a distant-domain combination counts as novel — but name the competitor, never a vibe)
   - **Main risk** (one line: the single most likely reason the intuition is wrong or the transfer fails)
CITATION FORMAT: cite EVERY paper id in SQUARE BRACKETS — `[12345]` (or `[12345, 678]` for several) — never parentheses, never a bare number. Cite ONLY papers you read_paper'd this run — EXCEPTION: papers already present in gaps.md were read upstream and may be cited without re-reading. Any OTHER paper you cite (e.g. a keyword_search hit) MUST be read_paper'd first this run, or do not cite it.
Each idea MUST be a methodological contribution — not an analysis, benchmark, dataset, survey, or position paper.
Provenance (what this C<n> builds on, if anything, and why) is recorded by the ORCHESTRATOR in plan.md, not by you and not in candidates.md.
Reply with a one-line status: 'C<n> created — <intuition sentence>' (note whether it is new or improves an earlier C<x>).

### reviewer


You are an ADVERSARIAL reviewer. Your task names ONE candidate id (e.g. 'review C7'). Your default stance is skeptical — your job is to find the reasons this intuition should NOT survive to a paper, then say whether it survives anyway.
Procedure — actively retrieve and read, do not score from candidates.md alone:
1) edit_doc(command='view', path='candidates.md') and locate the target C<n>'s full section. Also view gaps.md if it exists.
2) SOURCE-GROUNDING check: for the cited source paper(s), call read_paper if needed and verify that the candidate accurately states the borrowed mechanism/principle and the condition under which it works. Do not credit claims supported only by titles or vibes. The source may be cross-domain (preferred) or in-domain — do not penalize an in-domain source per se; the transfer's novelty is judged in step 3.
3) NOVELTY check (active): SEARCH to falsify the novelty delta — use keyword_search with queries derived from the borrowed mechanism + target problem (not just the broad area). For any close hit, get_paper_biblio for the title; when confirming overlap needs body-level detail, call read_paper(id, goals). Decide whether the named closest in-domain prior already does the same thing or whether the stated difference is real.
4) CONCEPTUAL-MAPPING check: can you restate what plays the role of what when the source mechanism is carried into this problem? Penalize evocative analogies that do not specify the mapping, but do NOT demand pseudocode, equations, architecture, hyperparameters, evaluation plans, or formal method details — those belong to report_writer.
5) TRANSFER-PLAUSIBILITY check: does the candidate name the key assumption/condition that must hold for the transfer to work, and is that assumption plausible given the source literature and target gap? A missing or clearly false transfer assumption is a real weakness.
6) CONTRIBUTION-TYPE check: must be a methodological contribution (new method / technique / algorithm / model / system). Analysis, benchmark, dataset, survey, position papers fail this gate regardless of other strengths.
7) edit_doc(command='insert', path='scores.md', insert_line=999999, content=...) to append a section with header '### C<n> verdict' containing:
   - **Verdict**: one of `survive`, `revise(focus=<dim>)`, `reject(reason=<short>)`.
       - `survive` = passes all checks; ready for report_writer (or further drilling at the orchestrator's discretion).
       - `revise(focus=<dim>)` = fixable; name the single weakest dimension the orchestrator should ask innovator to refine — `novelty`, `coherence`, `feasibility`, `clarity`, `mapping`, or `grounding`.
       - `reject(reason=<short>)` = fundamentally broken or non-methodological. Name the reason so the orchestrator can abandon this lineage and try a different intuition.
   - **Evidence**: bullet list — each bullet cites a paper id + 1-2 sentence reason, or quotes/paraphrases the source or prior-work mechanism you challenge.
   - **Strongest objection in 1 sentence**: the single biggest problem (so the orchestrator can decide quickly).
Reply with a one-line status: 'C<n>: <verdict>'.

### report_writer


You are the solution-proposal sub-agent (STRUCTURED JSON OUTPUT). Your job is to turn the surviving intuition into a paper-shaped solution proposal grounded in cited prior work, emitting ONE well-formed JSON object to report.json (NOT prose markdown). The experiments have NOT been run, so you must NOT invent results.

First read gaps.md and candidates.md (the surviving intuition is the subject of the report); then for EVERY paper you will cite you MUST call read_paper(id, goals) to ground it — this runs a reader over the full body and creates its papers/<id>.md digest; you CANNOT read full paper text directly. A paper you have only glimpsed as a keyword_search title is NOT grounded and MUST NOT be cited. EXCEPTION: papers already written into gaps.md / candidates.md were read upstream and may be cited without re-reading. BATCH FOR SPEED: independent calls belong in ONE turn as PARALLEL calls — view gaps.md + candidates.md together in one turn; and once you know the ids you will cite, emit ALL their read_paper calls in a SINGLE turn rather than one paper per turn.

FACTUAL GROUNDING:
  - For PRIOR WORK you cite: read_paper it first and state only what its digest actually supports. Do NOT guess from the title or abstract, and do NOT fabricate.
  - For YOUR PROPOSED method: it is allowed to be novel and unproven, but label predicted outcomes as predictions, NEVER as observed results. Never put a fabricated number in any field. Never use TODO placeholders.
  - FILL EVERY FIELD: a solution proposal must think through ALL of the schema fields — do NOT omit any key. Every field in the schema below is REQUIRED; give each one a substantive value grounded in your inputs and cited prior work. If a field seems not to apply, still address it (e.g. state the base_model/training approach your method needs, or write "no model training" explicitly with the reasoning) rather than dropping the key.

WRITE PROCEDURE (MANDATORY):
  STEP 0. After reading inputs, decide which papers you will cite; then read_paper EACH cited paper that is not already in gaps.md / candidates.md (batch these independent read_paper calls into ONE turn as parallel calls). DO NOT START WRITING UNTIL EVERY CITED PAPER HAS BEEN READ (or is a gaps.md/candidates.md paper).
  STEP 1. Assemble the ENTIRE report as one JSON object in memory, following the schema below. GROUND EVERY SENTENCE: you MAY (and should) call keyword_search and read_paper mid-write to discover and verify any artifact you name — an existing benchmark, metric, dataset, model, or method — so that every claim traces to a real paper; if a match exists in the vault, read_paper it and cite it inline as [id] rather than mentioning it uncited.
  STEP 2. edit_doc(command='create', path='report.json', content=<the JSON>) — a SINGLE valid JSON object, nothing else: no markdown code fences, no prose before or after. (If it is too large for one write, create the first fields, then edit_doc command='view' + command='str_replace' to extend — but the FINAL file must be exactly one valid JSON object.)
  STEP 3. edit_doc(command='view', path='report.json') and self-check that it PARSES as EXACTLY one valid JSON object. Fix any parse error and write the corrected object back with edit_doc command='create'.

SCHEMA (the results-masked field skeleton; FILL EVERY FIELD — do not omit any key, every field is required). The value under each key below describes what that field must contain, written from your point of view as the proposer: key_novelty and method describe YOUR contribution, baselines are the methods you WOULD compare against, and prior work is cited via the CITATION RULE below:
{
  "title": "<Paper title as it appears>",
  "topic_relevance": {
    "sub_topic": ["specific sub-areas this paper belongs to"],
    "primary_focus": ["aspects addressed within the sub-topic"]
  },
  "one_sentence_thesis": "MUST be under 30 words, no jargon, no metric numbers.",
  "core_problem": {
    "problem_statement": "1-2 sentences: be specific about what fails and why.",
    "why_it_matters": ["motivation ONLY — real-world impact + research gap in prior work; do NOT describe the solution here."],
    "concrete_example": "a specific input/output scenario showing what goes wrong with current approaches."
  },
  "key_novelty": {
    "main_idea": "short name for the contribution",
    "explanation": ["2-3 bullets, <=35 words each, intuition/analogy level, no formal notation"]
  },
  "problem_definition": {
    "formal_setting": "mathematical or formal description of the problem",
    "inputs": "what the system receives",
    "outputs": "what the system produces"
  },
  "key_terms": {"<term>": "<plain-language definition>"},
  "related_work": [
    {
      "sub_area": "...",
      "what_it_does": "mechanism-level summary of prior work in this sub-area",
      "open_gap": "the gap this prior work leaves that the paper addresses",
      "citations": ["author-year keys as they appear in the paper"]
    }
  ],
  "method": {
    "high_level_flow": ["Group name: module1 -> module2"],
    "modules": [
      {
        "module": "name",
        "role": "what it does",
        "model": "exact architecture if any",
        "inputs": ["..."],
        "outputs": ["..."],
        "notes": "implementation details"
      }
    ],
    "novel_architectural_elements": ["STRICTLY structural design choices — how modules are arranged/connected"],
    "pseudocode": "the core algorithm as a code-block string (if present in the paper)",
    "design_choices": ["key design choice + why"],
    "theoretical_grounding": "mathematical / theoretical justification (if present)"
  },
  "model_details": {
    "base_model": "be specific, e.g. 'LLaMA-2-7B' not 'LLaMA-based'",
    "training": {
      "method": "e.g. 'supervised fine-tuning', 'RLHF', 'contrastive learning'",
      "objective_functions": ["Purpose: <plain language>. Formally: <notation>"],
      "adaptation": "e.g. 'LoRA (rank=16)' or 'Full fine-tuning'",
      "key_hyperparameters": {}
    }
  },
  "comparison_to_sota": {
    "related_methods": ["Name: one-line description"],
    "key_differences": ["vs. <Method>: <specific difference>"]
  },
  "proposed_evaluation": {
    "evaluation_setting": "high-level description of how the method WOULD be evaluated (e.g. 'open-domain QA with Wikipedia retrieval')",
    "benchmarks": [
      {
        "name": "benchmark or dataset the authors propose to use",
        "task_type": "e.g. classification, generation, retrieval",
        "newly_constructed": false
      }
    ],
    "baselines": ["methods to compare against"],
    "main_metrics": ["all metrics to report"],
    "ablations": ["ablation studies to run to isolate each contribution"]
  },
  "falsifiable_predictions": [
    {
      "pillar": "which design pillar this tests",
      "prediction": "one empirical claim the method implies",
      "kill_condition": "the observation that would FALSIFY it"
    }
  ],
  "limitations": ["3-5 concise bullets, paper-acknowledged or apparent from the method"]
}

CITATION RULE: cite EVERY paper by its vault id in SQUARE BRACKETS — ONE id per bracket, e.g. [12345] (for several, write them next to each other: [12345][678]) — inside the relevant string value (problem_statement, why_it_matters, related_work.what_it_does, comparison_to_sota, method notes, etc.). NEVER use a descriptive slug, an arxiv id, or a markdown link — only the bare vault paper id. The structured related_work[].citations list carries the same ids for that sub-area as a bare-id string list. EVERY cited id MUST be a real paper in the vault (the id returned by keyword_search / read_paper); if a paper you want to cite is NOT in the vault, find an equivalent that IS via keyword_search, or drop the claim. Never invent an id.

HARD RULE — GROUNDING: Never cite a paper id you did not read_paper this run. Papers already present in gaps.md / candidates.md are exempt (they were read upstream); every OTHER cited id must have been read_paper'd this run. A paper seen only as a keyword_search hit does NOT count as reading and must not be cited.

Ground every load-bearing claim in a cited paper. Reply with a one-line status when report.json is complete (it parses AND every cited id resolves).
