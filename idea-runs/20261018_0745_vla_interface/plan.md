# plan — What the controller should tell the VLA: the controller-to-VLA interface

**Goal**: ONE focused, sharp, well-grounded methodological intuition for this problem that a simulated CVPR 2027 panel rates at ≥ 5/10 acceptance odds, executable within the Constraints in problem.md.

**Active direction**: Axis `language sub-task grounding mismatch between controller and pretrained VLA`, Gap 1 — controller-side methods learn which phrasings a frozen VLA executes only from episode-level outcomes, never from the VLA's own immediate response to a candidate command.
**Status**: `under_review`

## Candidate axes
- A1 `language sub-task grounding mismatch between controller and pretrained VLA` — done: 2 gaps (executability learned only from episode outcome; executability treated as state-independent)
- A2 `non-language intermediate representations (points, traces, goal images) for conditioning pretrained VLAs` — done: 2 gaps (cue-to-target binding only by co-occurrence; single open-loop steering strength)

## History
- `forming` at turn 0: run created (round 2, embodied, user-suggested direction: cheap substitutes for frontier-model controllers); spawning gap_finders on two axes in parallel.
- `drilling` at turn 1: chose A1/Gap 1 (read executability from the VLA's immediate response), cheapest to test and not tied to fine-tuning; A1/Gap 2 is its state-conditioned extension. Spawning innovator → C1.
- `under_review` at turn 2: innovator wrote C1 (new) — the frozen VLA as listener in a reference game: read which object its predicted action chunk commits to reach under each candidate command at the current state; train a small controller-side speaker on that per-state reach signal (amortized RSA) instead of episode success. Spawning reviewer on C1.
- `drilling` at turn 3: reviewer → C1 `revise(focus=novelty)`: CoVer-VLA [2602.12281] already reranks VLM rephrasings by the frozen VLA's pre-execution chunks with a language verifier. Surviving delta: a language-free, referent-referenced listener score (fixes the wrong-referent case a language verifier inherits) + an amortized speaker at forward-pass cost; listener-population safeguard to be re-mapped to independent checkpoints. Revise cycle 1 → C2.
- `under_review` at turn 4: innovator wrote C2 (improves C1): language-free referent-referenced listener score (where the frozen VLA's predicted reach lands vs the controller's pointed referent), amortized speaker trained against independent checkpoints; positioned vs CoVer-VLA [2602.12281] and ReGuide [2609.38616]; committed effect ≥15 pts intended-instance commitment over CoVer-style selection on relational-lookalike scenes at ≤1/10 VLA samples. Spawning reviewer on C2.
