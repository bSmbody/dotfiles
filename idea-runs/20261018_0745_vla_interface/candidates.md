### C1 — VLA-as-listener: learn what to say from where the VLA reaches, not from whether the episode succeeds

- **Intuition**: Treat the frozen VLA as the listener in a reference game. For each candidate sub-task command at the current state, read off which object the VLA's own predicted action chunk commits to reach, and train a small controller-side "speaker" to say commands whose immediate reach lands on the intended target. Executability is then learned from the VLA's comprehension process at every state, in one forward pass, instead of from the outcome of whole episodes.

- **Gap it attacks**: Axis "language sub-task grounding mismatch between controller and pretrained VLA", Gap 1. Today a controller learns which phrasings a frozen VLA executes only from episode success. [2607.04517] spends 76,800 rollouts (83 h on 2×H100) for π0 and gets no signal between commands that alias to the same behaviour. [2606.31958] learns its prompt Q per task. [2610.10526] falls back on a demo-based proxy (r=0.54). The one method that reads the VLA's pre-execution response, [2610.19438], uses it only for consensus or confidence, and both fail (confidence-based selection −28.0). Yet the challenge's own failure ("second mug from the left" → nearest mug) is a wrong-target commitment that is visible in the first predicted chunk, long before the episode ends. Closing the gap would let a ≤8B controller be fitted to a new VLA at forward-pass cost and reused on unseen scenes and tasks, which is the route to needing the frontier model less.

- **Source inspiration**: Computational pragmatics, from reference games between a speaker and a fixed listener. Novelty type: recombination-of-distant-concepts.
  (1) [2609.14207] trains a VLM speaker against a listener that predicts, word by word, where a human's gaze goes while reading the expression. Rewards come from where those fixations land relative to the target (first hit, distance shaping), not only from the final guess. Process-trained speakers become concise (15.4 → 4.0 words) and more successful with real humans (75.2 → 80.0%). A control listener that gives only the final point reproduces the outcome-trained behaviour, so the gain comes from the process signal.
  (2) [2006.00418] (amortized Rational Speech Acts, RSA) shows why a graded listener signal beats outcome reward. A speaker trained on a fixed listener's graded probability of the target matches explicit sample-and-rerank RSA at one-sample cost and generalises to held-out colour/shape combinations. The same architecture trained by REINFORCE on binary success stays at the naive speaker's level, or fails to learn at all.
  (3) [2110.05422] adds the safeguard. Speakers drift into listener-specific gibberish when the listener is over-confident on novel utterances, and training against a population of listeners restores calibration and generalisation.

- **How it maps to this problem**:
  - The **speaker** is the small controller, or the command-writer under a frontier planner.
  - The **listener** is the frozen VLA (π0/π0.5, SmolVLA, OpenVLA-OFT).
  - The **referent** is the object or part the current sub-task must act on. The controller already knows it: from simulator object poses during training, from its own pointing at test time.
  - The **gaze** is the end-effector path the VLA commits to in its predicted action chunk from the current state, matched against the scene's objects.
  - The **listener population** is several stochastic chunk samples from the VLA's flow/diffusion head, which give a graded "probability the VLA goes to the target under this command" rather than a hit/miss.

  Training needs only states, not finished episodes: demo frames, perturbed layouts, and mid-task states left by earlier sub-tasks. Each state yields a per-command reward. That is the dense, state-conditioned signal Gap 1 lacks, and it also feeds Gap 2's need for per-state executability. At test time the amortized speaker emits one command. Only when the VLA's reach under that command misses the target does the controller rerank a few alternatives, at one VLA forward pass each. If no phrasing lands, the state itself is flagged as non-executable, so the controller can change cue or re-pose, as [2610.17746]'s home-reset finding suggests.

- **Why it could work / feasibility**: The pragmatic mechanism needs a fixed listener whose interpretation can be read cheaply and gradedly; [2006.00418] and [2609.14207] show that this, not binary success, is what makes speaker learning efficient. Both conditions hold for VLAs:
  - The VLA is frozen.
  - Its interpretation is exposed before execution.
  - Phrasing changes its pre-execution chunks: paraphrase disagreement is informative from the first replan [2610.19438].
  - Its target choice shows up as an early committed approach that largely decides which object gets manipulated. [2610.06235] records committed approaches toward the scene-prior target in 86.5–98.3% of trials, with completion tracking them.
  - Attribute/spatial re-references are among the cheapest fixes [2610.17746], so there is room for wording to matter.

  The key assumption is that where the predicted chunk heads predicts which object the VLA will actually manipulate. It must be target-directed, not just a measure of how much the command changes the action: [2610.06235] shows action-prediction deviation alone does not mean the VLA goes to the newly named target. Cost is one VLA forward pass per (state, command, sample) on a single 24 GB GPU, with no environment resets. The saving against the 76,800-rollout budget of [2607.04517] is likely orders of magnitude, but it must be measured. The [2609.14207] KL penalty and the [2110.05422] listener population guard against the speaker exploiting readout quirks.

- **Novelty vs. closest in-domain work**:
  - [2607.04517] learns a command policy by GRPO from episode-level success, with one command per rollout.
  - C1 replaces that reward with the frozen VLA's per-state, target-referenced reach response, needs no episode completion, and applies per sub-task.
  - [2610.19438] reads pre-execution chunks but never against an intended target, and never to choose what to say.
  - [2605.28527]'s frozen-feature value probe needs outcome labels and is not calibrated to the matched command under goal swaps (original goal preferred on only 53.7% of pairs), so it cannot score phrasings.

- **Main risk**: The first chunk's heading may not reveal the eventual target: approach motions can be ambiguous between nearby objects, and OpenVLA-OFT's chunks are short. The readout would then reward commands that look right early but drift, and it says nothing about motor-skill failures after correct targeting, so end-task gains would be capped by them.
