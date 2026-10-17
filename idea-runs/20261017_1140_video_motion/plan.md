# plan — Training-free motion quality in text-to-video diffusion transformers

**Goal**: ONE focused, sharp, well-grounded methodological intuition for this problem that a simulated CVPR 2027 panel rates at ≥ 5/10 acceptance odds, executable within the Constraints in problem.md.

**Active direction**: Axis `motion amplitude under classifier-free guidance in training-free video diffusion sampling`, Gap 1 — CFG and its motion variants scale the video guidance difference as one undifferentiated vector, so the inter-frame (motion) part cannot get more gain than the frame-shared (appearance) part; with appearance-dominated predictions, more guidance means sharper, not more dynamic.
**Status**: `drilling`

## Candidate axes
- A1 `motion amplitude under classifier-free guidance in training-free video diffusion sampling` — done: 2 gaps (one gain for appearance and motion; open-loop motion strength with no state feedback)
- A2 `early-step formation of coarse motion in video diffusion denoising` — done: 2 gaps (early-window objectives are prompt-independent so static-coherent commitments are kept; commitment competition settled by RoPE anchoring, local samplers can't move it)

## History
- `forming` at turn 0: run created; spawning gap_finders on the first two axes in parallel.
- `drilling` at turn 1: both axes mapped (4 gaps). Chose A1/Gap 1 (single guidance gain over appearance and motion): zero extra NFE, directly explains the problem's "sharper but not more dynamic" failure, testable on Wan2.1-1.3B with the lab's RAFT/VBench, and the gap_finder's targeted searches found no decomposed-gain method. A1/Gap 2 (closed-loop motion strength) is a natural extension the innovator may fold in; A2 gaps kept as fallbacks. Spawning innovator → C1.
- `under_review` at turn 2: innovator wrote C1 (new) — treat the CFG guidance difference as a video to be motion-magnified (Eulerian motion magnification): conservative gain on its frame-shared part, larger gain only on its coarse, slowly varying inter-frame part. Closest: FDG [2506.19713] (spatial-frequency split, images), MotionCFG [2603.14073] (one gain). Spawning reviewer on C1.
- `drilling` at turn 3: reviewer → C1 `revise(focus=coherence)`. Objection: under plain CFG the inter-frame part already gets the full gain and sweeping it barely changes dynamics [2603.14073], so "reallocate gain" works only via (a) relief from early appearance lock-in (lower frame-shared gain early; supported by History Guidance [2502.06764] and ALG [2506.08456]) or (b) motion-band gains far above the appearance ceiling; the additive latent split is the intensity variant that cross-fades rather than moves [1804.02684, 2506.02300]; concurrent TrajCFG [2610.14153] (per-token CFG gain, zero NFE, Wan2.1-1.3B DD 65.28→70.83) is the zero-cost baseline to beat. Revise cycle 1: spawning innovator → C2 BUILD_ON C1.
