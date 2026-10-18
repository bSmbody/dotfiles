# plan — A small open model as the high-level controller of a VLA

**Goal**: ONE focused, sharp, well-grounded methodological intuition for this problem that a simulated CVPR 2027 panel rates at ≥ 5/10 acceptance odds, executable within the Constraints in problem.md.

**Active direction**: Axis `distilling frontier-model controller traces into small embodied controllers`, Gap 1 — on-policy distillation localizes the failing decision assuming deterministic replayable transitions; with stochastic VLA execution the failing controller decision is not identifiable from a trace, so embodied distillation falls back to off-policy labels or whole-episode reward.
**Status**: `drilling`

## Candidate axes
- A1 `task-state tracking and sub-task success judgement by small VLM controllers` — done: 2 gaps (write-once unverified progress state; symmetric judges trained off closed-loop states)
- A2 `distilling frontier-model controller traces into small embodied controllers` — done: 2 gaps (decision-level credit assignment under stochastic VLA execution; task-state estimate never trained to be corrected)

## History
- `forming` at turn 0: run created (round 2, embodied, user-suggested direction: cheap substitutes for frontier-model controllers); spawning gap_finders on two axes in parallel.
- `drilling` at turn 1: chose A2/Gap 1 — embodied-specific and methodological (credit assignment when the executor is stochastic), less likely to collide than the task-state gaps (A1/Gap 1 and A2/Gap 2 overlap with each other and with StageGuard/AGM-style monitors). Spawning innovator → C1.
