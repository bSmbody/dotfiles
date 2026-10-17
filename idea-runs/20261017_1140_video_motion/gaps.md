## Axis: early-step formation of coarse motion in video diffusion denoising

### What has been done
- **Locating when coarse motion commits.** Several analyses agree that coarse motion is decided early in sampling, within about the first 10–30% of the schedule.
  - FlowMo decodes the clean-latent estimate x̄1 on Wan2.1-1.3B. Layout is fixed by about step 4 of 50, and motion is added in steps 4–8 [2506.01144].
  - A prompt-tampering probe (DDIM-invert a video, then resample with a subject-edited prompt only inside a timestep range) finds an early motion-dominant regime, with a boundary at τ≈700–900 of 1000. This holds on ModelScope, Latte and CogVideoX [2512.22175].
  - In Wan2.1-T2V-1.3B, object-token cross-attention starts with several candidate regions per frame and converges to one trajectory within about 5 of 50 steps. Self-attention picks the winner, and RoPE spatial decay anchors frames that commit late to the positions of frames that committed early [2609.23658].
  - Motion-energy maps of the decoded x̂0 reach 93% convergence by step 5 of 40 (Wan2.2-14B, image+text-to-video). Re-noising the same seed changes the route by at most 25%, against 68% across seeds [2603.30043].
  - In image-to-video, intermediate features lock onto the conditioning image's details after one step and produce a static "shortcut" [2506.08456].
- **Re-initialising the low-frequency band of the initial noise (before the window, with extra passes).**
  - FreeInit re-diffuses its own full sample, keeps the 3D-FFT low band and refreshes the high band, over 2–4 extra full passes [2312.07537].
  - FreqPrior does the same with a variance-preserving filter and partial sampling, which still costs two extra samplings [2502.03496].
- **Correcting a single trajectory inside the window, using the model's own clean estimate.**
  - FlowMo takes gradient steps on z_t during steps 1–12. Its loss is the largest patch-wise temporal variance of consecutive-frame velocity differences. This costs ×2.39 time [2506.01144].
  - SpecLoR runs at steps 2–5 of 40. It clips the 3D amplitude spectrum of the look-ahead x̂0 toward a universal natural-video envelope, leaves the phase untouched, and re-noises. This costs 4 extra NFEs [2606.11969].
  - Self-Refining Video Sampling (SRVS) runs predict-and-perturb at a fixed noise level for t<0.2. It refines only regions marked uncertain, at 1.5× NFE [2601.18577].
- **Modulating conditioning or attention inside the window.**
  - Adaptive Low-Pass Guidance (ALG) low-passes the image-to-video conditioning latent inside the CFG terms before a switch time t_trans [2506.08456].
  - A global scale λ<1 on the RoPE height/width frequencies during the first 5 steps relaxes spatial anchoring [2609.23658].
- **Injecting an external motion target.** Video-MSG pastes cut-out objects along bounding boxes planned by GPT-4o, using a T2I model, an I2V model, RAM, Grounding-DINO and SAM. It then starts denoising from this sketch, forward-noised to α·T [2504.08641].
- **Screening seeds early.**
  - Early Planning Beam Search (EPBS) scores the step-τ x̂0 of many seeds with a task-specific trajectory verifier [2603.30043].
  - PRISM is a reward head on the frozen DiT's early blocks, trained on 26k human preference pairs [2606.20310].
  - LatSearch runs a sequential-Monte-Carlo-style search with a trained latent reward. Its early-step training targets are video rewards scaled by similarity to the final latent [2603.14526].
  - Proprio self-scores finished latents by their flow residual, so each candidate must be fully generated [2605.28230].

### Open gaps on this axis

- **Gap:** Training-free T2V samplers that intervene in the early commitment window score the blurry clean-latent estimate against a prompt-independent idea of a well-formed video. FlowMo uses minimal temporal variance of frame differences, SRVS uses mode-seeking predict-and-perturb, SpecLoR uses a universal 1/f amplitude envelope with the phase untouched, and FreeInit/FreqPrior use the model's own earlier sample. All of them assume coherence is the only thing that can go wrong at commitment. That leaves a coherent but under-animated commitment (the dog trotting in place) unresolved: it satisfies every one of these objectives, so it is kept rather than corrected.
- **Near-miss methods and coverage:**
  - [2506.01144] FlowMo acts in the right window (steps 1–12 of 50, where it shows motion forms) and uses only the model's own prediction. Its loss, max_{w,h} Var_f |u_{f+1} − u_f|, is minimised by static or uniform motion, and dynamic degree falls (Wan2.1-1.3B 83.21→81.96, CogVideoX-5B 65.29→63.92).
  - [2601.18577] SRVS works at t<0.2 and calls itself temporal mode-seeking with "reduced temporal variance".
  - [2606.11969] SpecLoR works at steps 2–5. Its target amplitude is the same for every prompt. It leaves untouched the phase, which it says "encodes spatiotemporal displacement". Its stochastic variant lowers dynamic degree from 0.916 to 0.850.
  - [2312.07537] FreeInit lowers dynamic degree on all three backbones it tests (AnimateDiff 97.03→75.30) and erases small, fast-moving objects.
  - [2502.03496] FreqPrior still lists "unnatural smoothness" as a limitation.

  The five share one deficiency: nothing in their in-window objective depends on what the prompt asks the motion to be. The only near miss with a motion target, [2504.08641] Video-MSG, gets it from an external planner stack as rigid box-wise cut-and-paste sketches injected by forward-noising. It shows no gain on action, dynamic-attribute or interaction prompts ("difficult to guide solely with bounding boxes"), and its single global α trades trajectory adherence against naturalness. The learned latent rewards [2606.20310] and [2603.14526] do judge motion quality on noisy latents. But they need trained heads and human or verifier labels, and they are used only to choose among seeds.

  Query trail:
  - Searches: "FreeInit", "FlowMo", "\"video diffusion\" \"early denoising\"", "\"text-to-video\" \"noise initialization\"", "\"dynamic degree\" video diffusion", "\"video diffusion\" static videos motion", "\"self-refining\" video sampling", "\"text-to-video\" training-free motion".
  - Recency queries since 2025-10-17: "training-free video motion", "video diffusion early timesteps", "video diffusion noise initialization".
  - Screened by abstract only, not read and not used as evidence: TeDiO, STAS, Φ-Noise, ProxyUp, CausalMotion.
- **Methodological deficiency:** The training objective does not match the failure (training-objective mismatch). These early-window objectives judge coarse motion only by in-sample smoothness or typicality, never by agreement with the prompt. A static but coherent clip is therefore a fixed point or minimiser of all of them.
  - FlowMo's ablation notes that "most patches are static", and its loss shrinks when frame differences shrink [2506.01144].
  - SRVS's refinement reduces temporal variance by construction [2601.18577].
  - SpecLoR's envelope ignores the prompt and leaves untouched the phase that carries displacement [2606.11969].

  So these methods remove incoherent motion but cannot tell an under-animated commitment from a correct one. Where a target is supplied, as in [2504.08641], it lives in a form (rigid object boxes in pixel space) that cannot express articulated or state-change motion.
- **Why it matters:** Small open T2V models (e.g., Wan2.1-1.3B on 24 GB GPUs) mostly fail by under-animation. Today a practitioner can buy coherence (FlowMo, SRVS, SpecLoR) or get a planned trajectory only through a multi-model planner stack. "Sharper but no more dynamic" therefore stays unsolved inside the sampler. Closing this gap would show whether a frozen model's own early predictions hold enough prompt-conditioned information to tell a coherent-static commitment from a coherent-dynamic one. That would separate the coherence-versus-dynamism trade-off these papers report from the simple absence of a motion target.
- **Evidence route:**
  - Generate on motion-heavy prompts (VBench dynamic-degree subset, VideoJAM-bench) mixed with low-motion prompts, on Wan2.1-1.3B, against FlowMo, SRVS and SpecLoR at matched NFE.
  - RAFT flow magnitude and VBench dynamic degree should rise on the high-motion prompts but not on the low-motion ones. Motion smoothness and subject consistency should not fall below FlowMo or SpecLoR.
  - Diagnostic: take seeds whose baseline output is near-static. At the end of the window (about step 8 of 50), the decoded x̂0 should already show the added displacement, while FlowMo and SpecLoR leave flow magnitude at or below baseline on the same seeds.
  - Run a small human two-alternative test on "the amount of motion matches the prompt".

- **Gap:** Prior samplers try to improve early coarse motion in one of three ways:
  - local edits inside one trajectory after commitment (SRVS, SpecLoR, FlowMo);
  - whole-seed resampling or screening (FreeInit/FreqPrior extra passes, early beam search with a verifier or a trained reward head);
  - a single hand-tuned global knob (RoPE frequency scale, image-to-video low-pass).

  All of them leave the competition among coarse-motion hypotheses to the model's default dynamics. That competition is settled within the first ~5–15% of steps by the initial noise and by RoPE spatial anchoring, a positional bias that pulls late-committing frames onto early-committed positions and so favours stationary solutions. No method acts on it within a single trajectory.
- **Near-miss methods and coverage:**
  - [2609.23658] finds the mechanism in Wan2.1-T2V-1.3B: candidate regions compete unstably in steps 1–5, and a frame that settles early pulls neighbouring frames' candidates onto its position through RoPE anchoring, so "the basketball remains stationary in the air". Its training-free fix, a global λ on the RoPE height/width frequencies for 5 steps, "requires manual tuning of λ". A learnable per-head λ failed.
  - [2603.30043] measures that re-noising the same seed changes the committed route by at most 25%, against 68% across seeds. Its remedy, EPBS, needs a verifier with privileged positions of the agent, goal and obstacles.
  - [2601.18577] SRVS says its predict-and-perturb is "local search ... rather than a global resampling", and that for maze-like tasks "finding a good initial noise may be more effective".
  - [2606.11969] SpecLoR shows that interventions after about step 6 of 40 cannot repair the phase, and that locking the early phase traps wrong non-rigid motion.
  - [2506.08456] ALG shows the same static lock-in in image-to-video after one step. Its lever is the conditioning image, which text-to-video does not have.
  - [2606.20310] PRISM and [2603.14526] LatSearch rank seeds from early latents, but only with trained reward heads (26k human pairs for PRISM, similarity-scaled verifier labels for LatSearch) and only by choosing among seeds.
  - [2312.07537] FreeInit and [2502.03496] FreqPrior re-seed through extra full or partial sampling passes.

  Across all of these, commitment is either worked around globally per seed, at multi-pass or trained-verifier cost, or edited locally after the winner is fixed. Query trail: the same as the first gap, plus "\"inference-time scaling\" video diffusion" and the recency query "video diffusion early timesteps".
- **Methodological deficiency:** The commitment step has the wrong inductive bias, and the samplers are local by design (wrong inductive bias plus algorithmic limitation). Which candidate wins across frames is decided by positional locality. RoPE spatial anchoring favours same-position matches across frames, i.e. stationary configurations, and it acts before any existing correction [2609.23658]. The in-trajectory samplers are local operators around the current x̂0: predict-and-perturb at a fixed noise level, amplitude edits that leave phase untouched, one gradient step on z_t. They inherit whichever hypothesis won, as shown by the ≤25% same-seed route diversity [2603.30043] and SpecLoR's untouched phase [2606.11969]. The only training-free lever on the commitment mechanism itself is a global, hand-tuned frequency scale that does not depend on the competing hypotheses [2609.23658].
- **Why it matters:** Under a fixed NFE budget on consumer GPUs, the only ways to get a different coarse motion today are to multiply sampling cost (several seeds or passes) or to train a reward head on human preference data. Neither explains why stationary solutions win. Closing this gap would show whether the commitment competition inside one trajectory can be steered, or kept open long enough for a better motion hypothesis to win. That would turn the current seed lottery over coarse motion into a controllable step of the sampler.
- **Evidence route:**
  - Measure same-seed route diversity as in [2603.30043]: the cosine between motion-energy or RAFT-flow maps of the end-of-window x̂0 and the final video. Compare the baseline, SRVS, SpecLoR and a method that claims to close the gap.
  - The closing method should change the committed coarse motion of under-animated seeds (static to displaced, measured by RAFT flow on the final video) much more often than the local samplers, at ≤ +20% NFE.
  - At equal NFE, it should match or beat best-of-N and early screening on dynamic degree and motion smoothness.
  - Attention check: compared with baseline, the cross-attention candidate that wins should more often lie away from the earliest-committed frame's position, without more flicker or subject-consistency errors.
