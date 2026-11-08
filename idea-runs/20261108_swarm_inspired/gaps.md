# Gaps (compiled by orchestrator from earlier runs' gap_finder outputs and digests already in papers/)

## Axis L1: low-bit KV precision control for long CoT
### Gap L1-1: precision is decided once, at write time, and cannot be recovered cheaply
- What has been done: write-time token/head/layer mixed precision (KVarN [2606.03458], TaSQ [2610.03027], OSCAR [2605.17757], ThinKV [2510.01290]); promotion only with a stored FP16 copy in CPU (Runtime-Certified [2605.20868]); read-time progressive precision over an 8-bit store (ReadKV [2610.11245]).
- Failure: at 2 bits a minority of requests run away (loops / cap hits) and dominate cost [2609.38121]; the only cheap remedies are full-request upgrade (3.2x memory) or restart [2606.02011].
- Why it matters: cost per correct answer at memory saturation.

## Axis L2: parallel reasoning / test-time scaling and its KV cost
### Gap L2-1: parallel branches are memory-expensive and exchange no information until the final vote
- What has been done: independent sampling + voting; branches that share a prefix KV through paging; latent multi-agent communication by KV concatenation in program search (SwarmEvolve [2611.08483]).
- Failure: N branches cost N x KV memory at full precision; branches cannot reuse each other's partial progress; a long-CoT branch that runs away still consumes its full budget.
- Why it matters: test-time scaling is the main accuracy lever for reasoning models; its KV cost limits how many branches fit.

## Axis L3: KV eviction / pruning / sparse reading in long CoT
### Gap L3-1: importance scores are unreliable and deletion is irreversible
- What has been done: attention-score eviction (SnapKV/H2O/R-KV family); random eviction matches them on reasoning [2609.03430]; accuracy tracks permanently deleted fraction, so offloading beats deleting [2605.09490]; heads change what they read during generation [2610.02713].
- Failure: a token judged unimportant early is gone when a later step needs it; selection signals are noisy.

## Axis L4: hybrid models and recurrent memory states (memory matrix)
### Gap L4-1: recurrent states cannot be branched, merged or shared like KV caches
- What has been done: hybrids keep a few full-attention layers; states are a small share of memory [2610.36950]; zeroing all linear-layer states barely changes NIAH, so retrieval lives in attention KV [2608.30386]; SwarmEvolve cannot run on hybrids because several agents' fixed-size states cannot be merged [2611.08483].
- Failure: KV-level tricks that rely on concatenating or forking caches (latent communication, branch merging, prefix sharing with edits) do not transfer to hybrid models.

## Axis L5: variant attention algorithms at decode time
### Gap L5-1: efficient-attention designs target prefill/encoders, not the long-output decode regime
- What has been done: fast-weight view of attention with compress+route experts (MiTA [2602.01219], vision/LRA only, non-causal); KV quantization changes per-step read cost but not the attention algorithm.
- Failure: in long CoT the query changes every step and the context grows every step; per-step selection or compression must be cheap and stable over tens of thousands of steps.
