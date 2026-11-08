
### C2 verdict
- **Verdict**: reject(reason=no evidence of headroom; decomposes into token-type mixed precision plus a trained pointer-copy head)
- **Evidence**:
  - [2509.20534] (GPT's cited source) does exist, but it is hash consing in JuliaSymbolics: identical symbolic subexpressions are deduplicated through a canonical weak-reference table. C2 does not deduplicate anything. A repeated literal's KV differs with its context, so the borrowed principle ("store canonical objects once, refer by address") does not establish what C2 needs: that a literal's downstream use depends only on its identity.
  - [2607.07144] (GPT's named neighbour) does exist and does what GPT says: it losslessly archives an already-quantized VQ index stream and supports random access and substring search on GPT-2. GPT's stated difference is correct, but this is not the closest prior work.
  - The "literals stay in high precision" half is per-token mixed-precision KV with a token-type importance rule. MiKV [2402.18096] keeps important tokens in high precision and the rest low. IntactKV [2403.01241] keeps one token class (pivots) exact. SemKV [2608.28911] finds that above the quality cliff, importance indicators are interchangeable and the gain of mixing is grid interpolation, which argues against a token-type rule giving anything extra. Addendum 1 also excludes precision-allocation rules.
  - The "copy head fetches raw bytes" half is the pointer-generator / CopyNet output interface [1704.04368][1603.06393][2307.06962]. In a decoder-only LLM the exact token ids are already stored at no cost, so the only new part is training a copy switch into a low-bit-KV model.
  - The target failure is a run that never stops: with 2-bit KV, Qwen3-8B hits the AIME25 length cap 11% -> 42% of the time, and LCB 11% -> 71% [2609.38121]. BreadthKV [2610.05685] also finds that derailed runs that hit the length cap dominate the loss. Neither source attributes the failures to copying literals wrongly, so C2 targets a failure mode nobody has shown is the main cost.
- **Strongest objection in 1 sentence**: In deep layers a literal's KV carries computed context (what the number means and the partial results built on it), so a byte table can only repair the emitted copy token and not the attention reads that compute with it; the remaining fix, keeping literal KV in high precision, is a known token-selective mixed-precision rule that the user has excluded.

#### Notes
- **Closest prior work**:
  - MiKV [2402.18096] and IntactKV [2403.01241]: token-selective high-precision KV.
  - SemKV [2608.28911]: indicators are interchangeable above the cliff.
  - Pointer-generator [1704.04368] and CopyNet [1603.06393]: copy-from-context output.
  - Fractal KV [2607.07144]: lossless symbolic storage of quantized KV, a different object.
  - Searches run:
    - All dates: numeric tokens in high precision; token-aware mixed precision; pointer/copy mechanisms in LLMs; outlier tokens kept in full precision; copy heads / retrieval heads under KV compression; numbers and digits under KV quantization.
    - Since 2025-06: the same themes again for recent work.
  - No paper combined a lossless literal side table with a low-bit KV copy path, so the exact combination is unclaimed. Each half is standard, though, and the combination has no motivating measurement.
- **Plausibility at memory saturation**:
  - Per-token cost: the generated token ids already sit in memory at about 4 bytes per token. Storing literals "losslessly" saves nothing on its own. Keeping their KV in BF16 costs 16 bits per value against 2.
  - Memory cost: if 15-25% of math-CoT tokens are digits, operators or identifiers, the average rises from about 2 to about 4-5.5 bits. That gives back most of the 2-bit saving, and the gain is already known to be grid interpolation [2608.28911].
  - Pointer-only variant: literal KV stays at 2 bits and only the output copy is exact. This fixes errors where the wrong digit is emitted while copying. It cannot fix attention reads in which later tokens compute with the number (carrying in arithmetic, comparisons, substitution), because those read the literal's deep-layer K and V, not its id. Re-embedding the raw id at layer l is not the layer-l V.
  - Training cost: the switch needs LoRA training and changes the output distribution.
  - Net: memory, latency and accuracy gains are unlikely, unless literal copy errors turn out to cause a large share of the 2-bit runaways. No evidence shows that.
- **Cheapest falsification (training-free, about 1 GPU-day)**:
  - Setup: Qwen3-8B on AIME25 (30 problems x 4 seeds) with OSCAR/KIVI INT2 KV.
  - Arms: (a) uniform INT2; (b) INT2 with the KV of every literal token (regex over digits, operators, identifiers) kept in BF16; (c) INT2 with the same number of randomly chosen tokens kept in BF16.
  - Measures: accuracy and length-cap hit rate.
  - Second check: teacher-force BF16 traces through the INT2 model and measure what fraction of first-divergence positions are copies of an earlier literal.
  - Kill condition: if (b) is not clearly better than (c) at equal bytes, or literal copies are a small share of divergences, there is no headroom for C2. Arm (b) is an upper bound on C2's accuracy benefit, since exact copies are at most as good as exact KV.
