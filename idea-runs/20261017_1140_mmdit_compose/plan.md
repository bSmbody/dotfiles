# plan — Training-free compositional alignment in MM-DiT text-to-image models

**Goal**: ONE focused, sharp, well-grounded methodological intuition for this problem that a simulated CVPR 2027 panel rates at ≥ 5/10 acceptance odds, executable within the Constraints in problem.md.

**Active direction**: Axis `attribute leakage and object omission through MM-DiT joint attention`, Gap 1 — layout-free leakage fixes treat each text token as a fixed carrier of its phrase, but in joint attention a noun-phrase token is rewritten every block by what it absorbs from other phrases and other objects' regions; no layout-free method controls that per phrase, so text-stream leakage is corrected only downstream in the latent.
**Status**: `drilling`

## Candidate axes
- A1 `attribute leakage and object omission through MM-DiT joint attention` — done: 2 gaps (token-as-fixed-carrier leakage fixes; preset omission strength)
- A2 `object counting and spatial relations in training-free text-to-image guidance` — done: 2 gaps (count correction not computed from the early state; no instance-level relational term)

## History
- `forming` at turn 0: run created; spawning gap_finders on the first two axes in parallel.
- `forming` (parked) at turn 1: both axes mapped (4 gaps). The three other lanes already have active directions; to save budget this lane is parked as the first substitute if one of them dies.
- `drilling` at turn 2: activated as substitute after inference_search was closed. Chose A1/Gap 1 (per-phrase text-stream routing without layout): sharp mechanism (text-stream attribution dominates early steps, 89.9% at step 0 [2606.15796]; DreamRenderer [2503.12885] shows per-phrase routing works but needs boxes), zero-NFE attention-routing change, standard benchmarks. A1/Gap 2 (closed-loop omission strength) kept as fallback. Spawning innovator → C1.
