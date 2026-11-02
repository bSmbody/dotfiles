# pool_R2: adaptive allocation of KV precision or budget across heads, layers, tokens and roles (2024-01 to 2026-11)

Search ran 2026-11-01. "read = Y" means `papers/<id>.md` exists. 18 papers were newly read and digested in this pass: 2610.11245, 2609.17652, 2608.23599, 2605.06675, 2610.18026, 2610.15259, 2606.24033, 2609.24298, 2512.19206, 2610.19605, 2609.34380, 2607.01831, 2502.15075, 2510.10964, 2605.08317, 2608.28911, 2605.17613, 2604.04722. Other Y rows reuse digests that already existed or were written in parallel by other agents. Those rows are marked "(prior digest)" or "(digest by other agent)". For rows marked "(digest by other agent)", the key fact comes from the abstract.

```tsv
arxiv_id	first_date	title	subcategory	relevance	read	key_fact
2610.11245	2026-10-08	Read What Matters: Query-Adaptive Quantization for KV Caches (ReadKV)	query-time precision / progressive code	H	Y	Stores an 8-bit progressive code. Per query it picks key-channel read depth by sum_h(q'_c sigma_c)^2, then value-token read depth by sum_h alpha_hat^2 over the GQA group. Fixed K/V split. Only perplexity and a single-layer A10G kernel; no reasoning results, no offload.
2609.17652	2026-09-15	Fathom: Per-Query Read Depth for Sparse Decoding over Offloaded KV Caches	bit-plane offload / per-query read depth	H	Y	4-bit K stored as bit planes in host memory. Per query it reverse-water-fills plane depth per channel for the top-k scan. Selected rows are then read exactly. Not faster when the index sits in HBM; batch-1 offload tests only.
2608.23599	2026-08-19	Geodesia-KV: Monotonic Equipotential Allocation	block precision ladder + query-sparse read	H	Y	Block precision {16,8,4,2,1} set from EMA attention mass with b ∝ log(mass x range). Demotion only, never promotion. Separates resident bits from read bits. Perplexity-only evaluation, vLLM plugin.
2605.06675	2026-04-22	RateQuant: Optimal Mixed-Precision KV Cache Quantization via Rate-Distortion Theory	head-wise K/V bit allocation	H	Y	Offline reverse water-filling per (layer, head, K/V): b_i = b_bar + (ln w_i - mean ln w)/ln beta, with w = gradient^2. AM/GM gain is about 2 on Qwen3. A distortion-model mismatch inverts the allocation. Perplexity and commonsense benchmarks only.
2610.18026	2026-10-13	ChampionKV: Head-Wise Adaptive Budget Allocation	head-wise token budget by concentration	H	Y	Head token budget ∝ 1/max attention, used as a concentration proxy: dispersed heads get more tokens. Applied at prefill only, for eviction rather than precision. Gains are mixed on 7-8B models.
2610.15259	2026-10-11	RECAP: Calibrating Low-Bit Reasoning Models on the History They Read	K/V asymmetric read geometry (calibration)	H	Y	Derives G^K_t = E[a^2 ||v_t - y||^2 qq^T / d] and g^V_t = E[a^2] over future queries with GQA aggregation. Used as a PTQ calibration loss for W4A4KV4, not for allocation. AIME-120 +9.7 to 15.8 over FlatQuant. Token importance does not transfer across trajectories (AUC 0.43-0.50).
2606.24033	2026-06-23	Block-GTQ: RoPE-Block Rate Allocation for KV-Cache Quantization	within-head key allocation	H	Y	Static key bit allocation over RoPE blocks from Q/K energy; values stay uniform. A joint K/V split is listed as unexplored. R1-Qwen-7B at K3V2 reaches AIME24/25 49.6/38.8, against 0/0 for uniform TQ-MSE.
2609.24298	2026-09-21	KV-COBRA: Co-Optimized Bit-Rank Allocation	head-wise bit+rank allocation	H	Y	Allocates rank and bits per head offline. Its attention-KL bound writes 1/2 Δs^T F(p) Δs, then bounds F(p) <= I/2, which discards the dependence on concentration. V-heavy splits win. No refresh during generation.
2512.19206	2025-12-22	MixKVQ: Query-Aware Mixed-Precision KV Cache Quantization for Long-Context Reasoning	channel-wise online K precision (long CoT)	H	Y	Key channels get BF16/INT4/INT2 by accumulated |q| times key scale, updated lazily every R tokens. V is fixed at 2 bits. Qwen-32B reasoning average 66.04 vs BF16 67.84 and KIVI-2 58.89.
2610.19605	2026-10-14	PN-Mix: Pair-Norm Guided Mixed-Precision Key Cache Quantization	channel-pair K precision (long output)	H	Y	At 2.25 bits on AIME up to 32K tokens, V-only quantization is close to FP16 while K-only degrades. Pair-norm salience computed at prefill stays stable through decode. Uses 2.26 key bits.
2605.08317	2026-05-08	RDKV: Rate-Distortion Bit Allocation for Joint Eviction and Quantization	token/channel water-filling incl. eviction	H	Y	V token weight = cumulative attention (linear, from TV distance). K channel weight = ||Q_c|| ||K_c||. b* = [log2(w sigma / lambda)]_+, so eviction is the zero-rate case. Allocated once after prefill.
2608.28911	2026-08-28	SemKV: Semantic Mixed-Precision KV Cache Quantization Guided by the Quality Cliff	token-wise mixed precision	M	Y	Quality cliff at (2.0, 2.322] bits for an affine base. Above the cliff, eight importance indicators are interchangeable, so mixing helps only by grid interpolation. 2.0-bit generation raises the max-length termination rate.
2605.17613	2026-05-17	VeriCache: Turning Lossy KV Cache into Lossless LLM Inference	compressed draft + offloaded full-KV verify	H	Y	Drafts on compressed KV and verifies against full KV reloaded from CPU or remote every 20-50 tokens. 1.92-2.73x over full KV. Acceptance is about 0.8 at draft length 30 with 4x compaction.
2607.01831	2026-07-02	Lynx: Progressive Speculative Quantization for KV Transfer	MSB anchor + residual stream	M	Y	In PD disaggregation, decoding starts on the MSB anchor stream; drafts are verified once the residual arrives. The residual always arrives in full; no selective fetch.
2609.34380	2026-09-28	DPS: Dual-Mode Precision LLM Serving with Semi-Unified Memory	load-adaptive precision serving	M	Y	Switches nested FP8/FP16 weights by global KV pressure and reuses the weight residual memory for KV. KV precision is not changed. Decisions are per load, not per request.
2510.10964	2025-10-13	Not All Bits Are Equal: Scale-Dependent Memory Optimization for Reasoning Models	precision vs count, memory budget	M	Y	Below an effective "8-bit 8B" size, eviction beats KV quantization on AIME25/GPQA. Above it they are comparable, but 2-bit KV still loses.
2502.15075	2025-02-20	Quantize What Counts: More for Keys, Less for Values	K/V asymmetric bits	M	Y	K gets more bits because ||W^K|| > ||W^V||. The rule is global, not per head and not attention-aware. Tested only up to 2K context.
2604.04722	2026-04-06	Don't Waste Bits! Adaptive KV-Cache Quantization for On-Device LLMs	token-wise learned precision	M	Y	An MLP picks {2,4,8,16} bits per token from predictive entropy, rarity and attention variance. Same precision for K and V. SmolLM-only experiments.
2605.20868	2026-05-20	Runtime-Certified Bounded-Error Quantized Attention	tiered KV + promotion from CPU	H	Y	(prior digest) INT8 K and INT4 V on GPU, FP16 copy in CPU. Promotes high-mass blocks covering 0.995 mass, plus value promotion when rho_b eta_b > tol. Four-rung fallback ladder.
2607.28699	2026-07-30	WitCert: Sound Runtime Risk Observability and Gating for KV-Cache Quantization	certified fallback	H	Y	(prior digest) Sound per-head TV bound; pages FP16 back in from CPU when the bound exceeds tau. The bound is vacuous at 1-2 bits.
2608.05326	2026-08-05	QEvict: Recoverable Quantized KV Eviction	quantization+eviction tiers, promotion	H	Y	(prior digest) Windows move among full, INT2/INT4 and evicted tiers by cumulative attention. Supports promotion and demotion.
2605.09490	2026-05-10	Not All Thoughts Need HBM	semantics-aware memory hierarchy	H	Y	(prior digest) Four tiers (HBM, DDR full precision, compressed, evicted) driven by cumulative attention. Accuracy depends on the fraction evicted.
2608.07009	2026-08-07	HiSparse: Hierarchical KV Cache Management	host-resident KV + GPU cache	M	Y	(prior digest) Exact top-k fetch from host inside the CUDA graph; 87% hit rate.
2610.02713	2026-10-02	WakeKV: Reactive, Reversible KV Residency for Heads That Change Their Minds	head-wise residency	H	Y	(prior digest) 63-85% of heads drift during generation, so a static head classification is wrong. Per-head LRU with a CPU reservoir.
2610.18642	2026-10-13	MultiAlloc: Budget-Aware Precision Allocation	layer bits x high-precision token count	H	Y	(prior digest) Offline static per-layer (q_l, k_l).
2502.04420	2025-02-06	KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV	layer-wise K/V bit pairs	H	Y	(prior digest) Offline search over (K bits, V bits) per layer, applied statically.
2505.18610	2025-05-24	PM-KVQ: Progressive Mixed-precision KV for Long-CoT	progressive demotion, block allocation	H	Y	(prior digest) 16 -> 8 -> 4 -> 2 bits as memory fills. Block-wise integer program over Taylor sensitivity.
2510.01290	2025-10-01	ThinKV: Thought-Adaptive KV Cache Compression	role/thought-type precision	H	Y	(prior digest) Reasoning and execution thoughts get 4 bits, transitions get 2 bits, plus eviction. Pure quantization can make outputs 5.1x longer.
2610.03027	2026-10-02	TaSQ: Tailoring the Quantization Space for 1-Bit KV	1-bit VQ, query-guided channel weights	H	Y	(prior digest) About 1.25 bits; AIME25 drops 17.8 points on Qwen3-4B-Thinking.
2606.03458	2026-06-02	KVarN: Variance-Normalized KV Quantization	2-bit, error accumulation	M	Y	(prior digest) Pseudo-decode protocol; 2.3 bits close to FP16 on AIME24.
2410.13212	2024-10-17	AsymKV: Layer-Wise Asymmetric Quantization Configurations	K/V asymmetric, layer-wise	H	Y	(prior digest) K error is amplified more than V. K2/V1 split by layer; RepoBench-P drops 13.5 points.
2610.05685	2026-10-05	Spend Bytes on Breadth: Precision-Count Trade-offs for Long-CoT	precision vs token count	H	Y	(prior digest) Offline distortion picks the wrong bit width in 2 of 3 models. More tokens at lower bits beats eviction in 17/18 settings.
2608.07001	2026-08-07	GraceKV: Global Allocation of Resolution and Coverage	global resolution/coverage allocation	M	Y	(prior digest) A single priority queue over layer x head x slot covering both coverage and resolution actions.
2410.10819	2024-10-14	DuoAttention: Retrieval and Streaming Heads	head-wise full vs streaming	H	Y	(prior digest) Learned gate per KV head; retrieval heads keep full KV. Head-wise token budget, not precision.
2404.15574	2024-04-24	Retrieval Head Mechanistically Explains Long-Context Factuality	head roles	M	Y	(prior digest) Retrieval heads are under 5% of heads; masking them breaks CoT.
2606.11164	2026-06-09	ReasonAlloc: Hierarchical Decoding-Time KV Budget Allocation	layer + online head token budget	H	Y	(prior digest) Layer budget from mass-0.93 token demand, head budget reallocated every 128 tokens. Token budget, not precision.
2609.02029	2026-09-02	HeadWiseKV: Budgeted Per-Head Cache Residency for Hybrids	head-wise window length	M	Y	(prior digest) Static per-head suffix length from a codebook.
2610.33625	2026-10-24	RAQ-MLA: Role-Aware Quantization for MLA Caches	role-aware (latent vs rope-key)	M	Y	(prior digest) Latent acts as V and the rope key as K. Separate attention-output-aligned transforms; about 2.5 bits.
2511.18643	2025-11-23	Kitty: 2-bit KV with Dynamic Channel-wise Precision Boost	channel-wise K boost	M	Y	(prior digest) 12.5-25% of K channels at INT4, the rest INT2; first 32 tokens kept at full precision.
2608.04074	2026-08-04	Spend Bits Where Queries Look (NovaKV)	query-weighted transform coding	M	Y	(prior digest) Closed-form non-orthogonal K transform with UU^T ∝ Q^TQ; V at INT2.
2605.17757	2026-05-18	OSCAR: Offline Spectral Covariance-Aware Rotation for 2-bit KV	2-bit rotation	M	Y	(prior digest) Attention-aware rotations; optimality assumes frozen errors.
2608.02691	2026-08-03	OptR: Output-Aware Rotation for INT2 KV	2-bit rotation	L	Y	(prior digest) Output-aware rotation for INT2 KV.
2606.20474	2026-06-18	UltraQuant: 4-bit KV Caching for Context-Heavy Agents	FP4 KV serving	M	Y	(prior digest) 4-bit KV is faster than FP8 only when memory is short. Keeping boundary layers in BF16 changes the method ranking.
2606.03928	2026-06-04	VaSE: value-range-aware eviction for reasoning	value payload outliers	L	Y	(digest by other agent) Evicting large-range values triggers reflection loops.
2606.02011	2026-06-01	2-bit weight reasoning failures + loop rescue	per-request fallback (weights)	H	Y	(prior digest) Detects loops, then commits an earlier answer or reruns in FP16. Weights only.
2606.25519	2026-06-24	Quantization Inflates Reasoning (CTIR)	length inflation	M	Y	(prior digest) Weight PTQ lengthens CoT; only QAT gives a Pareto improvement.
2605.17170	2026-05-16	TriAxialKV: Extreme Low-Precision KV for Agentic Inference	role/semantic precision	H	Y	(digest by other agent) Tags each token by recency, modality and semantic role (user/tool/observation/reasoning) and allocates INT2/INT4 from per-tag sensitivity under a budget. Matches BF16 on OSWorld with a 4.5x larger KV.
2607.12550	2026-07-14	JoLT: Joint Rank-bit Allocation	rank+bit allocation	L	Y	(digest by other agent) Tucker decomposition plus quantized residual; one Lagrangian dual allocates per group.
2609.03494	2026-09-03	GrowPage: On-Demand KV Budgeting for Reasoning Serving	per-request KV capacity	M	Y	(digest by other agent) Per-request KV capacity grows at runtime from dual-timescale query summaries. Capacity, not precision.
2610.09827	2026-10-07	Dual-QK: Sharp Queries and Flat Keys for Prunable 2-bit KV	2-bit + query channel pruning	L	Y	(digest by other agent) Non-orthogonal Q/K transforms; beats OSCAR at 40% query-channel sparsity.
2608.07915	2026-08-08	SPECTRA: Beyond the 2-Bit Cliff via Spectral Transform Coding	sub-2-bit transform coding	L	Y	(digest by other agent) Uses variable spending to get past the 2-bit cliff.
2610.14448	2026-10-10	KV4-RL: INT4 KV for RLVR rollouts	sink/recent protection	L	Y	(digest by other agent) INT8 protection of sinks and recent tokens reduces sampler mismatch.
2602.03203	2026-02-03	ForesightKV: Learning Long-Term Contribution	future-importance eviction	M	Y	(digest by other agent) Learns long-term contribution for eviction in reasoning models.
2606.31519	2026-06-30	RaBitQCache: Rotated Binary Quantization for KVCache	binary proxy, adaptive top-p	L	Y	(digest by other agent) Unbiased binary score estimator; budget adapts to attention sparsity.
2604.19157	2026-04-21	SAW-INT4: System-Aware 4-Bit KV for Serving	serving INT4	L	Y	(digest by other agent) System-aware 4-bit KV for serving.
2609.30854	2026-09-25	The KV Cache Is the New Memory Wall	systems analysis	L	Y	(digest by other agent) Systems analysis of the KV memory wall.
2402.18096	2024-02-28	MiKV: No Token Left Behind	token-wise importance mixed precision	H	N	abstract only: keeps evicted tokens at low precision and important tokens at high precision.
2405.14256	2024-05-23	ZipCache: Salient Token Identification	token-wise mixed precision	H	N	abstract only: normalized attention score marks salient tokens for higher bits; periodic recompression.
2403.04643	2024-03-07	QAQ: Quality Adaptive Quantization for KV Cache	K/V separate + token adaptive, CPU copy	H	N	abstract only: separate K and V strategies; outliers kept. ReadKV App B.2 says QAQ keeps an unquantized CPU copy and re-quantizes on demand.
2407.15891	2024-07-22	RazorAttention: Retrieval Heads	head-wise full vs compressed	M	N	abstract only: retrieval heads keep full cache; others keep sink + recent plus a compensation token.
2410.19258	2024-10-25	HeadKV: Not All Heads Matter	head-level token budget	M	N	abstract only: head budget from retrieval+reasoning score.
2406.02069	2024-06-04	PyramidKV	layer-wise token budget	M	N	abstract only: pyramidal layer budgets.
2407.11550	2024-07-16	Ada-KV	head-wise adaptive token budget	M	N	abstract only: cross-head top-k from an eviction-loss upper bound.
2506.08018	2025-05-18	KVmix: Gradient-Based Layer Importance-Aware Mixed-Precision KV	layer-wise K/V bits by gradient	M	N	abstract only: per-layer K/V bits from gradient importance; AAAI 2026 oral.
2412.03131	2024-12-04	DiffKV: Differentiated Memory Management (SOSP 2025)	K/V + token + head differentiation	H	N	abstract only: differentiates K vs V, token importance and per-head dynamic sparsity, with mixed precision and pruning per request.
2412.12706	2024-12-17	More Tokens, Lower Precision	precision vs count	M	N	abstract only: quantized pruning (more tokens at lower bits) wins on retrieval.
2509.03377	2025-09-03	TRACE: CXL Bandwidth via Lossless Compression and Precision Scaling	bit-plane memory controller	M	N	abstract only: bit-plane substrate in a CXL controller with precision-scalable fetch. Cited by ReadKV as the closest precedent for precision tiers plus bit-plane retrieval.
2610.02800	2026-10-02	BitNest: Bit-Nested Speculative Decoding	nested precision draft (weights + KV)	M	N	abstract only: low-precision base plus residual refinement shared between draft and target; extends to KV.
2609.35800	2026-09-18	HeadGuard: Selective Head Protection for Low-Bit VLM KV	head-wise protection	M	N	abstract only: about 1/8 of heads chosen offline keep BF16 image keys; protecting keys alone keeps most of the gain.
2606.08635	2026-06-07	SpectrumKV: Per-Token Mixed-Precision KV Transfer	token-wise FP16/INT8/INT4	L	N	abstract only: PD transfer; a deployment-time probe decides whether INT4 is tolerated.
2609.26173	2026-08-09	Component Type, Not Reconstruction Error, Predicts Attention Quantization Sensitivity	sensitivity predictors (weights)	L	N	abstract only: V projections dominate the perplexity increase; reconstruction error has median R^2 of 0.044.
2605.24786	2026-05-24	CONF-KV: Confidence-Aware Eviction with Mixed-Precision Storage	uncertainty-driven budget	M	N	abstract only: per-step budget from next-token confidence; FP16/INT8 storage.
2509.06261	2025-09-08	FineServe: Precision-Aware KV Slab	heterogeneous-precision serving	L	N	abstract only: memory management for serving mixed-precision models.
2610.15629	2026-10-11	The Price of Precision: Calibrated Cost Model for Mixed-Precision Serving	cost model for precision choice	M	N	abstract only: the binding resource (compute, weights or KV) decides whether fewer bits are faster; DP allocator.
2610.15640	2026-10-11	Context-Aware Precision Scheduling for SLMs	context-length-dependent precision schedule	L	N	abstract only: weight precision schedule changes with context length.
2603.08727	2026-02-19	ARKV: Adaptive KV Management under Limited Memory	tri-state full/quant/evict, layer entropy	M	N	abstract only: per-layer original-quantization ratio from attention entropy, variance and kurtosis; per-token heavy-hitter state.
2509.03136	2025-09-03	GVote: Adaptive KV Compression without Budget	per-request adaptive budget	L	N	abstract only: Monte-Carlo future queries decide the budget.
2606.26875	2026-06-25	Information-Aware KV Compression for Long Reasoning	forward influence of uncertain tokens	M	N	abstract only: high-uncertainty tokens influence distant future more than high-attention tokens.
2607.16248	2026-06-27	DGAP: Local Distribution Restoration for Low-Bit KV	runtime restoration	M	N	abstract only: detects risky steps from quantized logits and restores the top-K distribution.
2603.20616	2026-03-21	MixedDimKV: Mixed-Dimension Budget Allocation	per-token dimension + head allocation	M	N	abstract only: allocates dimensions per token; head-level variant beats HeadKV.
2606.28831	2026-06-27	HARD-KV: Head-Adaptive Regularization for Decoding-time KV	head-adaptive top-p budget, tiers	M	N	abstract only: calibrated logits allow consistent top-p budgets across heads; dense/sparse/condensed tiers; tested on AIME.
2604.11501	2026-04-13	Attention-Weighted Value Projection	attention-weighted V objective	M	N	abstract only: optimal rank-r value projection uses the eigenvectors of V^T alpha^T alpha V.
2610.03135	2026-10-02	Page-EntroKV: Entropy-Weighted Eviction under GQA	Renyi-2 entropy head pooling	M	N	abstract only: GQA heads pooled by collision-entropy weights, so sharp retrieval heads are not diluted.
2609.19880	2026-09-17	D-Quant: Driftable Entropy Coding for KV	variable-length codes	L	N	abstract only: entropy coding beyond fixed-width levels.
2610.23939	2026-10-08	PeekKV: First Content Token Knows Which Heads Matter	head selection drift	M	N	abstract only: active heads shift between prefill and decode, but stay stable along decode.
2603.04427	2026-02-16	Thin Keys, Full Values	K/V asymmetric dimension	L	N	abstract only: low-dimensional keys for selection, full values.
2510.05529	2025-10-07	H1B-KV: Hybrid One-Bit Caches	1-bit hybrid	L	N	abstract only.
2509.09754	2025-09-11	LAVa: Layer-wise Eviction with Dynamic Budget	layer budget	L	N	abstract only.
2509.08315	2025-09-10	EvolKV: Evolutionary KV Compression	layer budget search	L	N	abstract only.
2510.00636	2025-10-01	Expected Attention: future query distribution	future-attention estimation	M	N	abstract only: estimates attention from the distribution of future queries.
2605.03562	2026-05-05	HeadQ: Model-Visible Distortion and Score-Space Correction	head-wise score correction	L	N	abstract only (withdrawn by author).
2506.02006	2025-05-24	MorphServe: Runtime Quantized Layer Swapping and KV Resizing	load-adaptive precision serving	M	N	abstract only: swaps quantized layers and resizes KV under load.
2610.03007	2026-10-02	AvoKV-E: Payload-Aware Eviction for Long Reasoning	value payload	L	N	abstract only.
2609.04748	2026-09-04	Quantization Amplifies Cache-Induced Divergence	divergence	L	N	abstract only.
2610.06251	2026-10-05	Shared Stopping Decisions Change Answers in HQQ	batch-dependence	L	N	abstract only.
2508.04257	2025-08-06	KVSink: Attention Sinks in KV Quantization	sink protection	L	N	abstract only.
2601.16986	2026-01-05	Crystal-KV: Answer-First KV for CoT	role-aware CoT KV	L	N	abstract only.
2506.07533	2025-06-09	MoQAE: Mixture of Quantization-Aware Experts	chunk-level precision routing	L	N	abstract only.
2503.23294	2025-03-30	Cocktail: Chunk-Adaptive Mixed-Precision	chunk-wise precision by query relevance	M	N	abstract only.
2610.22016	2026-10-15	Fidelity-Consumability Decoupling in KV Caches	geometric fidelity vs usability	L	N	abstract only.
2609.04263	2026-09-02	Quality Recovery for Quantized KV via Low-Rank Attention Adaptation	recovery	L	N	abstract only.
2604.04921	2026-04-06	TriAttention: Trigonometric KV Compression for Long Reasoning	long reasoning eviction	L	N	abstract only.
```

## Seed novelty check

### Seed 1: K and V are sensitive in opposite directions to attention concentration; online asymmetric precision per head or block. Status: **narrowed**, not killed.

Closest work:
- **RateQuant** [2605.06675] already publishes the closed-form water-filling the seed asks GPT to derive: b_i = b_bar + (ln w_i − mean ln w)/ln β, per (layer, head) and separately for K and V under one byte budget. It also gives an a priori gain formula (AM/GM of sensitivities). The difference is that its sensitivity comes from offline gradients and is static. Seed 1 must not claim the water-filling form; it can only claim *where the sensitivity comes from* (online attention statistics with opposite K/V dependence).
- **RECAP** [2610.15259] already writes the per-entry diagonal sensitivities over future queries with GQA aggregation: g^V = E[a²] and G^K = E[a² ||v−y||² qqᵀ/d]. These are the V-side "Σp²" law and a K-side law that vanishes when one token takes all the mass. It uses them only as calibration-loss weights, with no allocation and no online control. This narrows the "theory" contribution, and the seed should cite it as prior derivation. Its K formula measures output MSE, not KL. Seed 1's KL view (Var_p(δs)) and the |q|-vs-score-gap separation are still not covered.
- **ReadKV** [2610.11245] uses a_V = Σ_h α̂² to decide value precision at read time, and query-energy-weighted per-channel depth for keys. This is per-step read depth over an 8-bit store, not stored precision per head. Its K/V split is a fixed input.
- **KV-COBRA** [2609.24298] writes the Fisher form ½ΔsᵀF(p)Δs, then bounds F(p) ≤ I/2. That discards exactly the concentration dependence seed 1 relies on, which is a useful foil. **ChampionKV** [2610.18026] gives dispersed heads more *token* budget (∝ 1/max attention), the eviction analogue of the K-side direction.
- **Don't Waste Bits** [2604.04722] feeds attention variance and entropy into a learned per-token precision controller. It is heuristic, uses the same precision for K and V, and only SmolLM is tested.
- K-vs-V global asymmetry: Quantize What Counts [2502.15075] (K > V by weight norm), PN-Mix [2610.19605] (on AIME, V-only 2.25-bit is near FP16 while K-only degrades), MixKVQ [2512.19206], AsymKV [2410.13212]. KV-COBRA finds V-heavy splits better. So the evidence on which side matters more conflicts; a theory that makes the answer depend on head concentration can explain the disagreement.

What remains novel: (a) one statistic of the attention distribution (n_eff/Σp² plus the score-gap-vs-|q| decomposition) that sets **both** K and V bits per head or block **in opposite directions**; (b) doing this **online during decode** (all of RateQuant, Block-GTQ [2606.24033], KVTuner [2502.04420], MultiAlloc [2610.18642], RDKV [2605.08317] and KV-COBRA are static or prefill-only); (c) evaluation on long CoT at memory saturation.

Must cite and position against: RateQuant, RECAP, ReadKV, KV-COBRA.

Kill-test addition: compare against RateQuant's offline gradient allocation at equal bytes, not only against uniform allocation. WakeKV [2610.02713] (63–85% of heads drift) supports going online. PN-Mix finds channel saliency stable from prefill, so online gains must come from head- or token-level concentration drift, not from channel drift.

### Seed 2: per-request difficulty-aware KV precision admission and upgrade for answers-per-second. Status: **open**, adjacent work only.

- No paper found that picks **KV precision per request by difficulty**. WebSearch also found none. KVTuner (as quoted by a web summary) names "adaptively tune the KV cache quantization precision considering the accuracy requirement of requests" as open.
- Nearest work: DPS [2609.34380] switches *weight* precision by *global KV pressure* (not per request, not KV precision). MorphServe (2506.02006, abstract only) swaps quantized layers under load. GrowPage [2609.03494] grows per-request KV *capacity*, not precision. 2606.02011 [2606.02011] detects loops in 2-bit-weight reasoning and reruns in FP16, which is the closest analogue of "upgrade on a difficulty signal" but for weights and with a full restart. Not All Bits Are Equal [2510.10964] shows the precision-vs-count optimum depends on model scale, but chooses it globally.
- Building blocks for the upgrade cost: progressive codes with readable prefixes (ReadKV [2610.11245], Fathom [2609.17652]), and FP16 copies in CPU (Runtime-Certified [2605.20868], WitCert [2607.28699]). Geodesia-KV [2608.23599] explicitly rules out promotion without a dense copy. PM-KVQ [2505.18610] demotes by memory pressure but not per request.
- Risk: RECAP [2610.15259] finds per-token importance does not transfer across trajectories (AUC 0.43–0.50), which warns that early difficulty signals may be weak. The seed's oracle-upper-bound kill test is the right first step.

### Seed 3: a propagation model of KV quantization error over long decoding as an allocation metric. Status: **narrowed**.

- RECAP [2610.15259] already supervises historical K/V errors by "how strongly later queries read them", averaged over future query positions in the trajectory. This is a first-order, single-layer, future-query-weighted sensitivity used for calibration. It does not model propagation across steps or layers.
- KVarN [2606.03458] and VeriCache [2605.17613] document that error accumulates over decode steps. WitCert [2607.28699] shows that no single layer's error is fatal, so per-step bounds are conservative. RateQuant [2605.06675] uses a gradient (Fisher) proxy, which is a loss-propagated sensitivity, but only for teacher-forced next-token loss, not multi-step decoding.
- Information-Aware KV (2606.26875, abstract only) defines a "Forward Influence" of tokens on distant future contexts for eviction. It is the nearest "future-propagation" metric but concerns retention, not error amplification. ForesightKV [2602.03203] and Expected Attention (2510.00636, abstract only) predict future attention, not error amplification.
- Still open: a cross-step and cross-layer linearized propagation metric that predicts the 2610.05685 inversion (offline picks 4 bits, end-to-end optimum is 2 bits) [2610.05685]. No paper explains that inversion. KV-COBRA [2609.24298] shows a proxy can mislead (an exact solver on the proxy makes perplexity worse), which supports the motivation.

### Seed 4: base code resident in HBM, residual bit planes on CPU, residual fetched only for concentrated blocks. Status: **narrowed, crowded**, the highest collision risk.

- Runtime-Certified Quantized Attention [2605.20868] already keeps INT8 K and INT4 V on GPU with FP16 originals in CPU, and promotes the highest-mass blocks (covering 0.995 mass) plus value blocks with large ρ_b·η_b. This is "fetch exact data for blocks where attention concentrates", at 4–8 bits.
- WitCert [2607.28699] pages FP16 back from CPU when a sound bound fires; the bound is vacuous at 1–2 bits.
- ReadKV [2610.11245] does progressive bit-plane reading with value depth set by α̂², but all bits stay resident (8-bit store). It names tiered memory for refinement levels as future work.
- Fathom [2609.17652] keeps bit planes in host memory and reads them per query, but only for key scans before exact top-k row fetch.
- VeriCache [2605.17613] and Lynx [2607.01831] draft on low precision and verify against full KV fetched later. QEvict [2608.05326], Not All Thoughts Need HBM [2605.09490] and WakeKV [2610.02713] promote from lower tiers by cumulative attention or on miss. TRACE (2509.03377, abstract only) does bit-plane precision-scalable fetch in a CXL controller.
- Narrow remaining gap: (i) base at about 1.25 bits (TaSQ-level) rather than INT4/INT8; (ii) a *probabilistic / expected* trigger computed from base codes alone (Σp² × residual variance) that stays non-vacuous at 1–2 bits, which WitCert and 2605.20868 lack; (iii) the PCIe cost model at memory-saturated long-CoT batch. The seed must position against 2605.20868 and ReadKV directly. "Fetch the residual for high-mass blocks" on its own is not novel.

## Inaccessible papers
- None failed to download. Several rows are abstract-only by choice (pre-2025-06 classics such as MiKV, ZipCache, QAQ, RazorAttention, HeadKV, PyramidKV, Ada-KV, DiffKV, and lower-relevance 2025-2026 items). DiffKV (2412.03131, SOSP 2025) and QAQ (2403.04643) are worth a full read before writing about seeds 1 and 4 (DiffKV differentiates K/V, token and head; QAQ keeps a CPU copy for re-quantization).
- "Xie et al. 2025" (precision tiers + bit-plane retrieval, cited by ReadKV) most likely corresponds to TRACE 2509.03377. The author match was not confirmed and the body was not read.

## Query log
arXiv via `$LIT search -k 30` unless noted: 81 arXiv queries plus 7 WebSearch queries.
1. head-wise KV cache compression
2. retrieval heads streaming heads KV cache
3. head-wise mixed precision KV cache quantization (0 hits)
4. layer-wise KV cache budget allocation
5. mixed-precision KV cache quantization token importance
6. KV cache mixed precision quantization
7. key value asymmetric quantization bits
8. KV cache quantization attention heads sensitivity
9. importance-aware mixed precision KV cache
10. KV cache quantization eviction hybrid
11. attention entropy quantization
12. query-aware KV cache quantization
13. KV cache bit allocation
14. attention entropy key value quantization sensitivity (0 hits)
15. head-wise key value bit allocation
16. asymmetric key value precision
17. per-request KV cache precision
18. difficulty-aware quantization serving
19. KV quantization error propagation decoding
20. progressive precision KV cache residual offload (0 hits)
21. bit-plane KV cache
22. KV cache precision
23. KV cache quantization reasoning
24. KV quantization long chain-of-thought
25. KV cache quantization heads
26. key cache value cache bits
27. progressive KV cache quantization
28. KV cache quantization offload
29. KV cache precision serving
30–41. month sweeps: "KV cache quantization", "mixed-precision KV cache", "KV cache head budget", each with --since 2026-05-01, 2026-07-01, 2026-09-01 and 2026-10-01
42. ZipCache salient token quantization
43. QAQ quality adaptive quantization KV
44. RazorAttention
45. HeadKV head-level KV cache
46. PyramidKV
47. dynamic precision KV cache
48. KV cache precision promotion
49. retrieval heads quantization
50. value quantization attention weights error
51. key quantization softmax error
52. token precision trade-off KV
53. multi-tier KV cache precision
54. KV cache quantization error accumulation
55. quantization reasoning difficulty
56. adaptive quantization per query difficulty (0 hits)
57. nested quantization KV cache
58. residual quantization KV cache
59. hierarchical quantized KV cache
60. attention sparsity quantization error
61. Fisher information KV cache quantization (0 hits)
62. KV quantization reasoning length
63. precision scheduling LLM serving
64. KV cache quantization theory
65. key value sensitivity quantization
66–73 (--since 2025-06-01): attention concentration KV cache; uncertainty-aware KV cache; speculative decoding quantized KV cache; self-speculative quantized KV; head-wise offloading KV cache; query-adaptive KV reading; attention sink quantization; KV cache quantization reasoning model accuracy hard problems
74–81 (--since 2025-06-01): request-level quantization precision routing; accuracy-aware quantization serving reasoning; low-bit fallback full precision rerun reasoning; quantization error accumulation autoregressive decoding theory; future attention KV cache importance prediction; KV cache quantization sensitivity end-to-end; head-level precision KV cache; value cache attention-weighted quantization

WebSearch (used only to find arXiv ids):
- W1. arxiv KV cache quantization attention entropy head-wise key value bit allocation 2026 → 2609.24298, 2605.06675, 2606.24033, 2604.04722
- W2. arxiv per-request adaptive KV cache precision reasoning model serving difficulty → 2509.03136, 2609.03494, 2412.03131, 2603.08727; no per-request difficulty-aware KV precision found
- W3. arxiv KV cache residual bit-plane fetch from CPU attention concentration progressive precision → 2610.11245
- W4. arxiv KV cache quantization error propagation future queries long decoding sensitivity metric bit allocation → 2610.11245, 2606.24033, 2502.15075
- W5. arxiv "value cache" quantization error concentrated attention sharp heads key error diffuse attention theory → no paper with the head-sharpness framing
- W6. arxiv 2026 KV cache precision upgrade escalation during generation low-bit fallback high precision reasoning → 2603.08727, 2604.04722, 2607.16248; no mid-generation escalation paper
- W7. Rui Xie Asad Ul Haq Linsen Ma Liu Liu 2025 KV cache bit-plane precision memory controller arxiv → 2509.03377 (TRACE, unconfirmed)
