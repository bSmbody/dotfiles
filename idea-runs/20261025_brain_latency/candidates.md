### C1 — Arrival-time ghost marks: a Smith predictor for a black-box brain

**Intuition** Before each brain call, draw "ghost" marks on the image at the places where each tracked object, and the gripper, will be when the answer is expected to arrive. The brain answers in terms of those ghosts ("grasp ghost 3 on its left side", "5 cm left of the phantom gripper"). When the answer lands, every ghost is replaced by its real, tracked counterpart. As in a Smith predictor, the prediction is used only for deciding and the measurement only for acting. A forecast error can change *which* decision the brain makes, but it cannot move *where* the decision lands.

**Gap it attacks**
- **Primary: axis "latency of frontier-model brains", gap 1.** Today a black-box brain chooses a target, grasp side or subgoal on the frame from the start of its call. No method gives it a readable view of the scene at answer-arrival time. The existing forward models ([2607.12659], [2606.02486], [2607.24008]) live in the executor's private latent and look ahead less than a second. Generative video forecasts drift even at sub-second horizons [2605.09670]. Without a fix, the brain picks a conveyor box that will have left the reachable zone by the time its answer arrives. Downstream re-targeting cannot repair a decision that was wrong to begin with.
- **The same representation closes two linked gaps:** same axis, gap 2 (re-anchoring a stale spatial decision to the moving entity it refers to), and axis "compensating delayed high-level commands", gap 1 (splitting the exactly known ego part from the object-motion part). The answer is written relative to entities, never in a frame fixed at query time. So binding it at arrival needs no per-object templates [2609.31112] and no retraining [2602.02459].
- **The ego/world split falls out of the binding.**
  - The gripper's change comes from the executor's committed plan (shown) and its logged pose (bound), so it is exact.
  - Object motion during the call is *observed* by the tracker by the time the answer arrives, not predicted. Only the executor's own sub-second reaction needs extrapolation.
  - This turns the seconds-long object forecast that A2 gap 1 assumes into hindsight plus a sub-second forecast.

**Source inspiration** Novelty type: recombination of distant concepts (process control + time-delay teleoperation + visual prompting of black-box LMMs).
- **Smith predictor [2010.05486].** The controller is designed for the delay-free plant model and acts on the model's predicted undelayed output. The delayed measurement enters only as a correction for model mismatch. When the model is right, the delay leaves the characteristic equation entirely [2010.05486, Sec II, Eq 10]. In the networked version, the nominal delay is a measured or averaged round-trip time, and the variable remainder is bounded. Timestamped "skip old packets" selection doubles the tolerable variable delay over unnumbered selection [2010.05486, Sec I, Remark 5, Sec IV-B].
- **Predictive displays [1809.08627].** SARPD renders the robot's own tools at the pose that the operator's already-sent commands will produce. It overlays them on the delayed video, so the slow decision-maker sees the exact ego part immediately. At 1 s delay this made a peg transfer task 19% faster with no extra errors. The environment itself stays unpredicted, which the authors list as future work [1809.08627, Sec II-B, IV–V].
- **Enabler: Set-of-Mark [2310.11441].** It is what makes a black-box frontier model a reader of such overlays. Unique, speakable marks let the model answer with IDs that map back to regions exactly, and marks moved slightly off a region are still associated [2310.11441, Sec 2.1, 2.3].

**How it maps to this problem**
- **Roles.** The brain is the controller, the world plus executor is the plant, and the brain-call latency is the dead time.
- **Nominal delay.** A running estimate of this brain's latency, as networked Smith predictors use measured round-trip times.
- **The "delay-free model output" is a ghost layer drawn on the latest frame:**
  - a phantom gripper at the pose the executor's committed plan reaches at the estimated arrival time (SARPD's ego rendering);
  - for each tracked object, a numbered mark at its extrapolated arrival position, with a faint trail from where it is now (SoM marks, displaced in time instead of in space).
- **What the brain answers.** It answers only in ghost terms: which ghost, a point or side on it in that object's own frame, and relative moves in the phantom gripper's frame.
- **The "measurement correction" is the binding step at arrival:**
  - each ghost ID becomes the object's actual tracked pose, and the phantom becomes the logged gripper pose;
  - the executor then intercepts the target using only a sub-second extrapolation.
- **Timestamps play the role of packet numbering.** Each answer carries its query stamp, and a newer answer supersedes an older one.
- **Plumbing only:** the tracker (simulator ground truth first, then an off-the-shelf video segmenter), constant-velocity extrapolation, and the latency estimate. The single contribution is the decide-on-prediction / act-on-measurement split, carried by an entity-relative answer.

**Why it could work / feasibility**
- **Each half has been shown separately:**
  - black-box frontier models refer reliably to numbered marks [2310.11441];
  - mark-ID answers that are late-bound to tracked keypoints already run as a zero-shot closed-loop policy with GPT-4o [2409.01652, Sec 3.3–3.4];
  - showing a slow decision-maker the predicted effect of its committed commands speeds it up without adding errors [1809.08627];
  - a predictor plus measured correction removes the dead time when the model is right, and tolerates bounded variation [2010.05486].
- **Why forecast error drops out of execution.** For targets attached to a rigid entity, the executed location depends only on the measured pose. The forecast only has to be good enough to get the choice right (which box, whether it is still reachable, which side faces the gripper), not the coordinates. That is a much weaker demand than the pixel forecasting that fails in [2605.09670] or the point forecasting that fails under multimodal futures in [2101.11992].
- **Key assumption.** Over one brain call (a few seconds), object motion in the target tasks (conveyors, rolling or pushed objects) is predictable enough to preserve the brain's *choice*.
- **Fits the constraints:**
  - nothing is trained;
  - GPU use is limited to a tracker;
  - a scripted or motion-planning executor makes the committed plan during the call exact, which keeps engineering risk low for a team new to robotics;
  - moving-object variants of ManiSkill or RoboCasa only need objects to move kinematically while the simulator keeps running;
  - API spend is a few cents per call times a few thousand calls.

**Novelty vs. closest in-domain work**
- **Closest prior work:**
  - ReKep [2409.01652] already late-binds mark-ID answers to tracked keypoints, but its marks show positions at query time and it assumes other keypoints stay static.
  - [2606.20458] re-projects a stale black-box choice for ego motion only, while the brain still reasons on the old frame.
  - [2602.02459] needs a white-box VLM that has been fine-tuned.
- **Our delta:** C1 is the first to give a black-box brain an arrival-time view and still keep execution independent of forecast error.
- **Training-free baselines it must beat:**
  - raw stale execution;
  - ego-only re-projection [2606.20458];
  - query-time marks with late binding, ReKep-style [2409.01652] (the decisive ablation: it isolates the arrival-time forecast);
  - discard-and-replan [2506.07223];
  - verify-and-hold [2603.19418];
  - telling the brain Δ in the prompt [2610.09294];
  - pausing the world (upper bound).

**Main risk** Over query-time tracked marks, the gain comes only from *which-decision* errors. If those are rare in natural moving-object tasks, or if the brain misattributes ghost marks drawn away from the objects' current pixels (the SoM confusion seen with overlapping or off-center marks [2310.11441, Sec 4.4]), the effect over the ReKep-style baseline may be too small for the panel.
