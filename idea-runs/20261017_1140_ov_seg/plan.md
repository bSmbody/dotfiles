# plan — Training-free open-vocabulary semantic segmentation from frozen foundation models

**Goal**: ONE focused, sharp, well-grounded methodological intuition for this problem that a simulated CVPR 2027 panel rates at ≥ 5/10 acceptance odds, executable within the Constraints in problem.md.

**Active direction**: Axis `small objects and stuff classes in training-free open-vocabulary segmentation`, Gap 1 — fine detail is recovered only by redistributing the class evidence of a single CLIP pass on the patch grid; no stage re-queries the VLM where, and at the scale at which, evidence is ambiguous, so structures that never win a token are unrecoverable.
**Status**: `under_review`

## Candidate axes
- A1 `spatially noisy CLIP patch tokens for dense prediction` — done: 1 gap (dense global component written into normal tokens' content in intermediate layers; all fixes act on last-block mixing or sparse outliers)
- A2 `small objects and stuff classes in training-free open-vocabulary segmentation` — done: 2 gaps (no uncertainty-triggered evidence re-acquisition; context extent is a global knob, not a per-location decision)

## History
- `forming` at turn 0: run created; spawning gap_finders on the first two axes in parallel.
- `drilling` at turn 1: both axes mapped (3 gaps). Chose A2/Gap 1 (evidence re-acquisition): it matches the problem's concrete failure (poles/signs absorbed), has a crisp new metric (recovery rate of small segments that win no patch), and is a plug-in that composes with every existing method, which gives broad tables at low compute. A1/Gap (intermediate-layer global component) kept as fallback; A2/Gap 2 (per-location context extent) as second fallback. Spawning innovator → C1.
- `under_review` at turn 2: innovator wrote C1 (new) — Distilled Sensing [1001.5311] for sparse weak signals: after the first CLIP pass, discard only (location, class) hypotheses at that class's own background level, then re-encode surviving locations at progressively finer zoom against only their surviving classes; a thin structure only has to survive elimination, not win a patch. Spawning reviewer on C1.
