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


### C2 — Point, then say it so the VLA reaches there: a referent-scored, amortized speaker for a frozen VLA

- **Intuition**: The controller decides *which object* it means as a point, and learns *what to say* by checking where the frozen VLA's predicted reach lands relative to that point. The score never re-reads language, so it cannot inherit the VLA's or a verifier's misreading of "the second mug from the left". A small speaker trained on this score emits, in one pass, the wording that this particular VLA will carry to the pointed object. It is checked against several independently trained VLAs so that it does not learn one checkpoint's quirks.

- **Gap it attacks**: Axis "language sub-task grounding mismatch between controller and pretrained VLA", Gap 1, narrowed after review.
  - CoVer-VLA [2602.12281] already chooses the prompt from the frozen VLA's pre-execution chunks, so "nobody reads the VLA's immediate response" is no longer the gap.
  - The open failure is the challenge's own wrong-referent case: same-category instances that only a relation or ordinal tells apart.
  - CoVer's verifier scores each candidate against the *original* instruction through frozen SigLIP2 text–image encoders. Its ceiling is therefore its own grounding of "second mug from the left". Its evaluations never contain such referents (App. 8.1). Its F1 of 0.77 is measured against random actions, not wrong-referent ones (App. 8.5.1).
  - It also pays K×M samples plus a 1B verifier at every chunk. The verifier is trained at 3.8× π0's pre-training FLOPs, which is out of budget here.
  - Closing this would give a cheap controller a reusable model of *which words carry a pointed referent into this VLA*. That is the missing piece between pointing controllers and language-only frozen VLAs: a frozen VLA follows a mask tint only once a colour word routes it (mask-only 5.2–7.3% vs 62.7–83.5% with the word [2512.20014]).

- **If improving prior candidate**: Improves C1, whose novelty fell to CoVer-VLA [2602.12281]. Three changes:
  - (i) The listener score is redefined as language-free and referent-referenced, and the wrong-referent case is made the headline, with an explicit separating result against CoVer.
  - (ii) The "listener population" is re-mapped from stochastic samples of one VLA to independently trained checkpoints. Within-model samples are the dropout-style population that [2110.05422] shows fails, and they share one model's bias [2610.19438]. Those samples are kept only as the graded L0 probability of [2006.00418].
  - (iii) C2 is positioned against ReGuide [2609.38616], found in this pass. ReGuide already reads the referent from the predicted chunk endpoint but corrects by scripted motion, not by wording.

- **Source inspiration**: Computational pragmatics. Novelty type: recombination-of-distant-concepts, plus reinforcing-a-weak-connection, because the referent readout exists in-domain but only as a motion trigger.
  - (1) Amortized RSA [2006.00418]. A speaker trained on a fixed listener's *graded probability of the intended referent* matches explicit sample-and-rerank RSA at one-sample cost and generalises to held-out combinations. The same speaker trained by REINFORCE on binary success fails to learn. In a reference game the listener's output is a choice of referent, so the reward lives in referent space, not in language space. That is the property CoVer's language-alignment score lacks.
  - (2) [2609.14207]. Scoring where the listener's comprehension *process* lands (estimated fixations relative to the target box) beats outcome-only listeners. A KL penalty to the initial speaker is required to stop reward hacking of a model listener.
  - (3) [2110.05422]. Speakers drift into listener-specific gibberish against one over-confident listener. Only a population of *separately trained* listeners restores generalisation to held-out listeners. A dropout population inside one model does not.
  - (4) Why a language-referenced judge is the wrong anchor. Contrastive image–text encoders are near chance at telling which object stands in which spatial relation (CLIP ViT-L/14: 26.1 on 4-way What'sUp, 49.5 on 2-way COCO-spatial), and hard-negative fine-tuning cannot even fit the data [2310.19785]. Resolving a relational referent to a point, by contrast, is a separable, trainable skill: a pointing VLM gets 49.8 vs 15.3 for GPT-4o on lookalike-object references [2406.10721].

- **How it maps to this problem**:
  - The **intended referent** is the object or region the controller points at for this sub-task. During speaker training it comes from simulator object poses, so no perception error enters. At test time it comes from the controller's own pointing.
  - The **literal listener** is the frozen deployment VLA (π0/π0.5, SmolVLA, OpenVLA-OFT).
  - Its **interpretation** is the end-effector endpoint obtained by integrating its predicted chunk. This is the same readout ReGuide uses [2609.38616].
  - The **graded L0 score** is the share of a few chunk samples whose endpoint commits to the pointed object rather than to any other object.
  - The **speaker** is a small VLM (≤8B, LoRA). It takes the image, the point and the sub-task, and is trained on that score at many simulator states (demo frames, perturbed layouts, states left by earlier sub-tasks), with a KL anchor to its initial wording.
  - The **listener population** is the other independently trained public checkpoints of the same benchmark. The speaker is rewarded for wording that carries the referent across them, and one checkpoint is held out to detect drift.
  - At test time the speaker emits one command per sub-task. The controller spends one VLA pass to confirm the reach and reranks a handful of alternatives only on a miss. If no wording lands, the state is flagged as not language-redirectable and handed to a non-language fallback, such as ReGuide-style geometric rebinding or a re-pose.

- **Why it could work / feasibility**:
  - **Graded listener signal.** The mechanism needs a fixed listener whose referent choice is readable before acting, and a graded score of it [2006.00418, 2609.14207]. Both hold for VLAs. The committed approach largely decides which object is manipulated (86.5–98.3% of trials in [2610.06235]). ReGuide shows this endpoint-to-box readout identifies the policy's referent well enough to trigger corrections that lift compositional success by 55.5–56.8 points on three backbones [2609.38616].
  - **Room for wording to matter.** Attribute and spatial re-references are among the cheapest fixes for π0.5-class policies [2610.17746]. CoVer itself shows that choosing the right rephrase redirects π0 to the correct object (+31 OOD) [2602.12281].
  - **A real listener population.** ReGuide runs π0.5, GR00T N1.7 and OpenVLA-OFT on identical LIBERO cells with one readout [2609.38616], so the population costs nothing to obtain.
  - **Cost.** Training costs only batched VLA forward passes at simulator states, with no episodes and no success labels. That avoids the 76,800 rollouts of [2607.04517] and the success-gated, per-task distillation of [2610.14885], which could not update 66 of 140 LIBERO-plus tasks.
  - **Key assumption.** The pointed referent is right. That is guaranteed in training and is the controller's job at test time, where [2406.10721] shows it remains imperfect.

- **Novelty vs. closest in-domain work**: Each nearby method has one ingredient but not the combination.
  - **vs. [2602.12281] CoVer-VLA:** it reranks K×M samples per chunk with a verifier that scores against the original language. C2 scores against a point, needs no language verifier, and amortizes into one command.
  - **vs. [2609.38616] ReGuide:** it uses the same referent-referenced endpoint readout only to trigger scripted transport. It never changes the words, needs demo pose statistics, and leaves relational instructions untested.
  - **vs. [2610.14885]:** it amortizes a verifier into the VLA's own weights, per task, from successful episodes.
  - **Result that would separate C2 from CoVer.** On scenes where same-category lookalike instances are told apart only by position or ordinal (SimplerEnv/LIBERO-Plus-style distractor layouts, where wording can still redirect), the referent score should select candidates that commit to the intended instance at least 15 points more often than CoVer-style language-verifier selection. The comparison holds the rephrase pool and VLA samples fixed, so only the scoring rule differs. C2 should also tie CoVer on CoVer's own category-distractor tasks, and the amortized speaker should keep most of that gain at no more than one tenth of CoVer's VLA samples per decision. If the gap is under 5 points, C2 is only a cheaper CoVer.

- **Main risk**: On LIBERO-finetuned checkpoints wording barely moves the VLA. In-scene target swaps redirect only 0.5–13% of trials [2610.06235], and paraphrase cost is low on Spatial/Object [2610.19438]. The referent score would then be flat for every command, C2 would mostly output "not redirectable", and its gains would hinge on finding benchmarks and checkpoints where language still steers.
