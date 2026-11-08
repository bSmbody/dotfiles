# Mechanism-level ideas for efficient long-reasoning inference, in the style of SwarmEvolve

## Problem definition
Reasoning LLMs (e.g., Qwen3-8B thinking) generate 10K-60K-token chains of thought per problem. Serving them is bounded by the KV cache (memory capacity limits batch size; reading KV bounds per-step latency). We want NEW MECHANISMS that improve accuracy-per-GPU-second (cost per correct answer at memory saturation) for long-reasoning inference, within the directions: (L1) low-bit KV and precision control, (L2) parallel reasoning / test-time scaling and its KV cost, (L3) KV eviction / pruning / sparse reading, (L4) hybrid models and recurrent memory states (memory matrix), (L5) variant attention algorithms at decode time.

Inspiration to emulate (see papers/2611.08483.md): SwarmEvolve innovated by (1) finding a primitive whose cost profile changed (latent reasoning + KV-cache passing), (2) pushing it to an extreme scale nobody tried (hundreds of agents per round on one GPU), (3) turning free by-products into mechanisms (hidden states as a free diversity metric; KV concatenation as idea crossover), and (4) choosing a setting with an exact evaluator and measuring time-to-quality. We want ideas with this flavour: a concrete mechanism, enabled by a cheap primitive or a free by-product, that changes what is affordable.

## Challenge
- Low-bit (2-bit) KV saves ~3x memory, but on some models it makes a subset of requests run away (loops, hitting the length cap): Qwen3-8B AIME25 cap-hit 11% (BF16) -> 42% (OSCAR INT2) [2609.38121]. Cost per request at memory saturation scales ~ bits x L^2, so runaways dominate cost.
- KV is a deterministic function of the token ids: re-prefilling the generated prefix at higher precision restores exact KV state in <1 s for 16K tokens, but already-sampled bad tokens cannot be undone [2606.02011 is the weight-quant analogue that must restart from scratch].
- Parallel sampling (self-consistency, best-of-N) multiplies KV memory and branches never exchange information until a final vote.
- Eviction scoring is unreliable on reasoning (random eviction matches SnapKV/R-KV [2609.03430]); permanent deletion is what hurts [2605.09490].
- Hybrid models (GDN + few full-attention layers): recurrent states are small (~7-17% of request memory at bf16 [2610.36950]) and retrieval relies on attention layers [2608.30386]; states cannot be merged/branched/shared like KV caches (SwarmEvolve's stated limitation [2611.08483]).

## Constraints
Target: NeurIPS/ICLR/MLSys-level method paper. Compute: 8x H200 (~1 TB HBM), training-free or light training preferred; open models (Qwen3 4B-32B, Qwen3.5 hybrids, GPT-OSS-20B). Must be implementable in vLLM/SGLang or HF within ~3 months by one PhD student with AI coding help. Evaluation on AIME/HMMT/LiveCodeBench/GPQA with a cost-per-correct-answer metric.
