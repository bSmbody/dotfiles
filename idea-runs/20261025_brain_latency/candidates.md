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


### C2 — Contingent answers over arrival-time hypotheses: the slow brain decides for every future it cannot yet rule out

**Intuition** While the brain is thinking, the scene's future is still open: ball 2 may bounce off the box or roll past it, and cup 4 may or may not still be reachable. So we do not ask the brain for one decision about one forecast. We show it the few futures, each checked by the executor, that would change its decision, and ask for a contingency plan: "if 2 bounces back (2b), grasp 2; if it rolls past (2a), take 4". When the answer arrives, the measured state picks the branch. The forecast only decides which options the brain weighs. Measurement decides which branch runs and where it lands.

**Gap it attacks**
- **Primary: axis "latency of frontier-model brains", gap 1, which-decision errors.** With seconds of latency and several moving objects, the brain picks a target that will have left the arm's reach, or one whose motion forks (it deflects, stops, or a new object arrives).
  - Late binding [2409.01652] fixes *where* that choice lands, but it still executes the wrong choice.
  - A single forecast fails when the future is multimodal [2101.11992].
  - Discard-and-replan [2506.07223] pays for another multi-second call, and by then the next fork has happened.
- **Secondary: axis "compensating delayed high-level commands", gap 2.** Each branch carries its own condition, which the executor checks at arrival. So the stale decision is tested against its own referents, not against a global staleness score.
- **Why it matters.** The brain's choice becomes robust to forecast error, so success can hold as latency grows without extra brain calls. This is the regime where frontier-brain systems now have to pause the world.

**If improving prior candidate** C1, with each point of the reviewer's verdict addressed:
- **(i) Where vs which.** C1's phantom gripper and the *where* half are dropped. ReKep-style late binding [2409.01652] and ego-only re-anchoring [2606.20458] already cover them; C2 keeps them as plumbing. The contribution is now only about *which* decision is made.
- **(ii) What trails-plus-Δ prompting cannot supply.** C1 drew one ghost per object, which is a point forecast the brain could reproduce from trails and Δ. C2's view carries two things the brain cannot get from trails and Δ:
  - interceptability per hypothesis, certified by the executor from arm kinematics, its committed plan and its intercept planner, none of which the brain sees;
  - more than one hypothesis per object when the futures fork.

  The answer also changes form, from one choice to a contingency plan that measurement resolves.
- **(iii) A standard-derived testbed.** The Dynamic Object Manipulation (DOM) benchmark, time-rescaled (below), with its which-decision sub-dimensions named.
- **(iv) Ghost-to-object association.** It no longer rests on spatial proximity, and it is pilot-gated with a fallback that does not depend on rendering.

**Source inspiration** Novelty type: recombination of distant concepts (contingency planning in autonomous driving, deferred-decision interception control, and visual prompting of black-box LMMs).
- **Contingencies from Observations [2104.10558].** Under uncertain futures, plan a policy whose later decisions depend on events not yet observed, not a single trajectory.
  - Why it works: a noncontingent planner takes the max of an expectation, "the single best compromise decision common to all possible values". The contingent planner takes the expectation of a max, "the best of all worlds", so its value is never lower [2104.10558, App A-G, Eqs 11–17].
  - It pays off only if the uncertain event is revealed before the contingent decision must execute [2104.10558, Sec I].
  - On CARLA forks (another car may or may not yield), noncontingent planners reach 0/30 (underconfident) or 9–12/30 (overconfident) near-expert successes, against 27–28/30 for the contingent one [2104.10558, Table II].
- **LookOut [2101.06547].** One immediate action is safe under every predicted future, and each future gets its own continuation. "Decision-postponing avoids over-conservative behaviors while staying safe until more information is obtained" [2101.06547, Sec 3.4, Eq 13]. This cuts collisions by 38% against a single plan [2101.06547, Sec 4.3].
  - The futures are chosen for *planning* diversity: samples are rewarded for inducing different ego plans, not for being different trajectories, so the few hypotheses spent are the ones that matter for the decision [2101.06547, Sec 3.2, Eq 7].
- **Deferred-decision trajectory optimization [2610.17003].** This is the closest control analogue. To intercept one of several *moving* candidates, it keeps one branch per candidate, all sharing the applied control, and separates them as late as feasibility allows. It falls back to guidance toward a retained candidate when no branch is verified [2610.17003, Sec I, III-C]. The decision-maker there is a fast optimizer that re-solves at every step; nothing in it is a slow semantic reasoner.
- **Enabler, with the reviewer's caveat: Set-of-Mark [2310.11441].** Speakable marks on regions let a black-box model answer with IDs. Marks on an object's own pixels are SoM's tested regime. Displaced or overlapping marks invite misattribution [2310.11441, Sec 2.3, 4.4], so C2 keeps the identity mark on the object (see (iv) below).

**How it maps to this problem**
- **The brain call is the interval in which the uncertainty resolves.** CfO's precondition holds by construction: by the time the answer arrives, the tracker has seen which future happened.
- **Hypotheses (the forecast fan).**
  - For each tracked object, the executor rolls a handful of cheap motion modes forward to the expected arrival time: keep going; deflect at known scene geometry; slow down and stop; and, scene-wide, a new object entering.
  - Following LookOut, it keeps an extra hypothesis only if that hypothesis changes the executor's verdict or the object's task-relevant zone.
- **Certification (what the brain cannot compute).** For each hypothesis, the executor's own intercept planner reports whether, and in which time window, it could grasp that object given what it is already committed to. This is SayCan's "can" [2204.01691], but evaluated per hypothesis at arrival time, not at the current state.
- **What the brain sees.**
  - The usual SoM mark on each object's current pixels.
  - Each hypothesis as a small labeled ghost (2a, 2b), tied to mark 2 by a tether line and carrying a reach badge (a time window, or "unreachable").
  - The same list repeated in text.
- **What the brain answers.** A short ordered list of condition → action pairs.
  - Conditions come from a closed vocabulary the executor can evaluate from measurements: "hypothesis 2b realized", "object 4 interceptable", and a final "otherwise re-ask".
  - Actions are entity-relative, as in C1, so *where* stays late-bound.
- **At arrival.** The tracker assigns each object to its nearest hypothesis, or to none. The executor re-checks interceptability on the measured state and runs the first branch whose condition holds. If no condition holds, it re-asks the brain (DDTO's fallback).
- **During the next call,** the running branch plays the role of LookOut's shared immediate action, so the executor does not idle.
- **One mechanism; the rest is plumbing.** The single mechanism is a contingent brain answer over executor-certified arrival-time hypotheses, selected by measurement. Mode rollouts, interceptability checks and the tracker are plumbing.

**Why it could work / feasibility**
- **Why contingency helps.** The gain is the Jensen gap in [2104.10558]. It is non-zero exactly when the best choice differs across futures that are revealed before execution, which is what a fork during a brain call is. Both driving papers measure large gains from it [2104.10558, 2101.06547].
- **Why the trails-plus-Δ prompt cannot match it.**
  - Reachability under the arm's committed plan is not in the image, so the brain would have to infer it.
  - The brain would also have to extrapolate motion itself, and frontier VLMs remain far below humans at choosing the next visual state of an observed trajectory: best 43.8% vs 98.6%, GPT-6 about 60% on the composed subtask [2610.04506, Sec 4.2]. These are human-action clips, not rolling objects, so this bounds the extrapolation ability rather than measuring it.
  - Even a perfect extrapolator that commits to one choice is a noncontingent planner, and it loses the compromise at every fork.
- **Standard-derived testbed: DOM [2601.22153].**
  - It is already run non-paused by RAVEL, on an RTX 4090, with released assets [2609.34170, Sec 4.2, App A.2].
  - Its speeds (0.15–0.75 m/s) are calibrated for sub-second VLA latency [2601.22153, Sec 4.3, 5.1]. The derived variant keeps DOM's scenes, objects, trajectory families (straight, curved, collision-deflected, repeatedly appearing) and instruction templates, and scales speeds so that object travel during one brain call fits the workspace.
  - **Which-decision errors should be frequent** in four sub-dimensions:
    - Long-horizon Sequencing: prioritizing among objects that keep appearing;
    - Dynamic Adaptation: direction shifts and deflections, i.e. forks;
    - Visual Understanding and Motion Perception: several objects in motion at once.
  - **Negative control:** Closed-loop Reactivity, a single target, where C2 should only tie late binding.
- **The executor already exists.** DOM's scripted automatic demonstrator takes object pose and velocity and runs approach, grasp, place and reset with short-horizon motion prediction [2601.22153, Sec 4.3]. It serves as both the arm and the interceptability oracle. Nothing is trained, and simulator ground-truth tracks come first.
- **Association robustness (the reviewer's point iv).**
  - The brain never has to link a ghost to an object by proximity: the label prefix is the object ID, the tether and the text list repeat it, and the identity mark stays on the object, where SoM was tested.
  - Pilot gate: probe association on rendered DOM frames before the main runs.
  - If accuracy is too low, the hypotheses go into text only, keyed to the on-object marks. The mechanism (contingent answer, measured selection) is unchanged by this fallback.
- **Cost.** One call per decision, and contingent branches absorb forecast misses that would otherwise trigger a re-call. This fits the problem's "need the frontier model less" target and the roughly $1,000 budget.
- **Key assumption.** Over one call, the decision-relevant futures per object are few, and cheap kinematic modes cover them. The frontier brain can then write short contingency lists that stay consistent.

**Novelty vs. closest in-domain work**
- **Closest prior work:**
  - ReKep [2409.01652] late-binds *where* but executes one fixed choice per stage.
  - LLM-written conditionals (PyRUA-Lean [2610.01939], Code-as-Monitor [2412.04455]) branch on current primitive results or monitor violations and then retry or re-plan. They do not branch over enumerated arrival-time hypotheses with executor-certified feasibility, and they do not model latency.
  - SayCan [2204.01691] gates on feasibility in the current state, with one choice per step.
  - AgenticCache [2604.24039] confirms or replaces a late plan.
  - PreAct-Nav [2610.04916] has a VLM review predicted rollouts of its own candidate move and pick one.
  - DDTO [2610.17003] is candidate-contingent, but an optimizer has no semantic brain.
- **No read or retrieved work** has a black-box brain answer with a contingency plan that measurement resolves at arrival.
- **Decisive ablation:** query-time marks plus motion trails plus Δ in text, with ReKep-style late binding [2409.01652, 2610.09294]. A second variant asks that prompt for a free-form fallback, to separate executor certification from the contingent answer form.

**Main risk** On time-rescaled DOM, decision-relevant forks may be rare, or a trails-plus-Δ prompt with a free-form fallback may handle them well. The gain would then shrink to executor-certified reachability alone. A pilot measuring the which-decision error rate of that baseline on Long-horizon Sequencing and Dynamic Adaptation settles this before the main runs.



### C3 — Latency is a "when" problem: speculate the brain's answer the way interceptors defer a target choice

**Intuition** In real-time dynamic manipulation, a slow brain mostly picks the *right* object. It just names it after the object has rolled out of reach. So the executor should not wait. While the brain thinks, it moves along the path that keeps the objects the brain is most likely to name still catchable when the answer lands. A fast local model guesses those likely answers, and a scripted check certifies which objects remain catchable. When the brain's answer arrives, the executor commits to the named object.

**Gap it attacks**
- **Primary: axis "latency of frontier-model brains", gap 1.** That gap says the brain's choice is made about a state that no longer exists. C3 first measures what this actually costs on a standard non-paused benchmark. It separates a wrong choice from a right choice that arrives too late. It then fixes the dominant part.
  - Prediction from the released DOM code: in DOM, latency barely changes *which* object the brain names, but it fully decides *whether that object is still catchable* when the name arrives.
  - The released evaluator holds the arm at its home pose until an action arrives [2601.22153, digest]. Every second of brain latency is therefore a second the target spends rolling away.
- **Secondary: axis "execution monitoring", gap 2 (the escalation rule is blind to latency).** The certifier compares each candidate's remaining catchable window with the brain's measured latency. It is the missing rule "this choice cannot wait for the brain; that one can".
- **Why it matters.**
  - RT-Safe found that about 84% of real-time collisions of VLM agents happen while the agent idles during inference [2610.09294].
  - Frontier-brain manipulation systems pause the world [2610.28259, 2610.14117].
  - Until in-call behaviour is fixed, a seconds-latency brain cannot be used on moving objects at all, however good its decisions are.

**If improving prior candidate** C2. Route chosen: **discovery + method**, because the checks below show that C2's contingent answer cannot beat the reviewer's ranked-list baseline on DOM except under hand-built conditions.
- **Checked against DOM's released code, not its prose [2601.22153, digest].**
  - Instruction tags (category, height, area, position, distance to robot, velocity) are computed once, from the *initial* object states. The referent of every single-object task is therefore fixed at t0.
  - The long-horizon task's tag is "entire set of objects", with fastest-first order, so order carries no instruction semantics.
  - So no DOM task has an instruction keyed to a motion outcome, and no new arrival can outrank the target. The preferred action changes with the realized future only through reachability. That is exactly where a ranked list gated at arrival matches the contingent form ([2204.01691]-style gating).
- **Reviewer points.**
  - **(i) Positioning against AESOP [2407.08735].** AESOP already branches over the brain's possible *answers* inside the executor, keeping all of them feasible for K steps, with K set from the 95th percentile of measured latency.
    - C2's claimed delta, branches over world futures inside the brain's answer, is dropped. On DOM it has nothing to act on.
    - C3 keeps AESOP's principle. It extends it to the case AESOP cannot handle: the options are moving targets whose catchable windows close at different times, so they cannot all be kept feasible.
  - **(ii) The ranked-list baseline.** It is now a measured arm of the discovery, along with the C2 contingent prompt. The prediction is that they tie (see effect sizes).
  - **(iii) Deterministic vs exogenous forks.**
    - Straight, curved and collision-deflected rolls are deterministic physics. The certifier gives them a point forecast fitted to the live track.
    - Scripted pushes and collisions (DR) and the force/torque perturbation events are exogenous. They get a tolerance band plus re-solving on the live track at 10 Hz.
    - No hypotheses are shown to the brain.
  - **(iv) Effect sizes:** committed below.
  - **(v) Release and cost:** verified below.
  - **(vi) Certifier:** specified below as new engineering.
- **Kept from earlier verdicts.**
  - Identity marks sit only on objects' current pixels, which is SoM's tested regime [2310.11441]. No ghosts are drawn.
  - Late binding is built in, because the released demonstrator tracks the live pose [2601.22153]. This covers ReKep-style binding [2409.01652].
  - The trails-plus-Δ prompt remains a brain-prompt arm.

**Source inspiration** Novelty type: recombination of distant concepts (speculative execution from computer architecture and agent systems, plus deferred-decision interception from aerospace control).
- **Speculative Actions [2510.04371].** While a slow, authoritative actor (a frontier LLM) computes, a fast speculator guesses its top-k next actions. Their consequences are pre-launched, and a branch is committed only if it matches.
  - Top-3 beats top-1 by a wide margin (54.7% hit rate in chess, "significantly" higher accuracy on HotpotQA).
  - The scheme is lossless only under Assumption 2: wrong guesses have no side effects or can be rolled back. Physical, irreversible effects are named as the case where "naive speculation is harmful" [2510.04371, Sec 2–3].
- **Deferred-decision trajectory optimization for moving candidates [2610.17003].** It handles the case speculation cannot.
  - "Committing too early can direct an agent toward a non-target, whereas excessive deferral can leave insufficient time or control authority for capture."
  - Its answer is one branch per candidate. All branches share the applied control and separate as late as feasibility allows. When no branch can be verified, it falls back to guidance toward a candidate still in play [2610.17003, Sec I, III-C].
  - The identity there comes from repeated queries to a sensor, and the decision-maker is an optimizer.
- **Why the two combine.** Physical pursuit violates exactly Speculative Actions' Assumption 2: a wrong speculative pursuit spends the reachability the right answer needs. DDTO is the principled form of speculation when the side effects are irreversible.

**How it maps to this problem**
- **Roles.**
  - Actor: the frontier brain (Astra). Given SoM marks and the tracker's table (IDs, positions, velocities), it names the target and the container.
  - Speculator: a local open VLM of at most 8B on the same prompt, returning top-3 IDs with confidences in under a second.
  - DDTO's candidates: the speculator's top-k objects.
  - The moment of identity revelation: the brain's answer, at a latency measured online.
  - DDTO's shared prefix: what the arm does during the call.
- **The certifier (new engineering, scripted, CPU only).** For each candidate it forecasts the object's track and computes the time window in which the arm could grasp it.
  - Inputs:
    - the live 25 Hz track;
    - a point forecast (constant velocity with friction deceleration fitted on the last 0.5 s, plus specular reflection off known container and table edges);
    - the demonstrator's own reach rule (0.75 m);
    - an end-effector speed and acceleration bound measured from demonstrator logs.
  - Exogenous pushes are not forecast. Re-solving at 10 Hz absorbs them, and a tolerance band set from pilot forecast residuals at horizon Δ, in the spirit of DDTO's conformal regions, keeps the window conservative.
  - It is validated offline by replaying DOM test trials and checking its "catchable" verdicts against the demonstrator's actual outcomes.
- **During the call.**
  - Among about 30 candidate end-effector waypoints, the executor drives toward the one that maximizes the speculator-weighted probability that the brain's eventual choice is catchable when the answer arrives. The arrival time is taken at the 90th percentile of measured latency, following AESOP.
  - If only one candidate is catchable, the executor simply speculates on it. If none is, it holds.
- **At arrival.** The brain's ID is bound to the tracked object, and the released demonstrator intercepts it.
  - If the named object is no longer catchable, the executor takes the catchable candidate the speculator ranks highest, following DDTO's fallback.
  - If the speculator ranked the brain's choice outside its top-k, the executor still switches whenever the certifier says that object is catchable.
- **One mechanism, the rest plumbing.** The single mechanism is in-call pursuit that keeps the brain's likely answers catchable, weighted by a speculator. The speculator, certifier, tracker (simulator ground truth) and demonstrator are plumbing.

**Why it could work / feasibility**
- **Why waiting fails in DOM.** Speeds are 0.15–0.75 m/s and reach is 0.75 m, so a moving object stays in reach for roughly 2–10 s. A 4 s call therefore loses most fast objects before the answer. Calls range from 3.1 s for GPT-3.5 [2407.08735] up to 31–105 s for frontier proposals in SCBT [2610.25455].
- **Why hedging recovers it.**
  - The speculator's top-3 covers the brain's answer far more often than its top-1 [2510.04371].
  - Holding several candidates reachable through a shared prefix is DDTO's validated move [2610.17003].
  - DOM's arm dynamics are scripted and known, which is the assumption DDTO needs.
- **Released and runnable (verified in code).**
  - DynamicVLA/DOM released training and testing code on 2026-04-26. The evaluator `simulations/evaluate.py` is non-paused (non-blocking action receive, hold-last-action, wall-clock pacing). The demonstrator is released as `simulations/state_machines/pick_sm.py` and `place_sm.py`, but it gates only on the *current* distance, so the window certifier above is new [2601.22153, digest].
  - RAVEL ran DOM non-paused on an RTX 4090 [2609.34170].
  - Simulation load: 6 sub-dimensions × 200 trials × about 25 method-and-latency configurations × about 15 s each, about 31 h of real-time simulation on 4 GPUs. This is well under the 40 GPU-day cap. Engineering is about 3 days for the certifier, 2 days for the brain client, and no training.
- **API cost, grounded.**
  - Astra list prices are $10/M input, $1/M cached input and $50/M output including reasoning [2610.01939, App E].
  - One grounding call is about 1.5k cached system tokens, at most 6k fresh tokens (three 480×360 images plus the table) and at most 1.5k output tokens, about $0.14 at the upper bound. This is cross-checked against CALL's ~5k Astra tokens per LIBERO episode [2610.14117] and measured in the pilot.
  - DOM reuses each trial's initial state identically across methods [2601.22153], so one Astra answer per trial and prompt type is cached and replayed at every injected latency Δ ∈ {0, 1, 2, 4, 8} s and for every executor arm.
  - Three prompt types (single ID, ranked list, contingent) × 1,200 trials, plus about 600 non-cacheable re-asks and a 300-call pilot, is about 4,500 calls, or $450–630.
  - A 200-trial live-latency subset checks that replay matches live calls. All of this fits the ≈US$1,000 budget.
- **Committed effect sizes.** P is the paused-world success of brain + demonstrator per sub-dimension.
  - **Discovery, Δ = 4 s, moving-object trials:**
    - waiting for the brain keeps ≤ 0.5·P;
    - ≥ 80% of lost trials are late-but-right (the brain's ID equals its paused answer);
    - latency-induced wrong IDs are ≤ 5% of trials;
    - ranked-list-plus-arrival-gate and the contingent prompt each land within ±3 points of brain-wait.
  - **Method, Δ = 4 s:**
    - hedged pursuit recovers ≥ 60% of the brain-wait loss on VU/SR/MP;
    - it beats speculate-top-1-then-switch by ≥ 8 points on VU and SR;
    - it beats speculator-only, with no brain, by ≥ 10 points on VU;
    - it ties within ±3 on Closed-loop Reactivity (one object, nothing to hedge), the negative control.
  - **Cost:** no brain call is made when at most one candidate is certified catchable, which should cut calls by ≥ 30% at ≤ 2 points of success.
  - Falsifier: if wrong-ID errors exceed 15% of trials, the discovery refutes C3's premise and points back to C1/C2.
- **Key assumption.** The speculator's top-3 usually contains the brain's answer, and DOM scenes usually hold two or three candidates with overlapping catchable windows.

**Novelty vs. closest in-domain work**
- **Prior parts:**
  - AESOP [2407.08735] keeps the brain's possible answers jointly feasible during its latency, but over d fixed interventions with static anomalies, where all options can be kept.
  - SIGMA [2610.09520] keeps the local planner driving and checks the cloud answer's validity on arrival.
  - AgenticCache [2604.24039] executes cached symbolic plans and confirms or replaces them when the late LLM answer comes.
  - Speculative Actions [2510.04371] requires reversible side effects.
  - DDTO [2610.17003] has no slow semantic oracle.
- **Delta:**
  - speculation whose side effects are physical and irreversible, made safe by DDTO-style deferral among *moving* candidates whose windows close during the brain's own latency, weighted by a speculator's prediction of the brain's answer;
  - first measured on a standard non-paused benchmark with a frontier brain, with the latency penalty split into which-object vs when errors.

**Main risk** On DOM's perception sub-dimensions the speculator may agree with the brain so often, or the candidates' windows may overlap so rarely, that hedged pursuit ties speculate-top-1. The method would then shrink to "speculate and switch", and the contribution to the discovery plus the certifier. A 100-trial pilot on VU and SR settles this.
