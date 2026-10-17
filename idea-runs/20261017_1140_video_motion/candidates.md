### C1 — Guidance as motion magnification: separate gains for the frame-shared and inter-frame parts of the CFG difference

**Intuition** Treat the classifier-free-guidance difference (conditional minus unconditional prediction) as a short video and do to it what Eulerian motion magnification does to real footage: pass its frame-shared part (appearance) through at an ordinary, conservative gain, and give only its coarse, slowly varying inter-frame part (the displacement the prompt adds) a larger gain. Turning guidance up then magnifies the motion the prompt asks for instead of only sharpening each frame.

**Gap it attacks** Axis "motion amplitude under classifier-free guidance in training-free video diffusion sampling", Gap 1. CFG and its motion variants multiply the whole spatiotemporal guidance difference by one gain: a scalar in [2603.14073], a spatial energy map in [2604.26503], a prediction-parallel projection in [2410.02416], a global ratio in [2508.03442]. T2V predictions are appearance-dominated [2506.01144], so most of any extra gain goes to appearance. Frames get sharper or over-saturated while the dog keeps trotting in place, and uniform extrapolation "reinforce[s] the dominant static modes" [2603.14073]. Closing the gap would make guidance strength a motion control at plain CFG cost (2 NFE per step). It would also test whether "sharper but not more dynamic" comes from how the gain is allocated rather than from model capacity.

**Source inspiration** Eulerian video motion magnification (signal processing / computational photography).
- [1804.02684] models a video as a fixed image moved by a motion field and aims for the same image moved by a magnified field. Eulerian methods do this without tracking: they extrapolate the difference between frames' representations by a factor α ("anchor + α × difference", the same form as CFG). Two conditions make this clean. First, only a representation of position ("shape") is magnified, and intensity/appearance ("texture") is passed through unmagnified, because otherwise the method "also magnif[ies] intensity changes" and noise. Second, a temporal band-pass selects the motion of interest and keeps noise from being magnified. Linear magnification stays clean only up to a moderate factor.
- FD4MM [2403.07347] adds the spatial rule. It magnifies only the inter-frame difference of low-spatial-frequency features, because that band holds a stable motion field. High-frequency detail, which carries appearance and noise, is passed through unchanged and recoupled afterwards to avoid ringing.
- [2506.02300] already carries magnification from videos to a model-derived difference direction: it treats a classifier's gradient as "infinitesimal motion" and linearly extrapolates it. Extrapolating in a basis that does not isolate position mainly brightens, darkens or blurs. Extrapolating the position-encoding part moves structure.

Novelty type: recombination-of-distant-concepts (video motion magnification → diffusion guidance).

**How it maps to this problem**
- The guidance difference plays the role of the subtle video to be magnified. In flow matching, the velocity difference between the two branches at the same noisy input is a rescaled difference of their two clean-video estimates, so it is itself a (blurry) video and a temporal filter can be applied to it.
- The unconditional branch plays the reference/anchor; the guided prediction plays the magnified frame.
- The frame-shared (temporal-mean) part of the difference plays EVM's unmagnified "texture" and keeps a conservative gain. This also matches FDG [2506.19713]: in images, the coarse spatial band of the guidance is what over-saturates and kills diversity at high gain, and in a video that colour/layout push is largely common to all frames.
- The slowly varying inter-frame part at coarse spatial scales plays the band-passed motion signal and gets the larger "magnification" gain. The extra displacement that the conditional branch has relative to the unconditional one is therefore extrapolated further.
- Fast frame-to-frame changes (flicker-like) and fine-detail inter-frame changes play the noise and detail that EVM and FD4MM keep out of the magnifier. They get no extra gain.
- It is applied in the early window where coarse motion commits. There the clean estimate is blurry, i.e. dominated by coarse spatial scales, which is the regime where small-motion, first-order magnification applies.
- By-product: every step yields, at no cost, the share of the guidance difference that is inter-frame versus frame-shared. This tests the appearance-dominance premise directly, and could later set the motion gain from the sample's state (Gap 2).

**Why it could work / feasibility**
- *Condition the mechanism relies on:* the magnified channel must encode small displacements of an otherwise shared appearance, and must be separated from that appearance [1804.02684, 2403.07347]. The temporal-mean / inter-frame split does this separation along time. FlowMo shows that taking inter-frame differences is what exposes motion in appearance-dominated T2V predictions [2506.01144].
- *Size of the push:* only a moderate extra gain on one band is needed, which is the regime where linear magnification is reported clean [1804.02684].
- *Exactness:* CFG is linear in the two predictions, so splitting the difference into bands and recombining them is exact and essentially free. FDG does the same for spatial bands at no extra cost [2506.19713].
- *Cost:* no extra NFEs, gradients, LLM or attention hooks. It runs on Wan2.1-1.3B on one 24 GB GPU, transfers unchanged to CogVideoX-2B and LTX-Video, and can also be stacked on MotionCFG's anchor [2603.14073].
- *Key assumption:* early on, the conditional estimate already contains more (or differently directed) coarse motion than the unconditional one, so the inter-frame part of the difference points toward the prompt's motion. MotionCFG's finding that contrasting against a motion-degraded anchor roughly doubles flow suggests that such a branch-difference motion signal exists [2603.14073].

**Novelty vs. closest in-domain work** FDG [2506.19713] also gives separate gains to bands of the guidance difference, but it splits images by spatial frequency to trade saturation against detail, with no temporal axis and no motion. MotionCFG [2603.14073] targets motion, but it changes only the anchor and keeps one gain over the whole difference. Here the split is along time (frame-shared vs. inter-frame, band-limited as in motion magnification), and its purpose is to enlarge displacement rather than detail.

**Main risk** In the early window both branches may be about equally static. The inter-frame band of their difference would then carry little prompt-specific displacement, and boosting it would give flicker or ghosted double edges (a cross-fade, like extrapolating in a basis that does not encode position [2506.02300]) rather than larger motion.


### C2 — Early lock-in relief: withhold guidance from the frame-shared part of the CFG difference while motion commits

**Intuition** Early in sampling, the frame-shared part of the CFG difference acts like a sharp conditioning image handed to every frame at once. Extrapolating it at full gain locks the clip into one appearance and layout before motion forms, which is the static shortcut that strong history guidance and early image detail are known to cause. So, only during that early window and only at coarse scale, C2 passes the frame-shared part through without extrapolation (as motion magnification leaves texture unmagnified), keeps the ordinary CFG gain on the inter-frame part, and then returns to plain CFG.

**Gap it attacks** Axis "motion amplitude under classifier-free guidance in training-free video diffusion sampling", Gap 1 (one guidance gain over appearance and motion).
- *Concrete failure:* in the early, high-noise steps, every current rule extrapolates the frame-shared and inter-frame parts together: a scalar [2603.14073], a spatial field [2604.26503], a per-token field [2610.14153], or a time-only interval that switches both off at once [2404.07724]. T2V predictions are appearance-dominated [2506.01144], so the early CFG update is mostly a frame-identical appearance push. Turning guidance up therefore commits the static template harder ("sharper but no more dynamic"). Switching early guidance off wholesale removes whatever motion the difference carries as well: Interval Guidance lowers FLOW on Wan2.1-1.3B (4.10 → 3.76) and on Wan2.1-14B (2.95 → 2.65), and costs CLIPScore [2603.14073].
- *Why closing it matters:* it would separate guidance that locks in from guidance that moves, at plain CFG cost (2 NFE per step). It would also test whether under-animation is a lock-in induced by guidance.

**If improving prior candidate**
- *C1 weakness:* C1 argued for reallocating gain without a mechanism. Under plain CFG the inter-frame part already gets the full gain, and sweeping that gain barely changes dynamics [2603.14073]. C1 also magnified the inter-frame residual of an additive latent, which is the basis its own sources say cross-fades [1804.02684, 2506.02300].
- *What changed:*
  - C2 names mechanism (a), relief from early appearance lock-in [2502.06764, 2506.08456, 2404.07724].
  - The lever is reversed: lower the frame-shared gain early, and never raise the inter-frame gain above plain CFG. C1's raise survives only as the ablation that would indicate mechanism (b).
  - The split is confined to the coarsest band in the early window, so the only change relative to CFG is a frame-identical term.
  - C2 states that it changes the amount of motion, not its kind.
  - C2 is positioned against TrajCFG, Interval Guidance and CFG-Zero*.
  - The unchanged-transfer claim is dropped.

**Source inspiration**
- *History Guidance [2502.06764]:* strong guidance toward history frames makes "overly static videos", because copying the latest history frame is a trivial solution. Guiding with fractionally noised history, whose guidance carries only low-frequency content, raises dynamics while keeping quality (Kinetics-600 FVD 181.6 → 170.4). Principle: guidance freezes a video when it pushes hard on content that every frame can simply copy.
- *ALG [2506.08456]:* in image-to-video, features lock onto the conditioning image's details after one step and confine sampling to a static shortcut. Low-passing that shared input only until t_trans = 0.06 already gives +32% dynamic degree, at near-unchanged quality. Principle: the lock-in happens in an early window, and withholding the shared content only there relieves it.
- *Interval Guidance [2404.07724]:* in images, guidance at high noise collapses layouts onto "a handful of template images" and saturates colour. Detail comes from mid-range guidance, so early guidance can be removed without losing crispness. Principle: the early part of guidance is what commits the template.
- *Eulerian motion magnification [1804.02684]:* supplies the form. Extrapolate only the part that encodes change, and pass shared texture through at unit gain. Its small-motion condition says where a split into temporal mean and residual separates appearance from motion faithfully.

Novelty type: reinforcing-a-weak-connection. A lock-in mechanism shown for history-conditioned and image-conditioned video is carried to text CFG in T2V, with the form taken from motion magnification.

**How it maps to this problem**
- *The copyable shared content* (HG's history frames, ALG's input image) becomes the frame-shared (temporal-mean) part of the text-CFG difference. T2V has no conditioning image, but CFG manufactures one: the push toward the prompt's appearance, which every frame receives identically.
- *Guidance strength on that content* becomes the extrapolation gain on the frame-shared part, which C2 withholds early.
- *ALG's switch time* becomes the end of the window in which layout and coarse motion commit (about steps 1–8 of 50 on Wan2.1-1.3B [2506.01144, 2609.23658]). After it, plain CFG returns and restores sharpness and alignment, as mid-range guidance does in [2404.07724].
- *The inter-frame part* keeps the ordinary CFG gain. It is neither removed, as in Interval Guidance, nor magnified, as in C1.
- *Regime:* the split is taken on the coarsest spatial band only. Early guidance energy lives in that band [2506.19713], and layout and position commit there [2609.23658]. At that scale, early displacements are small relative to the band, which is EVM's condition for the temporal mean to stand in for appearance [1804.02684]. Finer bands keep plain CFG.
- *Amount, not kind:* C2 changes how much motion commits, specifically whether the subject stays anchored to one position. It adds no motion target and does not scale existing motion. Like ALG, it removes a static attractor, so the motion that forms is whatever the conditional branch already prefers. It can turn "trotting in place" into "crossing the beach" only if the conditional prediction already leans toward crossing and the static solution was winning by lock-in. It cannot produce a motion the model does not represent [2506.01144, 2607.26706].

**Why it could work / feasibility**
- *Condition the mechanism relies on:* a strong early push on content that every frame shares and the model can satisfy by copying ([2502.06764] copy solution, [2506.08456] one-step lock-in). Two facts make the frame-shared CFG term such a push in T2V. First, predictions are appearance-dominated, so the early difference is mostly frame-shared [2506.01144]. Second, high-noise guidance commits layouts to templates [2404.07724], and RoPE spatial anchoring then holds the template at the same position across frames ("the basketball remains stationary") [2609.23658]. This fits MotionCFG's reading that uniform CFG reinforces "the dominant static modes" [2603.14073].
- *Why not just drop early guidance:* evidence on weakening early guidance as a whole is mixed. Zeroing the first update (CFG-Zero* [2503.18886]) raises Wan2.1-1.3B dynamic degree from 65.28 to 68.90 [2610.14153]. Interval Guidance and CADS lower FLOW [2603.14073]. C2's account is that weakening all of it removes the inter-frame motion push along with the lock-in, so only the asymmetric rule should reliably help. The deciding comparison has three arms: frame-shared part withheld (C2), all guidance withheld (interval style), and inter-frame part raised (C1 style, mechanism (b)).
- *Exactness and cost:*
  - CFG is linear in the two predictions, so splitting the difference into temporal-mean and residual parts and recombining them is exact, as with FDG's bands [2506.19713].
  - Relative to plain CFG, the only change is a coarse term that is identical in every frame, so it cannot create ghosts or double edges.
  - There are no extra NFEs, gradients, LLM calls or attention hooks. It runs on Wan2.1-1.3B on one 24 GB GPU.
  - Each step yields, at no cost, the split of the difference's energy between frame-shared and inter-frame parts, which tests the appearance-dominance premise directly.
- *Per-backbone window:* on CogVideoX the earliest clean estimates are dominated by watermarks, and MotionCFG had to delay its window there [2603.14073]. The window is therefore set per backbone, and no unchanged transfer is claimed.
- *Key assumption:* in T2V, the static commitment is driven at least partly by the guidance's frame-shared push, not only by the model's own prior.

**Novelty vs. closest in-domain work** ALG [2506.08456] relieves the same lock-in by low-passing an external I2V image in both branches, with a third NFE early on. C2 finds the T2V counterpart of that image inside the text-CFG difference, namely its frame-shared part, and withholds only its extrapolation, at plain CFG cost.
- Interval Guidance [2404.07724] and CFG-Zero* [2503.18886] weaken early guidance, or the first update, as a whole.
- The concurrent zero-NFE baseline TrajCFG [2610.14153] raises per-token gains to as much as 10 (base 6), mostly on foreground subjects, so the subject's shared appearance is extrapolated harder too. It reaches Wan2.1-1.3B dynamic degree 70.83 (from 65.28). C2 must beat it, and the two compose if TrajCFG's gains are restricted to the inter-frame part.
- TPD [2607.26706] gates the CFG update per frame, but it does so to restore late events, using an LLM and a third branch.

**Main risk** In T2V the static commitment may come from the model's prior and RoPE anchoring rather than from the guidance's frame-shared push. Interval Guidance's lower FLOW on Wan2.1 is consistent with this [2603.14073]. In that case, withholding the shared gain would only cost early prompt alignment, and C2 would behave like Interval Guidance on one band.
