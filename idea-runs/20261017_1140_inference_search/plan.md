# plan — Compute-efficient inference-time search for diffusion and flow generators

**Goal**: ONE focused, sharp, well-grounded methodological intuition for this problem that a simulated CVPR 2027 panel rates at ≥ 5/10 acceptance odds, executable within the Constraints in problem.md.

**Active direction**: Axis `verifier reward hacking under inference-time search`, Gap 1 — trust in the verifier is one candidate-independent scalar (α/λ, β, n/θ/M) fixed before search, so search has no per-candidate signal of when a higher verifier score stops meaning higher true quality.
**Status**: `under_review`

## Candidate axes
- A1 `intermediate reward estimation for pruning and resampling diffusion trajectories` — done: 1 gap (scalar estimate + fixed prune/resample rule ignores spread of final score vs sibling gaps)
- A2 `verifier reward hacking under inference-time search` — done: 2 gaps (fixed scalar trust; compensatory multi-verifier aggregation)

## History
- `forming` at turn 0: run created; spawning gap_finders on the first two axes in parallel.
- `drilling` at turn 1: both axes mapped (3 gaps). Chose A2/Gap 1 (per-candidate verifier trust): broadest paper story (why search-scaling plateaus) and less crowded than A1's uncertainty-aware pruning, where VASR [2604.06779] and StitchVM [2605.19804] already derive the variance term. A2/Gap 2 (non-compensatory aggregation) kept as fallback; it may be absorbed by Gap 1 if the innovator uses verifier disagreement as the reliability signal. Spawning innovator → C1.
- `under_review` at turn 2: innovator wrote C1 (new) — Double-DQN-style decoupling: re-score each finalist on a few re-noise-and-denoise redraws (DiffPure-style) and use the share of its score that survives as per-candidate trust and a per-prompt stopping signal. Spawning reviewer on C1.
