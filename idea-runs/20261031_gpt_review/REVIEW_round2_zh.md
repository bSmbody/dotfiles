# GPT 第二轮（PROMPT_round2）结果审查（2026-10-31）

审查对象：`decision.json`，以及三个方向的证据调查：`rl-evidence.md`、`context-evidence.md`、`serving-evidence.md`。
GPT 的结论是 **0 个存活**：C1（RL）2/6、C2（上下文）2/6、C3（服务）1/6，全部被它自己否决。它推荐的下一步是"用一周证伪 RL 后期修复开销"，并明确声明这不是一个已验证的方法 idea。
说明：三个候选的单独审稿文件（`papers/*-c*-review.md`）没有上传，所以我只能从证据文件里了解 C3 的内容（BF16 指数无损压缩 + FlashInfer 寄存器内重建，被 GAAC 和 ZipFusion 覆盖）。C1、C2 具体提了什么，我看不到。

## 1. 核查结果

| 项目 | 结果 |
|---|---|
| 引用 | 抽查三份文件里的 32 个 arXiv 编号，**全部存在，标题一致**。GAUSS（2610.37989）GPT 说 HTML 打不开，但它在 arXiv 上确实存在 |
| 关键数字（对照原文） | RollVerify：训练成本从 98.1 降到 57.5 GPU-days，后期接受率下降，约在第 400 步切回 on-policy，均与原文一致。KV4-RL：rollout 累计加速 1.80×，但整个迭代只加速 1.27×，与原文一致 |
| 一个需要补充的细节 | RollVerify 附录里，**不切回 on-policy、一直训到 700 步**，成本仍能从 81.3 降到 64.3 GPU-days，而且准确率持平。GPT 说"后期接受率降到约 0.5 时加速消失"，这对应的是正文 Fig 5 的生成时间，并不是说整体收益消失了 |
| 方法论 | 明显比第一轮严谨：每个方向都先列有数字的瓶颈，区分实测、模拟和估算，标出不可外推的边界，并逐条列出检索 query |

## 2. 对"0 存活"的判断

- **服务方向、上下文折叠方向：我同意 0 存活。** 这两个方向的自然操作，都在近 30 天内被点名的论文覆盖了：
  - 服务方向：阶段感知调度（PASCAL）、尾延迟调度（UniBoost）、deadline 感知的 chunk 划分（SLOWeave）、压缩 draft + 全 KV 验证（VeriCache）、无损 KV 压缩（GAAC、ZipFusion）。
  - 上下文方向：可逆折叠（ReFold）、异步摘要（APEC/Slipstream）、续跑验证（TRACE/SJC）、前缀树训练（Tree Training/AReaL-DTA）。

  这两个方向偏系统，对新手来说门槛高、竞争也激烈。
- **RL 长 rollout 方向：0 存活成立，但有一个信号 GPT 没有追下去。** KV4-RL 测到：rollout 加速 1.80×，整个训练迭代只加速 1.27×；训练后期 **learner 占 60.5%**，其中 policy update 单项占 39.6%。也就是说，rollout 侧被一系列工作加速之后（TRACE、KV4-RL、S3R、RollVerify、EfficientRollout），**长序列 RL 的瓶颈正在转移到 learner 侧**，即 16K–32K 长序列上的 logprob 重算、反向传播和参数同步。GPT 的 RL 检索全部集中在 rollout 侧，没有覆盖 learner 侧。这不能证明那里有空白，但它是三份报告里唯一一个"有实测数字、又没被检索覆盖"的方向。

## 3. 三轮下来的总体结论

| 轮次 | 候选数 | 经过对抗式审稿后 |
|---|---|---|
| Claude（IdeaScientist） | 20 | 只剩 C14，约 3/10 |
| GPT 第一轮前 5 | 5 | 4 个否决，1 个需要大改（被 ParaTTT 覆盖） |
| GPT 第二轮 | 3 | 0 |

不同模型、不同流程得出的结论一致：**在长推理效率这个大方向上，纸面上的空白已经被 2026 年下半年密集的工作填满了。** 但这不等于没有机会。三份证据调查提供了一张很有价值的**瓶颈地图**，每一项都有实测数字和对应的近邻工作。新手直接拿去做第一个实测项目，起点会比从零开始高很多。

## 4. 建议

1. **（推荐）先做一次便宜的检索，确认 learner 侧有没有空白**：我用 IdeaScientist 派一个 gap_finder，方向是"长 rollout RL 的 learner 侧开销：长序列 logprob 重算、policy update、参数同步"。如果它也被覆盖了，这条线就停。
2. **GPT 推荐的一周证伪实验值得做，但要清楚它是测量研究，不是论文 idea。** 用 RollVerify 或 KV4-RL 的开源实现，在你们的 H200 上复现一次长 rollout 的 GRPO，分开记录 rollout、re-prefill、learner 和整步的时间。好处有两个：一是新手能借此熟悉 RL 系统栈（verl/AReaL、vLLM、FSDP）；二是你们会得到**自己系统上的真实瓶颈数据**，这比任何纸面检索都可靠。
3. **和师兄对一下这张瓶颈地图**，问他组里实际在跑什么、哪一项最痛。选题从这里出发。
