# Pool R3: KV-cache compression for reasoning models and long generation (2024-06 to 2026-11)

Scope: KV eviction/merging/compression for long CoT, benchmark and evaluation studies, quantization-induced reasoning-length effects (and KV-side follow-ups to [2606.25519] / [2606.02011]), serving and cost evaluations, low-bit KV support in serving stacks, and offload/hierarchy for long decoding. 151 papers listed, 82 with a digest in RUN/papers/ (read=Y). Newly read and digested in this pass (16): 2606.25519, 2606.02011, 2606.00206, 2510.08525, 2506.08889, 2606.03928, 2603.11504, 2511.18643, 2604.19157, 2608.01631, 2512.07993, 2601.03043, 2609.03494, 2512.19206, 2610.37921, 2609.30854. Some read=Y rows rely on digests written by other agents in this run, or by earlier passes.

## Pool table

```tsv
arxiv_id	first_date	title	subcategory	relevance(H/M/L)	read(Y/N)	key_fact
2606.25519	2026-06-24	Quantization Inflates Reasoning: Token Inflation as a Hidden Cost of Low-Bit Reasoning Models	quant-length (weights)	H	Y	CTIR=(len_q-len_bf16)/len_bf16; weight-only INT3 CTIR up to 292% (Qwen3-4B HQQ); 1.1x CTIR raises p90 TTFT 1050->1400 s in vLLM; only QAT is Pareto; KV not studied
2606.02011	2026-06-01	Extreme Low-Bit Inference in Reasoning Models: Failure Modes and Targeted Recovery	quant-length (weights)	H	Y	W2A16 Qwen3-8B/32B at 32K: loop/hit-max/think-closed metrics correlate |r|>=0.7 with acc loss; 4K-8K budgets hide loops; loop rescue (commit or FP16 rerun) cuts length ~92%; B200 FP8/NVFP4 KV doubles/quadruples max batch
2606.00206	2026-05-29	Quantized Reasoning Models Think They Need to Think Longer, but They Do Not	quant-length (weights+KV4)	H	Y	PTQ raises CoT (AWQ-3bit 5.2K->23.4K on MATH-500); W4A4KV4 FlatQuant 8.0K vs 5.2K; overthinking errors 19->139; KL concentrated at high-entropy 'Wait' positions (rho=0.92); 50-token logit penalty cuts CoT 4-28%
2609.39801	2026-09-30	RATIO: Reasoning Analysis and Token-level Inference Optimization for Quantized Reasoning Models	quant-length (weights)	M	N	abstract only: RATIO finds model-specific overthinking tokens of quantized reasoning models and penalises each with a tailored weight (follow-up to marker penalties)
2504.04823	2025-04-07	Quantization Hurts Reasoning? An Empirical Study on Quantized Reasoning Models	quant-length (weights/KV/act)	H	N	abstract only: COLM 2025 study of weight, KV and activation quantization on R1-Distill/QwQ/Qwen3; harder tasks degrade more; KV3 already hurts (as cited by Kitty)
2606.15682	2026-06-14	ReQAT: Achieving Full-Precision Reasoning Accuracy with 4-bit Floating-Point Quantization-Aware Training	quant-QAT FP4 W4A4KV4	M	N	abstract only: ReQAT, ICML 2026; W4A4KV4 FP4 failures concentrate on low-entropy symbolic-commitment tokens; QAT recipe restores full-precision reasoning accuracy
2606.13233	2026-06-11	ReSET: Accurate Latency-Critical NVFP4 Reasoning via Step-Aware Temperature Scaling	quant-NVFP4 reasoning	L	N	abstract only: ReSET, step-aware temperature scaling for latency-critical NVFP4 reasoning
2610.09202	2026-10-06	Few Bits, One Law: Toward W2A4KV2	quant-QAT W2A4KV2	L	N	abstract only: CanonQ QAT framework toward W2A4KV2 via canonical rotations + Gaussian codebooks
2610.03027	2026-10-02	Tailoring the Quantization Space for 1-Bit KV Cache Compression	KV-quant 1-bit VQ	H	Y	TaSQ ~1.25-bit; Qwen3-4B-Thinking AIME25 74.4->56.7, NIAH64K 95.3->81.5; length/cap-hit near BF16; SGLang, batch 6->84, 1.87x throughput
2606.03458	2026-06-02	KVarN: Variance-Normalized KV-Cache Quantization Mitigates Error Accumulation in Reasoning Tasks	KV-quant 2-bit	H	Y	KVarN 2.3-bit: Qwen3-4B AIME24 60.0 vs FP16 61.1; token counts near FP16 (KVQuant-1% 3857->5021 tokens); vLLM code; no public 2-bit KV in frameworks
2605.17757	2026-05-18	OSCAR: Offline Spectral Covariance-Aware Rotation for 2-bit KV Cache Quantization	KV-quant 2-bit rotation	H	Y	OSCAR INT2 2.28 BPE: -3.78 mean on Qwen3-4B-Thinking, QuaRot-INT2 -74; SGLang paged Triton; 32K cap, 5 seeds
2608.02691	2026-08-03	Output-Aware Rotation for INT2 KV-Cache Quantization	KV-quant 2-bit rotation	H	Y	OptR: offline per-KV-head orthogonal corrections on QuaRot/OSCAR rotation minimising post-W_O output error through the INT2 path; needs calibration (digest by another agent)
2511.18643	2025-11-23	Kitty: Accurate and Efficient 2-bit KV Cache Quantization with Dynamic Channel-wise Precision Boost	KV-quant 2-bit mixed	H	Y	Kitty: 12.5-25% key channels INT4, rest INT2; AIME 32K gap 13->3-4 pts vs KIVI-2; throughput vs HF FP16 only (8x batch, 2.1-4.1x); 8K cap for speed test
2512.19206	2025-12-22	MixKVQ: Query-Aware Mixed-Precision KV Cache Quantization for Long-Context Reasoning	KV-quant mixed-precision	H	Y	MixKVQ query-aware key-channel bits (~2.7b); R1-Qwen-32B avg 66.04 vs BF16 67.84, KIVI-2 58.89; 32K cap; speed only on Llama2-13B ShareGPT
2505.18610	2025-05-24	PM-KVQ: Progressive Mixed-precision KV Cache Quantization for Long-CoT LLMs	KV-quant progressive	H	Y	PM-KVQ progressive mixed precision for long-CoT, ICLR 2026, code (from existing digest)
2510.01290	2025-10-01	ThinKV: Thought-Adaptive KV Cache Compression for Efficient Reasoning Models	KV-quant+evict hybrid	H	Y	ThinKV: pure KV quant can inflate length 5.1x; eviction does not; thought-adaptive quant alone only 1.1x throughput
2610.05685	2026-10-05	Spend Bytes on Breadth: Precision-Count Trade-offs for Decode-Time KV Compression in Long Chain-of-Thought Reasoning	KV-quant x eviction bytes	H	Y	BreadthKV: at equal bytes quantize older tokens and keep more; offline distortion picks wrong bit-width on 2/3 models; eviction loss = runs hitting cap
2610.18642	2026-10-13	MultiAlloc: Budget-Aware Precision Allocation for KV Cache Quantization	KV-quant allocation	H	Y	MultiAlloc per-layer bit-width plus high-precision token count under budget; offline profiling
2502.04420	2025-02-06	KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization for Efficient and Nearly Lossless LLM Inference	KV-quant allocation	M	Y	KVTuner offline layer-wise K/V precision pairs (ICML 2025)
2610.19605	2026-10-14	PN-Mix: Pair-Norm Guided Mixed-Precision Key Cache Quantization for Efficient Long-Output LLM Inference	KV-quant mixed (long output)	H	Y	PN-Mix: higher key precision for post-RoPE channel pairs with large q-k pair-norm product, chosen once at prefill, reused through long decode; sinks kept
2604.19157	2026-04-21	SAW-INT4: System-Aware 4-Bit KV-Cache Quantization for Real-World LLM Serving	KV-quant INT4 serving	H	Y	SAW-INT4: token-wise INT4 + block Hadamard (keys only) fused in SGLang; naive INT4 collapses on Qwen3-4B-Thinking (BDR-128 73.1 vs 75.6); paged-incompatibility argument vs Kitty/VQ/channel-wise
2606.20474	2026-06-18	UltraQuant: 4-bit KV Caching for Context-Heavy Agents	KV-quant FP4 serving	H	Y	UltraQuant FP4 KV (vLLM, MI355X): throughput = FP8 KV at half bytes; FP4 faster than FP8 only past FP8 cache capacity
2604.04722	2026-04-06	Don't Waste Bits! Adaptive KV-Cache Quantization for Lightweight On-Device LLMs	KV-quant on-device	L	Y	On-device learned per-token KV precision controller (entropy, rarity, attention variance features)
2609.38121	2026-09-29	WUSH-KV: KV Cache Quantization with Data-Adaptive Transforms	KV-quant transform	M	N	abstract only: WUSH-KV data-adaptive transforms for KV quantization (SGLang context)
2610.09827	2026-10-07	Dual-QK: Sharp Queries and Flat Keys for Prunable 2-bit KV Caches	KV-quant 2-bit	M	Y	Dual-QK: paired non-orthogonal q/k transforms (A B^T=I) flatten key scales for INT2 and concentrate queries for pruning
2610.15384	2026-10-11	E8 Lattice Key Quantization for Low-Bit KV-Cache Compression	KV-quant lattice	M	N	abstract only: E8 lattice key quantization for low-bit KV cache
2605.08317	2026-05-08	RDKV: Rate-Distortion Bit Allocation for Joint Eviction and Quantization of the KV Cache	KV-quant x eviction	M	Y	RDKV: eviction (0 bits) and quantization as one rate-distortion allocation per layer-head, weights from attention TV change
2607.12550	2026-07-14	A JoLT for the KV cache: Near-Lossless KV Cache Compression via Joint Rank-bit Allocation	KV-quant x low-rank	M	Y	JoLT: prefill-cache Tucker (ST-HOSVD) + bit allocation over layer groups; prefill only
2609.24298	2026-09-21	KV-COBRA: KV Cache Compression via Co-Optimized Bit-Rank Allocation	KV-quant x low-rank	M	Y	KV-COBRA: per-head SVD rank and bit-width co-optimised under a global byte budget
2609.19880	2026-09-17	D-Quant: Driftable Entropy Coding for KV Cache Quantization	KV-quant entropy coding	M	N	abstract only: D-Quant driftable entropy coding of quantized KV
2608.28911	2026-08-28	SemKV: Semantic Mixed-Precision KV Cache Quantization Guided by the Quality Cliff for Long-Context LLM Inference	KV-quant mixed	M	Y	SemKV: fractional-bit grid shows a quality cliff (Llama-3.1-8B fine to 2.32 bits then collapses); semantic mixed precision
2608.04074	2026-08-04	Spend Bits Where Queries Look: KV Cache Vector Quantization with Attention-Preserving Transforms	KV-quant VQ	M	Y	NOVA-KV: closed-form non-orthogonal key transform UU^T=cM_q so query-weighted logit error becomes MSE; 2-bit VQ
2607.16248	2026-06-27	High-accuracy Low-Bit KV-Cache Quantization via Local Distribution Restoration	KV-quant low-bit	M	N	abstract only: local distribution restoration for low-bit KV
2605.19660	2026-05-19	OScaR: The Occam's Razor for Extreme KV Cache Quantization in LLMs and Beyond	KV-quant extreme	M	Y	OScaR: per-channel INT2 key bottleneck is token-norm imbalance; norm-aware rescaling
2607.01065	2026-07-01	GSRQ: Gain-Shape Residual Quantization for Sub-1-bit KV Cache	KV-quant sub-1-bit	M	Y	GSRQ: gain-shape residual K-means for sub-1-bit K/V (ICML 2026)
2606.24033	2026-06-23	Block-GTQ: RoPE-Block Rate Allocation for KV-Cache Quantization	KV-quant RoPE-block	M	Y	Block-GTQ: static RoPE-block key precision; R1-Distill-Qwen-7B K3V2 AIME24/25 avg@8 49.6/38.8 vs fp16 54.2/37.9, uniform TQ-MSE 0
2605.11478	2026-05-12	FibQuant: Universal Vector Quantization for Random-Access KV-Cache Compression	KV-quant VQ	L	N	abstract only: FibQuant universal VQ for random-access KV
2506.18879	2025-06-23	CommVQ: Commutative Vector Quantization for KV Cache Compression	KV-quant VQ	M	N	abstract only: CommVQ commutative VQ compatible with RoPE, ICML 2025
2506.19505	2025-06-24	AnTKV: Anchor Token-Aware Sub-Bit Vector Quantization for KV Cache in Large Language Models	KV-quant sub-bit VQ	M	N	abstract only: AnTKV anchor-token-aware sub-bit VQ
2510.06175	2025-10-07	VecInfer: Efficient LLM Inference with Low-Bit KV Cache via Outlier-Suppressed Vector Quantization	KV-quant VQ	M	N	abstract only: VecInfer outlier-suppressed VQ with low-bit KV kernels
2605.17170	2026-05-16	TriAxialKV: Toward Extreme Low-Precision KV-Cache Quantization for Agentic Inference Tasks	KV-quant agentic	M	Y	TriAxialKV: INT2/INT4 by recency x modality x role (incl. <think> reasoning) for agentic workloads in SGLang
2610.14448	2026-10-10	KV4-RL: Unlocking Faster Asynchronous Rollouts for RLVR with INT4 KV Cache Quantization	KV-quant RL rollout	M	Y	KV4-RL: 4.25-bit token-wise INT4 + Hadamard KV for async GRPO rollouts; KV quant beats weight quant for rollout speed; INT4 can degrade learning
2606.09864	2026-06-01	Alignment Collapse Under KV Cache Quantization: Diagnosis and Mitigation	KV-quant safety eval	L	N	abstract only: low-bit KV quantization silently removes refusals (Mistral-7B -15.2% at 1.03x ppl)
2605.24786	2026-05-24	CONF-KV: Confidence-Aware KV Cache Eviction with Mixed-Precision Storage for Long-Horizon LLM	KV-quant x eviction	M	N	abstract only: CONF-KV uses next-token confidence to choose per-step budget with mixed-precision storage
2412.03131	2024-12-04	DiffKV: Differentiated Memory Management for Large Language Models with Parallel KV Compaction	KV-quant x pruning system	M	N	abstract only: DiffKV differentiated K/V precision and pruning with parallel compaction (SOSP 2025)
2406.03482	2024-06-05	QJL: 1-Bit Quantized JL Transform for KV Cache Quantization with Zero Overhead	KV-quant 1-bit JL	M	Y	QJL 1-bit sign-JL keys (from existing digest)
2410.13212	2024-10-17	AsymKV: Enabling 1-Bit Quantization of KV Cache with Layer-Wise Asymmetric Quantization Configurations	KV-quant 1-bit	M	Y	AsymKV K2/V1: RepoBench-P -13.5 pts, near lossless TriviaQA
2504.19874	2025-04-28	TurboQuant: Online Vector Quantization with Near-optimal Distortion Rate	KV-quant VQ rotation	H	Y	TurboQuant; ranking depends on keeping first/last layers BF16
2605.13810	2026-05-13	Provable Quantization with Randomized Hadamard Transform	KV-quant theory dither	M	Y	Randomised Hadamard + subtractive dither matches TurboQuant MSE constant
2512.01953	2025-12-01	KV Pareto: Systems-Level Optimization of KV Cache and Model Compression for Long Context Inference	KV-quant x weights system	M	N	abstract only: KV Pareto, systems-level joint KV and model compression for long context
2505.24133	2025-05-30	R-KV: Redundancy-aware KV Cache Compression for Reasoning Models	evict-reasoning	H	Y	R-KV redundancy-aware eviction; 10% cache near-full on R1-Distill; budget measured vs mean length
2506.15969	2025-06-19	LazyEviction: Lagged KV Eviction with Attention Pattern Observation for Efficient Long Reasoning	evict-reasoning	H	Y	LazyEviction: token importance recurrence, MRI-based lagged eviction
2512.12008	2025-12-12	Hold Onto That Thought: Assessing KV Cache Compression On Reasoning	benchmark-eviction	H	Y	Hold Onto That Thought: H2O/SnapKV-D best for reasoning; low budgets lengthen traces and cause non-terminating babble
2609.03430	2026-09-03	Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning	evict-reasoning baseline	H	Y	Random Attention: with prompt protected, random per-head eviction matches SnapKV/R-KV/VaSE; serves 32-43% more tok/s in vLLM
2606.03928	2026-06-02	Value-Aware Stochastic KV Cache Eviction for Reasoning Models	evict-reasoning	H	Y	VaSE: evicting large-Range values causes loops; value reservation + stochastic sampling beats R-KV by 4.4-4.9 pts; 3.1x tok/s vs full at bs16
2510.08525	2025-10-09	Which Heads Matter for Reasoning? RL-Guided KV Cache Compression	evict head-level RL	H	Y	RLKV: GRPO-trained head gates; compressing retrieval heads -> overlength errors, reasoning heads -> loops; dynamic budget critique of R-KV; SGLang 1.56x at 0.4 sparsity
2512.07993	2025-12-08	SkipKV: Selective Skipping of KV Generation and Storage for Efficient Inference with Large Reasoning Models	evict sentence-level	H	Y	SkipKV: R-KV produces longer outputs than FullKV at all budgets; padding breaks batch eviction; sentence eviction + steering up to 28% shorter than FullKV
2603.11504	2026-03-12	LongFlow: Efficient KV Cache Compression for Reasoning Models	evict per-step fused	H	Y	LongFlow ||alpha v||_1 score fused in kernel; 16K cap, 3.2K budget; 11.8x FullKV throughput at max batch (Qwen3-1.7B)
2512.00504	2025-11-29	G-KV: Decoding-Time KV Cache Eviction with Global Attention	evict-reasoning	H	N	abstract only: G-KV global (local+historical) attention scoring plus RL/distillation post-training for decode-time eviction (Microsoft)
2601.16986	2026-01-05	Crystal-KV: Efficient KV Cache Management for Chain-of-Thought LLMs via Answer-First Principle	evict-reasoning	M	N	abstract only: Crystal-KV answer-first principle for CoT KV management
2604.10900	2026-04-13	CASK: Core-Aware Selective KV Compression for Reasoning Traces	evict/merge reasoning	M	N	abstract only: CASK argues scorer refinement barely changes keep-set; core-aware selective compression of traces
2605.23200	2026-05-22	Adaptive Mass-Segmented KV Compression for Long-Context Reasoning	evict region quota	H	N	abstract only: AMS (NeurIPS 2026) shows global top-k causes 'region wipe-out' of contiguous reasoning blocks; region-aware quotas
2606.26875	2026-06-25	Information-Aware KV Cache Compression for Long Reasoning	evict info-theoretic	M	N	abstract only: Forward Influence metric of compressed tokens on future context, beyond attention
2609.04971	2026-09-04	BeaconKV: Key-Value Cache Compression Guided by Beacon Queries for Efficient Large Reasoning Model Inference	evict-reasoning	M	N	abstract only: BeaconKV (ICML 2026) - recent queries are poor proxies for future attention; uses beacon queries
2610.03007	2026-10-02	AvoKV-E: Payload-Aware KV Cache Eviction for Long Reasoning	evict-reasoning	H	N	abstract only: AvoKV-E - low-attention entries can carry large value payloads; delays eligibility of fresh states
2610.20641	2026-10-07	AbridgeKV: Compressing Long Reasoning into the KV Cache of Learned Pause Tokens	trained compression (pause tokens)	H	N	abstract only: AbridgeKV - eviction on untrained models yields longer outputs, often up to the length limit; trains model to compress blocks into learned pause-token KV
2602.03203	2026-02-03	ForesightKV: Optimizing KV Cache Eviction for Reasoning Models by Learning Long-Term Contribution	evict learned	H	Y	ForesightKV learned long-term contribution scorer + GRPO, ICML 2026
2602.10238	2026-02-10	Learning to Evict from Key-Value Cache	evict learned	M	Y	KV Policy per-head RL agents from K,V,position
2604.18002	2026-04-20	Neural Garbage Collection: Learning to Forget while Learning to Reason	evict learned RL	M	Y	Neural Garbage Collection: model learns to evict via outcome RL
2506.05345	2025-06-05	Inference-Time Hyper-Scaling with KV Cache Compression	evict learned (DMS)	H	Y	DMS learned eviction for inference-time hyper-scaling (NeurIPS 2025)
2606.26472	2026-06-25	EpiKV: Epiphany-Aware KV Cache Eviction Without the Attention Matrix	evict-reasoning	M	Y	EpiKV hidden-state shift score without attention matrix
2606.11164	2026-06-09	ReasonAlloc: Hierarchical Decoding-Time KV Cache Budget Allocation for Reasoning Models	evict budget allocation	M	Y	ReasonAlloc layer/head budget allocation for reasoning
2608.12331	2026-06-01	Thought-Aware KV Cache Compaction for Reasoning via Adaptive Attention Matching	merge/compaction reasoning	M	Y	Thought-aware attention-matching compaction on Qwen3-4B
2608.15797	2026-08-16	KV-Rescue: Recovering Reasoning Language Model KV Eviction Loss via Stepwise Interleaving	evict + rescue	M	Y	KV-Rescue interleaves small full-cache helper with evicted model
2608.08878	2026-08-09	DistillCache: KL-Guided Adaptive KV-Cache Eviction for Memory-Efficient LLM Inference	evict learned	M	Y	DistillCache RL eviction policy with KL reward
2609.03515	2026-09-03	What Matters for Aggressive Decoding-Time KV Eviction? Temporal Aggregation and Ranking Preservation	evict temporal aggregation	M	N	abstract only: EMNLP 2026 - EMA aggregation makes most scorer variants indistinguishable at eviction-set level
2605.18053	2026-05-18	Protection Is (Nearly) All You Need: Structural Protection Dominates Scoring in Globally Capped KV Eviction	evict protection	M	N	abstract only: under global caps all policies collapse without prompt-boundary protection; reserving 10% recovers most quality
2603.08743	2026-03-01	Zipage: Maintain High Request Concurrency for LLM Reasoning through Compressed PagedAttention	evict + PagedAttention	H	N	abstract only: Zipage compressed PagedAttention + scheduling for high-concurrency reasoning serving
2609.03494	2026-09-03	GrowPage: On-Demand KV Budgeting for Efficient LLM Reasoning Serving	evict serving budget	H	Y	GrowPage on nano-vLLM: per-request page growth; +60-64% TPS vs FullKV; mixed workload 84.9% @2213 tok/s vs Zipage-4096 83.7% @1690
2607.01237	2026-05-01	KARA: Efficient Reasoning LLM Serving via Sliding-Window KV Cache Compression	evict serving sliding-window	M	N	abstract only: KARA - threshold-triggered compression can reduce throughput; sliding-window compression for reasoning serving
2511.06029	2025-11-08	Lethe: Layer- and Time-Adaptive KV Cache Pruning for Reasoning-Intensive LLM Serving	evict layer/time adaptive	M	Y	Lethe (AAAI 2026): layer-wise attention-segment budgets + time-adaptive pruning; MATH500 R1-Qwen-7B 85.4 vs FullKV 86.4 (H2O 67.2)
2605.29873	2026-05-28	Moment-KV: Momentum-Based Decode-Time KV Cache Compression for Long Generation	evict decode-only	M	N	abstract only: Moment-KV momentum-based decode-time compression; keep prefill cache intact
2601.07891	2026-01-12	KVzap: Fast, Adaptive, and Faithful KV Cache Pruning	evict fast KVzip	M	N	abstract only: KVzap fast approximation of KVzip, prefill+decode, 2-4x on Qwen3 reasoning
2609.03235	2026-09-03	SGD-KV: Summarization Guided KV Cache Compression	evict head-aware	L	N	abstract only: SGD-KV summarisation-diagnostic head prioritisation
2610.02815	2026-10-02	iS-KV: Online Low-Rank KV Cache Compression via Block-Incremental SVD	low-rank online	M	N	abstract only: iS-KV block-incremental SVD for long-CoT decode cache
2610.37921	2026-10-27	FAD-KV: Adaptive Dictionary KV Caching for Efficient Reasoning Decoding	dictionary sparse coding	M	Y	FAD-KV screened sparse coding + fixed-size atom replacement; evaluated on non-thinking 3-8B models only
2610.06479	2026-10-05	Behavior-Preserving KV Cache Compression	evict behaviour-preserving	M	N	abstract only: retain entries whose removal changes output distribution most
2610.22130	2026-10-15	DropKV: Decoupling Residual-Output Perturbation for Near-Optimal KV-Cache Eviction	evict output perturbation	L	N	abstract only: DropKV decoupled residual-output perturbation (NeurIPS 2026)
2609.07966	2026-09-07	MetaKV: Adaptive KV Cache Compression for Constrained LLM Inference	compression config selection	L	N	abstract only: MetaKV picks compression config per prompt/resource constraint
2609.37988	2026-09-29	KV-Kaizen: Learning Context-Adaptive Cache Compression Choices	compression choice learned	L	N	abstract only: KV-Kaizen learns context-adaptive non-eviction compression choices
2610.02713	2026-10-02	WakeKV: Reactive, Reversible KV Residency for Heads That Change Their Minds	evict reversible head residency	M	Y	WakeKV: 63-85% heads drift during generation; reversible residency
2609.22158	2026-08-26	StepKV: Step-Aware KV Cache Compression for LLM Agents	evict agents step-level	L	Y	StepKV step-level retention for agents
2610.07643	2026-10-06	Monte Carlo Estimation for KV Cache Eviction	evict MC futures	L	Y	LORE-KV Monte Carlo futures for prompt eviction
2607.21475	2026-07-23	Error Certificates for KV-Cache Eviction via Randomized Design	evict error certificate	M	Y	Randomised Poisson eviction gives per-step error estimate
2502.11147	2025-02-16	RaaS: Reasoning-Aware Attention Sparsity for Efficient LLM Reasoning	evict-reasoning (early 2025)	M	N	abstract only: RaaS reasoning-aware attention sparsity with timestamps (baseline in LazyEviction/ThinKV)
2503.00979	2025-03-02	Dialogue Without Limits: Constant-Sized KV Caches for Extended Responses in LLMs	evict long response	M	N	abstract only: MorphKV constant-size cache for extended responses (ICML 2025)
2507.08806	2025-06-17	Think Clearly: Improving Reasoning via Redundant Token Pruning	evict improves reasoning	M	N	abstract only: Think Clearly - pruning redundant reasoning tokens improves accuracy
2510.13797	2025-10-15	Breadcrumbs Reasoning: Memory-Efficient Reasoning with Compression Beacons	trained compression beacons	M	N	abstract only: Breadcrumbs Reasoning compresses reasoning into learned beacons
2506.08889	2025-06-10	SeerAttention-R: Sparse Attention Adaptation for Long Reasoning	sparse-attn decode learned	H	Y	SeerAttention-R: Qwen3-8B AIME24 full 74.5%/15.1K tok; Quest 2K budget 13.3%/30.0K tok; 32K cap, 64 samples; kernel 9x, no e2e serving
2601.03043	2026-01-06	Lil: Less is Less When Applying Post-Training Sparse-Attention Algorithms in Long-Decode Stage	sparse-attn length inflation	H	Y	Lil: H2O/Sink/Quest/InfLLM outputs up to 90% longer than full; LZ77 shows repetition; Guardian early stop saves up to 90% tokens <2% acc
2508.07101	2025-08-09	Less Is More: Fast and Accurate Reasoning with Cross-Head Unified Sparse Attention	sparse-attn reasoning	M	N	abstract only: LessIsMore training-free cross-head unified sparse attention for long reasoning
2510.07486	2025-10-08	AsyncSpade: Efficient Test-Time Scaling with Asynchronous Sparse Decoding	sparse-attn async decode	M	N	abstract only: AsyncSpade asynchronous sparse decoding for test-time scaling under high concurrency
2506.13059	2025-06-16	Multipole Attention for Efficient Long Context Reasoning	sparse-attn clustering	M	N	abstract only: Multipole Attention for long reasoning (clustered key centroids)
2510.09883	2025-10-10	DELTA: Dynamic Layer-Aware Token Attention for Efficient Long-Context Reasoning	sparse-attn layer-aware	M	N	abstract only: DELTA dynamic layer-aware token attention for long-context reasoning (ACL 2026 Findings)
2506.04108	2025-06-04	Rectified Sparse Attention	sparse-attn rectified	M	N	abstract only: Rectified Sparse Attention periodically densely refreshes KV to stop error accumulation
2512.16391	2025-12-18	Kascade: A Practical Sparse Attention Method for Long-Context LLM Inference	sparse-attn practical	L	N	abstract only: Kascade practical sparse attention for long-context inference
2602.04541	2026-02-04	LycheeDecode: Accelerating Long-Context LLM Inference via Hybrid-Head Sparse Decoding	sparse-attn hybrid-head	M	N	abstract only: LycheeDecode hybrid-head sparse decoding (ICLR 2026)
2510.05688	2025-10-07	vAttention: Verified Sparse Attention	sparse-attn verified	M	Y	vAttention: top-k + sampled residual with error guarantee
2406.10774	2024-06-16	Quest: Query-Aware Sparsity for Efficient Long-Context LLM Inference	sparse-attn query-aware	M	Y	Quest page-level query-aware selection (baseline that inflates length)
2605.09490	2026-05-10	Not All Thoughts Need HBM: Semantics-Aware Memory Hierarchy for LLM Reasoning	offload hierarchy	H	Y	Not All Thoughts Need HBM: eviction cliff 22%->0% at 70->50% budget; 4-tier HBM/DDR/compressed/evicted
2608.07009	2026-08-07	HiSparse: Scaling Sparse-Attention Decoding with Hierarchical KV Cache Management	offload sparse serving	H	Y	HiSparse in upstream SGLang: host-memory full KV, small GPU cache, fused top-k fetch
2608.05326	2026-08-05	QEvict: Recoverable Quantized KV Eviction for Attention-Drift-Robust Long-Context Decoding	offload/quant tiers	H	Y	QEvict recoverable INT2/INT4 tier still attended
2608.08097	2026-08-08	OasisKV: Scaling In-Decode KV Cache Beyond HBM with Lookahead Sparse Prefetching	offload prefetch	M	N	abstract only: OasisKV lookahead sparse prefetching to scale in-decode KV beyond HBM
2609.34555	2026-09-28	PulseInfer: I/O-Centric Sparse KV Cache Offloading for Efficient Long-Context LLM Decoding	offload I/O	M	N	abstract only: PulseInfer - sparse offloading shifts the bottleneck to fragmented PCIe recalls
2609.37538	2026-09-29	AVSG: Accelerated Vectorized Sparse Gather for Efficient KV Cache Offload in Sparse-Attention LLM Serving	offload gather kernel	L	N	abstract only: AVSG vectorised sparse gather for KV offload in sparse-attention serving
2605.18071	2026-05-18	KVDrive: A Holistic Multi-Tier KV Cache Management System for Long-Context LLM Inference	offload multi-tier	L	N	abstract only: KVDrive holistic multi-tier KV management
2510.13602	2025-10-15	NOSA: Native and Offloadable Sparse Attention	offload native sparse	M	N	abstract only: NOSA native and offloadable sparse attention (EMNLP 2026)
2602.07721	2026-02-07	ParisKV: Fast and Drift-Robust KV-Cache Retrieval for Long-Context LLMs	offload retrieval	M	N	abstract only: ParisKV drift-robust KV retrieval (ICML 2026)
2509.24626	2025-09-29	SparseServe: Unlocking Parallelism for Dynamic Sparse Attention in Long-Context LLM Serving	serving sparse attention	M	N	abstract only: SparseServe parallelism for dynamic sparse attention in long-context serving
2510.11292	2025-10-13	LouisKV: Efficient KV Cache Retrieval for Long Input-Output Sequences	offload retrieval long I/O	M	N	abstract only: LouisKV KV retrieval for long input-output sequences
2610.08811	2026-09-23	KVFetch: Temporal Prefetching for the Missing Half of KV Cache Compression	offload prefetch	L	Y	KVFetch temporal prefetching for sequential copying
2605.20868	2026-05-20	Runtime-Certified Bounded-Error Quantized Attention	quant tier + fallback	M	Y	Runtime-certified INT8K/INT4V with FP16 CPU fallback
2605.17613	2026-05-17	VeriCache: Turning Lossy KV Cache into Lossless LLM Inference	lossy->lossless KV	M	Y	VeriCache: compressed-KV self-drafting verified against full off-GPU KV, making lossy compression lossless
2607.28699	2026-07-30	WitCert: Sound Runtime Risk Observability and Gating for KV-Cache Quantization	quant risk meter	M	Y	WitCert sound TV bound per head/step; vacuous at 1-2 bit
2501.01005	2025-01-02	FlashInfer: Efficient and Customizable Attention Engine for LLM Inference Serving	serving kernel library	M	N	abstract only: FlashInfer customizable attention engine, MLSys 2025 (FP8 KV / paged kernels)
2503.18773	2025-03-24	BitDecoding: Unlocking Tensor Cores for Long-Context LLMs with Low-Bit KV Cache	kernel low-bit KV	M	N	abstract only: BitDecoding tensor-core kernels for low-bit KV in long context
2410.00161	2024-09-30	KV-Compress: Paged KV-Cache Compression with Variable Compression Rates per Attention Head	serving variable-rate paged	M	N	abstract only: KV-Compress paged cache with per-head variable compression in vLLM
2609.30854	2026-09-25	The KV Cache Is the New Memory Wall	survey/SoK serving	M	Y	SoK: same 2-bit quant derived 1.25x (W1) vs 4.82x (W2); variance, position sensitivity, cost columns unreported
2609.17863	2026-09-15	The Inference Engineering Pareto Atlas: Which Optimizations Dominate the Cost, Quality, and Latency Frontier?	benchmark cost-quality atlas	M	N	abstract only: Pareto atlas of 54 vLLM configs incl. FP8 KV; quality only on GSM8K, non-reasoning model
2608.03036	2026-08-04	LLM Serving in the Wild: An Empirical Study of Frameworks, Methods, and System Designs	benchmark serving frameworks	L	N	abstract only: empirical study of LLM serving frameworks and system designs
2605.01708	2026-05-03	SplitZip: Ultra Fast Lossless KV Compression for Disaggregated LLM Serving	lossless KV transfer	L	Y	SplitZip lossless exponent coding for disaggregated KV transfer
2610.33719	2026-10-24	ZipFusion: Fusing Lossless KV Decompression with Attention for Efficient LLM Decoding	lossless KV kernel	L	N	abstract only: ZipFusion fuses lossless KV decompression with attention
2608.01631	2026-08-03	Does Accuracy Equal Evidence? Reasoning Faithfulness under KV Cache Compression	benchmark faithfulness	H	Y	Fixed-trace replay: eviction keeps answers but breaks chains (RWAC), accuracy ranking anti-correlates with chain validity; KIVI-2bit near Full-KV
2502.01941	2025-02-04	Semantic Integrity Matters: Benchmarking and Preserving High-Density Reasoning in KV Cache Compression	benchmark high-density reasoning	M	N	abstract only: Semantic Integrity Matters - benchmarking KV compression on high-density reasoning (ICML 2026)
2607.11942	2026-07-11	How Query Visibility Changes KV-Cache Compression Rankings: A Matched-Budget Audit	benchmark protocol audit	M	N	abstract only: query-aware vs query-agnostic protocol reorders compression rankings (matched budget)
2407.01527	2024-07-01	KV Cache Compression, But What Must We Give in Return? A Comprehensive Benchmark of Long Context Capable Approaches	benchmark long-context	L	N	abstract only: 2024 comprehensive benchmark of long-context-capable KV approaches (long input, short output)
2412.10319	2024-12-13	SCBench: A KV Cache-Centric Analysis of Long-Context Methods	benchmark KV-centric	L	N	abstract only: SCBench KV-cache-centric multi-turn analysis (ICLR 2025)
2610.13570	2026-10-09	Constructing Pareto Frontiers of Optimal Reasoning Termination Methods for Overthinking in Reasoning Models	eval overthinking termination	L	Y	Step-wise truncation probing / Pareto of termination methods
2604.06787	2026-04-08	When Is Thinking Enough? Early Exit via Sufficiency Assessment for Efficient Reasoning	early exit	L	Y	DTSR sufficiency-assessment early exit at reflection tokens
2506.05333	2025-06-05	Kinetics: Rethinking Test-Time Scaling Laws	test-time scaling with memory cost	H	N	abstract only: Kinetics - test-time scaling laws should count attention/KV memory cost, favouring sparse attention
2502.10424	2025-02-05	QuantSpec: Self-Speculative Decoding with Hierarchical Quantized KV Cache	spec-decode quantized KV	M	Y	QuantSpec hierarchical 4-bit KV self-speculation
2609.17943	2026-09-16	ASPIRE: Asynchronous Batched Self-Speculative Decoding for Long-Context LLM Inference	spec-decode sparse draft	M	Y	ASPIRE batched self-spec with sparse-KV draft; full KV kept
2608.30252	2026-08-31	Strong Drafts Need Compact Memories: Long-Context Speculative Decoding with Compressed KV Cache	spec-decode compressed draft KV	L	Y	MASW compressed draft memory
2512.01278	2025-12-01	Accelerating Large-Scale Reasoning Model Inference with Sparse Self-Speculative Decoding	spec-decode sparse reasoning	M	N	abstract only: sparse self-speculative decoding for large-scale reasoning inference
2610.30644	2026-10-22	Speculative Acceptance Does Not Decay with Position: A Full-Length Diagnostic on Long Chain-of-Thought with Independent Drafts	spec-decode long CoT	L	Y	Acceptance does not decay with position over full long CoT
2609.19969	2026-09-17	DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression	native KV compression	M	Y	DeepSeek-V4.1-Flash native FP4 KV + CSA2
2609.36760	2026-09-29	QuantMLA: Function-Aligned Dual-Path Quantization for Low-Bit MLA KV Caching	MLA quant	L	Y	QuantMLA dual-path low-bit MLA cache
2610.33625	2026-10-24	RAQ-MLA: Role-Aware Quantization for Multi-Head Latent Attention Caches	MLA quant	L	Y	RAQ-MLA role-aware MLA cache quantization
2610.20686	2026-10-14	RoLaQ: Joint Rotation and Range Calibration for 2-Bit KV Caches in Multi-Head Latent Attention	MLA quant 2-bit	L	Y	RoLaQ: 2-bit MLA latent with K/V-aware subspace rotation + learned ranges
2410.10819	2024-10-14	DuoAttention: Efficient Long-Context LLM Inference with Retrieval and Streaming Heads	head-level allocation	M	Y	DuoAttention full KV for retrieval heads, streaming for others
2410.19258	2024-10-25	Not All Heads Matter: A Head-Level KV Cache Compression Method with Integrated Retrieval and Reasoning	head-level allocation	L	N	abstract only: HeadKV head-level budgets for retrieval and reasoning (ICLR 2025)
```

## Evaluation protocols and metrics for long-CoT KV compression, and where they disagree

**Accuracy.** Most papers report pass@1 on AIME24/25/26, MATH-500, GPQA-D and LiveCodeBench. How many samples they average over varies a lot. SeerAttention-R uses 64 samples on AIME, 8 on MATH and 16 on GPQA [2506.08889]. VaSE uses 16 or 8 runs [2606.03928], GrowPage 32 [2609.03494], SAW-INT4 and OSCAR 5 seeds [2604.19157, 2605.17757], and CTIR uses greedy decoding on 30–100 items [2606.25519]. The SoK notes that confidence intervals are almost never reported [2609.30854].

**Generation cap.** The cap is the largest hidden variable:
- LongFlow uses 16K [2603.11504].
- SkipKV uses 8K, 10K and 16K [2512.07993].
- Kitty runs its throughput test at 8K and its main lm-eval benchmarks at a 4K cap; only its AIME runs go to 32K [2511.18643].
- SeerAttention-R, SAW-INT4, MixKVQ, OSCAR, ThinKV and 2606.02011 use 32K.

[2606.02011] shows that a 4K–8K cap truncates loops and systematically overstates the end-to-end benefit of low-bit inference. [2601.03043] caps incorrect runaways at 2× the full-attention length to avoid overstating savings. Neither the cap-hit rate nor the cap itself is reported consistently.

**Budget definition.** Eviction papers disagree on what "compression ratio" means:
- R-KV and SkipKV use a fixed budget divided by the mean full-KV length.
- RLKV shows this leaves short samples uncompressed and overstates compression. It uses a per-sample dynamic budget (sparsity × that sample's full length) [2510.08525].
- LongFlow quotes the budget relative to the 16K cap [2603.11504].
- VaSE sets the budget to ≈ the per-task mean length / 4 [2606.03928].

**Length and loops.**
- SeerAttention-R, SkipKV, Lil, Hold-Onto-That-Thought, RLKV and ThinKV report output length.
- Loop and cap metrics are rarer. [2606.02011] defines loop rate (n-gram), hit-limit rate, think-closed rate, TTFA and commit gap. RLKV splits errors into repetitive / incorrect / overlength [2510.08525]. CTIR uses an embedding-similarity repetitiveness score [2606.25519]. Lil uses LZ77 compression ratio [2601.03043].

The direction of the length effect is contested:
- ThinKV says eviction does not lengthen outputs while quantization inflates them up to 5.1× [2510.01290].
- SkipKV, Lil, SeerAttention-R, Hold-Onto-That-Thought and AbridgeKV find that eviction or sparse attention lengthens outputs [2512.07993, 2601.03043, 2506.08889, 2512.12008, 2610.20641].
- RLKV warns that mean length on correct samples is biased toward easier instances [2510.08525].
- TaSQ and KVarN report near-BF16 lengths at 1.25–2.3 bits [2610.03027, 2606.03458].

**Quality beyond accuracy.** Fixed-trace replay shows that eviction can keep answers while invalidating chains. Accuracy rankings anti-correlate with chain validity, while KIVI-2 keeps the chains [2608.01631]. This is a component diagnostic, not end-to-end generation.

**Efficiency.** Metrics are not comparable across papers:
- Kernel speedup only: SeerAttention-R.
- Tokens/s at maximum batch under HuggingFace/FlashAttention-2 without paging, against HF FP16 baselines: Kitty, LongFlow, VaSE, SkipKV.
- Paged-engine metrics such as TPS_sys, per-request TPS and TTFT under swept concurrency: SAW-INT4 in SGLang, RLKV dual pool in SGLang, GrowPage in nano-vLLM, Random Attention in vLLM, UltraQuant in vLLM.
- Wall time for a fixed problem set: RLKV, SkipKV in samples per minute.

Tokens/s rewards length inflation. Only a fixed-problem-set wall time (RLKV Table 3, SkipKV Table 1) comes close to cost per correct answer, and no paper reports cost per correct answer directly. FP8-KV is almost never a baseline. Exceptions are UltraQuant, where FP4 beats FP8 only past FP8's cache capacity, and the B200 capacity table in [2606.02011]. SAW-INT4 argues that per-channel scales, mixed precision, VQ codebooks and token eviction are hard to make paged/fused. It also shows that HF-measured methods fall below SGLang BF16, which undercuts throughput claims made outside a serving engine [2604.19157]. The SoK shows the same 2-bit method's derived speedup ranges from 1.25× to 4.82× depending on the batch/context regime [2609.30854].

**KV-side follow-ups to 2606.25519 / 2606.02011.** No paper found isolates CTIR, loop rate or cap-hit rate under KV-only quantization:
- [2606.00206] includes only joint W4A4KV4: CoT 5.2K→8.0K on R1-Qwen-1.5B MATH-500.
- [2606.02011] reports only KV capacity (max batch), not KV-induced loops.
- VaSE links large-Range value states to both loops under eviction and per-token quantization error [2606.03928].

## Inaccessible or not read
- No full text failed to download in this pass. Rows marked read=N were not read for time reasons (key fact from the abstract only), not because they were inaccessible.
- High-priority unread items for a follow-up pass: 2512.00504 (G-KV), 2605.23200 (AMS), 2610.03007 (AvoKV-E), 2610.20641 (AbridgeKV), 2603.08743 (Zipage), 2609.04971 (BeaconKV), 2506.05333 (Kinetics), 2504.04823 (Quantization Hurts Reasoning?, includes KV quant), 2607.01237 (KARA).
- DesireKV (AAAI 2026) appeared in a web search via ojs.aaai.org with no arXiv id found; not on arXiv as far as found, not read.

## Query log
lit.py searches (`-k 30`; month sweeps with --since):
- "KV cache compression reasoning models" (30 hits)
- "KV cache eviction long chain-of-thought" (11 hits)
- "KV cache reasoning trace redundancy" (6 hits)
- "long generation KV cache compression decoding" (30 hits)
- "KV cache quantization reasoning models" (30 hits)
- "KV cache quantization long chain-of-thought" (7 hits)
- "quantization reasoning length output length increase" (5 hits)
- "low-bit KV cache reasoning accuracy" (11 hits)
- "2-bit KV cache quantization decoding" (29 hits)
- "1-bit KV cache quantization" (30 hits)
- "benchmark KV cache compression reasoning" (30 hits)
- "KV cache compression length inflation reasoning" (0 hits)
- "KV eviction repetition loops reasoning models" (1 hits)
- "cost per correct answer reasoning serving" (1 hits)
- "end-to-end throughput reasoning model serving KV cache" (4 hits)
- "head-level KV cache reasoning RL" (1 hits)
- "SeerAttention-R" (1 hits)
- "RLKV reasoning heads" (1 hits)
- "sparse attention reasoning decoding" (30 hits)
- "KV cache merging reasoning" (11 hits)
- "thinking tokens KV cache" (26 hits)
- "KV cache offloading long decoding" (30 hits)
- "KV cache CPU offload sparse retrieval decode" (3 hits)
- "FP8 KV cache vLLM" (7 hits)
- "FP4 KV cache" (8 hits)
- "NVFP4 KV cache attention kernel" (2 hits)
- "FlashInfer" (30 hits)
- "low-bit KV cache kernel serving system" (3 hits)
- "KV cache quantization SGLang" (19 hits)
- "quantized KV cache throughput batch size memory-bound decode" (1 hits)
- "quantized reasoning models longer outputs" (2 hits)
- "quantization overthinking reasoning" (3 hits)
- "weight quantization reasoning length repetition" (0 hits)
- "KV cache quantization repetition degeneration" (0 hits)
- "reasoning model inference budget truncation length cap" (0 hits)
- "test-time scaling memory bound KV" (7 hits)
- "kinetics test-time scaling memory" (12 hits)
- "reasoning-aware KV cache" (30 hits)
- "KV cache budget reasoning models" (30 hits)
- "eviction reasoning models redundancy attention" (8 hits)
- "token eviction decoding phase reasoning" (5 hits)
- "token inflation quantization" (10 hits)
- "overthinking quantized" (3 hits)
- "KV compression faithfulness reasoning" (2 hits)
- "reasoning model efficient inference survey" (30 hits)
- "Reasoning-Aware Attention Sparsity long-decoding" (6 hits)
- "MorphKV" (1 hits)
- "TreeKV" (1 hits)
- "WindowKV" (1 hits)
- "KeyDiff" (7 hits)
- "PagedEviction" (1 hits)
- "SAW-INT4" (1 hits)
- "Kitty 2-bit KV channel-wise precision boost" (1 hits)
- "G-KV global attention eviction" (1 hits)
- "decoding-time KV eviction" (30 hits)
- "KV cache compression long output" (30 hits)
- "multi-step reasoning KV compression self-reflection" (1 hits)
- "reasoning trace compression step summary KV" (0 hits)
- "hierarchical KV cache GPU CPU reasoning" (1 hits)
- "sparse attention long reasoning training-free" (20 hits)
- "speculative decoding reasoning KV compression" (1 hits)
- "learned KV eviction reasoning" (14 hits)
- "KV cache" --since 2026-10-01 (14 hits)
- "KV cache reasoning" --since 2026-09-01 (23 hits)
- "KV cache reasoning" --since 2026-07-01 (30 hits)
- "KV cache reasoning" --since 2026-05-01 (30 hits)
- "KV cache quantization" --since 2026-09-01 (24 hits)
- "KV cache quantization" --since 2026-05-01 (30 hits)
- "KV cache eviction" --since 2026-07-01 (30 hits)
- "long reasoning decoding memory" --since 2026-05-01 (30 hits)

biblio lookups: 2606.25519 2606.02011 2606.00206 2610.19605 2609.39801 2504.04823, plus two triage batches (about 60 ids) and date lookups for 14 previously digested ids.

WebSearch queries (used only to find arXiv ids):
- "arxiv KV cache compression reasoning models benchmark output length increase eviction 2026" -> ForesightKV 2602.03203, LongFlow 2603.11504, VaSE 2606.03928
- "arxiv G-KV OR TreeKV OR WindowKV OR RaaS reasoning KV cache decoding eviction" -> G-KV 2512.00504, LazyEviction 2506.15969
- "arxiv vLLM SGLang 2-bit 4-bit KV cache quantization kernel serving throughput reasoning" -> SAW-INT4 2604.19157, Kitty 2511.18643
- "arxiv KV cache reasoning models end-to-end throughput per correct OR cost-per-correct compression" -> RLKV 2510.08525, LongFlow; no paper reports cost per correct answer
