# 交接文档：推理效率选题（截至 2026-11-08）

> 仓库：`bsmbody/dotfiles`，分支 `claude/bold-hypatia-nvtkpb`。所有材料都在 `idea-runs/` 下，已全部推送。
> 本地继续：`git fetch origin claude/bold-hypatia-nvtkpb && git checkout claude/bold-hypatia-nvtkpb`。
> IdeaScientist skill 已放进仓库：`.claude/skills/idea-scientist/`。在仓库根目录打开 Claude Code，它会自动识别这个 skill。

---

## 1. 一句话现状

- **主线**：研究提案已经写完（"长推理中低比特 KV 的按需精度救援"），还没跑任何实验。P0 的实验代码由 GPT 编写，目前停在检查点 4，代码包还没交给我们审。
- **支线**：你希望做"机制创新"，而不是"检测 → 修复"那类方法。我们用 IdeaScientist 构思了两轮共 10 个机制 idea，经过查新和审稿后全部被否。现在已经写好一份 prompt，准备交给 GPT 一次产出 50 个机制 idea（构思时同步做轻量查新）。

---

## 2. 方向演变（简）

1. **10-26**：多模态与视频推理调研 → `20261026_1230_mm_video_reasoning/SURVEY_zh.md`
2. **10-27**：学长给的方向：注意力剪枝、混合注意力、记忆矩阵、变种注意力、KV 量化时机。IdeaScientist 6 条 lane 共 20 个候选，只有 C14（混合模型选层）存活，模拟评审 1.8 → 3.2 → 2.7/10 → `20261027_efficient_attention/IDEAS_zh.md`
3. **10-31**：审了 GPT 产出的三轮候选，全部被否或大改 → `20261031_gpt_review/`
4. **10-31～11-01**：基线侦察，确定 scope S1：长思维链（CoT）下的低比特 KV，以"每答对一题的成本"为指标 → `20261031_baseline_scout/SCOPE_zh.md`
5. **11-01～11-05**：系统查新（4 路检索，共 392 篇）+ 交给 GPT 构思 + 3 轮检查点审阅 → 形成主线研究提案 → `20261101_s1_prep/`
6. **11-06**：MiTA 启发的两个想法查新：部分升精度空间较窄；"混合模型稀疏读"已有人做 → `20261101_s1_prep/NOVELTY_mita_ideas_zh.md`
7. **11-08**：受 SwarmEvolve 启发做机制创新。两轮共 10 个 idea，C4、C10 做了详细审稿，全部被否 → `20261108_swarm_inspired/`

---

## 3. 主线：按需精度救援（纸面方案）

**一句话**：默认用 2 bit 存 KV、把 batch 开大；一旦某个请求开始失控（打转、写满上限），就用它已生成的 token 重算出 FP8 KV，从当前位置接着写。目标是成本接近 2 bit，准确率接近 FP8。

- **定稿文件**：`20261101_s1_prep/PROPOSAL_zh.md`（md 版）
- **在线文档**：https://claude.ai/artifact/D1ACLwjtQ1hPWFR8mabhUP
- **关键依据**：
  - Qwen3-8B 的 AIME25 上，写满上限的比例从 BF16 的 11% 涨到 OSCAR INT2 的 42%（2609.38121）；
  - 显存打满时，单个请求的成本约正比于"比特数 × 长度²"；
  - KV 可以由 token 精确重算（2603.19664）。
- **实验设计**（以 PROPOSAL 为准）：
  - S0 定生成上限 → S1 主采样（只用 Qwen3-8B，BF16/FP8/INT2 × 60 题 × 16 次）→ S2 分叉实验（FP8 续写 / INT2 换种子续写 / FP8 重开 等，共 5 个分支）→ P2 系统实测 → P3 泛化（把 4B 放到这里）。
  - 两个止损点：H1 可救空间不到 5 个百分点就停；H4 中"FP8 续写比 INT2 续写多救回的比例"不到 10 个百分点就停。
- **已做的决定**：
  - 不做回滚；
  - 4B 不进入 P0；
  - P1 不再作为独立阶段；
  - "部分升精度"暂不加入，等 P2 数据出来再决定；
  - DMR（2602.02711）要补进近邻对比表。
- **未完成**：
  - [ ] 提案里的"离线分析"一节：你说过不做离线分析，但提案里还留着。删除后改为在 P2 做阈值扫描。还没改。
  - [ ] DMR 还没写进提案的近邻表。
  - [ ] GPT 检查点 4 的 P0 代码包还没上传给我们审。审阅要点见 `REVIEW_CP3_zh.md`：续写时不能重新套 chat 模板、随机种子可复现、判分规则、计费、判定脚本不能有可调阈值。
- **对主线的自我评价**：它本质上也属于"检测 → 修复"类，这正是你后来不满意的方向。如果之后找到合格的机制 idea，主线可以降为备选或测量性论文。主线的测量部分（损失集中在少数失控请求上、成本与长度平方成正比）单独拿出来也有价值。

**主线相关文件**：

| 文件 | 内容 |
|---|---|
| `20261101_s1_prep/PROPOSAL_zh.md` | 研究提案定稿 |
| `20261101_s1_prep/IDEA_FULL_zh.md`、`IMPLEMENTATION_zh.md`、`P0_RUNBOOK_zh.md` | 早期完整版、实现方案、学生操作手册（部分内容已被 PROPOSAL 取代） |
| `20261101_s1_prep/RESEARCH_PACK_zh.md`、`ADDENDUM_zh.md` | 给 GPT 的资料包和补遗一（事实 F1–F22、必比基线） |
| `20261101_s1_prep/REVIEW_CP1/2/3_zh.md` | 对 GPT 检查点 1–3 的审阅意见 |
| `20261101_s1_prep/pool_R1..R4.md`、`papers/` | 4 路检索的文献池和论文摘要 |

---

## 4. 支线：机制创新探索

### 4.1 你的要求（很重要）
要的是**改变推理时算什么、存什么、交换什么的机制**，效果由某个原理或不变量保证，而不是"检测到问题再修复"。不要求一定像 SwarmEvolve。

### 4.2 两轮结果（`20261108_swarm_inspired/`）

| idea | 一句话 | 结论 |
|---|---|---|
| C1、C3、C5 | 局部升精度、定期重放 KV、带有效期的页面清单 | 属于"检测 → 修复"，风格不符 |
| C2 | 粒子滤波式分支，借"路径退化"共享主干 KV | 未细审；可能已被 SMC 推理类工作覆盖 |
| C4 | GDN 状态补丁，支持分叉、变基、合并 | **否决**：HYPIC、PICASO、LinearKV 已覆盖；GDN 状态只管风格，内容存在 KV 里（2609.04434） |
| C6 | Sigma-Delta KV | 否决：SDQ-LLM；KVarN 指出误差集中在少数异常 token |
| C7 | 主干推理读取未选分支的潜空间推演 | 否决：TGR、LACE、LatentMAS |
| C8 | 伪 token 折叠 | 否决：SemantiCache、Meta-Soft |
| C9 | 多分支共享 KV 池、状态私有 | 否决：Hogwild! |
| C10 | 远端注意力延迟 B 步作答 | **否决**：MAC-Attention、ASPIRE；不训练时信息过期，GSM8K 从 85 掉到 10.5（Ladder） |

**详细文件**：`IDEAS_zh.md`（第一轮）、`IDEAS_round2_zh.md`（第二轮）、`candidates.md`（英文原文）、`scores.md`（C4、C10 的审稿全文）、`external_audit/`（你上传的外部审查）。

### 4.3 教训
1. 这个领域在 2026 年极其拥挤，**构思阶段就要查新**。
2. 比撞车更致命的是**价值前提和已有实验结果相反**（C4 栽在"状态只管风格"上，C10 栽在"信息过期等于注入错误答案"上）。
3. 关键假设要有已发表论文测到的数量级支撑。

### 4.4 下一步：交给 GPT 产出 50 个机制 idea
- **prompt**：`20261108_swarm_inspired/gpt_handoff/PROMPT_mechanism_zh.md`，直接整份粘贴即可。
- 覆盖 6 个方向：低比特 KV、淘汰与压缩、混合模型与记忆矩阵、变种注意力、并行推理、**多模态与视频推理**。
- 每个 idea 构思时至少查 3 组关键词，给出最接近的 1–3 篇工作及区别；不做对抗自审。
- 内含已否决清单和背景事实，避免它重复提出。
- GPT 交回后：先按"机制创新"的标准和已否决清单粗筛出 5–10 个，再对这几个做详细查新和对抗审稿（参照 `scores.md` 里 C4、C10 的审稿格式）。

---

## 5. 在本地用 IdeaScientist

- **skill**：`.claude/skills/idea-scientist/SKILL.md`。流程是 orchestrator 派子 agent 担任 gap_finder → innovator → reviewer → report_writer，最后由模拟评审组打分。
- **文献工具**：`python3 .claude/skills/idea-scientist/scripts/lit.py search "q1" "q2" -k 30 --since 2026-01-01`，另有 `biblio <id>`、`fulltext <id>`。
  - arXiv API 限流时会自动改用网页检索。
  - 查询词要短：长串关键词经常 0 命中，拆成 3–5 个词的短语效果更好。
- **检查工具**：`python3 .claude/skills/idea-scientist/scripts/check_run.py <run 目录> --quiet`。它要求所有被引用的论文都在 `papers/<id>.md` 里有摘要。
- **快速复用**：
  - 对单个 idea 做对抗审稿：派 reviewer 子 agent，提示词模板见 SKILL.md；可以参照 `20261108_swarm_inspired/plan.md` 和 C4、C10 的审稿任务写法。
  - 新开一轮：在 `idea-runs/` 下新建目录，写好 `problem.md`、`gaps.md`，把相关的 `papers/` 拷过去。

---

## 6. 关键事实速查（构思和审稿时常用）

| 事实 | 出处 |
|---|---|
| 推理任务上，随机淘汰 ≈ SnapKV/R-KV | 2609.03430 |
| 准确率取决于永久删除的比例 | 2605.09490 |
| 63–85% 的头在生成过程中改变关注位置 | 2610.02713 |
| 2 bit KV：Qwen3-8B AIME25 写满上限比例 11% → 42%；4B-Thinking 上强 2 bit 方法几乎无损 | 2609.38121、2608.02691 |
| FP4 KV 主要赢在容量；比 FP8 只快 1.06 倍 | 2609.33135 |
| KV 可以由 token 精确重算 | 2603.19664 |
| GDN 状态占请求显存 7–17%；状态清零，NIAH 下降不到 1 点；状态管风格、KV 管内容 | 2610.36950、2608.30386、2609.04434 |
| 训练过的滑动窗口注意力只比全注意力低 0.4–1 分 | 2606.11634 |
| 复用旧 query 的远端注意力，命中率超过 99% | 2604.00235 |
| 多模态推理失败中，72–78% 是"看错" | 2506.07218 |
| 把裁剪后的图换成噪声，答案几乎不变 | 2510.23482 |

---

## 7. 待办清单

- [ ] 把 `PROMPT_mechanism_zh.md` 交给 GPT，拿到 50 个机制 idea
- [ ] 粗筛出 5–10 个 → 详细查新 + 对抗审稿
- [ ] 和学长对齐：方向（机制创新 vs 主线测量）、H200 机时、是否要做混合模型或多模态
- [ ] （主线如果继续）删掉提案里的"离线分析"一节，补上 DMR；审 GPT 检查点 4 的 P0 代码包；跑 S0
