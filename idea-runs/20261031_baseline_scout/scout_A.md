# Scout A — KV-cache quantization and compression for long-generation / reasoning inference

Scope: low-bit KV (INT2/INT4/FP4/FP8, rotation, vector/codebook, mixed precision, MLA-latent), lossless KV coding, token-level KV compression for reasoning models, and their use with offloading. Literature through 2026-10-31. KIVI is the common anchor; it is used as a baseline row inside nearly every paper below but was not read this run, so it is named without an id.

## Baseline table

| Baseline [id] | First version | Venue | Code (as stated by the paper) | Models / lengths evaluated | Headline measured result | Runtime / kernel support | Weak at |
|---|---|---|---|---|---|---|---|
| TurboQuant [2504.19874] | 2025-04-28 | not stated in arXiv metadata | not stated (community vLLM PR #38479 used by [2606.03458; 2605.17757]) | Llama-3.1-8B-Inst, Ministral-7B; NIAH 4k-104k, LongBench-E (prefill-heavy) | NIAH 0.997 = full precision at 0.25 memory; LongBench-E avg 50.06 at 3.5 bits and 49.44 at 2.5 bits vs full 50.06 (Section 4.2-4.3, Table 1) | None in paper (one A100). The community vLLM path has TPOT 5.56x BF16 on MiniMax-M2.5 [2606.20474, Section 7] | No long-decode reasoning evaluation. Under decode-time reasoning it does worse than 2-bit KIVI: AIME24 48.9 at 4.6 bits vs KIVI 55.5 [2606.03458, Table 1]. With mixed precision disabled it collapses (mean drop -43.90 on Qwen3-4B-Thinking) [2605.17757, Table 2] |
| PM-KVQ [2505.18610] | 2025-05-24 | ICLR 2026 | https://github.com/thu-nics/PM-KVQ | R1-Distill-Qwen 7B/14B/32B, R1-Distill-Llama 8B/70B; AIME24/25, CMIMC, LCB; 32K output | 2-bit R1-Distill-Llama-70B AIME24 64.79 vs KIVI 51.88 (BF16 69.14); R1-Qwen-14B CMIMC drop 1.87 vs KIVI 21.87 (Section 4.2) | HF-level code; "not combined with ... inference engines" (Appendix E) | Dense GQA only, no MLA (Appendix E). Static offline block allocation. Beaten by ThinKV at similar bits (R1-Qwen-14B AIME 43.33 vs 50.00) [2510.01290, Table 1] |
| R-KV [2505.24133] | 2025-05-30 | not stated | https://github.com/Zefan-Cai/R-KV | R1-Distill-Llama-8B, R1-Distill-Qwen-14B; MATH-500 (16K), AIME24 (32K) | Lossless at 10% budget (AIME24) and 34% (MATH-500) on R1-Llama-8B; up to +40% over SnapKV (Section 4.2) | Not compatible with paged attention (Appendix D); gather compaction costs up to 37x TPOT at large batch [2510.01290, Section 5.1] | Permanent eviction. Only baseline is SnapKV. Serving-framework integration is weak |
| DMS [2506.05345] | 2025-06-05 | NeurIPS 2025 | not stated in body | Qwen-R1 1.5B/7B/32B, Qwen3-8B, Llama-3.2-1B; AIME24, MATH-500, GPQA, LCB; up to 32K | Pareto gains at matched KV reads: +12.5 AIME24, +8.3 LCB on average; Qwen-R1-32B +12.0 AIME24 (Section 5.1) | Needs retraining (logit distillation, about 100 steps per unit of CR, Section 4); evaluated with its own implementation | Needs training. CR up to 8x and 32K only. Standard attention only, MLA is future work (Appendix A) |
| ThinKV [2510.01290] | 2025-10-01 | ICLR 2026 (Oral) | not stated | R1-Distill-Llama 8B/70B, R1-Qwen-14B, GPT-OSS 20B/120B, QwQ-32B, AceReason-14B; AIME, MATH-500, GSM8K, LCB; 32K | <3.67% of FullKV memory at a 1024-token budget with near-lossless AIME/LCB; QwQ-32B AIME 70.28 vs BF16 73.33 at 3.4 bits; 15.8x throughput over FullKV (Section 6.2, Tables 1, 3) | Custom CUDA quantization, Triton "Continuous Thinking" PagedAttention extension, vLLM serving experiment (Section 5, Figure 9) | "Not directly applicable to settings dominated by long input contexts" (Appendix F). Thought segmentation, schedule and keyword list are hand-set. No code stated |
| KVarN [2606.03458] | 2026-06-02 | not stated | https://github.com/huawei-csl/KVarN (vLLM) | Qwen3-4B, Phi-4-14B (reasoning), Llama-3.1-8B; AIME24, MATH500, HumanEval, IFEval, line retrieval | 2.3-bit uniform: Qwen3-4B AIME24 60.0 vs FP16 61.1 (KIVI 55.5); Phi-4-14B MATH500 84.8 vs 84.9 (KIVI 74.4) (Section 4.1.1, Table 1) | vLLM implementation; 0.18% normalization overhead; dequant within 1.4% of KIVI (Section 4.2, Appendix I) | Calibration-free and uniform 2-bit only. Not evaluated on MLA ("unclear", Appendix E). Small models (<=14B). Says no public serving framework supports 2-bit KV (Appendix E) |
| OSCAR [2605.17757] | 2026-05-18 | not stated | not stated | Qwen3-4B-Thinking-2507, Qwen3-8B, Qwen3-32B, GLM-4.7-FP8; GPQA, HumanEval, LCB v6, AIME25, MATH500; 32K | 2.28 BPE INT2: mean drop -1.42 (Qwen3-8B) and -3.78 (Qwen3-4B-Thinking) vs QuaRot-INT2 -60.70 / -74.24; Qwen3-8B AIME25 66.67 vs BF16 66.00 (Section 5.2, Tables 1-2) | SGLang paged INT2 mode with fused Triton kernels and prefix cache; up to 6.2x throughput at 100k (Sections 4, 5.4) | Fixed bit width with no per-token allocation; H100 only; theory holds only under a frozen-error surrogate (Appendix D). No code stated |
| QuantMLA [2609.36760] (sibling: RAQ-MLA [2610.33625]) | 2026-09-29 | not stated | not stated | DeepSeek-V2-Lite, Moonlight-16B, LongCat-Flash-Lite, GLM-4.7-Flash; GPQA, MATH500, AIME25, HumanEval, LCB, RULER to 32K | C4R4 within 0.26 points of BF16 on V2-Lite; GLM-4.7-Flash avg 53.75 at C4R4 (+2.70 over best baseline) and 51.43 at C2R4 (Section 4.2) | Native low-bit MLA attention in vLLM, within -7.42% to +4.29% of BF16 latency from 1K to 1M (Section 4.4) | Only INT4 (INT2 content). No DeepSeek-V4-generation model, whose KV is already FP4/FP8 QAT. Offline learned transforms. RAQ-MLA reaches about 2.5 bits but is measured on the GLM family only [2610.33625] |
| DeepSeek-V4.1-Flash (FP4-QAT KV + CSA2) [2609.19969] | 2026-09-17 | tech report | weights: https://huggingface.co/deepseek-ai/DeepSeek-V4.1-Flash; kernels named FlashMLA/DeepGEMM/TileKernels/DeepSelect | 552B MoE (16B active), 1M context, agentic/reasoning suite | Global KV of 890 bytes/token, about 1/4 of V4-Flash; persistent KV about 1/8 via SWA Bounded Replay; FP4 KV "only marginal" degradation (no number given) (Sections 1, 2.4.4, 3.2) | Production fused kernels; SSD/host persistent KV cache | SWA KV "kept FP8 due to its sensitivity to quantization" (Section 2.4.4). Authors flag CSA2 selection errors and approximate SWA replay as untested risks (Section 6). Too large for a newcomer to retrain |
| SplitZip (lossless) [2605.01708] | 2026-05-03 | not stated | https://github.com/Intelligent-Microsystems-Lab/SplitZip | Qwen3-32B, Llama-3-8B, Qwen3-30B-A3B KV; H200 + RDMA | Ratio 1.324 on BF16 at 613 GB/s encode / 2182 GB/s decode; up to 1.32x transfer, 1.30x TTFT; 1.14x over FP8 E5M2 (Section 4.2, Table 2) | Mooncake transfer, SGLang instrumentation | Only compresses transfers, not the resident HBM cache that attention reads. Ceiling set by exponent entropy; "codec overhead may outweigh" the gain at short context (Section 5) |

Supporting deployment reference, not a baseline row: UltraQuant [2606.20474] (2026-06-18, EMNLP 2026 Industry). FP4 KV with Hadamard rotation in vLLM on MI355X matches hardware FP8 KV throughput (1.38x vs 1.37x BF16) at half the bytes, and stays within 2 points of BF16 on reasoning (Sections 6.3, 7). Its Ultra-TQ decode kernel is upstreamed into vLLM; the FP4 kernel is not yet released (Appendix A).

## Stated limitations

Limitations the authors state themselves:
- **TurboQuant [2504.19874]** states no limitations section. Its KV evidence is prefill-heavy (NIAH, LongBench-E) and it reports no kernel or speed numbers [full text, Section 4].
- **PM-KVQ [2505.18610]**: "we do not consider ... MLA"; "we do not combine ... with other system-level optimization techniques and inference engines" [Appendix E].
- **R-KV [2505.24133]**: compatibility "with certain advanced attention mechanisms, such as paged attention ... presents a non-trivial challenge". Without framework interfaces, memory reallocation "can introduce significant overhead, potentially offsetting some of the acceleration gains" [Appendix D].
- **DMS [2506.05345]**: 1B-32B, contexts up to 32K, CR up to 8x; "extending DMS to ... Multi-head Latent Attention ... promising direction" [Appendix A].
- **ThinKV [2510.01290]**: "not directly applicable to settings dominated by long input contexts" [Appendix F]. Its own ablation shows thought-adaptive quantization alone gives only 1.1x throughput because "its substantial generation-length inflation negates most of the compression gains" [Section 6.3, Table 4].
- **KVarN [2606.03458]**: not for SSMs. For MLA "it is unclear how such attention mechanisms affect quantization quality". "End-to-end evaluation on a publicly available serving framework is hindered by the fact that currently such frameworks do not support 2-bit KV-Caches" [Appendix E].
- **OSCAR [2605.17757]**: the theory is "not yet a full proof of optimality for the complete autoregressive decoding process". It covers no NVFP4 or mixed formats, and "fixed bit-width ... does not study per-token bit allocation or thought-adaptive token precision". It targets only "SGLang-style paged serving on H100". Combining it with channel-wise schemes "while preserving an efficient serving layout remains open" [Appendix D].
- **QuantMLA [2609.36760]**: "no prior work has reported joint INT4 quantization of MLA's content and RoPE caches" [Section 4.1]. It offers no runtime certificate, and its content path is average-case [Section 3.2]. **RAQ-MLA [2610.33625]**'s path-split analysis is measured on GLM-4.7-Flash only [Section 3].
- **DeepSeek-V4.1-Flash [2609.19969]**: "Potential selection errors in CSA2 and approximate state reconstruction in SWA Bounded Replay may still cause capability degradation in untested boundary cases" [Section 6]. SWA KV is kept at FP8 "due to its sensitivity to quantization" [Section 2.4.4].
- **SplitZip [2605.01708]**: "for short contexts or compute-bound regimes, codec overhead may outweigh the reduced transfer volume". The compression ratio is "bounded by the redundancy in floating-point exponent values" [Section 5].
- **UltraQuant [2606.20474]**: the speed benefit over FP8 is "only observed when the context length is long enough, or concurrency high enough, to exceed the resident cache capacity of the FP8 baseline" [Section 9].
- **Supporting studies.** In Spend Bytes on Breadth [2610.05685], offline distortion curves "get the preference wrong on two of the three models" [Sections 1, 5.3]. WitCert [2607.28699] finds its band-norm certificate "1289x loose at 4 bits" and "vacuous" at 1-2 bits [Section 4.1].

Contradictions between papers:
1. **Does eviction inflate reasoning length?** ThinKV says eviction "does not cause an increase in generation length" and that only quantization does, by up to 5.1x [2510.01290, Sections 2, 6.3]. The other two papers disagree:
   - Hold Onto That Thought finds "lower budgets are capable of triggering longer reasoning traces", including non-terminating loops [2512.12008, Section 4.5, 4.7].
   - Spend Bytes on Breadth attributes much of eviction's loss to derailed runs that hit the length cap [2610.05685].

   The settings differ: ThinKV's eviction is segment-annealed K-means, while the other two use heavy-hitter or SnapKV-D eviction. So "eviction does not inflate length" holds only for some eviction policies.
2. **QuaRot-style Hadamard INT2 is either near-lossless or a total collapse.**
   - KVarN reports QuaRot 2/2 (2.3 bits) at 56.7 AIME24 on Qwen3-4B, against FP16 61.1 [2606.03458, Table 1].
   - OSCAR reports QuaRot-INT2 (2.25 BPE) at a mean drop of -74.24 on Qwen3-4B-Thinking-2507, with AIME25 at 0.00 [2605.17757, Table 2].

   The checkpoints (Qwen3-4B vs the 2507 Thinking variant) and benchmarks (AIME24 vs AIME25) differ. Group sizes, BF16 windows and kernels also differ, and neither paper explains the gap.
3. **How strong is TurboQuant?**
   - Its own paper reports near-lossless results at 2.5-3.5 bits on LongBench [2504.19874, Table 1].
   - In decode-time reasoning it falls below 2-bit KIVI even at 4.6 bits [2606.03458, Table 1].
   - With mixed precision disabled it collapses at 3.25 BPE [2605.17757, Table 2].
   - Yet TQ-style 4-bit with boundary-layer protection stays within 2 points of BF16 [2606.20474, Section 6.3].

   This supports KVarN's claim that prefill-style evaluation does not transfer to decoding. It also shows that boundary-layer protection (first and last 2 layers in BF16) changes the ranking.
4. **Does any serving framework support 2-bit KV?** KVarN says public serving frameworks do not support 2-bit KV [2606.03458, Appendix E]. OSCAR describes a production SGLang INT2 path [2605.17757, Section 4] but states no code. In public code the claim is still unsettled.
5. **How sensitive is a quantized tier?** Not All Thoughts Need HBM reports that an 8-bit compressed tier drops accuracy from 58% to 20% [2605.09490, Sections 3.2, 6]. PM-KVQ, KVarN and OSCAR report near-lossless results at 2-4 bits [2505.18610; 2606.03458; 2605.17757]. The 8-bit collapse is most likely an implementation artifact, but this is not checked (unverified).
6. **Precision versus token count.** ThinKV allocates precision by thought type [2510.01290]. Spend Bytes on Breadth finds that at fixed bytes, more tokens at lower precision usually wins [2610.05685]. MultiAlloc finds that adaptive per-layer splits beat any fixed split [2610.18642]. No paper reconciles where the precision-count frontier lies.

## Open problems

### OP1 — Decode-time error accumulation shows up as longer reasoning, and no method targets length
- **Setting.** KV quantization during long-CoT generation of 8K-32K tokens, judged by cost per solved problem rather than accuracy alone.
- **Magnitude.** Pure KV quantization inflates R1-Llama-8B output length by up to 5.1x. ThinKV's thought-adaptive quantization alone keeps accuracy (77.8) but gains only 1.1x throughput for this reason [2510.01290, Section 6.3, Table 4]. KVQuant-1% raises Qwen3-4B MATH500 output from 3857 to 5021 tokens (+30%) and AIME24 output from 12,477 to 14,794 tokens [2606.03458, Table 1]. Low eviction budgets cause non-terminating loops [2512.12008, Section 4.7].
- **Closest baselines and why they fall short.**
  - KVarN reduces token-scale error so that token counts stay near FP16 at 2.3 bits [2606.03458]. It is uniform 2-bit, tested only up to 14B, and never optimizes or bounds length.
  - ThinKV regularizes length by adding eviction [2510.01290], but the effect is a heuristic side effect.
  - No baseline treats expected generated length as an objective or measures it under matched memory with length included.
- **Type.** Methodological. Evaluation must report tokens and wall-clock per solved problem.

### OP2 — Local or offline proxies do not predict the end-to-end best allocation
- **Setting.** Choosing bit widths, token counts and rotations per layer or head for long decoding.
- **Magnitude.** Offline distortion curves at equal bytes pick the wrong bit width on 2 of 3 models (Qwen3-8B prefers 4 bits offline and 2 bits end to end). Neither offline attention error nor an online per-head probe finds the right width [2610.05685, Sections 1, 5.3]. In a 28-layer sweep, no single layer's pollution alone loses accuracy, so per-step bounds are conservative [2607.28699, Sections 6.4.1, 6.4.6]. OSCAR's optimality holds only under a frozen-error surrogate [2605.17757, Appendix D].
- **Closest baselines and why they fall short.**
  - KVTuner, PM-KVQ and MultiAlloc search allocations offline, statically and on calibration data [2502.04420; 2505.18610; 2610.18642]. MultiAlloc names its calibration dependence as a limitation.
  - KVarN's pseudo-decode protocol is a better proxy [2606.03458], but it is used for diagnosis, not for allocation.
- **Type.** Methodological: an accumulation-aware proxy or a cheap online signal that ranks allocations correctly end to end.

### OP3 — Baseline strength depends on unreported protocol details
- **Setting.** Comparing 2-4 bit decode-time KV quantizers on reasoning benchmarks.
- **Magnitude.** The same family of method swings from near-lossless to collapse across papers:
  - QuaRot-INT2: 56.7 AIME24 [2606.03458] vs 0.00 AIME25 [2605.17757].
  - TurboQuant: near-lossless [2504.19874], 48.9 at 4.6 bits [2606.03458], -43.90 mean drop with mixed precision disabled [2605.17757], within 2 points with boundary layers in BF16 [2606.20474].

  The protocol knobs behind these swings are boundary-layer BF16 protection [2606.20474, Section 6; 2606.03458, Appendix D], sink/recent BF16 windows (OSCAR 64/256 [2605.17757]; QuantMLA 4/128 [2609.36760]) and metadata in the bit count.
- **Closest baselines and why they fall short.** KVarN and OSCAR each define a careful protocol, but they disagree. No shared harness or bit-accounting standard exists for decode-time KV quantization.
- **Type.** Engineering and evaluation. The root cause of the QuaRot gap is unverified.

### OP4 — Architecture-native compressed caches are not covered by post-training KV quantizers
- **Setting.** MLA latents, natively FP4-QAT caches with cross-layer sharing, and the FP8 SWA caches of the newest open models.
- **Magnitude.** DeepSeek-V4.1-Flash already stores global KV in FP4 via QAT and shares it across layers (890 B/token). It keeps SWA KV at FP8 "due to its sensitivity" [2609.19969, Section 2.4.4]. In V4, SWA KV was "nearly half of the persistent KV cache capacity" [Section 3.2.1]. In MLA, the RoPE path's output response per unit cache error is 1.9-6.9x the content path's [2609.36760, Section 2.2].
- **Closest baselines and why they fall short.**
  - QuantMLA and RAQ-MLA reach INT4, INT2-content or about 2.5 bits, but only on older MLA models without native low-bit KV [2609.36760; 2610.33625].
  - PM-KVQ, KVarN and DMS each list MLA as out of scope [2505.18610, Appendix E; 2606.03458, Appendix E; 2506.05345, Appendix A].
  - None quantizes the SWA cache or goes below an already-QAT FP4 cache.
- **Type.** Methodological, plus engineering: the target is a 552B model, and native MLA kernels are required.
- **Grounding caveat.** The newcomer-feasibility of running V4.1-Flash on 8xH200 is unverified.

### OP5 — Low-bit tiers with recovery or offload lack a cheap, sound trigger at the bit widths that matter
- **Setting.** A hierarchy that keeps a low-bit HBM copy, an exact host or SSD copy, and permanent eviction, applied during long decoding.
- **Magnitude.**
  - Adding an INT2 tier cuts the discarded future attention mass from 64.8% to 35.7% [2608.05326, Section 3].
  - Even 3% permanent eviction leaves only 33% of full accuracy on MATH Level-5 [2605.09490, Section 6].
  - Sound certificates are 1289x loose at 4 bits and vacuous at 1-2 bits [2607.28699, Section 4.1].
  - Lossless coding tops out at about 1.32x on BF16 and 1.14x on FP8 [2605.01708].
  - DeepSeek's production design accepts approximate replay instead of exact recovery [2609.19969, Section 3.2.2].
- **Closest baselines and why they fall short.**
  - QEvict's promotions are driven by cumulative attention. It falls back to SDPA to expose attention probabilities, and quantized-to-evicted is permanent [2608.05326, Sections 4-5].
  - WitCert's certify-fallback works only around 8 bits [2607.28699].
  - Not All Thoughts Need HBM keeps full copies in DDR, so the total footprint does not shrink [2605.09490].
- **Type.** Methodological (a trigger signal) plus engineering (prefetch and kernel work).

## Recommended baseline set

A 2027 paper on KV compression for long reasoning should compare against the following, at matched bytes that include scales, BF16 windows and protected layers. It should report accuracy, generated tokens and throughput.

1. **FP8 KV (native vLLM/SGLang)** as the deployment floor. UltraQuant shows 4-bit gains over it only once memory binds [2606.20474]. Add the KIVI-2 anchor (not read this run; used as a baseline in every paper here).
2. **KVarN [2606.03458]**: the strongest public, calibration-free 2-bit decode-time quantizer, with vLLM code and long-CoT results.
3. **OSCAR [2605.17757]**: the strongest calibrated-rotation INT2 with a serving path. No code is stated, so reimplementation risk must be flagged. Use **TurboQuant [2504.19874]** through the vLLM community PR as the rotation/codebook anchor, with and without boundary-layer protection, because results flip on this.
4. **PM-KVQ [2505.18610]**: the long-CoT mixed-precision reference, with an ICLR 2026 paper and public code.
5. **ThinKV [2510.01290]**: the strongest hybrid of quantization and eviction for reasoning (ICLR 2026 oral). Required if the paper mixes precision with token count. No code is stated.
6. **R-KV [2505.24133]** and **DMS [2506.05345]**: the training-free and learned token-eviction references for reasoning. Required when byte budgets are below about 2 bits per element equivalent, where eviction competes.
7. **For MLA or native-low-bit models: QuantMLA [2609.36760]** (or RAQ-MLA [2610.33625]), plus the DeepSeek-V4.1-Flash native FP4 KV [2609.19969] as the "already compressed" reference point.
8. **For transfer or offload papers only: SplitZip [2605.01708]** as the lossless ceiling.

Week-1 runnable with stated public code: PM-KVQ, R-KV, KVarN, SplitZip, and TurboQuant through the vLLM PR. OSCAR, ThinKV, DMS and QuantMLA need reimplementation or are code-unknown.

## Search log
Run with `lit.py search` (arXiv):
- `--since 2026-05-01`: "KV cache quantization"; "KV cache quantization reasoning"; "2-bit KV cache"; "rotation KV cache quantization"
- `--since 2026-05-01`: "vector quantization KV cache"; "FP4 KV cache"; "lossless KV cache compression"; "KV cache compression reasoning models"; "KV cache offloading quantization"; "MLA latent cache quantization"
- `--since 2025-01-01`: "TurboQuant"; "KIVI tuning-free asymmetric 2bit" (0 hits); "CommVQ commutative vector quantization KV"; "KV cache quantization long chain-of-thought"; "quantized KV cache error accumulation decoding"; "KV cache compression benchmark reasoning"
- `--since 2026-05-01`: "quantization eviction hybrid KV reasoning" (0 hits); "KV cache quantization-aware training"; "generation length inflation quantization reasoning"

Biblio checked but not read (cannot be cited): MixKVQ, SPECTRA, OScaR, OptR (output-aware INT2 rotation), JoLT, Quantization Inflates Reasoning, InfoKV, Answer-Evidence gap (EMNLP Findings 2026). These are candidates for a second pass.

Total: 19 queries.
