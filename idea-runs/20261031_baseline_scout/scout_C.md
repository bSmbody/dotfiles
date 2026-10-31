# Scout C: Decoding acceleration for long reasoning generations

Scope covered: speculative decoding (SD) for long chain-of-thought (CoT), including trained drafters (EAGLE-3, DFlash), MTP heads as shipped, self-speculation with sparse or quantized drafts, and long-context SD. Also parallel / multi-path decoding, and reasoning-length efficiency at inference (early exit, termination budgets). The focus throughout is on how each method interacts with KV-cache cost at 16K-128K. Literature runs through 2026-10-31. Every id cited below has a digest in `papers/`.

## Baseline table

| Baseline [id] | Date (v1) | Venue | Code (as stated in the paper) | Models / generation lengths evaluated | Headline measured result | How the gain changes with generation length / batch | Weak point |
|---|---|---|---|---|---|---|---|
| EAGLE-3 [2503.01840] | 2025-03-03 | not stated in arXiv metadata | https://github.com/SafeAILab/EAGLE | Vicuna-13B, LLaMA-3.1-8B, LLaMA-3.3-70B, DeepSeek-R1-Distill-LLaMA-8B. Short benchmarks (MT-bench, HumanEval, GSM8K, Alpaca, CNN/DM); no long-CoT length stated | bs=1: 3.0x-6.5x over AR; DSL-8B mean 4.16x, GSM8K 5.01x (tau 6.93) (Section 4.1, Table 1) | Falls with batch. SGLang H100: 1.81x at bs=2, 1.38x at bs=64. vLLM: 1.75x at bs=2, 1.01x at bs=56 (Sections 4.3-4.4, Tables 3, 5). At long input (8-32K prefix, bs=1) it gets only 0.92x-1.06x on LLaMA-3.1-8B and 0.44x-0.52x on 70B [2608.30252, Table 1]. In long CoT on vLLM it reaches 1.64x-1.80x on Qwen3-8B-Thinking at medium batch [2601.11580, Section 3.2] | A drafter must be trained per target. The one-layer head lacks capacity for long histories [2608.30252, Section 3.2]. No limitations section |
| DFlash [2602.06036] | 2026-02-05 | ICML 2026 | stated (https://dflash.z-lab.ai; arXiv comment: github.com/z-lab/dflash) | Qwen3-4B/8B, Qwen3-Coder-30B-A3B, LLaMA-3.1-8B, Qwen3.5-9B/27B, gpt-oss-20B/120B. Thinking off: max 2048 tokens. Thinking on: GPQA, MATH-500, AIME25 | Thinking off: avg 4.9x over AR, 2.4x over EAGLE-3 (Section 5.1). Thinking on, Qwen3-8B: 4.17x-4.64x at T=0, 3.70x-4.03x at T=1 (Section 5.2, Table 2) | SGLang B200, Qwen3-8B Math500: 5.1x at c=1, 2.8x at c=32 (Table 3). vLLM, Qwen3.5-9B: 4.0x at c=1, 1.9x at c=32 (App A.4, Table 12). Context: base drafter tau on gov_report falls 4.53 → 2.67 → 2.09 at 1K / 16K / 32K; long-context fine-tuning recovers it to 3.81 / 3.56 (Section 5.4, Table 4) | Trained at ≤3-4K (App A.1) and degrades past 4K without adaptation. Draft KV of injected target features grows with context; its memory and latency at 32K+ are not measured. Only EAGLE-3 is compared |
| DeepSeek-V3 MTP [2412.19437] | 2024-12-27 | tech report | weights: https://github.com/deepseek-ai/DeepSeek-V3 | DeepSeek-V3 (671B/37B MoE). MTP depth D=1 | 2nd-token acceptance 85-90%, giving 1.8x TPS (Section 5.4.3) | No breakdown by batch or length. In decode deployment, per-expert batch ≤256 and the bottleneck is memory access (Section 3.4.2) | Only one extra token. A single released MTP module reused autoregressively loses acceptance by depth (0.92 → 0.68 → 0.38 for GLM-4.5-Air) [2601.11580, Section 3.2] |
| MagicDec [2408.11049] | 2024-08-20 | not stated in arXiv metadata | not stated in the paper | LLaMA-3.1-8B/70B, LLaMA-2-7B-32K, Qwen2.5-7B/32B, Mistral-7B. PG-19 prompts up to 32K-100K, but only 96 generated tokens (Section 5.1) | Up to 2.51x for LLaMA-3.1-8B at large batch on 8xH100 (Section 1, Section 5) | Gain grows with batch once the sequence passes a critical length (~4K on 8xA100). Below that, SD loses at large batch (Section 5.1, Fig 6). Small-draft + compressed KV beats self-spec unless both batch and length are large (Section 5.3) | Not evaluated on long generations. StreamingLLM draft accuracy is low. SnapKV draft fixes selection at prefill, which is "poorly suited to ... long-generation reasoning workloads" [2609.17943, Section 5.1] |
| QuantSpec [2502.10424] | 2025-02-05 | not stated | not stated | LLaMA-2-7B-32K-Instruct, LWM-Text-Chat-128k. 4K-128K prompts, 90 output tokens, bs=1 (Section 5.1) | 1.61x-2.08x at 8K-32K, up to 2.49x at 128K. INT4 attention kernel 2.88x vs FP16 FA (Section 5.2, Tables 3-4) | Gain grows with context (KV quantization dominates at long context, Fig 4). Batch >1 not measured | Verifier uses an INT8 KV, so output is lossless only relative to INT8, not FP16 (Section 4.2). Not tested on long generation, reasoning models or batching |
| Vegas [2602.07223] | 2026-02-06 | ICML 2026 | https://github.com/platformxlab/vegas | Qwen3-4B/8B, Qwen3-30B-A3B-Thinking, gpt-oss-20b. AIME25/CodeElo with ~19.7K avg output at max batch 128; LongBench-v2 96-120K input (Section 5) | 1.25x-2.70x decode throughput over vLLM on long-CoT; 1.15x-1.23x over MagicDec-Stream; +18-29% over best baseline at 96-120K (Sections 5.2-5.3) | Gain grows with context. It needs batch ≥8 on AIME25 to help at all (bs=1 suffices at LongBench-v2) (App F). Smaller gains on gpt-oss: only half its layers are dense, so the draft step is only reduced to 48% (Section 5.2) | Throughput-only; not useful for latency at small batch (App F). Sparse KV selection is fixed during drafting ("stale") [2609.17943, Section 1]. Full KV kept, so memory capacity is unchanged |
| ASPIRE [2609.17943] | 2026-09-16 | COLM 2026 | not stated | Qwen3-1.7B/8B, DS-R1-Distill-LLaMA-8B. AIME25/CodeElo (avg gen ~13.6-14.7K, max batch that fits: B=30-42), LongBench 16-18K, LongBench-v2 30-40K / 80-100K (Section 5.1, App C.1) | 1.70x-4.58x over AR. ~27% average gain over strongest prior self-spec (Vegas). Qwen3-8B: 1.86x on AIME25, 2.75x at 80-100K (Section 5.2) | Grows with context: Qwen3-8B 1.81x → 2.30x → 2.75x from 16K to 80-100K. Fixed synchronized drafting falls behind as context grows (Section 5.3) | A simple FSM controller gets within ~0.1-0.2x of the full scheduler (Section 5.3). Compared only against self-spec baselines. Batch is capped by full-KV memory |
| Dustin [2606.24957] | 2026-06-23 | ICML 2026 | not stated | Qwen2.5-72B, Llama-3.3-70B with small same-family drafts. PG-19 8K-32K at batch 8/16; LongBench accuracy (Section 5.1) | 9.17x end-to-end decode on Qwen2.5-72B at 32K, batch 16; 27.85x self-attention (Sections 5.3.1-5.3.2) | Advantage grows with both batch and context: 4.76x → 9.17x at batch 16 from 8K to 32K (Section 5.3.2). Verification is 87.5% of step latency at 32K, batch 16 (Section 1) | Verification is sparse, hence lossy ("near-lossless"). The mix parameter is static. It "does not reduce the KV-cache memory footprint" (Section 6, App L). Long CoT not evaluated |
| DTSR (early exit) [2604.06787] | 2026-04-08 | ACL 2026 Main | not stated | Qwen3-8B/14B/32B. GSM8K, MATH-500, AMC23, OlympiadBench, GPQA-D, LCB. Max generation 16K (Section 3.1) | Length cut 28.9%-34.9% at "almost the same" accuracy; >50% on LCB. Latency MATH-500 3.1 s → 1.9 s; AMC 8.3 s → 6.2 s (Sections 3.2, 4.2) | Benefit depends on serving: DEER shortens outputs yet raises latency (2.6K tokens, 4.2 s vs vanilla 3.1 s) because its synchronous checks break continuous batching (Section 4.2) | Each check re-prompts the model over the full CoT; that prefill and KV cost is not quantified. Up to 32B only; text only (Limitations). The oracle frontier is far above current methods [2610.13570] |
| Multiverse (parallel decoding) [2506.09991] | 2025-06-11 | not stated | https://github.com/Multiverse4FM/Multiverse | Multiverse-32B (Qwen2.5-32B SFT on 1K examples). AIME24/25, MATH500, GPQA-D at 32K (Section 6) | Accuracy on par with an AR-32B on the same data (AIME24 53.8 vs 54.6; AIME25 45.8 vs 45.0). Parallelism degree only 1.15-1.18 (Table 2) | Avg 18.5% speedup at parallelism 1.0-1.3, up to 2.1x for highly parallel samples (8-32K gen, bs=1). At a fixed 4K output, speedup scales with parallelism from bs=1 to 128 (Section 7) | Low realized parallelism; SFT only, RL future work (Section 9). Total KV not reduced: branches add KV and the merged sequence keeps it all |

Supporting evidence, read this run but not proposed as baselines:
- [2601.11580]: vLLM benchmark of n-gram, EAGLE, EAGLE-3, draft-model and MTP drafting up to 32K outputs.
- [2610.30644]: full-length measurement of acceptance against position.
- [2608.30252] MASW: a strong independent draft with compressed draft KV. Up to 2.08x on 8B and 3.33x on 70B at 8-32K prefixes, bs=1.
- [2608.20359] SSR: drafts the answer from partial-CoT prefixes. Up to 24.1% lower latency, but only the answer phase is accelerated.
- [2610.13570]: oracle termination frontiers (OTBench).
- [2608.01651] Bole: tree SD on Gated-DeltaNet hybrids using Qwen3.5 native MTP drafters. 2.74x geo-mean over SGLang-AR.

## Stated limitations

Authors' own limitations:
- **EAGLE-3 [2503.01840]**: no limitations section. The authors explain that speedup decays with batch because SD "leverag[es] redundant computational power. As batch sizes increase, this redundancy decreases" [full text, Section 4.3]. Models of 405B and up were untested [Section 4].
- **DFlash [2602.06036]**: no limitations section. The base drafter "degrades as context length grows beyond 4K" until it is fine-tuned [Section 5.4]. Speedup roughly halves from concurrency 1 to 32 in both SGLang and vLLM [Table 3, Table 12].
- **MagicDec [2408.11049]**: "only focuses on decoding performance"; prefill is left open; gains are larger on high-end GPUs [Section 6].
- **QuantSpec [2502.10424]**: no limitations section. Combining with sparse KV is left to future work [Section 2.3].
- **Vegas [2602.07223]**: "only delivers significant benefits when the context is sufficiently long"; "for latency-oriented scenarios (i.e., small batch sizes), Vegas may not provide enough benefits, but all sparse attention-based self-speculative decoding methods suffer similarly" [App F].
- **Dustin [2606.24957]**: the offline-profiled budget mix leaves a gap to an oracle. It "does not inherently expand the maximum supportable context length constrained by GPU memory capacity" [App L].
- **MASW [2608.30252]**: adaptor trained on only 2B tokens at 8K; fixed window and slot interval; the self-speculative variant is untested [Limitations].
- **SSR [2608.20359]**: "when reasoning dominates generation time, gains are limited since CoT generation is not accelerated" [Section 6].
- **DTSR [2604.06787]**: models up to 32B, text only [Limitations].
- **Termination frontiers [2610.13570]**: the frontiers are offline oracles, not deployable policies, and their cost metric counts tokens, not deployment overhead [App E].
- **Acceptance diagnostic [2610.30644]**: thin support beyond 8-12K; independent drafts only. Running EAGLE-3/PARD/DFlash under the same full-length protocol is "the single most important extension" [Section 8].
- **Multiverse [2506.09991]**: SFT only; RL to encourage parallelism is future work [Section 9].

Cross-paper contradictions and tensions:
1. **Batch scaling has opposite signs for the two SD families.** Trained-drafter SD loses gain with batch:
   - EAGLE-3: 1.81x → 1.38x at bs=64 in SGLang, 1.75x → 1.01x at bs=56 in vLLM [2503.01840].
   - EAGLE: 1.73x → 1.21x from bs=1 to 128; k=21 trees fall below 1x at bs=64 [2601.11580].
   - DFlash: 5.1x → 2.8x at c=32 [2602.06036].

   Sparse self-speculation gains with batch once context is long:
   - MagicDec: gain grows with batch beyond ~4K [2408.11049].
   - Vegas: needs batch ≥8 to help on AIME25 [2602.07223].
   - Dustin: 4.76x → 9.17x from 8K to 32K at batch 16 [2606.24957].

   The two families have never been compared head-to-head in the same engine on 16K+ generated CoT at saturated batch. ASPIRE and Vegas compare only self-spec methods; DFlash compares only against EAGLE-3.
2. **Does acceptance decay with length?** Three readings disagree:
   - Trained drafters lose acceptance at long input: DFlash tau 4.53 → 2.09 at 32K [2602.06036]; EAGLE-3 near 1x at 8-32K prefixes [2608.30252].
   - On long generated CoT, EAGLE-3 accepted length grows with position, from ~2.1-2.5 (<4K outputs) to ~2.5-5.7 (>13K outputs) [2601.11580].
   - Independent drafts show no positional decay through 12K [2610.30644].

   The reconciling hypothesis is a training-length mismatch plus the difference between long input and long generation. [2610.30644] states this hypothesis but does not test it with a trained drafter.
3. **"Lossless" is not uniform.**
   - QuantSpec verifies on INT8 KV, not FP16 [2502.10424].
   - Dustin verifies sparsely [2606.24957].
   - vLLM outputs differ across batch sizes even without SD [2601.11580].

   Speedups from these papers are therefore not all measured at the same output distribution.
4. **Fewer tokens is not lower latency.** DEER cuts output length yet raises latency under its synchronous implementation [2604.06787]. The 64.3% overthinking headroom is counted in tokens only [2610.13570].
5. **KV capacity, not compute, bounds long-CoT batch for every lossless SD method read.**
   - [2601.11580] restricted reasoning runs to medium batch "to avoid preemption once the KV cache becomes full".
   - ASPIRE runs at "the largest [batch] that fits in GPU memory" [2609.17943].
   - Dustin keeps the full KV [2606.24957].

## Open problems

**P1. Lossless SD that also cuts KV memory capacity for long-CoT serving.** Methodological plus engineering.
- **Setting:** long CoT (≥16K generated) at saturated batch on one GPU.
- **Magnitude:**
  - Every self-spec method here keeps the full FP16/BF16 KV, so batch is bounded by capacity: B=30 for Qwen3-8B on AIME25 at ~13.7K tokens [2609.17943, App C.1]; Vegas runs at max batch 128, "enough to saturate the available KV cache capacity" [2602.07223, Section 5.2].
  - [2601.11580] had to cap reasoning batch to avoid preemption.
  - Dustin states that its 9.17x does not shrink the footprint [2606.24957, App L].
- **Closest baselines and why they fall short:**
  - QuantSpec [2502.10424] shrinks the resident KV (INT8 target, INT4 draft by bit-sharing), but only at bs=1 and 90 output tokens, and its verifier is INT8, not FP16.
  - KV eviction for reasoning (R-KV [2505.24133], DMS [2506.05345]) saves memory but gives up exact output equivalence.
  - No paper read measures the tokens/s-per-GPU frontier when the extra memory freed by a compressed-yet-verified cache is spent on a larger batch during long CoT.
- **Open:** a draft/verify design whose verifier reads a compressed cache, with an exactness or bounded-error guarantee, evaluated at memory-saturated batch on 16-64K CoT.

**P2. Length-robust trained drafters, and the draft-side KV cost, for 16K-128K generation.** Methodological.
- **Magnitude:**
  - DFlash tau drops 54% from 1K to 32K without adaptation [2602.06036, Table 4].
  - EAGLE-3 gives 0.92x-1.06x at 8-32K prefixes on LLaMA-3.1-8B and 0.44x-0.52x on 70B [2608.30252, Table 1].
  - Yet independent drafts show no decay through 12K [2610.30644, Section 4], and EAGLE-3 acceptance rises with position in long CoT [2601.11580, Section 6].
- **Closest baselines and why they fall short:**
  - DFlash's long-context fine-tune was evaluated on long inputs only, up to 32K.
  - MASW [2608.30252] compresses draft KV, but only for long input at bs=1 with an 8K-trained adaptor.
  - None measures acceptance and draft KV memory over 32K-128K generated CoT.
- **Status:** the decay mechanism (training length vs position) is unverified. [2610.30644] names the trained-drafter run as its main missing experiment.

**P3. SD tuned for long CoT at large batch: choosing and combining drafter and verifier sparsity.** Mostly engineering, with a methodological cost-model component.
- **Magnitude:**
  - Trained-drafter gains roughly halve by concurrency 32 [2602.06036, Tables 3, 12].
  - Tree drafting falls below 1x at bs=64 [2601.11580, Section 3.2].
  - Verification takes 42-95% of runtime [2601.11580, Section 5.1] and 87.5% at 32K, batch 16 [2606.24957, Section 1].
  - Sparse self-spec reaches only 1.25x-2.70x on long CoT [2602.07223] and 1.70x-2.12x on short-input reasoning [2609.17943].
- **Closest baselines and why they fall short:**
  - ASPIRE and Vegas use the full model as drafter; DFlash and EAGLE-3 verify on the full KV; Dustin's sparse verifier is lossy and was tested on 8-32K inputs with short outputs.
  - None combines a strong parallel drafter (DFlash-style) with a cheap or compressed exact verifier.
  - [2601.11580] oracle analysis: adaptive proposal length reaches 2.75x vs 2.1x fixed, and the gap widens with batch [Section 8.1].
- **Open:** whether these gains compose additively. Unverified.

**P4. Using SD's own signals to decide when to stop reasoning, with costs measured in KV and latency, not tokens.** Methodological.
- **Magnitude:** 64.3% of thinking tokens come after the accuracy peak, and full thinking costs 9.03 points. Public routing, budget and early-exit methods all sit below their oracle frontiers [2610.13570, Section 1, Section 5.2].
- **Evidence for the link:**
  - DTSR shows that optimal exit points are followed by reflection cues ("Wait", "But let me check") and uses those cues to trigger a separate, costly sufficiency prompt [2604.06787, Section 2.2].
  - Independently, SD rejections concentrate on the same reflection-trigger tokens (reflection acceptance 0.747 vs ≥0.93 for numbers and operators) [2610.30644, Section 6].
- **Closest baselines and why they fall short:**
  - DTSR pays an extra prefill over the full CoT per check, and its benefit depends on the scheduler [2604.06787, Section 4.2].
  - SSR [2608.20359] drafts from partial CoTs but accelerates only the answer phase.
- **Open:** a termination signal derived from verification statistics at zero extra forward cost. Whether such a signal predicts sufficiency is unverified.

**P5. Drafting and verification for shipped hybrid / sparse-attention models with MTP heads.** Engineering plus methodological.
- **Magnitude:**
  - On gpt-oss-20b (half its layers windowed), sparse drafting reduces a draft step only to 48% of vanilla, so self-spec gains shrink [2602.07223, Section 5.2].
  - On GDN hybrids, per-node state snapshots cost 36-72 GiB at B=8-16 [2608.01651, Section II-C].
  - Shipped MTP is depth 1 in DeepSeek-V3 [2412.19437, Section 4.2]. Reusing a single MTP module drops acceptance 0.92 → 0.68 → 0.38 [2601.11580, Section 3.2].
- **Closest baselines and why they fall short:** Bole [2608.01651] fixes verification state cost (2.74x geo-mean), but it keeps the native MTP drafter and does not evaluate long-CoT generation length.
- **Open:** acceptance-improving drafting that is aware of the recurrent state, measured on 16K+ CoT. Unverified for long CoT.

## Recommended baseline set

Minimal comparison set for a 2027 paper on decoding acceleration for long reasoning. Every method runs in one engine (vLLM or SGLang), with continuous batching, on 16K-32K+ generated CoT (AIME25 / GPQA-D / LCB), sweeping batch from 1 to memory saturation:

1. **AR decoding in the same engine.** All speedups are relative to this. Report throughput, not per-request latency, because outputs vary across batch sizes [2601.11580].
2. **EAGLE-3 [2503.01840], with the draft trained on reasoning traces.** It is the de-facto production SD and has public code. Its long-CoT numbers already exist as a reference (1.64x-1.80x [2601.11580]).
3. **DFlash [2602.06036].** It is the strongest trained drafter as of ICML 2026, with public code and models. Reviewers will expect it, and its own data shows weaknesses in context length and concurrency that a new method can target.
4. **n-gram / prompt lookup.** A training-free baseline that is competitive on long CoT (1.50x-1.58x) and whose acceptance grows with position [2601.11580]. It costs nothing to include.
5. **Native MTP when the model ships it** (DeepSeek [2412.19437]; Qwen3.5 as used in [2608.01651]). This is the deployment default for shipped models.
6. **Vegas [2602.07223], plus MagicDec-StreamingLLM [2408.11049] as its standard weaker baseline.** Lossless sparse self-spec with public Vegas code, run in vLLM on long CoT at batch 128. ASPIRE [2609.17943] is the newer stronger point (COLM 2026) but states no code. Cite its numbers, and reimplement it only if code appears.
7. **If the method touches the verifier or KV precision:** QuantSpec [2502.10424], for quantized self-spec (no code stated, so a reimplementation cost applies); and Dustin [2606.24957] as a lossy sparse-verification upper reference (no code stated).
8. **If the method changes reasoning length:** DTSR [2604.06787] plus a fixed thinking budget, scored against OTBench oracle frontiers [2610.13570]. Report wall-clock and KV, not only tokens.

Week-1 feasibility for a newcomer: AR, n-gram, EAGLE-3 (via SGLang/vLLM), DFlash and Vegas have code, so they are runnable. MTP needs only a model that ships it. QuantSpec, ASPIRE and Dustin require reimplementation, which is kernel work, a cost to flag.

## Search log

All searches used `$LIT search` against arXiv; WebSearch was not used.
- "speculative decoding long reasoning" (10) | "EAGLE-3 speculative decoding" (10) | "self-speculative decoding sparse KV long context" (7) | "speculative decoding long chain-of-thought" (10). No date filter.
- --since 2026-05-01: "speculative decoding" (10) | "multi-token prediction inference" (10) | "reasoning length early exit thinking" (3) | "adaptive thinking budget" (10) | "speculative decoding batch size throughput" (10) | "parallel reasoning decoding" (10).
- --since 2026-04-01: "speculative decoding long context KV cache" (10) | "speculative decoding reasoning model" (10) | "EAGLE draft long context" (3) | "multi-token prediction speculative" (10) | "thinking early exit reasoning model" (9) | "chain-of-thought compression inference" (10).
- Title lookups: "EAGLE-3: Scaling up Inference Acceleration" | "MagicDec" | "TriForce speculative decoding" | "DeepSeek-V3 technical report" | "Dynamic Early Exit in Reasoning Models" (0 hits) | "Multiverse parallel generation".
- --since 2026-05-01: "speculative decoding large batch serving" (8) | "draft model sparse attention reasoning" (2) | "parallel thinking reasoning efficiency" (7) | "overthinking efficient reasoning inference" (6).
- No date filter: "speculative decoding hybrid linear attention" (5) | "Dynamic Early Exit reasoning DEER" (2) | "ThinkPrune" (2).
- Read this run (full text, digests appended): 2503.01840, 2408.11049, 2502.10424, 2602.07223, 2602.06036, 2601.11580, 2608.20359, 2412.19437, 2610.30644, 2609.17943, 2608.30252, 2604.06787, 2610.13570, 2506.09991, 2606.24957, 2608.01651. Reused existing digests: 2505.24133, 2506.05345.
- Seen in results but not read, so not cited: SpecExtend, LongSpec, SpecPV, S3R, Cassandra, TreeWY, ReaDy, SpecForge, Multi-Token Prediction Done Right, BitMTP, OS-Pruner, HybridThinker, CAT, and others.
