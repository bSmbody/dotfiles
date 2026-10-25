# plan — Frontier-model brains are slow

**Goal**: make the user's idea (a cerebellum-like forward model that lets a slow frontier brain act on the predicted future state; backup: brain-armed local reflexes) concrete and novel, then score it with the simulated CVPR 2027 panel.

**Active direction**: A1 gap 1 (brain-readable forecast at answer-arrival time) + A1 gap 2 / A2 gap 1 (re-anchoring the stale decision's referents, ego part exact from committed actions)
**Status**: `innovating`

## Candidate axes
- A1 `latency of frontier-model brains in real-time robot manipulation` — 2 gaps; seed part (b) uncovered, (a) only low-level sub-second (2607.12659), (c) partial (2606.20458 ego-only, 2609.31112 templates)
- A2 `delay compensation for delayed high-level commands (predictive displays, Smith predictors, latency-aware planning)` — 2 gaps; nothing transfers directly; transferable pieces: timestamping, committed actions as exactly known part, re-parameterizable commands, forecast instead of stale input
- A3 `execution monitoring with pre-specified recovery for LLM-planned robot tasks` — gap_finder spawned (backup mechanism) — 2 gaps; AgentChord 2605.11951 already pre-arms recoveries with no brain call (static scenes); weaker than A1/A2 → parked

## History
- `forming` at turn 0: run created at the user's request (novelty check first, then concretize, then one review + panel round). Seed idea from the conversation: Astra as cortex, executor as spinal cord; missing cerebellum (forward model hiding brain latency) and long-latency reflexes (brain-armed local corrections).
- `innovating`: all three gap_finders back. Chose A1+A2 because seed part (b) has no prior work and the combination (black-box frontier brain, seconds-scale Δ, independently moving objects, manipulation) is uncovered; A3 parked since AgentChord covers the core arming mechanism. Risk to watch: kitchen-sink (forecast + re-anchor + validity test) — innovator told to make one mechanism the core.
