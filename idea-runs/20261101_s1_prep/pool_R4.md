# pool_R4 — backward reference snowballing from 12 seeds (+ forward discovery from TaSQ, KVarN, OptR)

Run: 20261101_s1_prep. Seeds: TaSQ 2610.03027, KVarN 2606.03458, OSCAR 2605.17757, OptR 2608.02691, ThinKV 2510.01290, PM-KVQ 2505.18610, QuantMLA 2609.36760, RAQ-MLA 2610.33625, Spend Bytes on Breadth (SBB) 2610.05685, MultiAlloc 2610.18642, UltraQuant 2606.20474, QEvict 2608.05326.

183 resolved arXiv papers (52 rated H). read=Y means a digest exists in papers/ (written by R4 or another agent); key_fact for those comes from the digest. read=N rows were not read and are marked "abstract only". cited_by lists seed short names; "fwd:X" means found by forward discovery from seed X. Relevance: H = decode-time / low-bit (<=2.5 bit) KV quantization, KV compression for reasoning models, or precision/budget allocation; M = general KV compression, eviction or serving that bears on the problem; L = background (weight quantization, kernels, architectures).

## 1. Pool

```tsv
arxiv_id	first_date	title	cited_by_seeds	relevance(H/M/L)	read(Y/N)	key_fact
1911.02150	2019-11-06	Fast Transformer Decoding: One Write-Head is All You Need	PM-KVQ	L	N	abstract only
2210.17323	2022-10-31	GPTQ: Accurate Post-Training Quantization for Generative Pre-trained Transformers	OSCAR,TaSQ	L	N	abstract only
2211.05102	2022-11-09	Efficiently Scaling Transformer Inference	QEvict	L	N	abstract only
2211.10438	2022-11-18	SmoothQuant: Accurate and Efficient Post-Training Quantization for Large Language Models	OSCAR,QuantMLA,RAQ-MLA,TaSQ	L	N	abstract only
2304.01089	2023-04-03	RPTQ: Reorder-based Post-training Quantization for Large Language Models	QuantMLA	L	N	abstract only
2305.13245	2023-05-22	GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints	PM-KVQ,QEvict	L	N	abstract only
2305.17118	2023-05-26	Scissorhands: Exploiting the Persistence of Importance Hypothesis for LLM KV Cache Compression at Test Time	KVarN,QEvict	L	N	abstract only
2306.00978	2023-06-01	AWQ: Activation-aware Weight Quantization for LLM Compression and Acceleration	OSCAR,PM-KVQ,RAQ-MLA,TaSQ	L	N	abstract only
2306.07629	2023-06-13	SqueezeLLM: Dense-and-Sparse Quantization	TaSQ	L	N	abstract only
2306.14048	2023-06-24	H$_2$O: Heavy-Hitter Oracle for Efficient Generative Inference of Large Language Models	KVarN,OSCAR,OptR,PM-KVQ,QEvict,SBB,TaSQ,ThinKV	M	Y	Observes that attention in pretrained LLMs is >95% sparse and that accumulated attention scores follow a power law, so a few "heavy-hitter" tokens dominate. Proposes H2O, a fixed-size KV cache policy that keeps recent tokens plus ...
2307.08691	2023-07-17	FlashAttention-2: Faster Attention with Better Parallelism and Work Partitioning	OSCAR,QEvict,SBB,ThinKV	L	N	abstract only
2307.13304	2023-07-25	QuIP: 2-Bit Quantization of Large Language Models With Guarantees	KVarN,OSCAR,OptR	L	N	abstract only
2308.13137	2023-08-25	OmniQuant: Omnidirectionally Calibrated Quantization for Large Language Models	OSCAR,QuantMLA	L	N	abstract only
2309.06180	2023-09-12	Efficient Memory Management for Large Language Model Serving with PagedAttention	KVarN,MultiAlloc,OSCAR,OptR,QEvict,RAQ-MLA,ThinKV,UltraQuant	M	N	abstract only
2309.17453	2023-09-29	Efficient Streaming Language Models with Attention Sinks	MultiAlloc,OSCAR,PM-KVQ,QEvict,SBB,ThinKV	M	N	abstract only
2310.01801	2023-10-03	Model Tells You What to Discard: Adaptive KV Cache Compression for LLMs	OSCAR	L	N	abstract only
2312.04985	2023-12-08	SparQ Attention: Bandwidth-Efficient LLM Inference	QEvict	L	N	abstract only
2312.05821	2023-12-10	ASVD: Activation-aware Singular Value Decomposition for Compressing Large Language Models	OSCAR	L	N	abstract only
2312.07104	2023-12-12	SGLang: Efficient Execution of Structured Language Model Programs	OSCAR,RAQ-MLA,TaSQ,UltraQuant	M	N	abstract only
2401.06118	2024-01-11	Extreme Compression of Large Language Models via Additive Quantization	TaSQ	L	N	abstract only
2401.18079	2024-01-31	KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization	KVarN,OSCAR,OptR,QEvict,QuantMLA,RAQ-MLA,SBB,TaSQ,ThinKV,UltraQuant	M	N	abstract only
2402.02750	2024-02-05	KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache	KVarN,MultiAlloc,OSCAR,OptR,PM-KVQ,QEvict,QuantMLA,RAQ-MLA,SBB,TaSQ,ThinKV,UltraQuant	H	N	abstract only
2402.04396	2024-02-06	QuIP#: Even Better LLM Quantization with Hadamard Incoherence and Lattice Codebooks	OSCAR,TaSQ	L	N	abstract only
2402.12065	2024-02-19	WKVQuant: Quantizing Weight and Key/Value Cache for Large Language Models Gains More	OSCAR,PM-KVQ	M	N	abstract only
2402.15319	2024-02-23	GPTVQ: The Blessing of Dimensionality for LLM Quantization	TaSQ	L	N	abstract only
2402.18096	2024-02-28	No Token Left Behind: Reliable KV Cache Compression via Importance-Aware Mixed Precision Quantization	PM-KVQ,SBB	H	N	abstract only
2403.01241	2024-03-02	IntactKV: Improving Large Language Model Quantization by Keeping Pivot Tokens Intact	PM-KVQ	L	N	abstract only
2403.04643	2024-03-07	QAQ: Quality Adaptive Quantization for LLM KV Cache	ThinKV	M	N	abstract only
2403.05527	2024-03-08	GEAR: An Efficient KV Cache Compression Recipe for Near-Lossless Generative Inference of LLM	OSCAR,ThinKV	M	N	abstract only
2403.07378	2024-03-12	SVD-LLM: Truncation-aware Singular Value Decomposition for Large Language Model Compression	OSCAR	L	N	abstract only
2403.09636	2024-03-14	Dynamic Memory Compression: Retrofitting LLMs for Accelerated Inference	ThinKV	M	N	abstract only
2403.12544	2024-03-19	AffineQuant: Affine Transformation Quantization for Large Language Models	RAQ-MLA	L	N	abstract only
2404.00456	2024-03-30	QuaRot: Outlier-Free 4-Bit Inference in Rotated LLMs	KVarN,OSCAR,OptR,QuantMLA,RAQ-MLA,SBB	M	N	abstract only
2404.04793	2024-04-07	SqueezeAttention: 2D Management of KV-Cache in LLM Inference via Layer-wise Optimal Budget	MultiAlloc	M	N	abstract only
2404.14469	2024-04-22	SnapKV: LLM Knows What You are Looking for Before Generation	KVarN,OSCAR,QEvict,SBB,TaSQ,ThinKV	M	N	abstract only
2405.03917	2024-05-07	KV Cache is 1 Bit Per Channel: Efficient Large Language Model Inference with Coupled Quantization	TaSQ,ThinKV	H	Y	Coupled Quantization (CQ) jointly vector-quantizes groups of c contiguous channels of each key/value embedding with a learned (optionally Fisher-weighted) k-means codebook per channel group, exploiting inter-channel mutual informa...
2405.04434	2024-05-07	DeepSeek-V2: A Strong, Economical, and Efficient Mixture-of-Experts Language Model	KVarN,PM-KVQ,QuantMLA,RAQ-MLA,UltraQuant	L	N	abstract only
2405.04532	2024-05-07	QServe: W4A8KV4 Quantization and System Co-design for Efficient LLM Serving	PM-KVQ	M	N	abstract only
2405.06219	2024-05-10	SKVQ: Sliding-window Key and Value Cache Quantization for Large Language Models	OSCAR,PM-KVQ,QuantMLA,RAQ-MLA,TaSQ	M	N	abstract only
2405.12532	2024-05-21	PyramidInfer: Pyramid KV Cache Compression for High-throughput LLM Inference	SBB	L	N	abstract only
2405.14256	2024-05-23	ZipCache: Accurate and Efficient KV Cache Quantization with Salient Token Identification	MultiAlloc,OSCAR,QEvict,SBB	M	N	abstract only
2405.14366	2024-05-23	MiniCache: KV Cache Compression in Depth Dimension for Large Language Models	ThinKV	L	N	abstract only
2405.16406	2024-05-26	SpinQuant: LLM quantization with learned rotations	KVarN,OSCAR,QuantMLA,RAQ-MLA	L	N	abstract only
2406.01721	2024-06-03	DuQuant: Distributing Outliers via Dual Transformation Makes Stronger Quantized LLMs	QuantMLA	L	N	abstract only
2406.02069	2024-06-04	PyramidKV: Dynamic KV Cache Compression based on Pyramidal Information Funneling	KVarN,OSCAR,SBB,ThinKV,UltraQuant	M	N	abstract only
2406.03482	2024-06-05	QJL: 1-Bit Quantized JL Transform for KV Cache Quantization with Zero Overhead	UltraQuant	M	Y	Quantizes keys by a random Gaussian (orthogonalized) JL projection followed by the sign bit, and estimates q·k with an unbiased asymmetric estimator (query projected but unquantized). Outlier channels get a separate QJL instance w...
2406.10774	2024-06-16	Quest: Query-Aware Sparsity for Efficient Long-Context LLM Inference	PM-KVQ,QEvict,ThinKV	M	Y	Shows that which tokens are critical depends strongly on the current query, so history-based eviction (H2O) has low recall of top-attended tokens. Quest keeps the whole KV cache, stores per-page channel-wise min and max of keys as...
2406.11235	2024-06-17	QTIP: Quantization with Trellises and Incoherence Processing	KVarN	L	N	abstract only
2406.11430	2024-06-17	A Simple and Effective $L_2$ Norm-Based Strategy for KV Cache Compression	QEvict	L	N	abstract only
2406.13035	2024-06-18	D2O: Dynamic Discriminative Operations for Efficient Long-Context Inference of Large Language Models	KVarN	L	N	abstract only
2406.14909	2024-06-21	Mixture of Attention Spans: Optimizing LLM Inference Efficiency with Heterogeneous Sliding-Window Lengths	PM-KVQ	L	N	abstract only
2407.00079	2024-06-24	Mooncake: A KVCache-centric Disaggregated Architecture for LLM Serving	RAQ-MLA	L	N	abstract only
2407.08454	2024-07-11	Model Tells You Where to Merge: Adaptive KV Cache Merging for LLMs on Long-Context Tasks	TaSQ,ThinKV	L	N	abstract only
2407.08608	2024-07-11	FlashAttention-3: Fast and Accurate Attention with Asynchrony and Low-precision	OSCAR	L	N	abstract only
2407.10960	2024-07-15	Fast Matrix Multiplications for Lookup Table-Quantized LLMs	UltraQuant	L	N	abstract only
2407.11550	2024-07-16	Ada-KV: Optimizing KV Cache Eviction by Adaptive Budget Allocation for Efficient LLM Inference	QEvict,SBB,ThinKV	H	N	abstract only
2407.21018	2024-07-30	ThinK: Thinner Key Cache by Query-Driven Pruning	TaSQ	M	N	abstract only
2407.21118	2024-07-30	Palu: Compressing KV-Cache with Low-Rank Projection	OSCAR,SBB,ThinKV	M	Y	Palu factorizes the K/V projection weights by SVD, caches the low-rank latent h = x A, and reconstructs keys/values on the fly. For values (and for non-RoPE keys) it fuses the reconstruction matrix into neighbouring weights; for R...
2408.03675	2024-08-07	NACL: A General and Effective KV Cache Eviction Framework for LLMs at Inference Time	ThinKV	L	N	abstract only
2410.03111	2024-10-04	LoRC: Low-Rank Compression for LLMs KV Cache with a Progressive Compression Strategy	ThinKV	L	N	abstract only
2410.09426	2024-10-12	FlatQuant: Flatness Matters for LLM Quantization	QuantMLA,RAQ-MLA	L	N	abstract only
2410.14731	2024-10-16	MatryoshkaKV: Adaptive KV Compression via Trainable Orthogonal Projection	OSCAR	L	N	abstract only
2410.19258	2024-10-25	Not All Heads Matter: A Head-Level KV Cache Compression Method with Integrated Retrieval and Reasoning	ThinKV	H	N	abstract only
2410.21465	2024-10-28	ShadowKV: KV Cache in Shadows for High-Throughput Long-Context LLM Inference	SBB,ThinKV	M	N	abstract only
2411.17089	2024-11-26	KVPR: Efficient LLM Inference with I/O-Aware KV Cache Partial Recomputation	MultiAlloc	L	N	abstract only
2411.17525	2024-11-26	Pushing the Limits of Large Language Model Quantization via the Linearity Theorem	KVarN	L	N	abstract only
2411.18077	2024-11-27	MiniKV: Pushing the Limits of LLM Inference via 2-Bit Layer-Discriminative KV Cache	OSCAR,ThinKV	M	N	abstract only
2412.05896	2024-12-08	XKV: Personalized KV Cache Memory Reduction for Long-Context LLM Inference	MultiAlloc	M	N	abstract only
2412.12706	2024-12-17	More Tokens, Lower Precision: Towards the Optimal Token-Precision Trade-off in KV Cache Compression	SBB	H	N	abstract only
2412.13171	2024-12-17	Compressed Chain of Thought: Efficient Reasoning Through Dense Representations	ThinKV	L	N	abstract only
2412.18547	2024-12-24	Token-Budget-Aware LLM Reasoning	ThinKV	L	N	abstract only
2501.02625	2025-01-05	HALO: Hadamard-Assisted Lower-Precision Optimization for LLMs	OSCAR	L	N	abstract only
2501.13987	2025-01-23	OstQuant: Refining Large Language Model Quantization with Orthogonal and Scaling Transformations for Better Distribution Fitting	QuantMLA	L	N	abstract only
2501.16383	2025-01-25	RotateKV: Accurate and Robust 2-Bit KV Cache Quantization for LLMs via Outlier-Aware Adaptive Rotations	OSCAR,OptR,PM-KVQ,QuantMLA,RAQ-MLA	H	N	abstract only
2502.00527	2025-02-01	PolarQuant: Leveraging Polar Transformation for Efficient Key Cache Quantization and Decoding Acceleration	KVarN	M	N	abstract only
2502.02617	2025-02-04	PolarQuant: Quantizing KV Caches with Polar Transformation	QuantMLA	M	N	abstract only
2502.03805	2025-02-06	CriticalKV: Optimizing KV Cache Eviction from an Output Perturbation Perspective	QEvict	M	N	abstract only
2502.04420	2025-02-06	KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization for Efficient and Nearly Lossless LLM Inference	MultiAlloc,PM-KVQ,SBB	H	Y	Searches offline for a layer-wise (key-bits, value-bits) precision pair per layer under a memory constraint, using multi-objective optimization over a pruned search space (intra-layer Pareto pruning of precision pairs, inter-layer...
2502.11089	2025-02-16	Native Sparse Attention: Hardware-Aligned and Natively Trainable Sparse Attention	QuantMLA,ThinKV	L	Y	NSA replaces full attention with three gated branches over GQA/MQA KV: compressed coarse tokens (learned block compression), selected fine-grained blocks (top-n blocks scored by the compressed branch's attention probabilities), an...
2502.11147	2025-02-16	RaaS: Reasoning-Aware Attention Sparsity for Efficient LLM Reasoning	SBB,ThinKV	H	N	abstract only
2502.12067	2025-02-17	TokenSkip: Controllable Chain-of-Thought Compression in LLMs	ThinKV	L	N	abstract only
2502.12134	2025-02-17	SoftCoT: Soft Chain-of-Thought for Efficient Reasoning with LLMs	ThinKV	L	N	abstract only
2502.12665	2025-02-18	A$^2$ATS: Retrieval-Based KV Cache Reduction via Windowed Rotary Position Embedding and Query-Aware Vector Quantization	ThinKV	L	N	abstract only
2502.14882	2025-02-15	CalibQuant: 1-Bit KV Cache Quantization for Multimodal LLMs	ThinKV	M	N	abstract only
2502.15075	2025-02-20	Quantize What Counts: More for Keys, Less for Values	OSCAR,PM-KVQ	H	Y	The paper argues, from weight-norm training dynamics and a norm-based quantization error bound, that key projections have larger Frobenius/spectral norms than value projections, so under a fixed memory budget giving keys more bits...
2502.15589	2025-02-21	LightThinker: Thinking Step-by-Step Compression	ThinKV	L	N	abstract only
2503.00979	2025-03-02	Dialogue Without Limits: Constant-Sized KV Caches for Extended Responses in LLMs	ThinKV	M	N	abstract only
2503.05179	2025-03-07	Sketch-of-Thought: Efficient LLM Reasoning with Adaptive Cognitive-Inspired Sketching	ThinKV	L	N	abstract only
2503.06692	2025-03-09	InftyThink: Breaking the Length Limits of Long-Context Reasoning in Large Language Models	ThinKV	L	N	abstract only
2503.08311	2025-03-11	Mind the Memory Gap: Unveiling GPU Bottlenecks in Large-Batch LLM Inference	ThinKV	M	N	abstract only
2503.12340	2025-03-16	SVD-LLM V2: Optimizing Singular Value Truncation for Large Language Model Compression	OSCAR	L	N	abstract only
2503.18893	2025-03-24	xKV: Cross-Layer KV-Cache Compression via Aligned Singular Vector Extraction	OSCAR,SBB	L	N	abstract only
2504.04823	2025-04-07	Quantization Hurts Reasoning? An Empirical Study on Quantized Reasoning Models	QuantMLA	M	N	abstract only
2504.07986	2025-04-07	SEAL: Steerable Reasoning Calibration of Large Language Models for Free	ThinKV	L	N	abstract only
2504.19874	2025-04-28	TurboQuant: Online Vector Quantization with Near-optimal Distortion Rate	KVarN,OSCAR,OptR,QuantMLA,SBB,UltraQuant	H	Y	Data-oblivious online vector quantizer. A random rotation makes each coordinate of a unit vector follow a concentrated Beta (near-Gaussian) law with near-independent coordinates, so per-coordinate Lloyd-Max scalar codebooks (preco...
2505.10938	2025-05-16	Accurate KV Cache Quantization with Outlier Tokens Tracing	MultiAlloc	H	N	abstract only
2505.13866	2025-05-20	Reasoning Path Compression: Compressing Generation Trajectories for Efficient LLM Reasoning	ThinKV	M	N	abstract only
2505.18231	2025-05-23	NSNQuant: A Double Normalization Approach for Calibration-Free Low-Bit Vector Quantization of KV Cache	OptR,TaSQ	H	N	abstract only
2505.18610	2025-05-24	PM-KVQ: Progressive Mixed-precision KV Cache Quantization for Long-CoT LLMs	MultiAlloc,OSCAR,SBB,ThinKV	H	Y	Post-training KV-cache quantization for long-CoT dense LLMs. Progressive quantization stores KV in 16 bits first and, once the per-block memory budget fills, shrinks existing cache bit-width 16->8->4->2 via an "Equivalent Right Sh...
2505.23416	2025-05-29	KVzip: Query-Agnostic KV Cache Compression with Context Reconstruction	KVarN,ThinKV	L	N	abstract only
2505.24133	2025-05-30	R-KV: Redundancy-aware KV Cache Compression for Reasoning Models	SBB,ThinKV	H	Y	Targets decoding-time KV compression for reasoning models (DeepSeek-R1-Distill 7B/8B/14B), whose outputs are >8x longer than reference solutions and highly repetitive. Every buffer of generated tokens, R-KV rescores candidates wit...
2505.24357	2025-05-30	ReCalKV: Low-Rank KV Cache Compression via Head Reordering and Offline Calibration	OSCAR	L	N	abstract only
2506.04985	2025-06-05	FPTQuant: Function-Preserving Transforms for LLM Quantization	QuantMLA	L	N	abstract only
2506.08018	2025-05-18	KVmix: Gradient-Based Layer Importance-Aware Mixed-Precision Quantization for KV Cache	MultiAlloc	H	N	abstract only
2506.08889	2025-06-10	SeerAttention-R: Sparse Attention Adaptation for Long Reasoning	SBB	M	Y	A learned block-sparse attention for decoding of reasoning models. A lightweight AttnGate (pooled K + linear, with shared sparsity per GQA group) is self-distilled to mimic block-wise attention maps of the frozen model (OpenR1-Mat...
2506.13059	2025-06-16	Multipole Attention for Efficient Long Context Reasoning	ThinKV	M	N	abstract only
2506.15969	2025-06-19	LazyEviction: Lagged KV Eviction with Attention Pattern Observation for Efficient Long Reasoning	SBB,ThinKV	H	Y	Identifies Token Importance Recurrence (TIR) in reasoning traces: tokens (problem conditions, intermediate results) get low attention for a while and then are attended again; >95% of tokens show recurrence. Proposes LazyEviction, ...
2506.19143	2025-06-23	Thought Anchors: Which LLM Reasoning Steps Matter?	ThinKV	L	Y	Analyzes reasoning traces (mainly R1-Distill-Qwen-14B on MATH, plus Qwen3-30B-A3B on MMLU) at the sentence level. It measures each sentence's counterfactual importance by resampling, finds "receiver heads" that focus attention fro...
2507.14204	2025-07-14	LaCache: Ladder-Shaped KV Caching for Efficient Long-Context Modeling of Large Language Models	ThinKV	L	N	abstract only
2507.21433	2025-07-29	ReasonCache: Accelerating Large Reasoning Model Serving through KV Cache Sharing	ThinKV	M	N	abstract only
2508.16134	2025-08-22	CommonKV: Compressing KV Cache with Cross-layer Parameter Sharing	OSCAR	L	N	abstract only
2509.15038	2025-09-18	Value-Guided KV Compression for LLMs via Approximated CUR Decomposition	SBB	M	N	abstract only
2509.22944	2025-09-26	SINQ: Sinkhorn-Normalized Quantization for Calibration-Free Low-Precision LLM Weights	KVarN	L	N	abstract only
2509.23202	2025-09-27	Bridging the Gap Between Promise and Performance for Microscaling FP4 Quantization	OSCAR	M	N	abstract only
2510.01290	2025-10-01	ThinKV: Thought-Adaptive KV Cache Compression for Efficient Reasoning Models	OSCAR,SBB	H	Y	Hybrid quantization + eviction for long-output reasoning models. Attention sparsity (calibrated on a few layers) classifies each 128-token CoT segment into Reasoning, Execution or Transition thoughts. Think-Before-Quantize assigns...
2510.05373	2025-10-06	KVLinC : KV Cache Quantization with Hadamard Rotation and Linear Correction	OSCAR	M	N	abstract only
2510.08525	2025-10-09	Which Heads Matter for Reasoning? RL-Guided KV Cache Compression	SBB	H	Y	RLKV attaches a per-(layer, KV-head) gate α mixing full-causal and sink+local attention, freezes the LLM, and trains only the gates with GRPO (no KL term) plus an adaptive L1 penalty, using self-distilled curriculum data (3K DeepS...
2510.10964	2025-10-13	Not All Bits Are Equal: Scale-Dependent Memory Optimization Strategies for Reasoning Models	SBB	H	Y	An empirical study (more than 1,700 configurations, Qwen3 family, AIME25 and GPQA-Diamond) of how to spend a fixed memory budget for reasoning models: weight precision vs model size vs generation length vs parallel scaling, and KV...
2510.13334	2025-10-15	Taming the Fragility of KV Cache Eviction in LLM Inference	QEvict	M	Y	DefensiveKV: max-over-window (worst-case) importance aggregation + head prior; prompt-cache eviction only; QEvict baseline; INT4 stacking costs <1 pt LongBench
2511.01815	2025-11-03	KV Cache Transform Coding for Compact Storage in LLM Inference	SBB	M	N	abstract only
2511.06029	2025-11-08	Lethe: Layer- and Time-Adaptive KV Cache Pruning for Reasoning-Intensive LLM Serving	SBB	H	Y	Lethe: decode-time eviction with layerwise attention-drop budgets + decayed-attention recency retention; MATH500 R1-Qwen-7B 85.4 vs 86.4 FullKV; no precision allocation, no length/loop metrics
2511.18643	2025-11-23	Kitty: Accurate and Efficient 2-bit KV Cache Quantization with Dynamic Channel-wise Precision Boost	KVarN,OSCAR,OptR,SBB	H	Y	Builds on KIVI (per-channel K, per-token V, FP16 residual) with two additions: keep the first 32 tokens in full precision, and boost a small fraction (12.5% "Kitty", 25% "Kitty-Pro") of key channels, chosen at runtime by mean magn...
2512.00504	2025-11-29	G-KV: Decoding-Time KV Cache Eviction with Global Attention	SBB	H	N	abstract only
2512.07993	2025-12-08	SkipKV: Selective Skipping of KV Generation and Storage for Efficient Inference with Large Reasoning Models	SBB	H	Y	Training-free sentence-level KV management for reasoning models. (1) Evicts whole sentences scored by pairwise sentence-embedding similarity (semantic redundancy) instead of single tokens; (2) adds a SEAL-style steering vector (ex...
2512.12008	2025-12-12	Hold Onto That Thought: Assessing KV Cache Compression On Reasoning	SBB	H	Y	A benchmark study of decode-enabled KV eviction (H2O, SnapKV-D, R-KV, KNorm, StreamingLLM, PyramidKV) on long-reasoning tasks (GSM8K, MATH500 and others) for reasoning models (R1-Distill Llama-8B and Qwen-7B, Nemotron-Nano-8B) and...
2512.12895	2025-12-15	Wait, Wait, Wait... Why Do Reasoning Models Loop?	SBB	M	Y	Loop metric: 30-gram repeated >=20 times; low-temperature looping 76% (R1-Qwen-1.5B) vs 37% (32B); more on hard AIME problems; temporally correlated errors cause loops
2512.19206	2025-12-22	MixKVQ: Query-Aware Mixed-Precision KV Cache Quantization for Long-Context Reasoning	MultiAlloc,SBB	H	Y	MixKVQ is a plug-and-play key-cache mixed-precision scheme for long-CoT reasoning: key channels get BF16 / INT4 / INT2 according to a salience A_d = I_d * S_d (accumulated query magnitude per channel times key quantization scale),...
2602.10718	2026-02-11	SnapMLA: Efficient Long-Context MLA Decoding via Hardware-Aware FP8 Quantized Pipelining	QuantMLA,RAQ-MLA	M	N	abstract only
2603.05451	2026-03-05	FlashAttention-4: Algorithm and Kernel Pipelining Co-Design for Asymmetric Hardware Scaling	OSCAR	L	N	abstract only
2603.17946	2026-03-18	CARE: Covariance-Aware and Rank-Enhanced Decomposition for Enabling Multi-Head Latent Attention	OSCAR	L	Y	Post-hoc GQA->MLA conversion at KV-parity (Llama-3.1-8B, Qwen3-4B, others to 70B). Replaces weight-only SVD by activation-covariance-weighted SVD of sqrt(C)W for W_K and W_V, allocates rank across layers by greedy water-filling on...
2604.04722	2026-04-06	Don't Waste Bits! Adaptive KV-Cache Quantization for Lightweight On-Device LLMs	SBB	M	Y	A learned token-level KV precision controller for on-device LLMs: for each decoded token, a small MLP takes three saliency features -- next-token predictive entropy, token rarity (smoothed self-information of token frequency), and...
2604.04921	2026-04-06	TriAttention: Efficient Long Reasoning with Trigonometric KV Compression	SBB	H	N	abstract only
2604.17695	2026-04-20	MoE-nD: Per-Layer Mixture-of-Experts Routing for Multi-Axis KV Cache Compression	MultiAlloc	M	N	abstract only
2604.19157	2026-04-21	SAW-INT4: System-Aware 4-Bit KV-Cache Quantization for Real-World LLM Serving	OSCAR	H	Y	Asks which INT4 KV methods survive real serving constraints (paged blocks, coalesced access, fused FlashAttention-style decode). It argues token eviction, mixed precision, channel-wise scales, codebook lookups and PCA/SVD bases al...
2605.06675	2026-04-22	RateQuant: Optimal Mixed-Precision KV Cache Quantization via Rate-Distortion Theory	SBB	H	Y	RateQuant allocates bit-widths per (layer, KV head) and separately for K and V, offline, by reverse water-filling. Per-head sensitivity w_i is the mean squared gradient of LM loss w.r.t. K or V of that head on 16x512-token calibra...
2605.08114	2026-04-27	Statistical Inference and Quality Measures of KV Cache Quantisations Inspired by TurboQuant	UltraQuant	M	N	abstract only
2605.08317	2026-05-08	RDKV: Rate-Distortion Bit Allocation for Joint Eviction and Quantization of the KV Cache	SBB	H	Y	RDKV: reverse water-filling over {0,2,4,8,16} bits per V-token / K-channel per head; eviction = 0-bit end of same curve; allocated once after prefill (decode-phase is future work)
2605.17170	2026-05-16	TriAxialKV: Toward Extreme Low-Precision KV-Cache Quantization for Agentic Inference Tasks	SBB	H	Y	TriAxialKV: INT2/INT4 per (recency x modality x semantic-role) tag for agent prefill in SGLang; decode-generated tokens all INT4; SGLang FP4 KV unstable (-7.1 on Qwen3-14B BFCL); 1.26-1.52x throughput
2605.17757	2026-05-18	OSCAR: Offline Spectral Covariance-Aware Rotation for 2-bit KV Cache Quantization	OptR,QuantMLA,RAQ-MLA	H	Y	INT2 KV-cache quantization for long reasoning traces. Offline, from one small calibration pass (8878 tokens of MMLU-style text), it estimates attention-aware covariances and builds fixed per-layer rotations for keys (R_K = U_Q H_H...
2605.18856	2026-05-13	SPHERICAL KV: Angle-Domain Attention and Rate-Distortion Retention for Efficient Long-Context Inference	SBB	M	N	abstract only
2605.19660	2026-05-19	OScaR: The Occam's Razor for Extreme KV Cache Quantization in LLMs and Beyond	QuantMLA,RAQ-MLA	H	Y	OScaR: Hadamard on Q/K then token-norm scaling before per-channel INT2 (fixes Token Norm Imbalance); LongBench/NIAH near-lossless; no long-CoT eval; up to 3.0x decode, 4.1x throughput on H20
2606.03458	2026-06-02	KVarN: Variance-Normalized KV-Cache Quantization Mitigates Error Accumulation in Reasoning Tasks	RAQ-MLA,SBB	H	Y	Argues that prior KV quantizers are evaluated in prefill-like settings, while in long decoding the quantized cache feeds later layers and timesteps so errors accumulate, driven mainly by wrong per-token scales (magnitude error). K...
2606.03928	2026-06-02	Value-Aware Stochastic KV Cache Eviction for Reasoning Models	SBB	H	Y	Training-free decode-time eviction for reasoning models. It finds a small fraction of value vectors with abnormally large Range(v)=max−min; evicting them sends models into repetitive self-reflection loops. VaSE-AttnV reserves N_v ...
2606.08382	2026-06-07	STAR-KV: Low-Rank KV Cache Compression via Soft Thresholding for Adaptive Rank Control	SBB,fwd:KVarN	M	N	abstract only
2606.09864	2026-06-01	Alignment Collapse Under KV Cache Quantization: Diagnosis and Mitigation	fwd:KVarN	M	N	abstract only
2606.11164	2026-06-09	ReasonAlloc: Hierarchical Decoding-Time KV Cache Budget Allocation for Reasoning Models	SBB	H	Y	Training-free, decoding-time non-uniform KV budget allocation for long-CoT reasoning models. An offline probing pass measures each layer's token demand (smallest top-attention set reaching mass rho = 0.93) and preallocates layer b...
2606.23406	2026-06-22	HyperQuant: A Rate-Distortion-Optimal Quantization Pipeline for Large Language and Diffusion Models	fwd:TaSQ	L	N	abstract only
2606.24033	2026-06-23	Block-GTQ: RoPE-Block Rate Allocation for KV-Cache Quantization	fwd:KVarN,fwd:OptR	H	Y	Block-GTQ allocates key-cache precision across the 2-D RoPE frequency blocks of each (layer, KV head), statically from calibration. A blockwise logit-error bound |delta K| <= sum_i ||q^(i)|| ||e_k^(i)|| motivates a label-free scor...
2606.25519	2026-06-24	Quantization Inflates Reasoning: Token Inflation as a Hidden Cost of Low-Bit Reasoning Models	SBB	H	Y	A measurement study of weight-only PTQ (RTN, GPTQ, AWQ, HQQ, ParoQuant; INT4/INT3, group 128) on Qwen3-4B-Thinking-2507, Phi-4-Reasoning-Plus and Qwen3-30B-A3B-Thinking. It defines the CoT Token Inflation Ratio (CTIR), shows PTQ o...
2606.26472	2026-06-25	EpiKV: Epiphany-Aware KV Cache Eviction Without the Attention Matrix	SBB	H	Y	EpiKV is a training-free decode-time evictor for reasoning models (R1-Distill Llama-8B and Qwen-7B; MATH-500, AIME, GPQA). It scores each token at write time by a drift-corrected hidden-state shift: a rolling z-score of the residu...
2606.31519	2026-06-30	RaBitQCache: Rotated Binary Quantization for KVCache in Long Context LLM Inference	fwd:TaSQ	M	Y	RaBitQCache (ICML 2026) is a sparse-attention framework, not a compressed-storage KV quantizer. It builds a randomized-rotation binary (RaBitQ-style 1-bit) index of the keys and estimates q·k with binary-INT4 arithmetic as an unbi...
2607.01065	2026-07-01	GSRQ: Gain-Shape Residual Quantization for Sub-1-bit KV Cache	fwd:TaSQ	H	Y	GSRQ: gain-shape K-means in residual VQ; Llama-3-8B MATH-500 FP16 20.4 vs GSRQ 2-bit 19.0, 1-bit 14.2 (KIVI-1 0.8); not on reasoning models; Triton decode 1.6-3.4x
2607.12550	2026-07-14	A JoLT for the KV cache: Near-Lossless KV Cache Compression via Joint Rank-bit Allocation	fwd:KVarN	M	Y	JoLT: partial Tucker + rotated low-bit residual, Lagrangian rank/bit allocation for prefill cache only; generated tokens dense; fused kernel slower than BF16 attention
2607.17019	2026-07-19	Regularize or Localize: When Training-Time KV-Cache Geometry Pays Under Quantization	fwd:KVarN	L	N	abstract only
2607.20538	2026-07-10	Codec-Gauge: Learning Compression-Friendly Gauges for Transformer KV Caches	fwd:TaSQ	L	N	abstract only
2608.01631	2026-08-03	Does Accuracy Equal Evidence? Reasoning Faithfulness under KV Cache Compression	SBB,fwd:KVarN	H	Y	An evaluation paper (EMNLP 2026 Findings). It introduces fixed-trace replay: a Full-KV run produces <think>r</think>; each compression method then prefills q‖r with its own compressed cache of r (question cache protected) and rege...
2608.04074	2026-08-04	Spend Bits Where Queries Look: KV Cache Vector Quantization with Attention-Preserving Transforms	TaSQ,fwd:TaSQ	H	Y	NOVA-KV: non-orthogonal M_q-weighted key transform + equal-volume VQ at 2.22 BPE; RULER 128K Qwen3-8B 75.4 vs OSCAR 25.3 (BF16 83.4); OSCAR collapses on GPT-OSS-20B; SGLang decode ~= OSCAR speed
2608.04771	2026-08-05	Fewer Tokens, Smaller Cache: Reward-Coordinated Efficient Reasoning	SBB	M	N	abstract only
2608.05326	2026-08-05	QEvict: Recoverable Quantized KV Eviction for Attention-Drift-Robust Long-Context Decoding	SBB	H	Y	Questions two assumptions of KV eviction — that token importance is stable enough for permanent deletion and that a binary keep/evict decision suffices. Manages history as contiguous windows ranked by cumulative attention and assi...
2608.07915	2026-08-08	SPECTRA: Pushing the KV Cache Beyond the 2-Bit Cliff via Spectral Transform Coding	fwd:KVarN	H	Y	SPECTRA is a training-free transform codec. It factorizes each K/V projection with a G-weighted SVD (G is the activation second moment; the whitened weight is G^{1/2}W), caches an energy-ordered rank-r latent instead of K/V, and a...
2608.08081	2026-08-08	RotaryQuant: Fitting 120B MoE Models on Consumer Hardware via Fused Compressed-Space Attention	fwd:OptR	L	N	abstract only
2608.15797	2026-08-16	KV-Rescue: Recovering Reasoning Language Model KV Eviction Loss via Stepwise Interleaving	SBB,TaSQ	H	Y	Argues that accuracy lost to KV eviction is an information gap rather than a capability gap: an evicted 7B model and a full-cache 1.5B model make complementary errors, and an oracle choice between them recovers 79% of the eviction...
2608.23599	2026-08-19	Squeezing the Cache, Preserving the Truth: Monotonic Equipotential Allocation with Geodesia-KV	fwd:KVarN	L	Y	Geodesia-KV is a training-free KV policy family that (i) assigns each 64-token block a level on a monotone precision ladder {16,8,4,2,1(centroid)} from causal EMA attention mass aggregated over the GQA group, via a Lagrangian/anal...
2608.23962	2026-08-25	More GPUs or a Smaller Cache? Tensor Parallelism versus KV Compression for Memory-Bound LLM Serving	fwd:KVarN	M	Y	Simulator study: KV compression 1.20-2.00x cheaper per token than tensor parallelism below ~36B params/80GB, but worsens per-token latency 8-93%; no quality, no long context, no dequant cost
2608.30076	2026-08-30	Budget-Aware Compression Pipeline for Single-GPU LLM Inference: Methods, Trade-offs, and Coupling Effects	fwd:KVarN	L	N	abstract only
2609.03430	2026-09-03	Random Attention: Rethinking KV Cache Eviction for Efficient Reasoning	SBB	H	Y	Tests whether the selection score of KV eviction matters for reasoning models. Random Attention pins the entire prompt and keeps a uniformly random top-K of the generated trace independently per KV head, with no scoring pass. Acro...
2609.04263	2026-09-02	Quality Recovery for Quantized KV Caches via Low-Rank Attention Adaptation	fwd:KVarN,fwd:OptR	M	Y	The paper keeps a KV quantizer fixed (affine 4-bit, KIVI K2V2, KVarN K4V2, 2-bit affine) and distills the floating-cache model into low-rank updates of the Q/K/V projections. The student runs with the physically packed incremental...
2609.13205	2026-08-16	Self-Indexing Attention for Compression-Compatible Sparse Long-Context LLM Inference	fwd:KVarN	L	N	abstract only
2609.19880	2026-09-17	D-Quant: Driftable Entropy Coding for KV Cache Quantization	fwd:TaSQ	M	N	abstract only
2609.24298	2026-09-21	KV-COBRA: KV Cache Compression via Co-Optimized Bit-Rank Allocation	MultiAlloc,fwd:KVarN	H	Y	KV-COBRA co-optimizes, per (layer, head), the retained SVD rank r and bit width b (Hadamard-rotated scalar quantization of the projected coefficients) under a global byte budget: inner per-head enumeration of (r, b=B/r), outer dam...
2609.35800	2026-09-18	HeadGuard: Selective Head Protection for Low-Bit VLM KV-Cache Quantization	fwd:KVarN	M	N	abstract only
2609.36032	2026-09-28	TORQUE: Optimizing What (not) to Quantize Before and After Rotation	fwd:OptR	M	N	abstract only
2609.38121	2026-09-29	WUSH-KV: KV Cache Quantization with Data-Adaptive Transforms	fwd:OptR,fwd:TaSQ	H	Y	WUSH-KV adapts WUSH, a data-aware transform built from the second-order statistics of both factors of a matrix product, to KV-cache quantization. Separate key and value transforms are built from calibration data. The value transfo...
2610.09202	2026-10-06	Few Bits, One Law: Toward W2A4KV2	fwd:TaSQ	M	N	abstract only
2610.09827	2026-10-07	Dual-QK: Sharp Queries and Flat Keys for Prunable 2-bit KV Caches	fwd:KVarN,fwd:OptR	H	Y	Dual-QK replaces the shared orthogonal rotation of rotation-based KV quantization with a paired non-orthogonal query/key transform (A for queries, B for keys, A B^T = I): partial key whitening flattens key scales for INT2, while a...
2610.10381	2026-10-07	ResidualQuant: KV Cache Quantization for Looped Transformers with 2-Bit Residuals	fwd:KVarN	L	N	abstract only
2610.15384	2026-10-11	E8 Lattice Key Quantization for Low-Bit KV-Cache Compression	fwd:TaSQ	H	Y	The paper vector-quantizes keys with the E8 lattice (8-dim blocks, the densest 8-D sphere packing) at a 2-bit key payload, with scalar 2-bit values (k2v2). Table-based asymmetric scoring computes q·k from a precomputed query looku...
2610.16289	2026-10-12	Fast Quantized Johnson$-$Lindenstrauss Transforms	fwd:TaSQ	L	N	abstract only
2610.19605	2026-10-14	PN-Mix: Pair-Norm Guided Mixed-Precision Key Cache Quantization for Efficient Long-Output LLM Inference	fwd:KVarN	H	Y	PN-Mix gives higher precision to post-RoPE key channel pairs with large query-key pair-norm product sigma_{h,i} (mean ||q_i|| over GQA query heads times mean ||k_i||), computed once at prefill and reused across long decoding; sink...
2610.20686	2026-10-14	RoLaQ: Joint Rotation and Range Calibration for 2-Bit KV Caches in Multi-Head Latent Attention	fwd:OptR	H	Y	RoLaQ quantizes the shared MLA content latent to 2 bits. Offline, with frozen weights, it refines a shared rotation within subspaces defined by the frozen key and value up-projections (K/V-aware) and jointly learns quantization ra...
2610.23796	2026-10-16	FuTransformer: FP8 prefill and INT4 decode for Llama-style inference on Hopper	fwd:KVarN	M	N	abstract only
2610.24991	2026-10-18	Certified Sparse Attention via Perturbed Retrieval	fwd:KVarN	L	N	abstract only
2610.33076	2026-10-21	Double KV Cache Optimization on Apple Silicon: Block-FP4, Radial Quantization, and Fused Metal Kernels	fwd:KVarN	L	N	abstract only
```

## 2. Seed -> baselines it compares against

| Seed | Baselines actually run (from the paper's baseline / setup section) |
|---|---|
| TaSQ 2610.03027 | CQ 2405.03917 (pre-RoPE VQ), NSNQuant 2505.18231, NovaKV = "Spend Bits Where Queries Look" 2608.04074 (post-RoPE VQ; K codebook matched to 1,024 centroids); BF16 [§5.1 "Baselines and bit accounting"] |
| KVarN 2606.03458 | KIVI 2402.02750, QuaRot 2404.00456, KVQuant-1% 2401.18079, PolarQuant 2502.00527 (needs 4-bit K), TurboQuant 2504.19874 (3K/3V via vLLM PR #38479, first and last two layers unquantized), Kitty 2511.18643; App F: SnapKV 2404.14469, PyramidKV 2406.02069, KVzip 2505.23416 (prompt-only eviction at 7x) |
| OSCAR 2605.17757 | Group A (reported numbers only, no fused kernels): KIVI, Kitty. Group B: BF16, naive INT2/INT4, QuaRot-style Hadamard, block-diagonal Hadamard SAW-INT4 2604.19157, TurboQuant (official vLLM PR #38479, mixed precision disabled) |
| OptR 2608.02691 | BF16, TurboQuant (no MP), QuaRot-INT2, OSCAR; OptR applied on top of QuaRot and OSCAR; all with BF16 sink + recent windows |
| ThinKV 2510.01290 | Eviction: H2O 2306.14048, RaaS 2502.11147, R-KV 2505.24133, LazyEviction 2506.15969; quantization: KIVI, PM-KVQ 2505.18610; throughput vs R-KV (seq/ovl gather) |
| PM-KVQ 2505.18610 | RotateKV 2501.16383, KIVI, MiKV 2402.18096; KVTuner 2502.04420 in App C.4 |
| QuantMLA 2609.36760 | RTN, SmoothQuant† 2211.10438 and QuaRot† adapted to MLA (no prior joint INT4 MLA content+RoPE cache method) |
| RAQ-MLA 2610.33625 | KVarN (MLA mode), QuaRot and OSCAR applied to the MLA latent, positional key left in full precision |
| Spend Bytes on Breadth 2610.05685 | SnapKV-D, R-KV, H2O, StreamingLLM 2309.17453, random eviction, VaSE 2606.03928, KIVI-4, rank-32 low-rank, RDKV 2605.08317 (decode mode, approx. byte match), ThinKV (own re-implementation) |
| MultiAlloc 2610.18642 | OTT 2505.10938 (token-wise preservation), PM-KVQ (layer-wise mixed precision), KVmix 2506.08018 |
| UltraQuant 2606.20474 | vLLM OSS TurboQuant (Kurtić et al. 2026, Red Hat blog, not on arXiv), BF16 AITER FlashAttention, hardware FP8 KV, Ultra-TQ (own); boundary layers kept BF16 |
| QEvict 2608.05326 | Eviction: StreamingLLM, SnapKV, AdaKV 2407.11550, CriticalKV 2502.03805, DefensiveKV and Layer-DefensiveKV 2510.13334; quantization: KIVI, KVQuant, ZipCache 2405.14256; Full-KV |

Observations from the table:
- No seed runs FP8 KV or FP4 KV as a baseline except UltraQuant (FP8). TriAxialKV 2605.17170 is the only paper found here that runs SGLang FP4 KV, which it reports as unstable across models.
- TaSQ's only baselines are VQ methods (CQ, NSNQuant, NovaKV); it does not compare with KVarN, OSCAR or OptR at 2 bits.
- KVarN, OSCAR and OptR each use a different TurboQuant configuration: 3/3-bit with boundary layers kept, all layers at 2-bit with MP disabled, and no MP. The same mismatch underlies fact F6.
- MixKVQ 2512.19206 (query-aware per-channel BF16/INT4/INT2, online, on R1-Distill models) is cited by SBB and MultiAlloc, but no seed runs it as a baseline.

## 3. Cited works not on arXiv (or not resolved to an arXiv id)

| Work | Cited by | Status |
|---|---|---|
| CaM: Cache Merging for Memory-efficient LLMs Inference (ICML 2024, PMLR v235) | KVarN | not on arXiv (proceedings + OpenReview only), not read |
| OmniKV: Dynamic Context Selection for Efficient Long-Context LLMs (ICLR 2025) | ThinKV | not on arXiv, not read |
| Q-Hitter: A Better Token Oracle ... via Sparse-Quantized KV Cache (MLSys 2024) | ThinKV | not on arXiv, not read |
| HqeKV: Towards Hybrid Quantization and Eviction for KV Cache (Findings ACL 2026, code github skywclouds/HqeKV) | SBB, MultiAlloc | not on arXiv, not read; RDKV 2605.08317 App E compares against it |
| HaPPI: Efficient KV cache compression with Hadamard PCA-based power iteration | OSCAR | no arXiv hit in search, not read |
| LLM-MQ: Mixed-precision quantization for efficient LLM deployment | PM-KVQ | no arXiv hit in search, not read |
| TurboQuant: 2-bit KV cache compression with 4x capacity (Google blog) | OSCAR | blog, not a paper |
| TurboQuant vLLM PR #38479; vLLM OSS TurboQuant (Kurtić et al. 2026, Red Hat AI blog) | KVarN, OSCAR, UltraQuant | code/blog |
| TurboQuant+ (Turney & Contributors 2026, community implementation) | OScaR 2605.19660 | code |
| Productionizing TurboQuant on AMD GPUs; AITER (AMD ROCm blogs) | UltraQuant | blog |
| kv-cache-tester (Fox 2024, GitHub trace replay) | UltraQuant | code |
| Flash-decoding for long-context inference (blog) | OSCAR | blog |
| FlashMLA (github deepseek-ai/FlashMLA) | QuantMLA, RAQ-MLA | code |
| Introducing NVFP4 (NVIDIA technical blog) | ThinKV | blog |
| Gersho & Gray, Vector Quantization and Signal Compression (Springer) | TaSQ | book |
| Lloyd 1982; Max 1960 (IEEE Trans. IT) | UltraQuant | classic quantizer papers |

## 4. Resolution log

Method: for each seed, `$LIT fulltext <id>`, parsed the References section (scratchpad r4/refs.py, refs2.py; per-format manual reading for OptR, RAQ-MLA, MultiAlloc and UltraQuant, whose reference entries are line-wrapped), filtered to KV, quantization, cache, eviction, reasoning-efficiency and serving topics, then deduplicated by title (r4/dedup.tsv). Explicit arXiv ids printed in a reference were taken as-is and checked with `$LIT biblio`; all 183 ids in the pool returned a matching biblio record. Entries without an id were resolved as follows:

| Cited title (as in the seed) | Resolved | How |
|---|---|---|
| NSNQuant (TaSQ, OptR) | 2505.18231 | `$LIT search '"NSNQuant"'` |
| Think: thinner key cache by query-driven pruning (TaSQ) | 2407.21018 | search |
| KV cache is 1 bit per channel (TaSQ, ThinKV) | 2405.03917 | search |
| NovaKV, named in TaSQ's text | 2608.04074 | TaSQ App A names it as "Fernández-Menduiña et al., 2026" = "Spend bits where queries look" |
| Accurate KV cache quantization with outlier tokens tracing / OTT (MultiAlloc) | 2505.10938 | search |
| KVmix (MultiAlloc) | 2506.08018 | search (published 2025-05-18) |
| MixKVQ (SBB, MultiAlloc) | 2512.19206 | search |
| More tokens, lower precision (SBB) | 2412.12706 | search |
| DefensiveKV (QEvict) | 2510.13334 | search; arXiv title is "Taming the Fragility of KV Cache Eviction in LLM Inference" |
| Identify critical KV cache ... output perturbation (QEvict) | 2502.03805 | search; arXiv title "CriticalKV: ..." |
| A simple and effective L2 norm-based strategy (QEvict) | 2406.11430 | search |
| SparQ attention (QEvict) | 2312.04985 | search |
| Efficiently scaling transformer inference (QEvict) | 2211.05102 | biblio |
| PyramidInfer (SBB) | 2405.12532 | search |
| KVPR (MultiAlloc) | 2411.17089 | search |
| PolarQuant: polar transformation for key cache quantization and decoding acceleration (KVarN) | 2502.00527 | search; different paper from PolarQuant 2502.02617 (QuantMLA) |
| D2O (KVarN) | 2406.13035 | search |
| Scissorhands (KVarN, ThinKV, QEvict) | 2305.17118 | search |
| QAQ (ThinKV) | 2403.04643 | search |
| MiniCache (ThinKV) | 2405.14366 | search |
| IntactKV (PM-KVQ) | 2403.01241 | search |
| Quantization hurts reasoning? (QuantMLA) | 2504.04823 | search |
| PagedAttention / vLLM (most seeds) | 2309.06180 | search |
| SGLang (TaSQ, OSCAR, OptR) | 2312.07104 | search |
| Mooncake (RAQ-MLA) | 2407.00079 | search |
| QuIP# / QuIP / QTIP / linearity theorem (weight quant) | 2402.04396 / 2307.13304 / 2406.11235 / 2411.17525 | search |
| FlashAttention-3 (OSCAR) | 2407.08608 | search |
| Bridging the gap ... microscaling FP4 (OSCAR) | 2509.23202 | search |
| SVD-LLM V2; CARE (OSCAR) | 2503.12340; 2603.17946 | search |
| FlatQuant (QuantMLA, RAQ-MLA); AffineQuant (RAQ-MLA); AWQ (TaSQ, PM-KVQ, OSCAR, RAQ-MLA) | 2410.09426; 2403.12544; 2306.00978 | search |
| Fast matrix multiplications for lookup table-quantized LLMs (UltraQuant) | 2407.10960 | search |

Flags:
- ThinKV cites 2507.21433 under the title "MemShare: memory efficient inference for large reasoning models through kv cache reuse". The arXiv record for 2507.21433 is titled "ReasonCache: Accelerating Large Reasoning Model Serving through KV Cache Sharing", probably the same paper renamed. The pool lists it under the arXiv title.
- `$LIT search '"CaM" cache merging'` returned KVMerger 2407.08454, which is a different paper. CaM was marked not-on-arXiv after WebSearch (PMLR proceedings only).
- OScaR 2605.19660 (Su et al., Token Norm Imbalance) and OSCAR 2605.17757 (Zhou et al., spectral covariance rotation) are different papers with near-identical names. QuantMLA and RAQ-MLA cite both.
- Dropped as off-topic (benchmarks, model reports, generic architectures): ARC, PIQA, ReAct, LLaMA, Gemini 1.5, GSM-Symbolic, DeepSeek-R1, GLM-4.5, a reasoning survey, LongRoPE, Mamba-2, DeltaNet, Kimi Linear, hybrid linear attention analysis, a CIM accelerator, steering vectors, and "CoT matters".

Forward discovery (`$LIT search ... --since 2026-06-01 -k 30`). Long multi-term queries returned nothing because the backend matches every term, so the shorter queries below were used:
- TaSQ: `'"1-bit" KV cache'`, `'KV cache vector quantization'`, `'pre-RoPE key quantization'`. New relevant papers: GSRQ 2607.01065 (sub-1-bit RVQ), RaBitQCache 2606.31519, E8 lattice key quantization 2610.15384, WUSH-KV 2609.38121, D-Quant 2609.19880, HyperQuant 2606.23406, Codec-Gauge 2607.20538, Fast quantized JL 2610.16289, W2A4KV2 2610.09202.
- KVarN: `'KV cache quantization error accumulation'`, `'KV cache quantization reasoning'`, `'2-bit KV cache'`. New relevant papers: PN-Mix 2610.19605 (long-output mixed-precision K), Dual-QK 2610.09827, Block-GTQ 2606.24033, SPECTRA 2608.07915, JoLT 2607.12550, KV-COBRA 2609.24298, alignment collapse under KV quantization 2606.09864, quality recovery via low-rank adaptation 2609.04263, TP vs KV compression 2608.23962, HeadGuard 2609.35800, FuTransformer 2610.23796.
- OptR: `'rotation KV cache quantization'`, `'INT2 KV cache'`, `'KV cache quantization calibration rotation'`. New relevant papers: RoLaQ 2610.20686 (2-bit MLA rotation + range calibration), TORQUE 2609.36032, RotaryQuant 2608.08081.

Papers newly read and digested by R4 (10): 2608.04074, 2605.08317, 2605.19660, 2608.23962, 2607.01065, 2605.17170, 2511.06029, 2512.12895, 2607.12550, 2510.13334. R4 also read 2606.25519, 2512.19206 and 2608.07915 in full, but other agents had already appended digests for them, so R4 did not append.
