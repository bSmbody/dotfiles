# plan — Training-free compositional alignment in MM-DiT text-to-image models

**Goal**: ONE focused, sharp, well-grounded methodological intuition for this problem that a simulated CVPR 2027 panel rates at ≥ 5/10 acceptance odds, executable within the Constraints in problem.md.

**Active direction**: (none yet)
**Status**: `forming` (parked)

## Candidate axes
- A1 `attribute leakage and object omission through MM-DiT joint attention` — done: 2 gaps (token-as-fixed-carrier leakage fixes; preset omission strength)
- A2 `object counting and spatial relations in training-free text-to-image guidance` — done: 2 gaps (count correction not computed from the early state; no instance-level relational term)

## History
- `forming` at turn 0: run created; spawning gap_finders on the first two axes in parallel.
- `forming` (parked) at turn 1: both axes mapped (4 gaps). The three other lanes already have active directions; to save budget this lane is parked as the first substitute if one of them dies.
