# plan — Budgeted escalation from a cheap VLA to a frontier controller

**Goal**: ONE focused, sharp, well-grounded methodological intuition for this problem that a simulated CVPR 2027 panel rates at ≥ 5/10 acceptance odds, executable within the Constraints in problem.md.

**Active direction**: Axis `failure prediction signals for cheap VLA policies (when to ask for help)`, Gap 1 — triggers regress the cheap policy's failure probability, but the call decision needs the helper's advantage, which collapses past the recoverability horizon while failure probability stays high.
**Status**: `under_review`

## Candidate axes
- A1 `failure prediction signals for cheap VLA policies (when to ask for help)` — done: 2 gaps (failure probability ≠ helper advantage; helper-conditioned labels too expensive under a per-call budget)
- A2 `allocating a limited budget of frontier-model calls during embodied execution` — done: 2 gaps (myopic stationary threshold ignores remaining budget/time; constant call benefit across call types)

## History
- `forming` at turn 0: run created (round 2, embodied, user-suggested direction: cheap substitutes for frontier-model controllers); spawning gap_finders on two axes in parallel.
- `drilling` at turn 1: chose A1/Gap 1 (call when it helps, not when it fails); A1/Gap 2 (sparse helper labels) and A2/Gap 2 (call-type-dependent gain) are the natural method constraints and are visible to the innovator in gaps.md. Spawning innovator → C1.
- `under_review` at turn 2: innovator wrote C1 (new) — X-learner uplift trigger: free cheap-VLA rollouts give the no-call value per state, a few hundred randomized frontier calls give called outcomes, the trigger learns each call's imputed effect and fires only on savable states. Spawning reviewer on C1.
