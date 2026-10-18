# plan — A small open model as the high-level controller of a VLA

**Goal**: ONE focused, sharp, well-grounded methodological intuition for this problem that a simulated CVPR 2027 panel rates at ≥ 5/10 acceptance odds, executable within the Constraints in problem.md.

**Active direction**: Axis `distilling frontier-model controller traces into small embodied controllers`, Gap 1 — on-policy distillation localizes the failing decision assuming deterministic replayable transitions; with stochastic VLA execution the failing controller decision is not identifiable from a trace, so embodied distillation falls back to off-policy labels or whole-episode reward.
**Status**: `under_review`

## Candidate axes
- A1 `task-state tracking and sub-task success judgement by small VLM controllers` — done: 2 gaps (write-once unverified progress state; symmetric judges trained off closed-loop states)
- A2 `distilling frontier-model controller traces into small embodied controllers` — done: 2 gaps (decision-level credit assignment under stochastic VLA execution; task-state estimate never trained to be corrected)

## History
- `forming` at turn 0: run created (round 2, embodied, user-suggested direction: cheap substitutes for frontier-model controllers); spawning gap_finders on two axes in parallel.
- `drilling` at turn 1: chose A2/Gap 1 — embodied-specific and methodological (credit assignment when the executor is stochastic), less likely to collide than the task-state gaps (A1/Gap 1 and A2/Gap 2 overlap with each other and with StageGuard/AGM-style monitors). Spawning innovator → C1.
- `under_review` at turn 2: innovator wrote C1 (new) — key the VLA's per-chunk execution noise to (sub-task, chunk) so failed rollouts become replayable, then swap one controller decision with noise held fixed; decisions whose swap flips failure to success are the mistakes the teacher rewrites (common random numbers / counterfactual replay). Closest in-domain 2610.19834. Spawning reviewer on C1.
- `drilling` at turn 3: reviewer → C1 `revise(focus=novelty)`: CRN/fixed-noise replay is PEGASUS-era practice and Causal Agent Replay [2606.08275] already does do()-and-run-forward attribution (naming CRN as future work); localization rule wrong (should be the latest recoverable / commitment step, not first high-flip decision). Real novelty to re-center on: separating controller failures from VLA execution failures above a stochastic executor and using that credit to gate teacher calls. Revise cycle 1 → C2.
- `under_review` at turn 4: innovator wrote C2 (improves C1): VLA as AIVAT chance player [1612.06915] — subtract each sub-task execution's luck (deviation from the VLA's usual success rate from that progress state with that command), leaving the controller's own blame; call the frontier teacher only at the latest recoverable decision and only if snapshot-checked student alternatives cannot fix it. Noise coupling dropped, commitment rule adopted. Committed: ≥75% triage precision; ≥8/12/10 pts over failure-triggered correction / off-policy SFT / binary GRPO; off-policy SFT success at ≤1/3 teacher calls. Closest: MAGMA-GEN [2609.20056]. Spawning reviewer on C2.
