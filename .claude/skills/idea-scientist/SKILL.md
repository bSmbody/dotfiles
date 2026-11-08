---
name: idea-scientist
description: 按 IdeaScientist（jiarui-liu/IdeaScientist）的多角色流程做科研选题：gap finder 找方法缺口，innovator 跨领域迁移机制，adversarial reviewer 审，report writer 写成 results-masked 提案，最后用模拟评审组给出"录用把握 x/10"。用户要找 research idea、选题、"跑一下 ideascientist"、或评估一个 idea 能不能投某个会时使用。
---

# IdeaScientist（Claude Code 移植版）

上游把选题拆成三个可训练的角色：gap finder 找同问题已有工作里的方法缺口，innovator 从别的领域找能迁移过来的机制，
report writer 把通过审稿的直觉写成完整提案。另有 adversarial reviewer 和只负责读论文的 paper reader。
orchestrator 不检索、不读论文，只看各角色写出的文件来决定下一步。

这个移植版：
- 角色 prompt 原文照录在 `roles/`，评测 prompt 原文照录在 `eval/judges.md`；
- 文献库用 arXiv 代替 Svalbard Idea Vault（`scripts/lit.py`），paper reader 的工作由各角色按
  `roles/paper_access.md` 的读法自己完成，摘要照样落到 `papers/<id>.md`；
- `scripts/check_run.py` 做上游 reward 里那些确定性检查（格式、字段、引用必须读过）；
- `eval/cvpr_panel.md` 是新加的：三审稿人 + AC，把提案换算成录用把握。

## 运行目录

```
<run>/                    建议放在 idea-runs/<YYYYMMDD_HHMM>_<slug>/
  problem.md              问题定义 + 挑战 + 约束（你写）
  plan.md                 orchestrator 的状态机和历史（只有你写）
  gaps.md                 gap_finder 追加
  candidates.md           innovator 追加
  scores.md               reviewer 追加
  report.json             report_writer 写
  papers/<id>.md          读过的论文摘要（各角色追加）
  panel/<C>/R1..R3.md,AC.md   模拟评审组
  eval/                   上游评测 judge 的输出
```

`problem.md` 的格式：

```markdown
# <题目>
## Problem definition
<形式化设定、输入、输出>
## Challenge
<现有方法哪里失败、为什么、一个具体失败例子>
## Constraints
<目标会议与截止日期、算力和时间预算、可用资产；可行性按这里判断>
```

## 你是 orchestrator

先读 `roles/orchestrator.md`，按它执行。在 Claude Code 里的对应关系：

- **你不检索、不读论文**：不调用 lit.py search/fulltext，不读 `papers/`。想查什么，就派对应的子 agent。
- **你只写 plan.md**：其余文件归各自的角色所有。某个文件写得不好，就把反馈写进任务，重新派它的主人。
- **派子 agent**：用 Agent 工具（general-purpose），每个任务一个全新上下文，提示词用下面的模板。
  多个互不依赖的任务（不同轴的 gap_finder、不同 lane）可以放后台并行；同一个 lane 里，
  innovator → reviewer 的链条仍按上游的 depth-first 一次走一条。
- **每个角色交差后**跑 `python3 <skill>/scripts/check_run.py <run> --quiet`；有问题就把问题原文发回给该角色重做。

子 agent 提示词模板（`<skill>` 换成本文件所在目录的绝对路径）：

```text
You are the <ROLE> sub-agent of an IdeaScientist run.
1. Read <skill>/roles/<ROLE>.md (your role prompt) and <skill>/roles/paper_access.md (how the
   upstream tools map to this environment). Follow both exactly.
2. RUN = <absolute run dir>. Read RUN/problem.md. Its Problem definition and Challenge are
   prepended to your task. Its Constraints bind feasibility: an idea that cannot be executed
   within them is infeasible.
3. TASK: <只写该角色合同里的字段，见 roles/orchestrator.md 的 Instruction contract>
   gap_finder → AXIS: <一个轴>
   innovator  → TARGET: C<n>  GAP: <轴 + gap>  [BUILD_ON: C<x>, FOCUS: <维度/评审意见>]
   reviewer   → TARGET: C<n>
   report_writer → TARGET: C<n>  （输出到 RUN/report.json；多个候选时写 RUN/report_C<n>.json）
4. Before replying, run `python3 <skill>/scripts/check_run.py RUN --quiet` and fix every issue in
   the files you own.
Reply with your role's one-line status only.
```

## 评测

report 写完、`check_run.py` 通过之后：

1. **模拟评审组**（`eval/cvpr_panel.md`）：R1/R2/R3 三个审稿 agent 并行，结束后派 AC。
   AC 给出 `odds`（按预测成立计算的录用把握）、`p_core`、`odds_risk_adjusted`。
2. **上游 judge**（`eval/judges.md`，可选，用来交叉检查）：quality 一次；non-obviousness 两次调用，
   第一次只给问题和最近邻 prior work 的摘要、绝不给提案，第二次拿冻结的候选列表去评提案。
3. 没到目标分数时，把 AC 的 `fixes_ranked` 和 [fatal]/[major] 意见作为 FOCUS，
   派 innovator（BUILD_ON）或 report_writer 修订，再审、再评。评审意见只能通过任务字段传给角色，
   你自己不改它们的文件。

## 范围宽泛时（"不限方向"）

先按约束挑 3–5 个 lane，每个 lane 一个独立的运行目录和 problem.md，并行跑。
挑 lane 的标准写进顶层的 `lanes.md`：算力是否够、对目标会议的契合度、是否用得上已有资产。
最后按评审组的 `odds` 和 `odds_risk_adjusted` 横向比较。

## 诚实性

- "x/10" 是模拟评审组在"预测成立"假设下的估计，不是真实录用率；汇报时同时给出 `p_core` 和风险调整后的分数。
- 任何角色都不许编论文 id、编数字；`check_run.py` 会拒绝没读过就引用的 id。

## 许可

角色与评测 prompt 来自 IdeaScientist，CC BY-NC 4.0，详见 `NOTICE.md`。仅限非商业用途。
