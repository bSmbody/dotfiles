# Pool R1: KV-cache quantization for LLM inference (2024-01 to 2026-11)

Recall agent R1, 2026-11-02. The searches ran on arXiv through `lit.py`, with 104 queries and no rate-limit fallback (log at the end), plus 6 WebSearch queries used only to find arXiv ids. Every id below was resolved by `lit.py search` or `lit.py biblio`.

- **Rows:** 186 papers: 34 H, 100 M, 52 L.
- **read=Y:** 47 rows. 18 of them were newly read and digested this run: 2608.02691, 2610.09827, 2608.04074, 2608.07915, 2610.20686, 2610.11245, 2610.19605, 2607.01065, 2606.31519, 2610.14448, 2512.19206, 2511.18643, 2609.38121, 2610.15384, 2606.24033, 2609.33135, 2609.04263, 2510.10964. The other 29 reuse earlier digests in papers/.
- **read=N:** the key_fact comes from the abstract and is marked "abstract only".
- **Out of scope:** pure KV eviction, sparse attention, KV reuse, video/diffusion-only KV quantization and weight-only quantization are left out unless they bear on KV precision. Those belong to the R2/R3 pools.

## Table

```tsv
arxiv_id	first_date	title	subcategory	relevance(H/M/L)	read(Y/N)	key_fact
2605.09490		Not All Thoughts Need HBM: Semantics-Aware Memory Hierarchy for LLM Reasoning	tiered-offload	M	Y	Four-tier HBM/DDR/compressed/evicted; exact offload lossless [prior digest]
2401.18079	2024-01-31	KVQuant: Towards 10 Million Context Length LLM Inference with KV Cache Quantization	scalar-per-channel-preRoPE-NUQ	M	N	abstract only: Quantization is a promising approach for compressing KV cache activations; however, existing solutions fail to represent activations accurately in sub-4-bit precision.
2402.02750	2024-02-05	KIVI: A Tuning-Free Asymmetric 2bit Quantization for KV Cache	scalar-per-channel-K/per-token-V	H	N	abstract only: From this analysis, we developed a tuning-free 2bit KV cache quantization algorithm named KIVI.
2402.12065	2024-02-19	WKVQuant: Quantizing Weight and Key/Value Cache for Large Language Models Gains More	weight+KV-PTQ	L	N	abstract only: This paper addresses these challenges by focusing on the quantization of LLMs, a technique that reduces memory consumption by converting model parameters and activations into low-bit integers.
2402.18096	2024-02-28	No Token Left Behind: Reliable KV Cache Compression via Importance-Aware Mixed Precision Quantization	mixed-precision-token-importance	M	N	abstract only: However, the memory footprint of the KV cache poses a critical bottleneck in LLM deployment as the cache size grows with batch size and sequence length, often surpassing even the size of the model itself.
2403.04643	2024-03-07	QAQ: Quality Adaptive Quantization for LLM KV Cache	mixed-precision-adaptive	L	N	abstract only: Through the integration of dedicated outlier handling, as well as an improved attention-aware approach, QAQ achieves up to 10x the compression ratio of the KV cache size with a neglectable impact on model performance.
2403.05527	2024-03-08	GEAR: An Efficient KV Cache Compression Recipe for Near-Lossless Generative Inference of LLM	quant+lowrank+sparse-residual	M	N	abstract only: Our experiments demonstrate that compared to alternatives, GEAR achieves near-lossless 4-bit KV cache compression with up to 2.38x throughput improvement, while reducing peak-memory size up to 2.29x.
2404.00456	2024-03-30	QuaRot: Outlier-Free 4-Bit Inference in Rotated LLMs	rotation-Hadamard(W4A4KV4)	M	N	abstract only: We introduce QuaRot, a new Quantization scheme based on Rotations, which is able to quantize LLMs end-to-end, including all weights, activations, and KV cache in 4 bits.
2405.03917	2024-05-07	KV Cache is 1 Bit Per Channel: Efficient Large Language Model Inference with Coupled Quantization	1bit-VQ	M	Y	CQ coupled channel VQ, 1 bit/channel; collapses on long CoT (AIME25 14.4 per TaSQ) [prior digest]
2405.04532	2024-05-07	QServe: W4A8KV4 Quantization and System Co-design for Efficient LLM Serving	W4A8KV4-serving-system	M	N	abstract only: We uncover a critical issue: existing INT4 quantization methods suffer from significant runtime overhead (20-90%) when dequantizing either weights or partial sums on GPUs.
2405.06219	2024-05-10	SKVQ: Sliding-window Key and Value Cache Quantization for Large Language Models	scalar-sliding-window	L	N	abstract only: Our evaluation on LLMs demonstrates that SKVQ surpasses previous quantization approaches, allowing for quantization of the KV cache to 2-bit keys and 1.5-bit values with minimal loss of accuracy.
2405.12591	2024-05-21	Unlocking Data-free Low-bit Quantization with Matrix Decomposition for KV Cache Compression	matrix-decomposition-quant	L	N	abstract only: Through extensive experiments, DecoQuant demonstrates remarkable efficiency gains, showcasing up to a \sim75\% reduction in memory footprint while maintaining comparable generation quality.
2405.14256	2024-05-23	ZipCache: Accurate and Efficient KV Cache Quantization with Salient Token Identification	mixed-precision-salient-token	M	N	abstract only: For instance, when evaluating Mistral-7B model on GSM8k dataset, ZipCache is capable of compressing the KV cache by 4.98x, with only a 0.38\% drop in accuracy.
2405.16406	2024-05-26	SpinQuant: LLM quantization with learned rotations	rotation-learned(W/A/KV4)	M	N	abstract only: With 4-bit quantization of weight, activation, and KV-cache, SpinQuant narrows the accuracy gap on zero-shot reasoning tasks with full precision to merely 2.9 points on the LLaMA-2 7B model, surpassing LLM-QAT by 19.1 points and S...
2406.03482	2024-06-05	QJL: 1-Bit Quantized JL Transform for KV Cache Quantization with Zero Overhead	1bit-JL	M	Y	QJL 1-bit sign JL keys with unbiased estimator [prior digest]
2407.12820	2024-07-01	PQCache: Product Quantization-based KVCache for Long Context LLM Inference	PQ-retrieval	L	N	abstract only: Extensive experiments demonstrate that PQCache achieves both effectiveness and efficiency, with 4.60% score improvement over existing methods on InfiniteBench and low system latency in both prefilling and decoding.
2407.21118	2024-07-30	Palu: Compressing KV-Cache with Low-Rank Projection	low-rank	L	Y	Palu low-rank latent KV with fused reconstruction [prior digest]
2409.16546	2024-09-25	AlignedKV: Reducing Memory Access of KV-Cache with Precision-Aligned Quantization	precision-aligned-memory-access	L	N	abstract only: The proposed technique attains a 25% saving of memory access and delivers up to 1.3x speedup in the computation of attention in the decoding phase of LLM, with almost no loss of precision.
2410.11305	2024-10-15	QSpec: Speculative Decoding with Complementary Quantization Schemes	spec-decoding-complementary-quant	M	N	abstract only: Compared to high-precision baselines, QSpec achieves up to 1.64x speedup without quality degradation, and outperforms state-of-the-art speculative decoding methods by up to 1.55x in batched settings.
2410.13212	2024-10-17	AsymKV: Enabling 1-Bit Quantization of KV Cache with Layer-Wise Asymmetric Quantization Configurations	1bit-layerwise-asym	M	Y	AsymKV K2/V1 layer-wise; RepoBench-P -13.5 [prior digest; pack F8]
2410.15704	2024-10-21	Residual vector quantization for KV cache compression in large language model	RVQ	L	N	abstract only: Overall, the proposed technique is competitive with existing quantization methods while being much simpler and results in 5.5x compression compared to half precision.
2411.18077	2024-11-27	MiniKV: Pushing the Limits of LLM Inference via 2-Bit Layer-Discriminative KV Cache	2bit-layer-discriminative	M	N	abstract only: To tackle the challenge, we introduce MiniKV, a KV cache optimization method that simultaneously preserves long context task accuracy while significantly reducing KV cache size via a novel 2-bit layer-discriminative KV cache.
2412.08890	2024-12-12	Lexico: Extreme KV Cache Compression via Sparse Coding over Universal Dictionaries	sparse-coding-dictionary	M	N	abstract only: Our key finding is that key-value cache in modern LLMs can be accurately approximated using sparse linear combination from a small, input-agnostic dictionary of ~4k atoms, enabling efficient compression across different input prom...
2412.10319	2024-12-13	SCBench: A KV Cache-Centric Analysis of Long-Context Methods	KV-benchmark(SCBench)	M	N	abstract only: To address this gap, we introduce SCBench(SharedContextBench), a comprehensive benchmark for evaluating long-context methods from a KV cachecentric perspective: 1) KV cache generation, 2) KV cache compression, 3) KV cache retrieva...
2412.11741	2024-12-16	CSR:Achieving 1 Bit Key-Value Cache via Sparse Representation	1bit-sparse-representation	L	N	abstract only: The linear growth of the Key-Value (KV) cache responsible for storing attention keys and values to minimize redundant computations can lead to substantial increases in memory consumption, potentially causing models to fail to serv...
2412.19442	2024-12-27	A Survey on Large Language Model Acceleration based on KV Cache Management	survey	L	N	abstract only: However, the computational and memory demands of LLMs, particularly during inference, pose significant challenges when scaling them to real-world, long-context, and real-time applications.
2501.16383	2025-01-25	RotateKV: Accurate and Robust 2-Bit KV Cache Quantization for LLMs via Outlier-Aware Adaptive Rotations	rotation-outlier-aware-2bit	M	N	abstract only: In this work, we explore the potential of rotation technique for 2-bit KV quantization and propose RotateKV, which achieves accurate and robust performance through the following innovations: (i) Outlier-Aware Rotation, which utili...
2501.19392	2025-01-31	Cache Me If You Must: Adaptive Key-Value Quantization for Large Language Models	adaptive-KV-quant(AQUA-KV)	M	N	abstract only: In this work, we aim to improve Key & Value compression by exploiting two observations: 1) the inherent dependencies between keys and values across different layers, and 2) high-compression mechanisms for internal network states.
2502.00527	2025-02-01	PolarQuant: Leveraging Polar Transformation for Efficient Key Cache Quantization and Decoding Acceleration	polar-key-quant	M	N	abstract only: Quantizing the cache to lower bit widths is an effective way to reduce computational costs; however, previous methods struggle with quantizing key vectors due to outliers, resulting in excessive overhead.
2502.02617	2025-02-04	PolarQuant: Quantizing KV Caches with Polar Transformation	polar-transform	M	N	abstract only: Quantization of these KV embeddings is a common technique to reduce memory consumption.
2502.10424	2025-02-05	QuantSpec: Self-Speculative Decoding with Hierarchical Quantized KV Cache	spec-decoding+hierarchical-INT4	M	Y	QuantSpec INT8 KV as upper/lower INT4 halves; draft reads upper half [prior digest]
2502.04420	2025-02-06	KVTuner: Sensitivity-Aware Layer-Wise Mixed-Precision KV Cache Quantization for Efficient and Nearly Lossless LLM Inference	mixed-precision-layerwise(offline)	H	Y	KVTuner offline layer-wise (K,V) bit pairs [prior digest]
2502.15075	2025-02-20	Quantize What Counts: More for Keys, Less for Values	K-favored-allocation-theory	M	N	abstract only: Empirical evaluations across various prominent LLMs and benchmarks show that key-favored allocations (e.g., 4-bit keys, 2-bit values) retain up to 98.3\% accuracy compared to uniform allocations (e.g., 4-bit for both), while conse...
2502.15304	2025-02-21	SVDq: 1.25-bit and 410x Key Cache Compression for LLM Attention	SVD-latent-mixed-precision	M	N	abstract only: Our findings based on RULER and LongBench benchmarks demonstrate that SVDq can achieve an equivalent key cache precision as low as 1.25-bit.
2504.03661	2025-03-12	MILLION: Mastering Long-Context LLM Inference Via Outlier-Immunized KV Product Quantization	PQ-outlier-immunized	L	N	abstract only: Large language models (LLMs) are increasingly utilized for complex tasks requiring longer context lengths, with some models supporting up to 128K or 1M tokens.
2503.18599	2025-03-24	Oaken: Fast and Efficient LLM Serving with Online-Offline Hybrid KV Cache Quantization	online-offline-hybrid-accelerator	L	N	abstract only: Our experiments show that for a batch size of 256, Oaken achieves up to 1.58x throughput improvement over NVIDIA A100 GPU, incurring a minimal accuracy loss of only 0.54\% on average, compared to state-of-the-art KV cache quantiza...
2503.18773	2025-03-24	BitDecoding: Unlocking Tensor Cores for Long-Context LLMs with Low-Bit KV Cache	low-bit-KV-tensor-core-kernel	H	N	abstract only: While accuracy-preserving KV-cache quantization (e.g., 4-bit or 2-bit) reduces memory footprint, existing systems decode inefficiently by relying solely on CUDA cores, underutilizing Tensor Cores-the dominant compute resource on G...
2503.19950	2025-03-25	LogQuant: Log-Distributed 2-Bit Quantization of KV Cache with Superior Accuracy Preservation	log-distributed-2bit	L	N	abstract only: We introduce LogQuant, a groundbreaking 2-bit quantization technique for KV Cache in large language model (LLM) inference, delivering substantial memory savings while preserving superior performance.
2503.23294	2025-03-30	Cocktail: Chunk-Adaptive Mixed-Precision Quantization for Long-Context LLM Inference	chunk-adaptive-mixed-precision	L	N	abstract only: However, a context that is too long may cause intolerant inference latency and GPU memory usage.
2503.24358	2025-03-31	SQuat: Subspace-orthogonal KV Cache Quantization	query-subspace-orthogonal	M	Y	SQuat keys quantized with residual orthogonal to prompt-query subspace [prior digest]
2504.04823	2025-04-07	Quantization Hurts Reasoning? An Empirical Study on Quantized Reasoning Models	reasoning-quant-empirical	H	N	abstract only: Our investigation covers weight, KV cache, and activation quantization using state-of-the-art algorithms at varying bit-widths, with extensive evaluation across mathematical (AIME, MATH-500), scientific (GPQA), and programming (Li...
2504.19874	2025-04-28	TurboQuant: Online Vector Quantization with Near-optimal Distortion Rate	VQ-rotation(data-oblivious)	H	Y	TurboQuant random rotation + Lloyd-Max per coord; collapses on long-CoT without boundary layers (OptR, Dual-QK, WUSH tables) [prior digest]
2505.10938	2025-05-16	Accurate KV Cache Quantization with Outlier Tokens Tracing	outlier-token-tracing	M	N	abstract only: Extensive experiments show that our method achieves significant accuracy improvements under 2-bit quantization and can deliver a 6.4 times reduction in memory usage and a 2.3 times increase in throughput.
2506.08018	2025-05-18	KVmix: Gradient-Based Layer Importance-Aware Mixed-Precision Quantization for KV Cache	mixed-precision-gradient-layer	M	N	abstract only: On LLMs such as Llama and Mistral, KVmix achieves near-lossless inference performance with extremely low quantization configuration (Key 2.19bit Value 2.38bit), while delivering a remarkable 4.9x memory compression and a 5.3x spee...
2505.16210	2025-05-22	NQKV: A KV Cache Quantization Scheme Based on Normal Distribution Characteristics	normal-distribution-quant	L	N	abstract only: Currently, quantization methods for activations are limited to 8-bit, and quantization to even lower bits can lead to substantial accuracy drops.
2505.18231	2025-05-23	NSNQuant: A Double Normalization Approach for Calibration-Free Low-Bit Vector Quantization of KV Cache	calibration-free-VQ	M	N	abstract only: Extensive experiments show that NSNQuant consistently outperforms prior methods in both 1-bit and 2-bit settings, offering strong generalization and up to 3x throughput gain over full-precision baselines.
2505.18610	2025-05-24	PM-KVQ: Progressive Mixed-precision KV Cache Quantization for Long-CoT LLMs	mixed-precision-progressive(long-CoT)	H	Y	PM-KVQ progressive 16->8->4->2 shrink for long-CoT, block-wise Taylor sensitivity [prior digest]
2505.19586	2025-05-26	TailorKV: A Hybrid Framework for Long-Context Inference via Tailored KV Cache Optimization	quant+offload-hybrid	M	N	abstract only: Particularly, the Llama-3.1-8B with 128k context can be served within a single RTX 3090 GPU, reaching 82 ms per token during decoding.
2505.20839	2025-05-27	FireQ: Fast INT4-FP8 Kernel and RoPE-aware Quantization for LLM Inference Acceleration	INT4-FP8-kernel-RoPE-aware	M	N	abstract only: In this paper, we propose FireQ, a co-designed PTQ framework and an INT4-FP8 matrix multiplication kernel that accelerates LLM inference across all linear layers.
2506.07533	2025-06-09	MoQAE: Mixed-Precision Quantization for Long-Context LLM Inference via Mixture of Quantization-Aware Experts	mixed-precision-QAT-experts	M	N	abstract only: Existing approaches, such as quantization, have demonstrated promising results in reducing memory usage.
2506.18879	2025-06-23	CommVQ: Commutative Vector Quantization for KV Cache Compression	commutative-VQ(RoPE)	H	N	abstract only: Experiments on long-context benchmarks and GSM8K show that our method reduces FP16 KV cache size by 87.5% with 2-bit quantization, while outperforming state-of-the-art KV cache quantization methods.
2506.19505	2025-06-24	AnTKV: Anchor Token-Aware Sub-Bit Vector Quantization for KV Cache in Large Language Models	sub-bit-VQ-anchor-tokens	M	N	abstract only: While scalar quantization is constrained by 1-bit bound, vector quantization exploits intra-vector correlations and enables sub-bit regimes, making it more suitable for ultra-low-bit quantization.
2507.19427	2025-07-25	Step-3 is Large yet Affordable: Model-system Co-design for Cost-effective Decoding	model-system-codesign(Step-3)	L	N	abstract only: Step-3 innovates in two key dimensions: (1) A novel Multi-Matrix Factorization Attention (MFA) mechanism that significantly reduces both KV cache size and computation while maintaining high attention expressiveness, and (2) Attent...
2508.04257	2025-08-06	KVSink: Understanding and Enhancing the Preservation of Attention Sinks in KV Cache Quantization for LLMs	attention-sink-preservation	M	N	abstract only: Moreover, when applied to the well-established KVQuant method, KVSink further improves perplexity (PPL) and reduces reliance on 16-bit numerical outliers.
2508.06297	2025-08-08	KV Cache Compression for Inference Efficiency in LLMs: A Review	survey	L	N	abstract only: This has resulted in a significant memory bottleneck, limiting the inference efficiency and scalability of the models.
2508.10395	2025-08-14	XQuant: Breaking the Memory Wall for LLM Inference with KV Cache Rematerialization	rematerialization-from-activations	M	N	abstract only: This results in an immediate 2x memory savings compared to KV caching.
2509.00579	2025-08-30	KVComp: A High-Performance, LLM-Aware, Lossy Compression Framework for KV Cache	lossy-compression-framework	L	N	abstract only: Experimental results show that KVComp achieves on average 47\% and up to 83\% higher memory reduction rate compared to existing methods with little/no model accuracy degradation.
2509.06261	2025-09-08	FineServe: Precision-Aware KV Slab and Two-Level Scheduling for Heterogeneous Precision LLM Serving	heterogeneous-precision-serving	M	N	abstract only: Experimental results demonstrate that FineServe achieves up to 2.2x higher SLO attainment and 1.8x higher token generation throughput compared to the state-of-the-art GPU sharing systems.
2510.01290	2025-10-01	ThinKV: Thought-Adaptive KV Cache Compression for Efficient Reasoning Models	quant+eviction(thought-adaptive)	H	Y	ThinKV NVFP4/ternary by thought type + eviction; pure KV quant can inflate length 5.1x [prior digest; pack F3]
2510.05176	2025-10-05	PatternKV: Flattening KV Representation Expands Quantization Headroom	pattern-residual-quant	M	N	abstract only: Across long-context and test-time scaling settings on multiple backbones, PatternKV delivers consistent 2-bit gains, with a 0.08% average 4-bit drop relative to FP16, improves test-time scaling accuracy by 10% on average, and rais...
2510.05373	2025-10-06	KVLinC : KV Cache Quantization with Hadamard Rotation and Linear Correction	Hadamard+linear-correction	M	N	abstract only: However, aggressive quantization to very low precision (e.g., 2 bits) introduces significant errors in the stored key and value tensors, which propagate through the dot-product attention mechanism and ultimately degrade generation...
2510.05529	2025-10-07	H1B-KV: Hybrid One-Bit Caches for Memory-Efficient Large Language Model Inference	hybrid-1bit	L	N	abstract only: This paper introduces the Hybrid One-Bit KV Cache (H1B-KV), a comprehensive compression scheme that radically reduces memory usage without sacrificing context.
2510.06175	2025-10-07	VecInfer: Efficient LLM Inference with Low-Bit KV Cache via Outlier-Suppressed Vector Quantization	VQ-outlier-suppressed	M	N	abstract only: With only 2-bit quantization, VecInfer achieves performance comparable to full precision, while delivering up to \mathbf{2.7x} speedup in large-batch self-attention computation and \mathbf{8.3x} reduction in single-batch end-to-en...
2510.10964	2025-10-13	Not All Bits Are Equal: Scale-Dependent Memory Optimization Strategies for Reasoning Models	reasoning-memory-tradeoff(weights-vs-KV)	H	Y	Qwen3 1.7K configs: KV quant and eviction both move AIME25 memory-accuracy Pareto; eviction wins below ~8-bit-8B effective size, 4-bit KV competitive above, 2-bit plain KV loses significantly (Sec 5)
2510.11236	2025-10-13	XQuant: Achieving Ultra-Low Bit KV Cache Quantization with Cross-Layer Compression	cross-layer-ultra-low-bit	M	N	abstract only: XQuant introduces two key innovations: a computationally negligible data-free calibration method and cross-layer KV cache compression, enabling quantization to sub-1.4 bits.
2511.01815	2025-11-03	KV Cache Transform Coding for Compact Storage in LLM Inference	transform-coding-storage	M	N	abstract only: By exploiting redundancies in KV caches, KVTC achieves up to 20x compression while maintaining reasoning and long-context accuracy, and 40x or higher for specific use cases.
2511.18643	2025-11-23	Kitty: Accurate and Efficient 2-bit KV Cache Quantization with Dynamic Channel-wise Precision Boost	mixed-precision-channel+kernel	H	Y	Kitty 2-bit + 25% channels at 4-bit: Qwen3-8B AIME24/25 (32K) 70.67/59.67 vs 71.67/66.00; 8x batch, 2.1-4.1x tput vs HF FP16 (Table 4, Sec 5.5)
2512.19206	2025-12-22	MixKVQ: Query-Aware Mixed-Precision KV Cache Quantization for Long-Context Reasoning	mixed-precision-channel(query-aware)	H	Y	MixKVQ: R1-Distill-Qwen-32B reasoning avg 66.04 vs BF16 67.84, KIVI-2 58.89, RotateKV-4 64.51 (Sec 5.2)
2512.24449	2025-12-30	PackKV: Reducing KV Cache Memory Footprint through LLM-Aware Lossy Compression	lossy-compression	L	N	abstract only: Experimental results show that, under the same and minimum accuracy drop as state-of-the-art quantization methods, PackKV achieves, on average, \textbf{153.2}\% higher memory reduction rate for the K cache and \textbf{179.6}\% for...
2601.04719	2026-01-08	GPU-Accelerated INT8 Quantization for KV Cache Compression in Large Language Models	INT8-GPU-kernel	L	N	abstract only: We implement and evaluate GPU-accelerated INT8 quantization for KV cache compression, achieving 4x memory reduction with minimal accuracy degradation.
2601.10155	2026-01-15	LOOKAT: Lookup-Optimized Key-Attention for Memory-Efficient Transformers	PQ-keys-ADC	L	Y	LOOKAT PQ keys with LUT scoring [prior digest]
2602.02958	2026-02-03	Quant VideoGen: Auto-Regressive Long Video Generation via 2-Bit KV-Cache Quantization	video-2bit-PRQ	L	N	abstract only: Across LongCat Video, HY WorldPlay, and Self Forcing benchmarks, QVG establishes a new Pareto frontier between quality and memory efficiency, reducing KV cache memory by up to 7.0 times with less than 4% end to end latency overhea...
2602.08005	2026-02-08	ResidualKV: Residual-Based KV Cache Compression for Efficient Long-Context Inference	residual-compression	L	N	abstract only: Across Llama, Qwen, LLaVA-OV, and Qwen3-VL backbones, ResidualKV maintains near-full-cache performance using only 13%-16% KV storage and 30% attention computation on LongBench, and 8%-10% storage and 10% computation in matched-bud...
2602.10718	2026-02-11	SnapMLA: Efficient Long-Context MLA Decoding via Hardware-Aware FP8 Quantized Pipelining	MLA-FP8-kernel	M	N	abstract only: Furthermore, per-token granularity is employed to align with the autoregressive decoding process and maintain quantization accuracy. (ii) Quantized PV Computation Pipeline Reconstruction: Addresses the misalignment of quantization...
2603.04427	2026-02-16	Thin Keys, Full Values: Reducing KV Cache via Low-Dimensional Attention Selection	thin-keys-low-dim-selection	L	N	abstract only: At the 7B scale, training from scratch with r = d/4 (where d is the model dimension) matches full-attention perplexity (9.24 vs 9.25 PPL after 20B tokens, mean over two seeds) while using 12% fewer parameters and training 8% faste...
2602.23200	2026-02-26	InnerQ: Hardware-Aware Tuning-Free Quantization of KV Cache for Large Language Models	hardware-aware-tuning-free	M	N	abstract only: As a result, InnerQ reduces memory access and accelerates dequantization, achieving an average 1.3x speedup over prior KV cache quantization methods and 2.7x over the non-quantized baseline.
2603.14224	2026-03-15	Self-Indexing KVCache: Predicting Sparse Attention from Compressed Keys	self-indexing-compressed-keys	M	N	abstract only: By designing a sign-based 1-bit vector quantization (VQ) scheme, our method unifies compression and retrieval in a single, hardware-friendly format.
2603.16435	2026-03-17	VQKV: High-Fidelity and High-Ratio Cache Compression via Vector-Quantization	VQ-high-ratio	M	N	abstract only: As a result, VQKV achieves an 82.8\% compression ratio on LLaMA3.1-8B while retaining 98.6\% of the baseline performance on LongBench and enabling 4.3x longer generation length on the same memory footprint.
2603.27467	2026-03-29	TurboAngle: Near-Lossless KV Cache Compression via Uniform Angle Quantization	angle-quant	M	N	abstract only: Across seven models (1B to 7B parameters), per-layer early-boost achieves lossless compression on four models and near-lossless quality on six of seven, at 3.28 to 3.67 angle bits per element.
2603.28430	2026-03-30	IsoQuant: Hardware-Aligned SO(4) Isoclinic Rotations for LLM KV Cache Compression	rotation-SO(4)-isoclinic	M	N	abstract only: Orthogonal feature decorrelation is effective for low-bit online vector quantization, but dense random orthogonal transforms incur prohibitive O(d^2) storage and compute.
2604.02638	2026-04-03	AXELRAM: Quantize Once, Never Dequantize	quantize-once-never-dequantize	L	N	abstract only: The key enabler is a design-time fixed codebook: orthogonal-transform-based quantization concentrates each coordinate's distribution to N(0,1/d), so the optimal quantizer depends only on dimension d and bit-width b, not on input d...
2605.02905	2026-04-06	eOptShrinkQ: Near-Lossless KV Cache Compression Through Optimal Spectral Denoising and Quantization	spectral-denoising+quant	M	N	abstract only: This observation leads to eOptShrinkQ, a two-stage compression pipeline: optimal singular value shrinkage (eOptShrink) automatically extracts the shared structure, and the residual -- which satisfies the \emph{thin shell property}...
2604.08426	2026-04-09	KV Cache Offloading for Context-Intensive Tasks	FP8/NVFP4-offloading-study	M	N	abstract only: Recently, KV-cache offloading has emerged as a promising approach to reduce memory footprint and inference latency while preserving accuracy.
2604.15356	2026-04-10	Sequential KV Cache Compression via Probabilistic Language Tries: Beyond the Per-Vector Shannon Limit	sequential-trie-compression	L	N	abstract only: The first layer, probabilistic prefix deduplication, identifies semantically equivalent shared prefixes across sessions using the trie metric d_T(s, s') = -log_2 P_M(s ^ s') from Probabilistic Language Tries (PLTs).
2604.17935	2026-04-20	How Much Cache Does Reasoning Need? Depth-Cache Tradeoffs in KV-Compressed Transformers	theory-depth-cache-tradeoff	L	N	abstract only: Closing the conjecture amounts to upgrading max to product. (2) Bandwidth barrier.
2604.19157	2026-04-21	SAW-INT4: System-Aware 4-Bit KV-Cache Quantization for Real-World LLM Serving	INT4-system-aware-serving	H	N	abstract only: In this work, we identify the minimal set of 4-bit KV-cache quantization methods that remain viable under these constraints.
2604.19528	2026-04-21	Revisiting RaBitQ and TurboQuant: A Symmetric Comparison of Methods, Theory, and Experiments	RaBitQ-vs-TurboQuant-comparison	M	N	abstract only: We compare the two methods in terms of methodology, theoretical guarantees, and empirical performance, using a reproducible, transparent, and symmetric setup.
2605.06675	2026-04-22	RateQuant: Optimal Mixed-Precision KV Cache Quantization via Rate-Distortion Theory	rate-distortion-mixed-precision	M	N	abstract only: On Qwen3-8B at 2.5 average bits, calibrated RateQuant reduces KIVI's perplexity from 49.3 to 14.9 (70% reduction) and improves QuaRot by 6.6 PPL.
2604.24971	2026-04-27	PolyKV: A Shared Asymmetrically-Compressed KV Cache Pool for Multi-Agent LLM Inference	shared-asymmetric-KV-pool-multiagent	L	N	abstract only: Compression is asymmetric: Keys are quantized at int8 (q8_0) to preserve softmax stability, while Values are compressed using TurboQuant MSE -- a Fast Walsh-Hadamard Transform (FWHT) rotation followed by 3-bit Lloyd-Max quantizati...
2605.08114	2026-04-27	Statistical Inference and Quality Measures of KV Cache Quantisations Inspired by TurboQuant	TurboQuant-statistics	L	N	abstract only: Starting from the Beta distribution on the hypersphere, we trace how QJL on K inflates inner product variance by π/2, which softmax amplifies nonlinearly via Jensen's inequality, and we present statistical inference and informatio...
2607.05399	2026-05-03	Benchmarking KV-Cache Optimizations across Task Quality and System Performance for Long-Context Serving	KV-optimizations-benchmark	M	N	abstract only: KIVI4 provides the most stable quality across models, SnapKV delivers the strongest long-context throughput, and CaM yields large gains on selected QA workloads but exhibits substantial workload sensitivity in both quality and rea...
2605.03562	2026-05-05	HeadQ: Model-Visible Distortion and Score-Space Correction for KV-Cache Quantization	score-space-correction(withdrawn)	L	N	abstract only: In K-only WikiText-103 decode experiments with dense values, HeadQ removes roughly 84--94\% of the excess perplexity on the strongest 2-bit rows; in an auxiliary full-KV 2-bit composition, HeadQ plus an A^2 value policy improves a...
2605.05699	2026-05-07	When Quantization Is Free: An int4 KV Cache That Outruns fp16 on Apple Silicon	INT4-Apple-silicon	L	N	abstract only: We show it is \emph{inverted} on Apple Silicon's unified memory: a single fused Metal kernel (sign-randomized FFT + per-channel λ + per-group abs-max + int4 nibble pack), exposed as a HuggingFace \texttt{Cache} subclass, runs \emp...
2605.06014	2026-05-07	Quantizing With Randomized Hadamard Transforms: Efficient Heuristic Now Proven	theory-RHT	L	N	abstract only: In practice, URRs are often replaced by randomized Hadamard transforms (RHTs), which preserve orthogonality while admitting fast implementations.
2605.08317	2026-05-08	RDKV: Rate-Distortion Bit Allocation for Joint Eviction and Quantization of the KV Cache	joint-eviction+quant-RD	H	N	abstract only: Experiments on LongBench, RULER, and InfiniteBench show that RDKV outperforms the best evaluated baseline by 9.1% on average.
2605.11478	2026-05-12	FibQuant: Universal Vector Quantization for Random-Access KV-Cache Compression	universal-VQ-random-access	M	N	abstract only: On GPT-2 small KV caches, \textsc{FibQuant} traces a memory--fidelity frontier from 5x compression at 0.99 attention cosine similarity to 34x at 0.95.
2605.13810	2026-05-13	Provable Quantization with Randomized Hadamard Transform	theory-dither-Hadamard	M	Y	Dithered RHT quantizer unbiased, matches TurboQuant MSE constant [prior digest; pack F9]
2605.18856	2026-05-13	SPHERICAL KV: Angle-Domain Attention and Rate-Distortion Retention for Efficient Long-Context Inference	angle-domain-attention	M	N	abstract only: Existing methods such as eviction, windowing, quantization, and offloading reduce footprint, but often leave the critical-path bottleneck only partially addressed, especially when compressed states must still be reconstructed into...
2605.17170	2026-05-16	TriAxialKV: Toward Extreme Low-Precision KV-Cache Quantization for Agentic Inference Tasks	extreme-low-precision-agentic	M	N	abstract only: To this end, we introduce TriAxialKV, a novel mixed-precision KV-cache quantization scheme that assigns each token a triaxial tag, calibrates per-tag sensitivity, and allocates INT2/INT4 bitwidths under a fixed memory budget.
2605.17757	2026-05-18	OSCAR: Offline Spectral Covariance-Aware Rotation for 2-bit KV Cache Quantization	rotation-learned(offline)	H	Y	OSCAR INT2 offline covariance rotation, ~8x KV reduction on reasoning traces up to 32K; baseline for OptR/Dual-QK/NOVA/WUSH [prior digest]
2605.19660	2026-05-19	OScaR: The Occam's Razor for Extreme KV Cache Quantization in LLMs and Beyond	extreme-KV-quant-simple	M	N	abstract only: Compared with the BF16 FlashDecoding-v2 baseline, our OScaR implementation achieves a notable up to 3.0x speedup in decoding, reduces memory footprint by 5.3x, and increases throughput by 4.1x.
2605.20868	2026-05-20	Runtime-Certified Bounded-Error Quantized Attention	runtime-certified-tiered	M	Y	INT8 K/INT4 V on GPU + FP16 CPU fallback driven by per-head bounds [prior digest]
2605.21226	2026-05-20	OCTOPUS: Optimized KV Cache for Transformers via Octahedral Parametrization Under optimal Squared error quantization	octahedral-rotation-codec	M	N	abstract only: Recent rotation-preconditioned codecs (TurboQuant, PolarQuant) show that a structured random rotation followed by a per-coordinate scalar quantizer matched to an analytically tractable marginal is a near-optimal recipe for KV comp...
2605.27646	2026-05-26	Hurwitz Quaternion Multiplicative Quantization for KV Cache Compression	quaternion-multiplicative-VQ	M	N	abstract only: The multiplicative composition yields 24S effective codewords at S stored parameters; random initialization suffices because left-multiplication is an S^3 isometry, so seeded codebooks vary in end-task ppl by <1.5\%.
2606.09864	2026-06-01	Alignment Collapse Under KV Cache Quantization: Diagnosis and Mitigation	alignment-collapse-under-KVquant	M	N	abstract only: Across eleven instruction-tuned models (3.8B-72B) and five benchmarks (1,894 prompts), we find that low-bit quantization can silently destroy safety alignment: Mistral-7B loses 15.2% of its refusals at only 1.03x perplexity, and n...
2606.03458	2026-06-02	KVarN: Variance-Normalized KV-Cache Quantization Mitigates Error Accumulation in Reasoning Tasks	scalar-rotation-normalization	H	Y	KVarN 2.3 bit: Qwen3-4B AIME24 60.0 vs FP16 61.1, KIVI 55.5; token count near FP16; vLLM code [prior digest; pack F2]
2606.06521	2026-06-02	P-Cast Precision in FP8 Attention: Sink-Induced Collapse and the Optimality of S=2^8	FP8-attention-sink-numerics	M	N	abstract only: FP8 (E4M3) acceleration for attention computation offers significant throughput gains, but the 3-bit mantissa introduces precision challenges when the softmax probability matrix~P is cast to FP8 before the P \cdot V matrix multipl...
2606.08635	2026-06-07	SpectrumKV: Per-Token Mixed-Precision KV Cache Transfer for Prefill-Decode Disaggregated LLM Serving	per-token-MP-transfer(PD-disagg)	L	N	abstract only: At a 50% normalized KV budget on WikiText-2, SpectrumKV changes perplexity by +1.97%,-0.06%, and-0.44%, respectively, compared with PDTrim's +25.85%, +22.07%, and +35.63%.
2606.15682	2026-06-14	ReQAT: Achieving Full-Precision Reasoning Accuracy with 4-bit Floating-Point Quantization-Aware Training	FP4-QAT-W4A4KV4-reasoning	H	N	abstract only: Under the same training budget, ReQAT not only recovers but surpasses BF16 fine-tuning accuracy, while delivering up to 3.9x throughput speedup on NVIDIA DGX Spark and 3.1x on B200.
2606.20474	2026-06-18	UltraQuant: 4-bit KV Caching for Context-Heavy Agents	FP4-KV-serving	H	Y	UltraQuant FP4+Hadamard KV in vLLM (MI355X): FP4 tput ~ FP8 at half bytes; 4-bit faster than FP8 only when memory-bound [prior digest; pack F7]
2606.23406	2026-06-22	HyperQuant: A Rate-Distortion-Optimal Quantization Pipeline for Large Language and Diffusion Models	RD-optimal-quant-pipeline	L	N	abstract only: Across a suite of self-contained experiments (Table 1), HyperQuant outperforms the recent HIGGS scheme at every operating point from 3 to 5 bits per scalar (bps) on weights, and beats both TurboQuant and OCTOPUS on KV quantization...
2606.24033	2026-06-23	Block-GTQ: RoPE-Block Rate Allocation for KV-Cache Quantization	mixed-precision-RoPE-block	H	Y	Block-GTQ K3V2 on R1-Distill-Qwen-7B AIME24/25 49.6/38.8 vs fp16 54.2/37.9, uniform TQ-MSE 0/0; K2V2 Llama NIAH 70.6->97.4 (Abstract)
2606.26875	2026-06-25	Information-Aware KV Cache Compression for Long Reasoning	info-aware-KV-compression-reasoning	H	N	abstract only: Experiments on long-context reasoning benchmarks with Llama-3.1, Llama-3.2, and DeepSeek-R1 demonstrate that InfoKV consistently outperforms existing attention-based KV compression methods in both long prefilling and decoding scen...
2607.16248	2026-06-27	High-accuracy Low-Bit KV-Cache Quantization via Local Distribution Restoration	1bit-local-distribution-restoration	H	N	abstract only: Low-bit KV-cache quantization reduces this cost, yet it severely degrade quality; particularly, one-bit quantization reduces accuracy from 84.2% to 47.8% on Llama-3.1-8B under RULER.
2606.31519	2026-06-30	RaBitQCache: Rotated Binary Quantization for KVCache in Long Context LLM Inference	1bit-index-for-sparse-attn	M	Y	RaBitQCache: 1-bit RaBitQ key index (~3.5% of FP16) + adaptive top-p fetch of full KV; 3.88x decode at 30K, 2.16x e2e (Sec 5.3); not a storage quantizer
2607.01065	2026-07-01	GSRQ: Gain-Shape Residual Quantization for Sub-1-bit KV Cache	sub-1bit-RQ	M	Y	GSRQ gain-shape RQ: LongBench 1-bit 33.54 vs VQLLM 11.34 (LLaMA-3-8B); GSM8K 1-bit 26.16 vs FP16 76.19 (Tables 3-4); no long-CoT
2607.01831	2026-07-02	Lynx: Progressive Speculative Quantization for accelerating KV Transfer in Long-Context Inference	progressive-quant-KV-transfer	L	N	abstract only: Across multiple models and serving workloads, Lynx achieves Time-to-First-Token (TTFT) comparable to aggressive 4-bit KV quantization, while matching the accuracy of high-precision (BF16) inference, improving TTFT over standard 8-...
2607.07144	2026-07-08	Fractal KV-Cache Archives: Lossless Symbolic Storage with In-Place Retrieval for Long-Context LLM Inference	lossless-symbolic	L	N	abstract only: Keeping a small exact window (4 attention sinks plus 32 recent tokens) and archiving the rest, per-head residual vector quantization reduces the archived cache by 36-54x relative to an fp16 cache at a perplexity cost of 11-15%, an...
2607.20538	2026-07-10	Codec-Gauge: Learning Compression-Friendly Gauges for Transformer KV Caches	learned-gauge-transform	M	N	abstract only: Across six models at 3, 4, and 6 bits/value, learned gauges reduce zfp KL divergence by 44.0\% on average relative to raw coordinates and outperform random, Hadamard, DCT, and PCA/KLT controls.
2607.12550	2026-07-14	A JoLT for the KV cache: Near-Lossless KV Cache Compression via Joint Rank-bit Allocation	joint-rank-bit	M	N	abstract only: Across five models from four architecture families, covering multi-head attention, grouped-query attention, and mixture-of-experts architecture, JoLT achieves 2 - 3x compression with less than 0.2% perplexity degradation, without ...
2607.17019	2026-07-19	Regularize or Localize: When Training-Time KV-Cache Geometry Pays Under Quantization	training-time-KV-geometry(QAT)	M	N	abstract only: We train 110M-parameter models on 10B FineWeb tokens and report three findings. \textbf{(1)} At λ{=}0.01, \sigreg reduces hidden-state pairwise-cosine anisotropy by 38\% across three paired seeds.
2607.28495	2026-07-30	Stage-Replay Divergence Follows the KV Cache: Fixed-Prefix Precision Controls and Bidirectional Cache Transplantation	numerics/divergence	M	Y	BF16-level KV differences make 83% greedy suffixes diverge [prior digest; pack F13]
2607.28699	2026-07-30	WitCert: Sound Runtime Risk Observability and Gating for KV-Cache Quantization	runtime-certificate	M	Y	WitCert sound TV bounds for KV quant; certificate 1289x loose at 4 bit, vacuous at 1-2 bit [prior digest; pack F14]
2608.02691	2026-08-03	Output-Aware Rotation for INT2 KV-Cache Quantization	rotation-learned(output-aware)	H	Y	OptR 2.32 BPE: Qwen3-4B-Thinking mean 65.38 (OSCAR 62.71, BF16 67.58), AIME25 70.7 vs 71.3 BF16; QuaRot-INT2 collapses to 2.61; <2% overhead (Table 1, Sec 6)
2608.02901	2026-08-03	AnchorKV: Anchor-Residual KV Cache Compression	anchor-residual	M	N	abstract only: We propose AnchorKV, a compression scheme that shrinks the cache by 20x without discarding a single token.
2608.03229	2026-08-04	Unified Lookup-Table Inference with Signed-Digit K/V Caches for Ternary LLMs	ternary-LLM-signed-digit-KV	L	N	abstract only: Compressing this cache alone does not resolve the mismatch.
2608.04074	2026-08-04	Spend Bits Where Queries Look: KV Cache Vector Quantization with Attention-Preserving Transforms	VQ-transform-coding	H	Y	NOVA-KV 2.22 BPE (E-opt non-orthogonal key transform + VQ): Qwen3-4B-Thinking AIME25 67.3 vs BF16 70.0, OSCAR 63.3; GPT-OSS-20B mean 72.4 vs OSCAR 13.9; NIAH128K 75.4 vs OSCAR 25.3 (Table 3, Sec 5)
2608.05326	2026-08-05	QEvict: Recoverable Quantized KV Eviction for Attention-Drift-Robust Long-Context Decoding	quant+eviction-tiered	H	Y	QEvict recoverable INT2/INT4 tier between full and evicted; INT2 tier cuts dropped future attention 64.8%->35.7% [prior digest; pack F14]
2608.07001	2026-08-07	Every Cache Entry Earns Its Place: Global Allocation of Resolution and Coverage for KV Cache Compression	global-resolution+coverage	M	N	abstract only: Systematic experiments across diverse long-context tasks and compression ratios show that GraceKV ranks first in 25 of 32 settings and remains robust up to 128-fold compression.
2608.07915	2026-08-08	SPECTRA: Pushing the KV Cache Beyond the 2-Bit Cliff via Spectral Transform Coding	transform-coding+lowrank	M	Y	SPECTRA G-weighted SVD latent + water-filling bits: LongBench 54.00 at 7.7x, 48.8 at 11x (TurboQuant 47.11 at ~8x); no long-CoT eval (Sec 4.2)
2608.08081	2026-08-08	RotaryQuant: Fitting 120B MoE Models on Consumer Hardware via Fused Compressed-Space Attention	fused-compressed-space-attention	M	N	abstract only: Mixed-precision weight quantization assigns bit-widths by architectural role: 4-bit for dense layers, 2-bit for routed experts, and 8-bit for the shared expert whose high activation kurtosis resists aggressive compression.
2608.18147	2026-08-10	Entropy-Constrained Adaptive Stochastic Quantization	stochastic-quant-theory	L	N	abstract only: It is designed to alleviate the communication and memory bottlenecks of modern data and machine learning workloads, including model, gradient, and KV-cache compression and nearest-neighbor search.
2608.14191	2026-08-14	KV Cache Compression Through the Lens of Transform Coding	transform-coding-lens	M	N	abstract only: On Llama-3.1-8B-Instruct and Qwen-2.5-7B-Instruct, evaluated across LongBench, RULER, GSM8K, MMLU-Pro, and MATH-500, our method achieves near-lossless accuracy at approximately 5.8x compression, whereas each baseline degrades in a...
2609.13205	2026-08-16	Self-Indexing Attention for Compression-Compatible Sparse Long-Context LLM Inference	self-indexing-compression-compatible-sparse	M	N	abstract only: This 1-bit index enables efficient retrieval through bitwise operations widely supported by modern accelerators.
2608.23834	2026-08-24	Minima-KV: Retention-Preserving KV Cache Compression with Mixed-Format Paged Attention	mixed-format-paged-attention	M	N	abstract only: Across separate, configuration-bound Qwen3.6-27B profiles on a single 96-GB NVIDIA RTX PRO 6000 Blackwell GPU, deployment accounting reports 18.3 KiB of attention KV per live token, corresponding to 3.50x compression relative to B...
2608.23962	2026-08-25	More GPUs or a Smaller Cache? Tensor Parallelism versus KV Compression for Memory-Bound LLM Serving	TP-vs-KV-compression-serving	M	N	abstract only: We place tensor-parallel configurations (degree 1 to 8) and KV-compressed configurations (16/8/4-bit, keep-ratios down to 0.25) on one costnormalised axis, cost per million tokens against latency, using a profiled simulator calibr...
2608.27875	2026-08-28	HyQuant: Hybrid-Precision Quantization for LLM Attention	hybrid-precision-attention	M	N	abstract only: However, low-bit quantization of the \emph{attention} module often introduces large errors at very low bit-widths, causing performance degradation.
2608.28911	2026-08-28	SemKV: Semantic Mixed-Precision KV Cache Quantization Guided by the Quality Cliff for Long-Context LLM Inference	semantic-mixed-precision	M	N	abstract only: We show that uniform KV quantization on a fractional-bit grid does not degrade gracefully: under a prespecified multi-seed statistical protocol, Llama-3.1-8B-Instruct with an affine quantizer is statistically indistinguishable fro...
2608.30996	2026-08-31	Faithfulness Is Not Free: Auditing Offline KV-Cache Quantization in Retrieval-Augmented Generation	RAG-faithfulness-audit	L	N	abstract only: We evaluate Qwen2.5-7B-Instruct under INT8 and INT4 quantization on RGB and HotpotQA, measuring both accuracy and faithfulness with a hallucination detector, NLI entailment, and an LLM judge.
2609.00450	2026-08-31	HBQ: Hierarchical Scaling Block Quantization with Hardware-Efficiency-Aware Design for Accurate LLM Inference	block-scaling-format	L	N	abstract only: HBQ-A achieves W4A16-level accuracy with W4A5 and lower area than NVFP4, while HBQ-E further reduces hardware cost by 17% while outperforming existing BQ methods in accuracy.
2609.04263	2026-09-02	Quality Recovery for Quantized KV Caches via Low-Rank Attention Adaptation	QAT-like-adaptation	M	Y	LoRA Q/K/V adapters over packed quantized cache recover 54-76% PPL gap at 4 bit; 2-bit NIAH only 11-12/180 vs 170/180 float (Abstract, Sec 6)
2609.03494	2026-09-03	GrowPage: On-Demand KV Budgeting for Efficient LLM Reasoning Serving	on-demand-KV-budgeting-reasoning	M	N	abstract only: Existing KV compression methods usually rely on a predefined per-request budget and adjust only which KV states are retained, leaving the total capacity fixed throughout decoding.
2609.03949	2026-09-03	VestigeKV: The NoPE-MLA KV Cache Carries Its Own Sparse-Attention Signal in a Vestigial Branch	NoPE-MLA-vestigial-sparse-signal	L	N	abstract only: Selection by observed attention collapses there: on a NoPE-MLA model, H2O and SnapKV retrieve 0.00 and 0.33 of needles at 8x compression, because a token's importance has not yet been observed.
2609.04105	2026-09-03	Hardware-Aware FP4 FlashAttention-4	FP4-FlashAttention	M	N	abstract only: Blackwell's 4-bit floating-point (FP4) tensor cores do not automatically make attention faster because softmax conversion and on-chip dependencies dominate once its matrix products shrink.
2609.04748	2026-09-04	Same Request, Different Answer: Quantization Amplifies Cache-Induced Divergence in LLM Serving	quant-amplifies-cache-divergence	M	N	abstract only: On llama.cpp with GGUF weights this path divergence rises with quantization: for Qwen2.5-7B over ten independent server histories, it reached 37.4 percent of episodes at 16-bit and 82.5 percent at four-bit.
2609.11582	2026-09-10	OmniKVQuant: KV Cache Quantization for Omni-LLMs	omni-LLM-KVquant	L	N	abstract only: On Qwen2.5-Omni and Qwen3-Omni, OmniKVQuant enables 2-bit KV caches while substantially preserving performance across seven audio-visual benchmarks.
2609.15810	2026-09-14	VC-Attention: Value Smoothing and Softmax Casting for Low-bit Attention	low-bit-attention-value-smoothing	M	N	abstract only: We implement VC-Attention for B200, B300, H200, RTX PRO 6000, and RTX 5090.
2609.19880	2026-09-17	D-Quant: Driftable Entropy Coding for KV Cache Quantization	entropy-coding-driftable	M	N	abstract only: However, most existing methods rely on fixed-width quantization, where a b bit representation is inherently limited to 2^b quantization levels.
2609.19969	2026-09-17	DeepSeek-V4.1-Flash: Pushing the Limits of KV Cache Compression	MLA/native-FP4-KV	M	Y	DeepSeek-V4.1-Flash: architecture-native compressed sparse attention with FP4 KV [prior digest]
2609.35800	2026-09-18	HeadGuard: Selective Head Protection for Low-Bit VLM KV-Cache Quantization	head-protection-VLM	M	N	abstract only: At 2 bits, the six-task discriminative mean over eight models rises from 0.436 to 0.580 on the weakest base; protection can also improve generated answers and caption fidelity to BF16 outputs.
2609.24298	2026-09-21	KV-COBRA: KV Cache Compression via Co-Optimized Bit-Rank Allocation	bit-rank-co-allocation	M	N	abstract only: On perplexity, zero-shot, and long-context benchmarks from 0.5 to 4 bits per dimension (bpd), KV-COBRA shows the smallest accuracy degradation among evaluated methods at low bpd, with no per-token overhead.
2609.30854	2026-09-25	The KV Cache Is the New Memory Wall	KV-memory-wall-analysis	M	N	abstract only: We classify the literature into five domains, quantization, token eviction, KV paging, prefix caching, and heterogeneous tiering, evaluating one method per domain at 128k context under a single protocol.
2609.33135	2026-09-27	MpFA: Hardware-Efficient Train-Free QK4V8 FlashAttention Kernels on Blackwell GPUs	FP4/FP8-attention-kernel	H	Y	MpFA NVFP4 K + FP8 V (QK4PV8) on B200: decode 2.08x vs BF16 FA4, e2e 2.81x vs BF16 but only 1.06x vs FP8 FlashInfer; rank-one comp. recovers 62.5% of loss (Intro, Sec 5)
2609.33746	2026-09-27	PQ-HSA: Reusing Product-Quantized Scores for Hybrid Sparse-Approximate Attention	PQ-index-sparse	M	Y	PQ-HSA IVF-PQ 4 B/token index + exact top-k + approximate background [prior digest]
2609.36032	2026-09-28	TORQUE: Optimizing What (not) to Quantize Before and After Rotation	what-to-quantize-rotation	L	N	abstract only: We introduce TORQUE, a framework that improves on previous quantization works that use random rotations by jointly optimizing how many and which coordinates to preserve at high precision both before and after rotation, under a fix...
2609.36760	2026-09-29	QuantMLA: Function-Aligned Dual-Path Quantization for Low-Bit MLA KV Caching	MLA	M	Y	QuantMLA C2R4 (content INT2, RoPE INT4) 3.59x compression at 128K with native low-bit kernel [prior digest]
2609.37988	2026-09-29	KV-Kaizen: Learning Context-Adaptive Cache Compression Choices	learned-compression-choice	M	N	abstract only: On long-context tasks, KV-Kaizen improves on eviction and can be composed with it, reaching a 32x smaller decode-time cache on a 14B model while preserving accuracy.
2609.38121	2026-09-29	WUSH-KV: KV Cache Quantization with Data-Adaptive Transforms	rotation-data-adaptive	H	Y	WUSH-KV INT2: Qwen3-8B AIME25 46.7 vs OSCAR 34.4, BF16 67.8; REPORTS LENGTH: OSCAR 63.0k tok/42% cap vs BF16 45.4k/11%; TurboQuant-style H 91.8k/100% (Table 2)
2610.01230	2026-10-01	HHR: Hierarchical Hash Retrieval for Efficient LLM Generation	hash-retrieval	L	N	abstract only: For example, on LongBench, HHR improves the average score by 1.10 points and, at a context length of 128K, achieves up to a 3.30x decoding speedup and a 2.83x end-to-end speedup for Llama-3.1-8B-Instruct.
2610.03027	2026-10-02	Tailoring the Quantization Space for 1-Bit KV Cache Compression	1bit-VQ	H	Y	TaSQ ~1.25-bit Fisher-weighted VQ, SGLang batch 6->84 (1.87x tput); Qwen3-4B-Thinking AIME25 74.4->56.7, NIAH64K 95.3->81.5; lengths near BF16 [prior digest; pack F1]
2610.05685	2026-10-05	Spend Bytes on Breadth: Precision-Count Trade-offs for Decode-Time KV Compression in Long Chain-of-Thought Reasoning	quant+eviction-tradeoff	H	Y	BreadthKV: at fixed bytes, 2-4 bit KIVI + more tokens beats eviction; offline proxy picks wrong bitwidth in 2/3 models [prior digest; pack F5]
2610.06251	2026-10-05	Shared Stopping Decisions Change Answers in HQQ Cache Quantization	HQQ-cache-stopping-decisions	M	N	abstract only: Replacing only the question batched with the target changes four-bit HQQ answers in 170/384 test comparisons across two models.
2610.09202	2026-10-06	Few Bits, One Law: Toward W2A4KV2	W2A4KV2-scaling-law	M	N	abstract only: The strongest gains arise under joint W2A4KV2 compression: across LLaMA3-1B/3B/8B, CanonQ-Omni achieves up to 14.28x lower WikiText-2 perplexity and up to 57.9% higher mean zero-shot accuracy than prior state-of-the-art and repres...
2610.09827	2026-10-07	Dual-QK: Sharp Queries and Flat Keys for Prunable 2-bit KV Caches	rotation-nonorthogonal+channel-pruning	H	Y	Dual-QK 2.34 bit + 40% query-channel pruning: Qwen3-4B-Thinking AIME25 48.0 vs BF16 74.7 (KIVI-3bit 42.0, pruned OSCAR 6.0); 3.75x decode at 90K (Table 1, Sec 4.4)
2610.10381	2026-10-07	ResidualQuant: KV Cache Quantization for Looped Transformers with 2-Bit Residuals	looped-transformer-2bit-residual	L	N	abstract only: In particular, our method retains accuracy close to BF16 under mixed-precision settings while reducing theoretical KV storage by 80.7%, achieving up to 13.0% higher accuracy than the rotation-based baseline at nearly the same memo...
2610.11214	2026-10-08	Bridging KV-Cache Quantization and Linear Attention: From Theory to Pretrained Weight Migration	theory-quant-vs-linear-attn	L	Y	RAM-Net bridges per-KV quantization and linear attention [prior digest]
2610.11245	2026-10-08	Read What Matters: Query-Adaptive Quantization for KV Caches	progressive-code/query-adaptive-read	H	Y	ReadKV: 8-bit progressive (Lloyd tree) code, query-adaptive prefix reads; R=4 of W=8 within 0.66% C4 PPL at 1/4 reads; single-layer A10G only, no end-to-end serving (Abstract, Sec 7) — direct prior art for seed 4
2610.12338	2026-10-08	VFold: Symmetry-Aware Cross-Layer Value Cache Compression	cross-layer-value-compression	M	N	abstract only: One solution is to compress this memory by exploiting inter-layer cache similarities.
2610.14448	2026-10-10	KV4-RL: Unlocking Faster Asynchronous Rollouts for RLVR with INT4 KV Cache Quantization	INT4-KV-RL-rollout	H	Y	KV4-RL INT4+Hadamard KV with INT8 sink16/recent128: 1.80x rollout, within 0.5pt BF16; plain KV4 -4.6pt at 8B; KV4 decode 1.44-1.97x vs W4A16/W8A8 ~1x; length within 1% (Sec 4.2, 5.2, 6)
2610.15259	2026-10-11	RECAP: Calibrating Low-Bit Reasoning Models on the History They Read	long-CoT-calibration(W4A4KV4)	H	N	abstract only: Under W4A4KV4, RECAP improves accuracy over the baseline by 13.3 percentage points on MATH500 with DeepSeek-R1-Distill-Qwen-1.5B and 15.8 points on AIME-120 with Qwen3-4B.
2610.15384	2026-10-11	E8 Lattice Key Quantization for Low-Bit KV-Cache Compression	lattice-VQ	M	Y	E8 lattice keys k2v2: ~6x compression, 20% smaller than scalar k3v2, better PPL in 80% of settings, decode tput parity via LUT scoring (Abstract, Sec 4.5); PPL only
2610.15629	2026-10-11	The Price of Precision: A Calibrated Cost Model for Mixed-Precision LLM Serving	mixed-precision-cost-model	M	N	abstract only: Allocators that use average bit-width or a memory budget as a speed proxy can miss changes in the resource that limits execution.
2610.16289	2026-10-12	Fast Quantized Johnson$-$Lindenstrauss Transforms	fast-quantized-JL	M	N	abstract only: A prominent example is Quantized Johnson-Lindenstrauss (QJL), which compresses KV caches using 1-bit asymmetric quantization while approximately preserving the inner products required by the attention mechanism.
2610.17970	2026-10-13	AlignPred: Error-Controlled KV Cache Compression via Alignment and Predictive Coding	predictive-coding-error-controlled	M	N	abstract only: AlignPred's SGLang HiCache integration reduces persistent target-KV storage by 42-72% relative to native HiCache, with comparable latency.
2610.18642	2026-10-13	MultiAlloc: Budget-Aware Precision Allocation for KV Cache Quantization	mixed-precision-alloc(offline)	H	Y	MultiAlloc per-layer bits x per-layer high-precision token count under budget (offline profiling) [prior digest]
2610.19605	2026-10-14	PN-Mix: Pair-Norm Guided Mixed-Precision Key Cache Quantization for Efficient Long-Output LLM Inference	mixed-precision-channel(RoPE-pair)	H	Y	PN-Mix 2.26-bit keys (3/1-bit RoPE pairs chosen at prefill), V2: Qwen3-8B AIME24/25 74.67/64.00 vs FP16 76.33/67.00, Kitty 71.33/62.00, KIVI 56.33/51.33; 2.37x max tput on A100-40GB (Table 3, Sec 6.4)
2610.20686	2026-10-14	RoLaQ: Joint Rotation and Range Calibration for 2-Bit KV Caches in Multi-Head Latent Attention	MLA	M	Y	RoLaQ 2-bit MLA latent: avg 46.7/60.1/59.4 on DSV2-Lite/Moonlight/MiniCPM3 (+3.8/+2.8/+1.1 over best baseline); 3.96x capacity, 2.51x decode at 256K; RoPE key BF16 (Sec 4.2, Limitations)
2610.23796	2026-10-16	FuTransformer: FP8 prefill and INT4 decode for Llama-style inference on Hopper	FP8-prefill-INT4-decode-Hopper	M	N	abstract only: On one H100, prefill is up to 1.48x faster than compiled PyTorch FP8 and reaches 1.29 PFLOP/s.
2610.28500	2026-10-20	BitMTP: When Multi-Token Prediction Meets Low-Bit Large Language Models	low-bit-MTP	L	N	abstract only: On NVIDIA H20, BitMTP with hybrid decoding achieves five-task mean speedups of 2.2x on BitNet b1.58-2B and 2.1-2.4x on 1.7B-4B Bonsai models at comparable task quality.
2610.33076	2026-10-21	Double KV Cache Optimization on Apple Silicon: Block-FP4, Radial Quantization, and Fused Metal Kernels	Block-FP4-radial-Apple	L	N	abstract only: We evaluate five cache paths on an Apple Silicon M5 Max using MLX: a native bf16 baseline, block-scaled E2M1 FP4, a Python reference implementing radial quantization with a QJL-style residual, sequential FP4-to-Polar composition, ...
2610.33625	2026-10-24	RAQ-MLA: Role-Aware Quantization for Multi-Head Latent Attention Caches	MLA	M	Y	RAQ-MLA quantizes latent and positional key, ~2.5 bits avg, training-free [prior digest]
2610.33719	2026-10-24	ZipFusion: Fusing Lossless KV Decompression with Attention for Efficient LLM Decoding	lossless-decompression-fused-attn	M	N	abstract only: On an NVIDIA H100, ZipFusion achieves about 1.25x speedup over FlashInfer in decode attention.
2610.36950	2026-10-27	DCKV: Learned Transform Coding of the Prompt KV Cache in Hybrid Language Models	learned-transform-coding(prompt)	L	Y	DCKV learned entropy-coded prompt KV for hybrid model [prior digest]
2610.37921	2026-10-27	FAD-KV: Adaptive Dictionary KV Caching for Efficient Reasoning Decoding	dictionary-KV-reasoning-decoding	H	N	abstract only: As generation length increases, KV cache memory and computation grow linearly, making compression critical for efficient long-output reasoning.
2610.38210	2026-10-28	GAAC: Lossless KV Compression for Bandwidth-Efficient LLM Inference on Personal Devices	lossless-KV-personal-devices	L	N	abstract only: Across five tested models, GAAC achieves 1.405-1.407x lossless BF16 KV compression.
2610.39853	2026-10-29	KV Cache Quantization for Diffusion Language Models	diffusion-LM-KVquant	L	N	abstract only: Across LLaDA and Dream evaluations on GSM8K, HumanEval, MATH, and MBPP, dLLM-KVQ achieves the highest average score among quantized methods across the reported 4-bit and 2-bit prefix/dual cache settings.
```

## What is new since 2026-06 and NOT already in RESEARCH_PACK section 3

1. **The pack's "lengths stay near BF16" premise does not hold in general at 2 bits.** WUSH-KV [2609.38121] Table 2 reports mean generated tokens and budget-exhaustion rate per cell. On Qwen3-8B AIME25, BF16 uses 45.4k tokens with 11% of runs hitting the cap. OSCAR uses 63.0k with 42% at the cap, and WUSH-KV uses 53.4k with 12%. On LiveCodeBench v6 the cap rate is 11% for BF16 against 71% for OSCAR. On Qwen3-32B LiveCodeBench it is 3% against 53%. A TurboQuant-style Hadamard INT2 cache drives 91-100% of runs to the cap. Qwen3-4B-Thinking stays close: 21.8k tokens versus 24.2k. Length and cap inflation therefore depend on model and method. This should be added to section 2 as a fact. Pack section 5, item 9 ("TaSQ/KVarN lengths near BF16") should be narrowed to those methods and models. Every baseline needs a length and cap metric.

2. **Stronger 2-bit baselines from Jul-Oct 2026 are missing from section 3.**
   - NOVA-KV [2608.04074] (2.22 bits per element, non-orthogonal attention-preserving key transform plus VQ, SGLang). On Qwen3-4B-Thinking AIME25 it scores 67.3, against 70.0 for BF16 and 63.3 for OSCAR. On GPT-OSS-20B, a hybrid sliding-window MoE model, OSCAR collapses (mean 13.9) while NOVA-KV holds 72.4.
   - WUSH-KV [2609.38121], also in SGLang.
   - Dual-QK [2610.09827]: INT2 plus 40% query-channel pruning in SGLang, 3.75x decode speed at 90K. It still loses about 27 AIME25 points on 4B-Thinking.
   - PN-Mix [2610.19605] (EMNLP 2026): 2.26-bit keys using RoPE-pair query-key norm saliency. On Qwen3-8B AIME25 it scores 64.0 against 67.0 for FP16.
   - Block-GTQ [2606.24033]: RoPE-block rate allocation. Uniform TurboQuant-MSE gives 0 on AIME without sink protection.
   - Older but also absent: Kitty [2511.18643] and MixKVQ [2512.19206], both channel-boost methods with reasoning evaluations.
   - E8 lattice keys [2610.15384] and GSRQ [2607.01065] (sub-1-bit residual VQ, ICML 2026) cover the VQ, lattice and RVQ space. Neither has a long-CoT evaluation.

3. **Prior art for SEEDS, which the novelty check must address.**
   - Seed 4 (read-time residual bit-plane fetch): ReadKV [2610.11245] already stores an 8-bit progressive code. Each query reads a prefix: key-channel depth is chosen from the query, and value-token depth from the reconstructed attention. It is proven optimal for its separable objective. Its gap is that it shows no end-to-end serving gain (single layer, batch 1) and has no reasoning evaluation. QuantSpec (upper and lower INT4 halves) and Kitty (a 4-bit channel split into two 2-bit planes) are related layouts.
   - Seed 1 (K/V or per-head precision by attention concentration): the closest work is static channel- or RoPE-block-level allocation (PN-Mix, MixKVQ, Kitty, Block-GTQ) and OptR's per-KV-head output-aware rotations [2608.02691]. None of these allocates precision per head online from concentration.

4. **Systems facts.**
   - MpFA [2609.33135], with NVFP4 K and FP8 V on B200, gets 2.08x decode over BF16 but only 1.06x end-to-end over FP8 FlashInfer. This reinforces F7: FP4-class KV wins mainly through capacity.
   - KV4-RL [2610.14448] shows that at high concurrency KV precision is the dominant lever. KV4 speeds up decode 1.44-1.97x, while W4A16 and W8A8 give about 1.0x. Plain INT4 KV hurts RL learning (-4.6 points at 8B). INT8 sink-16 plus recent-128 protection fixes it, and lengths stay within 1%.
   - SAW-INT4 [2604.19157, abstract only] finds that block-diagonal Hadamard plus token-wise INT4 is the best serving-compatible 4-bit design. If confirmed, that makes it the realistic 4-bit floor next to FP8/FP4.

5. **MLA.** RoLaQ [2610.20686] gives 2-bit MLA latents with 3.96x capacity and 2.51x decode at 256K, but keeps the RoPE key in BF16. It joins QuantMLA and RAQ-MLA.

6. **Calibration and QAT on long history.**
   - RECAP [2610.15259, abstract only] calibrates W4A4KV4 reasoning models on the long prefix they read: +15.8 on AIME with Qwen3-4B. This is relevant to seed 3 (error propagation as an allocation proxy).
   - Low-rank adaptation over a packed cache [2609.04263] recovers perplexity but not 2-bit NIAH (11-12/180 cases versus 170/180 for floating point).
   - ReQAT [2606.15682, abstract only] does FP4 QAT that includes KV4 for reasoning.

7. **Unread but possibly relevant (abstract only).**
   - DGAP local distribution restoration for K1V1 [2607.16248]: RULER 47.8 to 83.2.
   - HQQ cache "shared stopping decisions change answers" [2610.06251].
   - Quantization amplifying cache-induced divergence [2609.04748].
   - Alignment collapse under KV quantization [2606.09864].
   - InfoKV [2606.26875] and FAD-KV [2610.37921], both for reasoning decode.

8. **Baseline numbers vary even more across papers (extends F6).**
   - On Qwen3-4B-Thinking AIME25, OSCAR scores 63.3 in OptR's paper, 63.3 in NOVA-KV's and 65.6 in WUSH-KV's. In Dual-QK it scores 6.0, but there it is run with 40% channel pruning.
   - Uniform TurboQuant without mixed precision or boundary protection scores 0.0 to 16.7 on Qwen3-4B-Thinking AIME24/25 in OptR, Dual-QK, NOVA-KV and WUSH-KV. It does better on larger models: 40.0 and 53.3 AIME25 for Qwen3-8B and Phi4-14B in OptR Table 1.

## Inaccessible or problematic papers
- None of the 18 attempted full-text reads failed.
- 2605.03562 (HeadQ) is withdrawn by its author, so it is listed but should not be cited as evidence.
- WebSearch-found ids 2606.26875, 2609.03494, 2604.08426, 2608.03229, 2508.06297 and 2608.29667 were checked with `lit.py biblio`, except 2608.29667 (a QAT survey), which is not in the table.

## Query log
WebSearch, for id discovery only:
1. "arxiv 2026 KV cache quantization 1-bit reasoning long chain-of-thought"
2. "arxiv KV cache NVFP4 MXFP4 quantization vLLM SGLang 2026"
3. "arxiv 2-bit KV cache vector quantization rotation reasoning models AIME 2026"
4. "arxiv MLA latent KV cache quantization DeepSeek FP8 low-bit 2026"
5. "arxiv October 2026 KV cache quantization new method outperforms KIVI TurboQuant"
6. "arxiv quantization-aware training KV cache low-bit attention fine-tuning 2026"

arXiv via lit.py (104 queries):
```
lit search "KV cache quantization" -k 30 -> 30 hits
lit search "2-bit KV cache quantization" -k 30 -> 30 hits
lit search "low-bit KV cache LLM inference" -k 30 -> 30 hits
lit search "KV cache INT4 quantization" -k 30 -> 21 hits
lit search "1-bit KV cache" -k 30 -> 30 hits
lit search "Hadamard rotation KV cache quantization" -k 30 -> 17 hits
lit search "learned rotation KV cache" -k 30 -> 15 hits
lit search "vector quantization KV cache" -k 30 -> 30 hits
lit search "product quantization key value cache" -k 30 -> 22 hits
lit search "residual quantization KV cache" -k 30 -> 30 hits
lit search "outlier channels key cache quantization" -k 30 -> 15 hits
lit search "KV cache" --since 2026-10-01 -k 30 --sort date -> 30 hits
lit search "KV quantization" --since 2026-10-01 -k 30 --sort date -> 30 hits
lit search "KV cache quantization" --since 2026-10-01 -k 30 -> 15 hits
lit search "KV cache quantization" --since 2026-05-01 -k 30 -> 30 hits
lit search "KV quantization" --since 2026-05-01 -k 30 -> 30 hits
lit search "quantized KV cache" --since 2026-05-01 -k 30 -> 30 hits
lit search "KV cache quantization" --since 2026-07-01 -k 30 -> 30 hits
lit search "KV quantization" --since 2026-07-01 -k 30 -> 30 hits
lit search "quantized KV cache" --since 2026-07-01 -k 30 -> 30 hits
lit search "KV cache quantization" --since 2026-09-01 -k 30 -> 24 hits
lit search "KV quantization" --since 2026-09-01 -k 30 -> 24 hits
lit search "quantized KV cache" --since 2026-09-01 -k 30 -> 24 hits
lit search "KV cache quantization" --since 2026-10-01 -k 30 -> 15 hits
lit search "KV quantization" --since 2026-10-01 -k 30 -> 15 hits
lit search "quantized KV cache" --since 2026-10-01 -k 30 -> 15 hits
lit search "KV cache" --since 2026-05-01 -k 60 -> 60 hits
lit search "KV quantization" --since 2026-05-01 -k 60 -> 60 hits
lit search "KV cache" --since 2026-07-01 -k 60 -> 60 hits
lit search "KV quantization" --since 2026-07-01 -k 60 -> 60 hits
lit search "KV cache" --since 2026-09-01 -k 60 -> 54 hits
lit search "KV quantization" --since 2026-09-01 -k 60 -> 52 hits
lit search "KV cache" --since 2026-10-01 -k 60 -> 27 hits
lit search "KV quantization" --since 2026-10-01 -k 60 -> 30 hits
lit search "FP8 KV cache" -k 30 -> 28 hits
lit search "FP4 KV cache" -k 30 -> 8 hits
lit search "NVFP4 KV cache" -k 30 -> 11 hits
lit search "MXFP4 attention KV" -k 30 -> 2 hits
lit search "per-channel key per-token value quantization" -k 30 -> 14 hits
lit search "quantization-aware training KV cache" -k 30 -> 24 hits
lit search "multi-head latent attention quantization" -k 30 -> 11 hits
lit search "MLA latent cache compression low-bit" -k 30 -> 3 hits
lit search "mixed-precision KV cache quantization" -k 30 -> 30 hits
lit search "key value cache quantization reasoning models" -k 30 -> 30 hits
lit search "long chain-of-thought KV cache quantization" -k 30 -> 7 hits
lit search "quantized attention kernel low-bit KV decoding" -k 30 -> 6 hits
lit search "calibration-free KV cache quantization" -k 30 -> 13 hits
lit search "KV cache compression codebook" -k 30 -> 19 hits
lit search "lattice quantization KV" -k 30 -> 7 hits
lit search "entropy coding KV cache" -k 30 -> 27 hits
lit search "attention sink quantization KV" -k 30 -> 15 hits
lit search "key cache quantization" -k 30 -> 30 hits
lit search "value cache quantization" -k 30 -> 30 hits
lit search "sub-bit KV cache" -k 30 -> 8 hits
lit search "low-rank and quantization KV cache" -k 30 -> 0 hits
lit search "KV cache quantization error accumulation decoding" -k 30 -> 4 hits
lit search "stochastic rounding KV cache" -k 30 -> 0 hits
lit search "token-wise precision KV cache" -k 30 -> 16 hits
lit search "KV cache quantization benchmark" -k 30 -> 30 hits
lit search "ternary KV cache" -k 30 -> 8 hits
lit search "3-bit KV cache" -k 30 -> 30 hits
lit search "KV cache transform coding" -k 30 -> 30 hits
lit search "TurboQuant KV" -k 30 -> 20 hits
lit search "RaBitQ KV cache" -k 30 -> 1 hits
lit search "pre-RoPE key quantization" -k 30 -> 5 hits
lit search "query-aware KV quantization" -k 30 -> 12 hits
lit search "quantized KV cache sparse attention retrieval" -k 30 -> 6 hits
lit search "quantized KV cache speculative decoding" -k 30 -> 17 hits
lit search "KV cache quantization vLLM throughput" -k 30 -> 8 hits
lit search "binary keys Hamming attention LLM" -k 30 -> 2 hits
lit search "SageAttention quantized attention FP4" -k 30 -> 0 hits
lit search "low-precision attention FP8 decoding kernel" -k 30 -> 3 hits
lit search "KV cache quantization hybrid linear attention model" -k 30 -> 3 hits
lit search "quantized KV cache long generation accuracy" -k 30 -> 26 hits
lit search "attention-aware KV quantization" -k 30 -> 30 hits
lit search "KV cache quantization GQA" -k 30 -> 10 hits
lit search "KV compression 2 bits per value" -k 30 -> 27 hits
lit search "extreme KV cache compression" -k 30 -> 30 hits
lit search "KV cache quantization" -k 30 --sort date -> 30 hits
lit search "quantized KV cache" -k 30 --sort date -> 30 hits
lit search "low-bit KV" -k 30 --sort date -> 30 hits
lit search "KV cache bits" -k 30 --sort date -> 30 hits
lit search "key value quantization attention" -k 30 --sort date -> 30 hits
lit search "KV cache quantization" -k 200 --sort date -> 200 hits
lit search "KV quantization" -k 200 --sort date -> 200 hits
lit search "KV cache quantized" -k 200 --sort date -> 200 hits
lit search "KV-cache quantization" -k 200 --sort date -> 200 hits
lit search "KV cache bit" -k 200 --sort date -> 200 hits
lit search "non-uniform quantization KV cache" -k 30 -> 8 hits
lit search "asymmetric quantization key value heterogeneous" -k 30 -> 0 hits
lit search "KV cache quantization channel reordering grouping" -k 30 -> 1 hits
lit search "dynamic KV cache quantization serving system" -k 30 -> 6 hits
lit search "KV cache compression quantization pruning joint" -k 30 -> 1 hits
lit search "quantization key cache rotary position embedding outliers" -k 30 -> 4 hits
lit search "normalization KV cache quantization" -k 30 -> 24 hits
lit search "quantize keys values different bits" -k 30 -> 30 hits
lit search "KV cache quantization reinforcement learning rollout" -k 30 -> 5 hits
lit search "angle quantization key cache spherical" -k 30 -> 1 hits
lit search "quantized KV cache offloading CPU" -k 30 -> 6 hits
lit search "mixed-format paged attention kernel" -k 30 -> 1 hits
lit search "KV cache quantization output length reasoning" -k 30 -> 3 hits
lit search "sparse attention indexer quantization FP8 keys" -k 30 -> 0 hits
lit search "KV cache quantization theory distortion rate" -k 30 -> 6 hits
lit search "KV cache quantization looping repetition" -k 30 -> 0 hits
```
