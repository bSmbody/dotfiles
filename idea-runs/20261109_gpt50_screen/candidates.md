# Candidates imported from GPT (gpt_handoff/PROMPT_mechanism_zh.md, 50 ideas, 2026-11-08)

Only the 7 shortlisted by the orchestrator's triage are imported here for review. The full list and the triage are in TRIAGE_zh.md. Text is GPT's own (Chinese), lightly reformatted; arXiv ids are GPT's claims and must be verified by the reviewer.

### C1 — [GPT D1-02] 量化胞腔联合边缘化 (quantization-cell joint marginalization)
- **Intuition**: 让低比特码表示 K/V 的联合分布，并在读出时边缘化。
- **Mechanism**: 码对应 (K,V) 联合胞腔 C；注意力累计 E[e^{qK}|C] 与 E[e^{qK}V|C]，最后相除，而不是先把胞腔压成均值（重建点）再过 softmax。
- **Why (GPT)**: 保留指数矩和 K/V 相关性，避免把胞腔先压成均值再过 softmax。Orchestrator note: if the within-cell distribution is Gaussian, E[e^{q·K}|C] = exp(q·mu + q^T Sigma q / 2), i.e. a per-cell variance correction to the logit — training-free and nearly free at read time.
- **Source**: 统计学 / Rao–Blackwell 化（GPT: 经典来源 arXiv 未查到）。
- **Novelty (GPT)**: closest "Quantized Keys Steal Attention" [2605.26266] corrects logit bias; this integrates numerator, denominator and V jointly.
- **Minimal experiment (GPT)**: Qwen3-8B / GPQA vs fixed KIVI codebook; only calibrate cell distributions.

### C2 — [GPT D1-03] 精确字面量旁路 (exact literal bypass)
- **Intuition**: 低比特 KV 存语境与地址，精确字面量（数字、运算符、标识符）走无损符号表。
- **Mechanism**: 字面量统一驻留；KV 携带表地址，复制头直接读取原始字节。
- **Why (GPT)**: 符号身份绕开浮点舍入，语境压缩与精确内容复制分开进行。
- **Source**: 编译器 / hash consing [2509.20534].
- **Novelty (GPT)**: Fractal KV [2607.07144] losslessly wraps quantized code streams; here raw literals leave the quantized channel and the output interface changes.
- **Minimal experiment (GPT)**: Qwen3-4B / AIME, LiveCodeBench vs same-total-bytes KIVI; LoRA-train a copy interface.

### C3 — [GPT D4-01] 最大耦合共读 (maximal-coupling co-read)
- **Intuition**: 多个头保留各自注意力分布，同时共同读取采样到的 V。
- **Mechanism**: 计算各头分布 p_h 与共同质量 c_i = min_h p_hi；固定次数采样共同部分与各头残差，GQA 共享的 V 只读一次。
- **Why (GPT)**: 每头边际仍为 p_h，线性值聚合无偏；共同质量变成共读机会。
- **Source**: 概率论 / 最大耦合 [1903.00632].
- **Novelty (GPT)**: SANTA [2605.01910] samples per head independently; this couples heads' reads.
- **Minimal experiment (GPT)**: Qwen3-8B / AIME vs independent SANTA at equal samples and full attention; training-free.

### C4 — [GPT D4-03] 守恒求积读取 (moment-conserving quadrature read)
- **Intuition**: 把稀疏读取变成每次都守恒指定值矩的求积。
- **Mechanism**: 缓存 u_i = P v_i（V 的低维投影）；以鞅消元生成非负权重 w，使 sum w = 1、sum w u = sum p u、E[w] = p，只读取 w 非零位置的 V。
- **Why (GPT)**: 投影输出每次精确守恒，完整线性读数保持无偏。
- **Source**: 数值求积 / Carathéodory [2510.14916].
- **Novelty (GPT)**: SANTA++ [2609.35629] samples by representative keys then corrects; here weights are generated under value-moment constraints.
- **Minimal experiment (GPT)**: Qwen3-8B / GPQA vs SANTA++ at equal reads; training-free, P calibratable.

### C5 — [GPT D6-01] 正交创新式重看 (orthogonal-innovation re-look)
- **Intuition**: 重看（再次裁剪/放大）只写入此前观测无法表达的新测量分量。
- **Mechanism**: 在固定视觉场 F 上，把新裁剪算子 A 投到既有观测行空间的正交补，存"创新"与重构系数，而不是把整段新视觉 token 追加进上下文。
- **Why (GPT)**: 正交分解可重构原测量；完全重复的观测产生零创新。
- **Source**: 信号处理 / Kailath 创新表示（arXiv 未查到）。
- **Novelty (GPT)**: GOTS [2607.23913] selects orthogonal tokens; this decomposes all observations and changes what a re-look writes.
- **Minimal experiment (GPT)**: Qwen3-VL-4B / V*, same crop trajectory vs full crop input; light-train a readout.

### C6 — [GPT D6-03] Chen 签名区间视频记忆 (Chen-signature interval video memory)
- **Intuition**: 用路径签名的群运算直接读取任意视频区间。
- **Mechanism**: 低维视觉轨迹加时间坐标，缓存块边界的截断签名；区间签名用 S[a,b] = S[0,a]^{-1} ⊗ S[0,b] 读取，无需重扫区间内部帧。
- **Why (GPT)**: Chen 乘法在截断张量代数中成立。
- **Source**: 粗糙路径 / 签名方法 [1603.03788].
- **Novelty (GPT)**: WeaveTime [2602.22142] trains order and retrieves history; here order is kept by non-commutative products.
- **Minimal experiment (GPT)**: Qwen3-VL-4B / Video-MME vs equal-capacity pooling; light-train projection and readout.

### C7 — [GPT D6-09] 组合编码视觉搜索 (group-testing visual search)
- **Intuition**: 把逐区域找目标改为预定编码的集合测试加一次译码。
- **Mechanism**: 固定 disjunct 矩阵把区域编入测试集合；共享编码器并行给出每个集合的 OR 读数（"这些区域里有没有目标"），译码定位目标。
- **Why (GPT)**: 目标稀疏且测试读数正确时，编码能唯一识别目标组合，测试次数约 O(k log n) 而非 n。
- **Source**: 编码理论 / 组合群测试 [2006.08420].
- **Novelty (GPT)**: Q-CueGraph [2608.04452] selects and budgets crops; this uses fixed set codes and algebraic decoding.
- **Minimal experiment (GPT)**: Qwen2.5-VL-7B / V*, same encoder vs per-region querying; light-train a set-predicate head.
