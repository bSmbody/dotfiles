# Scout B — efficient attention structures in released open-weight models, and their inference-side problems

Scope: structures that ship in 2025-2026 open-weight models (sparse attention with a learned indexer, compressed attention, latent attention, hybrid linear + full attention, sliding-window hybrids, gated attention), plus post-hoc conversion of dense checkpoints into them. Focus on decode at 32K-128K generated or cached tokens. Every [id] below has a digest in `papers/`. Numbers marked **(derived)** are my own arithmetic from configs stated in the cited paper, not numbers the paper reports.

## Structure / baseline table

| # | Structure [id] | Date | Released models that use it (as stated in read papers) | Code / weights (only if stated) | Inference cost profile: what grows with length, with numbers | Serving support stated | Known weak point |
|---|---|---|---|---|---|---|---|
| 1 | **DSA, DeepSeek Sparse Attention** (lightning indexer + token-level top-k over the MLA latent cache, MQA mode) [2512.02556] | 2025-12 (V3.2-Exp Sep 2025) | DeepSeek-V3.2 / -Exp / -Speciale [2512.02556]; GLM-5 [2603.12201]; GLM-5.1 (DSA, k=2048) [2608.07009]; "DSA and its variants": DeepSeek-V4, GLM-5.2, MiniMax-M3, LongCat-2.0 [2610.09025]; LongCat-2.0 built on DSA [2608.01662] | Inference code on HF for V3.2-Exp [2512.02556, Section 2.1] | Core attention O(Lk), k=2048; the **indexer stays O(L) per decoded token** ("still has a complexity of O(L^2)") and the full MLA latent cache stays resident [2512.02556, Section 2.3]. Measured on a 30B DSA model: indexer is "the bottleneck at long sequences" in decode; removing 75% of indexers gives 58->86 tok/s at 200K (1.48x) [2603.12201, Section 4.2]; this implies the indexer takes at least ~43% of decode time at 200K **(derived)** from 1/(1-0.75f)=1.48. KV bill: a 128K GLM-5.1 request holds 13.09 GB BF16 KV [2608.07009, Section 1]. | SGLang (IndexCache experiments [2603.12201]; HiSparse merged upstream [2608.07009]) | Indexer scan per token per layer; KV is never reduced; indexer reaches only ~60% precision against exact top-k [2512.03494, Section 3]; token efficiency: longer trajectories than Gemini-3.0-Pro [2512.02556, Section 5] |
| 2 | **CSA + HCA** (DeepSeek-V4: 4x learned compression + lightning-indexer top-k; 128x compression with dense attention; 128-token SWA branch; attention sink) [2606.19348] | 2026-04 | DeepSeek-V4-Pro (1.6T/49B), DeepSeek-V4-Flash (284B/13B) [2606.19348] | Inference code on HF for V4-Pro [2606.19348, Section 2.3] | At 1M: V4-Pro 27% FLOPs / 10% KV of V3.2, V4-Flash 10% / 7%; ~2% KV of BF16 GQA8 [2606.19348, Sections 1, 2.3.4]. Per decoded token the CSA indexer scans n/4 compressed keys with 64 heads x 128 dims, HCA attends densely to n/128 entries, CSA core attention is fixed at top-k (512 Flash, 1024 Pro) + 128 window [Section 4.2.1]. **(derived)** For V4-Flash at 128K per CSA layer: indexer 32,768 x 64 x 128 = 268M MACs vs core (512+128) x 512 x 64 x 2 = 42M MACs; indexer FLOPs exceed core attention past ~20K tokens (~74K for Pro); FP4 indexer keys at 128K are ~2 MiB/layer read per token vs ~0.3 MiB of FP8 main KV. Measured: at 507K cached context, cutting 50% of indexer blocks gives +14.9% TPS [2610.09025, Table 6], so the indexer is at least ~26% of decode time there **(derived)**. | vLLM (SPIN [2610.09025], MLIPS [2610.27438]); SGLang (HiSparse [2608.07009]) | Indexer stays linear; heterogeneous KV "violates fundamental assumptions behind PagedAttention"; SWA KV is ~8x the compressed KV on disk [2606.19348, Section 3.5] |
| 3 | **CSA2** (cross-layer sharing of main KV + indexer K with Full / Reindex / Reuse modes, Hierarchical Sparse Indexer, FP4 main KV, causal encoder-decoder) [2609.19969] | 2026-09 | DeepSeek-V4.1-Flash (552B; 8B active prefill / 16B decode) [2609.19969] | Not stated | Global KV 890 B/token (~1/4 of V4-Flash), persistent KV ~1/8 with SWA Bounded Replay [2609.19969, Abstract, Section 6]. Decode FLOPs grow only 1/4 from 4K to 1M [Section 1, Figure 2]. Remaining linear term stated by the authors: "the first Full Mode layer still scans the entire causally visible range" [Section 2.3.2]. | Not stated | Approximate SWA state reconstruction and CSA2 selection errors "may still cause capability degradation in untested boundary cases" [Section 6] |
| 4 | **NSA** (compressed + selected blocks + sliding window, GQA-group-shared selection) [2502.11089] | 2025-02 | None stated in NSA itself; HiSparse lists NSA among served families [2608.07009] | Triton kernel described; alt kernel FSA [2508.18224] | Per step loads floor((s-l)/d) compressed tokens + n*l' selected + w window [2502.11089, Section 5.2]; compressed term grows with s/d; full KV kept. "11.6x decode speedup at 64K" is an analytic memory-volume estimate (Table 4), not a measured latency [Section 5.2]. | SGLang via HiSparse [2608.07009] | Selection scored only through the compression branch; per-head selection disallowed for GQA; no measured end-to-end decode |
| 5 | **MoBA** (mean-pooled block gate, top-k blocks + own block) [2502.13189] | 2025-02 | "Deployed to support Kimi's long-context requests" [2502.13189, Abstract] | github.com/MoonshotAI/MoBA [2502.13189] | Gate cost N/B dot products per query, k*B tokens attended; full KV kept. Up to 6.5x attention prefill at 1M, 16x at 10M [Section 3.4]. **All evaluations use MoBA for prefill only and switch to full attention for generation** [Section 3.3]. | Not stated | Sparse decode untested; MoBA-only training worse on trailing tokens; SFT needs last layers full [Section 3.2] |
| 6 | **MSA, MiniMax Sparse Attention** (per-GQA-group block indexer with one shared index key head, top-16 x 128-token blocks + forced local block) [2606.13392] | 2026-06 | Research 109B MoE in the paper; MiniMax-M3 listed as a DSA-variant / block-indexed production model by [2610.09025] and [2610.27438] | Not stated | F_MSA = H_kv d_idx N^2 (index) + 4 H_q d_h N k B_k (main) [2606.13392, Eq 12]: index branch O(N) per decoded token, main fixed at 2,048 tokens. At 1M: 28.4x fewer attention FLOPs but measured 14.2x prefill / 7.6x decode [Sections 1, 5.4]. | Custom kernels described (exp-free top-k, KV-outer sparse attention) | Gap between FLOP and wall-clock reduction from index/top-k/gather overheads [Section 5.4]; "residual long-context retrieval gap" [Section 7] |
| 7 | **KDA hybrid** (Kimi Delta Attention, per-channel decay, 3 KDA : 1 MLA with NoPE) [2510.26692]; shipped at 2.8T in Kimi K3 (3:1 KDA : Gated MLA) [2607.24653] | 2025-10 / 2026-07 | Kimi-Linear-48B-A3B [2510.26692]; Kimi K3 [2607.24653] | fla KDA kernels, vLLM implementation, HF checkpoints [2510.26692] | State 128x128 per head per KDA layer, fixed; KV only in 1/4 of layers (up to 75% KV saving) [2510.26692, Abstract, Section 6.3]. Decode "approaches a maximum hybrid efficiency ratio of 3:1", measured 2.3x at 1M batch 1; the 6.3x headline is from larger batches ("theoretical") [Section 6.3, Figure 1b]. | vLLM [2510.26692]; DeltaLog vLLM path [2608.15533]; K3 KDA-aware paged prefix cache [2607.24653, Section 5.4.1] | MLA layers bound long-context decode; prefix caching only at sparse state checkpoints (block size forced to 1024-6144 tokens) and spec-decode rollback [2607.24653, Sections 5.4.1-5.4.2] |
| 8 | **Gated DeltaNet hybrid** (GDN : full-attention layers) [2412.06464] | 2024-12; shipped 2025-2026 | Qwen3-Next [2608.30386]; Qwen3.5-2B/4B/9B/27B/122B-A10B [2610.36950, 2609.33477, 2608.01651]; Qwen3.6-27B, 35B-A3B [2608.30310, 2608.15533]; OLMo-Hybrid-7B [2608.30310] | Not stated in GDN paper | Qwen3.5-4B: one state checkpoint ~49 MiB vs ~32 KiB KV per token [2609.33477, Section 1]; Qwen3.5-2B: 12,288 B/token BF16 KV (1.5 GiB at 128K) vs 9.84 MiB state [2610.36950]. **(derived)** At 32K the attention KV is ~20x the state in Qwen3.5-4B, ~80x at 128K. Recurrent-state read+write is 25.2-44.6% of decode latency at 1K context, B=64-256 (Qwen3.6-35B-A3B) [2608.15533, Section 2.3]. Tree spec-decode snapshots: 36 GiB at B=8, T=32 (Qwen3.5-122B-A10B) [2608.01651, Section II-C]. | SGLang (SuffixReplay [2609.33477], DASC [2608.30386], Bole [2608.01651]); vLLM (DeltaLog [2608.15533], GateSight [2610.14754]) | Recall: 1.3B GDN S-NIAH-2 100 -> 29.6 from 1K to 8K [2412.06464, Section 3.2]; GDN-H falls behind MLA on long context at 48B [2510.26692, Section 5.5.1]; zeroing states collapses RULER 0.987 -> 0.299 [2608.30310, Table 1] |
| 9 | **Lightning-attention hybrid** (7 lightning-attention : 1 softmax) [2506.13585]; 7 Lightning : 1 MLA retrofit [2606.15079] | 2025-06 / 2026-06 | MiniMax-M1-40k/-80k (456B/45.9B) [2506.13585]; Ling-2.5/2.6, Ring-2.5/2.6 (up to 1T) [2606.15079] | M1 on GitHub/HF [2506.13585]; linghe fused-kernel library [2606.15079] | M1 needs <50% of DeepSeek-R1's FLOPs at 64K generation and ~25% at 100K (theoretical FLOPs) [2506.13585, Section 1]. Softmax/MLA KV in 1 of 8 layers still grows linearly. Ling: beyond 32K attention dominates over MoE; at 256K+ full attention is "the absolute performance bottleneck" [2606.15079, Section 2.1.3]. | vLLM and Transformers [2506.13585] | Train/inference precision mismatch blocked RL reward growth (fixed by FP32 LM head) [2506.13585, Section 3.2]; pattern collapse in long generation [Section 5] |
| 10 | **Sliding-window : global hybrids** (banded 128-token window alternating with dense in gpt-oss; 5:1 local:global in Gemma 3/4) [2508.10925, 2503.19786, 2607.02770] | 2025-03 to 2026-07 | gpt-oss-20b/120b [2508.10925]; Gemma 3 1B-27B [2503.19786]; Gemma 4 2.3B-31B [2607.02770] | Open weights (model cards) | gpt-oss: GQA 8 KV heads x 64 dims in half the layers; **(derived)** ~36 KiB/token BF16 for 120b (18 dense layers), ~4.5 GiB per sequence at 128K [2508.10925, Section 2.2]. Gemma 3: KV overhead 60% (global-only) -> <15% (1:3, sw=1024) at 32K [2503.19786, Section 5.2]. Gemma 4: K=V and p-RoPE on global layers cut global KV by 37.5% [2607.02770, Section 2]. | Not stated | Global layers' KV grows linearly; Gemma 3 ratio/window ablations are perplexity-only and quality "rapidly degrade[s]" past 128K [2503.19786, Section 5.3] |
| 11 | **Gated attention** (head-specific sigmoid gate on SDPA output) [2505.06708] | 2025-05 | Output gates in Kimi Linear KDA/MLA [2510.26692, Section 4] and K3 Gated MLA [2607.24653, Section 2.1.2] | Code and models released [2505.06708, Abstract] | No KV change; <2% latency [2505.06708, Section 3.1]. First-token attention 46.7% -> 4.8% [Figure 2]. | Not stated | Not tested with KV eviction or quantization, whose sink handling it changes |
| 12 | **MLA and post-hoc conversion** of dense checkpoints: MHA2MLA [2502.14837], MLAfication [2610.17202], GQA -> Lightning + MLA retrofit [2606.15079]; dense -> hybrid: HALO [2601.22156], KL-guided selection [2512.20569], Opal [2609.31947] | 2025-02 to 2026-10 | Ling/Ring 2.6 is a released converted model [2606.15079]; MLA layers in DeepSeek V3.x/V4 and Kimi | MLAfication: up to 5.35x serving throughput vs BF16 GQA [2610.17202] | MLA: one latent per token shared across heads (MQA mode for decode) [2512.02556, Appendix A]. Opal 1:3 hybrid: ~4x lower cache+state memory at 128K, ~2x throughput [2609.31947, Section 4.3]. | vLLM for Opal efficiency tests [2609.31947] | QK-Norm blocks MLA weight absorption [2606.15079, Section 2.1.3]; training-free MLA conversion drops LongBench 27.40 -> 1.34 [2610.17202, Section 3.6]; converted hybrid reasoning gap AIME'24 73.8 -> 52.5 [2609.31947, Table 2] |

## Stated limitations

Limitations the authors themselves state:

- **DSA** [2512.02556]: the indexer "still has a complexity of O(L^2)" [Section 2.3]; "token efficiency remains a challenge; DeepSeek-V3.2 typically requires longer generation trajectories" [Section 5]. The paper reports no ablation of k or of indexer size.
- **DeepSeek-V4** [2606.19348]: the architecture is "relatively complex" [Section 6]. Hybrid KV violates PagedAttention assumptions, and on-disk SWA caching is write-heavy and a poor match for SSDs [Section 3.5]. They plan "low-latency architectures and system techniques" [Section 6].
- **DeepSeek-V4.1-Flash** [2609.19969]: the remaining Full-mode indexer is "a major computational bottleneck" for extremely long contexts [Section 2.3.2]. Bounded replay gives states that "are not mathematically identical across positions" [Section 3.2.2]. "Potential selection errors in CSA2 and approximate state reconstruction in SWA Bounded Replay may still cause capability degradation in untested boundary cases" [Section 6].
- **NSA** [2502.11089]: no limitations section. It frames earlier methods' failures as phase-restricted sparsity and GQA incompatibility [Section 2.1].
- **MoBA** [2502.13189]: trailing-token loss is higher without a switch to full attention, SFT is suboptimal under loss masking, and future work covers "complex reasoning tasks" [Sections 3.2, 5]. All results decode with full attention [Section 3.3].
- **MSA** [2606.13392]: runtime speedup is below the FLOP reduction because of index construction, top-k, reverse-index, gather and load-balancing overheads [Section 5.4]. A residual long-context retrieval gap remains [Section 7].
- **Kimi Linear** [2510.26692]: "Long-context retrieval remains the primary bottleneck for pure linear attention" [Section 4]. A 7:1 ratio gives "significantly worse validation performance" [Section 5.2].
- **Kimi K3** [2607.24653]: with block-hash prefix caching at the forced coarse block size, "caching is nearly useless". Per-draft state snapshots "would multiply state traffic — a cost that dominates at the large batch sizes" [Sections 5.4.1, 5.4.2].
- **GDN** [2412.06464]: memory collision versus fast decay is a trade-off, and recall degrades by 8K at 1.3B [Section 3.2].
- **MiniMax-M1** [2506.13585]: kernel precision mismatch, optimizer sensitivity, and pattern collapse at long output [Sections 3.2, 5].
- **Ling 2.6** [2606.15079]: reasoning depth is constrained in the flash model, long-horizon robustness is weak, and KV-cache management is future work [Section 5].
- **Gemma 3** [2503.19786]: degrades rapidly beyond 128K [Section 5.3].
- **Gated attention** [2505.06708]: the effect of non-linearity "remain[s] under-explored", and there is no theory of sinks and length generalization [Limitations].
- **Serving-side papers**:
  - HiSparse: 7-8 ms/token TPOT from exposed IO; host DRAM on GB200/GB300 is no larger than HBM [2608.07009, Section 5].
  - SPIN: history-based prediction misses "sudden attention shifts", and skipped blocks create "self-reinforcing prediction errors" [2610.09025, Section 6].
  - IndexCache: at 1/8 indexer retention Long Avg drops 50.2 -> 46.1 even with search [2603.12201, Section 4.3].
  - DeltaLog: no gain at small batch or small state [2608.15533, Section 6].
  - SuffixReplay: needs decaying states, and its budget is model dependent (OLMo 91.4% RULER) [2609.33477].
  - Attention Amnesia: CoT-SFT damages recall in distilled hybrids [2606.11052].

Cross-paper contradictions and tensions:

1. **Attention sinks: added versus removed.** gpt-oss [2508.10925, Section 2.2] and DeepSeek-V4 [2606.19348, Section 2.3.3] add learned sink logits to the softmax denominator. Gated attention [2505.06708, Section 4.3] removes the sink with an output gate (46.7% -> 4.8% first-token attention), and Kimi Linear/K3 adopt such gates [2510.26692, 2607.24653]. Sink-based eviction or quantization rules (keep the first tokens) therefore do not transfer across these families. No read paper tests this.
2. **Hybrid ratio.** Kimi Linear finds 3:1 best and 7:1 "significantly worse" in validation [2510.26692, Section 5.2]. Ling 2.6's equal-FLOP scaling law picks 7:1 and says more linear layers are fine at larger budgets [2606.15079, Section 2.1.2]. MiniMax-M1 ships 7:1 [2506.13585]. A from-scratch study finds 1:3 ≈ 1:1 at scale [2606.15378, Section 6.1]. The settings differ (attention type, scale, metric), so the right ratio for long generation is unresolved.
3. **Fixed windows versus dynamic selection.** MSA finds a FLOP-matched sink+window baseline has worse agent perplexity than dynamic selection [2606.13392, Appendix B.6]. SWARR finds pure SWA (8K window) matches full attention on math after on-policy RL [2606.11634, Section 4.3]. The two disagree on whether long-range access is needed, which depends on the task (agent retrieval vs math CoT).
4. **How harmful selection misses are.** The Lightning Indexer reaches only ~60% precision but end-to-end parity holds [2512.03494, Section 3]. SPIN's p99 top-K miss of 48.83% costs 1.24 RULER points [2610.09025, Table 3]. Yet IndexCache's 1/8 sharing loses 4 points on Long Avg [2603.12201], and V4.1 names selection errors as a remaining risk [2609.19969, Section 6]. No paper relates miss rate to downstream loss on long generation.
5. **Speed claims inside Kimi Linear.** "6x faster than full attention" at 1M [2510.26692, Section 5.6] versus a measured 2.3x at batch 1 and 6.3x "theoretical" [Section 6.3].
6. **Naming.** HiSparse labels DeepSeek-V4-Flash's attention "NSA" [2608.07009, Figure 4], while the V4 report calls it CSA (DSA over 4x-compressed entries) [2606.19348]. Baselines must be named precisely.
7. **Is the NSA decode gain measured?** NSA's 11.6x decode figure is a memory-volume estimate [2502.11089, Table 4]. MSA's measured decode gain is 3.7x smaller than its FLOP reduction [2606.13392, Section 5.4]. Sparse-attention decode claims based on FLOPs or access volume overstate wall-clock gains.

## Open problems

**OP1. The indexer scan is the last O(L)-per-token term in DSA-family decode, and shipped fixes still keep one full scan.**
- *Setting*: DSA / CSA / CSA2 models (DeepSeek-V3.2, V4, V4.1-Flash, GLM-5.x) generating or holding 128K-1M tokens.
- *Measured magnitude*:
  - The indexer is the decode bottleneck at long contexts: IndexCache 1.48x at 200K from dropping 75% of indexers, i.e. at least ~43% of decode time **(derived)** [2603.12201, Section 4.2].
  - On V4 at 512K-1M the indexer is "a major contributor" to ITL [2610.09025, Section 1]; 50% block skipping gives +14.9% TPS [Table 6].
  - From V4-Flash's config, indexer FLOPs and bytes are ~6x core attention per CSA layer at 128K **(derived)** [2606.19348, Section 4.2.1].
  - MSA's index branch keeps its decode gain at 7.6x vs 28.4x FLOPs [2606.13392, Section 5.4].
- *Closest baselines and why they fall short*:
  - IndexCache (cross-layer reuse) still scans in the retained layers and breaks at 1/8 [2603.12201].
  - MLIPS / Prism (pools from a producer layer): pool coverage decays with position (0.90 -> 0.66 from <200K to 500K-1M) [2610.27438, Section 3; 2610.22985].
  - SPIN (history prediction): only 30-50% block sparsity, self-reinforcing misses [2610.09025, Section 6].
  - V4.1-Flash already ships hierarchical pools and cross-layer reuse, but "the first Full Mode layer still scans the entire causally visible range" [2609.19969, Section 2.3.2].
  - None removes the one full scan per token, and none is evaluated on 32K+ *generated* reasoning traces as opposed to long prompts.
- *Type*: methodological (a sublinear selector with miss guarantees, or temporal reuse across decode steps) plus engineering (kernels).
- *Risk*: crowded. V4.1 has absorbed the layer-dimension ideas, so a paper here must attack the temporal dimension or the first scan.

**OP2. Sparse attention cuts KV reads but not KV residency. For long generations the capacity wall, not compute, sets throughput.**
- *Setting*: DSA/CSA serving at 32K-128K per request with high concurrency.
- *Measured magnitude*:
  - A 128K GLM-5.1 request holds 13.09 GB KV; 8xH200 saturates at ~60 requests at 32K/8K and ~15 at 128K [2608.07009, Sections 1, 2.2].
  - Sparse attention "did not drop [the memory bill] by a byte" [2608.07009, Section 1].
  - DSA keeps the full MLA cache [2512.02556, Section 2.3].
- *Closest baselines and why they fall short*:
  - HiSparse is exact offload with LRU (87% hit at 2x top-k), but costs 7-8 ms/token TPOT (3 ms with prefetch). It needs host DRAM much larger than HBM, which GB200/GB300 lack [2608.07009, Section 5].
  - V4.1-Flash reduces bytes per token with FP4 and cross-layer sharing (890 B/token) but keeps everything resident [2609.19969].
  - Eviction is unsafe because selections drift (staging only the current top-k misses 30% next step) [2608.07009, Section 1].
  - No read paper evicts or tiers generated-token KV with knowledge of the indexer's future demand while bounding the miss cost on long CoT.
- *Type*: methodological (indexer-aware eviction or prefetch with guarantees) plus engineering.

**OP3. Hybrid linear + full models: the recurrent state breaks per-token cache primitives, so prefix caching, speculative decoding and resumption rely on approximate replay or coarse checkpoints.**
- *Setting*: GDN/KDA/SWA hybrids (Qwen3.5/3.6, Kimi K3, DeepSeek-V4 SWA branch) in agentic multi-turn serving with long cached prefixes.
- *Measured magnitude*:
  - State checkpoint ~49 MiB vs ~32 KiB per KV token [2609.33477, Section 1].
  - Zeroing states drops RULER 0.987 -> 0.299; replay of 5-10% recovers 92.8-98.9% [2608.30310, Table 1]. OLMo-Hybrid keeps only 91.4% on RULER under SuffixReplay [2609.33477].
  - K3's state checkpoints force 1024-6144-token blocks [2607.24653, Section 5.4.1].
  - V4 SWA KV is ~8x the compressed KV on disk [2606.19348, Section 3.5.2]. V4.1's Bounded Replay is approximate, and "SWA state reconstruction at cache-resumption boundaries" is a named untested risk [2609.19969, Sections 3.2.2, 6].
  - Tree speculation snapshots take 36-72 GiB [2608.01651, Section II-C]; K3 calls per-draft snapshots traffic-dominant [2607.24653, Section 5.4.2].
- *Closest baselines and why they fall short*:
  - Tail-Replay / SuffixReplay: approximate, need decaying states, model-dependent budgets.
  - DASC: static masks, only 1.10-2.49x on head-wise GDN [2608.30386].
  - Bole and K3's input-replay kernel solve spec-decode rollback exactly but only at short generations [2608.01651].
  - No read paper gives an exactness or error bound for approximate replay over long generated continuations, and none evaluates quality drift after resumption on 32K+ reasoning.
- *Type*: methodological (error-bounded state reconstruction) plus engineering.

**OP4. Long chain-of-thought generation is the least-tested regime for these structures and for post-hoc conversions into them, and where it is tested the losses are large.**
- *Setting*: reasoning models (AIME-class, 16K-64K generated tokens) built on sparse, hybrid or SWA structures, especially conversions from dense checkpoints.
- *Measured magnitude*:
  - Opal's 9/36-layer converted Qwen3-4B hybrid: AIME'24 73.8 -> 52.5, AIME'25 63.7 -> 40.4 [2609.31947, Table 2].
  - CoT-SFT cuts distilled-hybrid NIAH at 256K from 67.2 to 9.4 (HypeNet-9B) [2606.11052, Section 6.2].
  - Training-free MLA conversion drops LongBench 27.40 -> 1.34 [2610.17202, Section 3.6].
  - GDN-H falls behind MLA on long context [2510.26692, Section 5.5.1].
  - MoBA never decodes sparsely [2502.13189, Section 3.3]. Gemma 3's ratio choice rests on perplexity only [2503.19786, Section 5.2].
  - KL-guided selection's long-context evaluation is mostly <10K tokens, and NIAH at 128K drops 0.954 -> 0.684 [2512.20569].
- *Closest baselines and why they fall short*:
  - Opal (on-policy distillation) still leaves a 21-23 pp AIME gap.
  - QK-Restore recovers only part of the loss (22.4 -> 45.0 vs 67.2 before SFT) [2606.11052].
  - SWARR covers pure SWA on math at 1.5B-4B only [2606.11634].
  - LISA reports reasoning gains at 1.5B with a 23.9% latency cut at 16K only [2607.19358].
  - Layer-selection methods (HALO, KL-LS, Jet-Nemotron) score with teacher-forced or short-task signals [2601.22156, 2512.20569, 2508.15884].
- *Type*: methodological.

**OP5. The residual full-attention layers of hybrids dominate memory at 32K-128K, and no read method compresses their KV during long decoding.**
- *Setting*: GDN/KDA hybrids with 1/4 or 1/8 full-attention layers generating long outputs.
- *Measured magnitude*:
  - Kimi Linear decode is bounded by the 3:1 ratio, i.e. by the MLA layers, at long length [2510.26692, Section 6.3].
  - Qwen3.5-2B attention KV is 1.5 GiB at 128K vs a 9.84 MiB state [2610.36950].
  - Opal serves its 9 retained layers with uncompressed caches [2609.31947].
- *Closest baselines and why they fall short*:
  - HeadWiseKV is static, prompt-independent and saves only 8.59% peak [2609.02029].
  - GateSight evicts once after prefill, with "no decode-time eviction" [2610.14754].
  - Oracle-guided sparse prefill gives "no decode-side ... KV-storage reduction" [2606.07703, Section 10].
  - DCKV compresses once after prefill and restores the full cache before decoding [2610.36950].
  - All treat the recurrent path as fixed, and GateSight's signals show the two memories partly duplicate each other [2610.14754, Section 3.2].
- *Type*: methodological. Overlaps scout A (KV compression), so check with A's table.

Unverified (not grounded in two read papers): whether DSA-family indexer keys themselves (FP4, a few hundred bytes per token [2608.07009, Section 3.2]) become the HBM limit at multi-million-token contexts once main KV is offloaded. Only one read paper gives the per-token figure.

## Optimizable structure

Dominant inference cost at 32K-128K generation, per structure:

- **DSA (V3.2, GLM-5.x)**: the lightning-indexer scan per token per layer, with the resident full MLA cache as the capacity term. Evidence: at least ~43% of decode time at 200K **(derived)** and an explicit "bottleneck" statement [2603.12201, Section 4.2]; 13.09 GB/request at 128K for GLM-5.1 [2608.07009].
- **CSA+HCA (V4)**: the CSA indexer (64 heads x 128 dims over n/4 keys). It exceeds core attention FLOPs beyond ~20K tokens on Flash and ~74K on Pro **(derived)** [2606.19348, Section 4.2.1]. It was the authors' own FP4 target [Section 5.2.1], and SPIN measures it as a major ITL term [2610.09025]. HCA's n/128 dense term is secondary.
- **CSA2 (V4.1-Flash)**: the single Full-mode indexer scan, plus resident global KV of 890 B/token [2609.19969, Sections 2.3.2, 6].
- **NSA**: the compressed-token term, (s-l)/d tokens per step [2502.11089, Section 5.2]. Selected and window tokens are fixed.
- **MoBA**: as evaluated, full-attention KV reads, because decode is dense [2502.13189, Section 3.3]. With sparse decode it would be the N/B gate plus k*B tokens.
- **MSA**: the index branch (H_kv d_idx N) plus selection/gather overheads; the decode gain is 7.6x vs 28.4x FLOPs [2606.13392, Section 5.4].
- **KDA hybrid (Kimi Linear, K3)**: KV reads of the 1-in-4 MLA layers. Decode speedup is capped at ~3:1 [2510.26692, Section 6.3]. At large batch the state traffic is also first-order [2607.24653, Section 5.4.2; 2608.15533].
- **GDN hybrid (Qwen3.5/3.6)**: full-attention KV at 32K+ (~20-80x the state **(derived)**) [2609.33477, 2610.36950]. At short context and large batch, recurrent-state read/write (25-45% of decode) dominates instead [2608.15533, Section 2.3]. Under speculative decoding, state snapshots dominate [2608.01651].
- **Lightning hybrid (M1, Ling 2.6)**: KV of the 1-in-8 softmax/MLA layers; at 256K+ full attention is "the absolute performance bottleneck" [2606.15079, Section 2.1.3].
- **SWA hybrids (gpt-oss, Gemma 3/4)**: KV of the dense/global layers. For gpt-oss-120b, ~4.5 GiB per sequence at 128K **(derived)** [2508.10925]. Window layers are fixed-size [2503.19786, 2607.02770].
- **Gated attention**: no new cost; it changes sink structure and thus the assumptions of eviction and quantization [2505.06708].
- **MLA conversions**: latent KV reads; the quality term, i.e. long-context fidelity, is the binding constraint, not cost [2610.17202, 2606.15079].

## Recommended baseline set

A minimal set a 2027 reviewer would accept for an inference-side paper on these structures, chosen to be runnable on 8xH200 by a newcomer:

1. **One DSA-family model + its dense twin.** DeepSeek-V3.2 vs DeepSeek-V3.1-Terminus is a clean pair: DSA is "the only architectural modification" [2512.02556, Section 2.1]. Add DeepSeek-V4-Flash (284B/13B active, vLLM/SGLang support) [2606.19348, 2610.09025, 2608.07009]. Method baselines on top: IndexCache [2603.12201], SPIN [2610.09025], MLIPS [2610.27438] for indexer cost; HiSparse [2608.07009] for KV residency. V4.1-Flash's CSA2 [2609.19969] must be discussed as the shipped state of the art even if its weights are not usable.
2. **One GDN hybrid family across sizes.** Qwen3.5 (2B-27B) / Qwen3.6 is the de-facto testbed of the read serving papers [2609.33477, 2608.30310, 2608.15533, 2608.01651, 2610.36950]. Serving baselines: SGLang native state checkpointing, Tail-Replay [2608.30310], SuffixReplay [2609.33477], DASC [2608.30386], DeltaLog [2608.15533], Bole [2608.01651].
3. **One KDA hybrid.** Kimi-Linear-48B-A3B has open weights, fla kernels and vLLM support, with an MLA/GDN-H comparison in the paper [2510.26692]. Cite K3 [2607.24653] for the production serving design (state-aware prefix cache, replay-based MTP).
4. **One SWA hybrid.** gpt-oss-20b/120b [2508.10925] or Gemma 3/4 [2503.19786, 2607.02770], to show the method is not specific to linear or sparse layers.
5. **A conversion baseline if the paper converts.** MLAfication [2610.17202] for MLA; Opal [2609.31947] (on-policy) and HALO [2601.22156] / KL-LS [2512.20569] (off-policy selection) for hybrids. MSA claims "near-lossless conversion from pretrained GQA" [2606.13392].
6. **Evaluation must include long generation.** AIME-class reasoning at 32K+ output in addition to RULER/LongBench prefill tasks. Report measured TPOT/throughput, not FLOPs or memory-volume estimates (contradiction 7 above). Many read papers evaluate prefill-only or short output [2502.13189, 2606.07703, 2610.14754, 2608.01651].

Lighter alternatives (a lightning hybrid such as MiniMax-M1 [2506.13585], NSA [2502.11089], MoBA [2502.13189]) are reference points for related work rather than required baselines: NSA has no released production model in the read papers, and MoBA decodes densely in its own evaluation.

## Search log

All via `$LIT search` (arXiv) unless noted; no WebSearch used.

| # | Query | --since | Hits | Used |
|---|---|---|---|---|
| 1 | DeepSeek sparse attention lightning indexer | — | 6 | 2608.01662, 2607.19358, 2603.12201, 2512.03494 |
| 2 | Kimi Linear delta attention | — | 8 | 2510.26692 |
| 3 | MiniMax lightning attention hybrid | — | 1 | 2506.13585 |
| 4 | multi-head latent attention inference | — | 8 | 2502.14837 (existing digest) |
| 5 | DeepSeek-V3.2 | — | 8 | none directly (id from biblio) |
| 6 | DeepSeek-V4 | — | 8 | 2606.19348, 2609.19969 |
| 7 | Qwen3-Next gated deltanet hybrid | — | 3 | none |
| 8 | gated attention sigmoid output gate attention sink | — | 3 | 2505.06708 |
| 9 | MoBA mixture of block attention | — | 0 | — (id 2502.13189 confirmed via `biblio`) |
| 10 | sliding window attention hybrid gpt-oss | — | 0 | — |
| 11 | DeepSeek-V3.2 sparse attention DSA | — | 0 | — (2512.02556 confirmed via `biblio`) |
| 12 | Mixture of Block Attention long context | — | 0 | — |
| 13 | gpt-oss model card | — | 3 | 2508.10925 |
| 14 | Gemma 3 technical report | — | 6 | 2503.19786, 2607.02770 |
| 15 | Qwen3.5 | — | 6 | none (no Qwen3.5 / Qwen3-Next architecture report found on arXiv) |
| 16 | Kimi K2 | — | 6 | 2607.24653 |
| 17 | sparse attention indexer decoding cost | 2026-05-01 | 8 | 2610.09025, 2608.07009, 2606.13392 |
| 18 | hybrid linear attention serving | 2026-05-01 | 8 | 2608.30310, 2608.30386, 2608.01651, 2610.14754 |
| 19 | MLA KV cache long context serving | 2026-05-01 | 4 | 2610.17202 |
| 20 | conversion dense to sparse attention DSA | 2026-05-01 | 0 | — |
| 21 | Qwen3-Next | — | 6 | none |
| 22 | Qwen3.5 technical report | — | 6 | none |
| 23 | local global attention interleaved KV cache | — | 2 | none |
| 24 | sliding window attention hybrid long reasoning | 2026-05-01 | 2 | none |
| 25 | linear attention decoding memory bound state | 2026-05-01 | 5 | 2608.15533, 2608.01651 |
| 26 | distill transformer into hybrid linear attention | 2026-05-01 | 0 | — |
| 27 | sparse attention long decoding reasoning | 2026-05-01 | 8 | 2606.13392 |
| 28 | hybrid linear attention long chain-of-thought reasoning | 2026-05-01 | 3 | 2606.11052, 2606.15079 |
| 29 | indexer KV cache offload sparse attention | 2026-05-01 | 1 | none |
| 30 | Kimi delta attention inference state | 2026-05-01 | 4 | 2608.30386 (existing digest) |

New digests written this run (body read via `$LIT fulltext`): 2512.02556, 2606.19348, 2609.19969, 2502.13189, 2510.26692, 2607.24653, 2506.13585, 2606.15079, 2505.06708, 2508.10925, 2503.19786, 2607.02770, 2603.12201, 2608.07009, 2610.09025, 2608.15533, 2608.01651, 2606.11052. Digests extended with inference-cost goals: 2502.11089, 2606.13392. Reused existing digests: 2412.06464, 2512.03494, 2610.27438, 2610.22985, 2607.19358, 2608.01662, 2610.17202, 2502.14837, 2601.22156, 2512.20569, 2508.15884, 2609.31947, 2606.11634, 2606.15378, 2608.30310, 2609.33477, 2608.30386, 2610.36950, 2609.02029, 2610.14754, 2606.07703, 2508.18224. Qwen3-Next / Qwen3.5 architecture is known here only through the serving papers that use those checkpoints; Qwen3-Coder-Next [not digested] gives no architecture detail.
