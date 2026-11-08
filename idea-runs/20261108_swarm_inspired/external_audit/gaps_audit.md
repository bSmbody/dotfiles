# Gap audit — inference-mechanism candidates C4, C6–C10

Cutoff 2026-11-08. Vault (14,616) has good coverage of this domain; prior run
2026-10-31 (context/serving/rl evidence) reused. Digests in `papers/`; depth labeled
per source (mostly annotation/abstract level).

## Axis KV-quantization error structure (C6)

**Near-misses:** SDQ-LLM [web:sdqllm] already transfers sigma-delta/noise-shaping to
1-bit LLM quantization (weight domain). GPTQ/GPTAQ family does intra-block residual
error compensation in weights [web:kvlinc, vault 2604.07955]. SPEAR does per-token
gated error compensators. KVarN [web:kvarn] directly studies autoregressive KV-quant
error accumulation in reasoning — and finds it driven by a few outlier tokens, which
is precisely C6's own acknowledged failure mode (concentrated heads).

**Gap promoted: 0.** "Error feedback along key-similar KV tokens" is a *placement*
of known machinery (sigma-delta + error-feedback + GPTQ-style propagation) onto the
token sequence; and KVarN's characterization says the harmful errors are concentrated
outliers — the setting where similarity-ordered cancellation has nothing to cancel
into. No falsifiable advantage claim survives the read.

## Axis latent-space branching / swarm (C7)

**Near-misses:** LatentMAS [web:latentmas] — training-free shared latent working
memory among agents (a branch can already consume another branch's latent state).
LACE [vault:290000928] — concurrent threads read each other via trained cross-thread
attention (+7pts). TGR [web:tgr] — same rolling boundary + short latent lookahead,
but rollouts used for *selection*. LaTER [web:later] — latent rollout as sequential
stage. Hogwild [web:hogwild] — shared-KV parallel generation (token level).

**Gap promoted: 0 (borderline).** The exact composition "ephemeral latent-future KV
consumed by the trunk via ordinary attention, training-free" is not in the sources
read — but every component exists and the premise value is weak: LatentMAS-type latent
signals yield ~0–1 AIME problems by the doc's own citation, and nothing yet shows a
trunk attends usefully to foreign unselected-branch KV. This is a *measurement
question* (does foreign latent KV get attended?) before it is a method gap.

## Axis KV folding / synthetic summary tokens (C8)

**Near-misses:** SemantiCache [vault:290001863] — clustered merge into representative
cores + Proportional Attention rebalancing to the original collective attention
influence = pseudo-token + mass preservation, single level. Meta-Soft [vault:290005203]
— synthesizes soft tokens and redistributes evicted semantics. LightThinker++
[vault:290001140] — folds reasoning traces via learned primitives. Prior run: ReFold/
APEC/Tether cover fold+restore.

**Gap promoted: 0.** C8's residual (hierarchical FMM re-folding, moment-matching for
arbitrary queries, kernel-free) is an increment over SemantiCache's already-existing
attention-mass-preserving merged cores — and its acknowledged killer (sharp facts not
representable by low-order moments; RoPE spreading cluster radius) is unsolved by the
proposal itself.

## Axis hybrid branch memory (C9) and recurrent-state versioning (C4)

**Near-misses:** Hogwild [web:hogwild] — shared append-only KV pool for parallel
workers exists (transformer). State-swap probe [web:stateswap] — attention-KV vs
recurrent-state functions are separable and swappable (Qwen3.5-GDN, Falcon-H1).
TransMamba converts attention→SSM state [web:transmamba]; Mamba-in-the-Llama
documents the large-state speculation difficulty.

**Gap promoted: 0.** C9 = Hogwild's existing primitive restricted to the shareable
channel — a division-of-labor note, not a mechanism; doc's own note: only ~1/4 of
layers see the pool → likely degenerates to voting. C4 (fork/rebase/merge of
recurrent states): no direct prior work found in this pass, but the round-1 spec is
missing — direction flagged less crowded, cannot certify without the actual
mechanism details.

## Axis delayed/batched remote attention (C10)

**Near-misses:** Entire offload family approximates or selects: SparDA lookahead
prefetch, ScoutAttention layer-ahead CPU precompute, AsyncTLS async two-level sparse,
OasisKV speculative staging [vault-offload-family]. Speculative decoding itself
batches attention over B candidate tokens — batched remote read exists in another
guise. KVBuffer [web:kvbuffer] demonstrates "defer a state read/write, apply batched
to amortize memory traffic" — on linear-attention state where batching is near-exact.

**Gap promoted: 1 (narrow).** *Exact* remote softmax contribution deliberately
deferred B steps and batched — staleness taken as a semantic change rather than
removed via selection — is not occupied by the sources read. It is a
systems-flavored mechanism whose value rests on an unmeasured quantity (per-step
drift of remote attention mass). Promoted with the explicit caveat: falsify remote-
mass drift first; the idea dies if drift per step is large.
