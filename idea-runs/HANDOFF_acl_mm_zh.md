# 交接：ACL / ACM MM 方向调研（用 Exa API）

## 背景
- 用户不再投 CVPR，改看 **ACL 2027** 和 **ACM MM 2027**（下文简称 MM），方向仍是“agent 操作机械臂 / 具身 agent”。
- 已有材料（都在 `idea-runs/`）：
  - `SURVEY_agent_arm_zh.md`：agent + 机械臂的整体综述（2026-10-26）；
  - `SUMMARY_zh.md`：IdeaScientist 三轮的结果与教训。最好的一轮是读仪表 3.5/10；大脑延迟那条只有 1.0/10，因为“前沿模型 + 经典机制”的组合会被拆回已有工作。
- 推荐过的方向：物理状态校验（Verify）、实时（不暂停）评测协议、执行模式下的安全、小模型规划器的 RL 后训练。

## 已知的截稿日期
- **ACL 2027**：ARR 截止 2027-01-04 AoE；会议 2027-08-20 至 22 日，京都；长文 8 页，短文 4 页（来源：https://2027.aclweb.org/ ）。主题赛道据二手报道是 “Homogenization and knowledge collapse in LLMs”，官网未确认。
- **ACM MM 2027**：还没有征稿通知。2026 年的正文截稿是 4/1。相关 topic area：Embodied and Immersive Multimedia、Multimedia and Language、Multimedia Generative and Foundation Models；审稿偏好多模态贡献（来源：https://2026.acmmm.org/site/cfp-guidelines.html ）。
- **MM 2026 已接收的具身论文**（来自 arXiv comments）：
  - VLA：CF-VLA 2604.24622（oral）、MMaDA-VLA 2603.25406、OGPO 2601.20701；
  - 导航 / 场景：OASIS 2610.30589（oral）、VTInstructor 2608.15284、SpaAct 2604.27620；
  - 多模态 agent：SPyCE 2607.13854。
- ACL / EMNLP 2026 接收的具身论文还没查到（arXiv API 被限流）。

## Exa API
- 网络密钥已配置：host 为 `api.exa.ai`，请求头 `x-api-key` 由代理注入，调用时**不要**自己加 key。
- 用法：`curl -s -X POST https://api.exa.ai/search -H "Content-Type: application/json" -d '{"query":"...","numResults":10}'`
- 旧会话里返回 401，原因是密钥只对新会话生效。

## 待办
1. 先用一个小请求验证 Exa 能用。
2. 查 ACL / EMNLP / NAACL 2025–2026 主会和 Findings 收了哪些 agent + 机器人 / 具身论文：题目、做法、数字，以及主要贡献类型（基准、语言接口、规划、评测）。
3. 同样查 ACM MM 2025–2026。
4. 总结两个会各自偏好什么选题，以及和 CVPR 口味的差别。比如 ACL 看重语言、交互、评测、LLM 行为分析，MM 看重多模态融合、效率、系统。
5. 结合 `SURVEY_agent_arm_zh.md` 的空白，给出适合 ACL 和 MM 的 3–5 个方向，并评估低算力下的可行性。截稿：ACL 2027-01-04；MM 约 2027 年 4 月初。
6. 结果写到 `idea-runs/SURVEY_acl_mm_zh.md`，提交并推送到 `claude/loving-feynman-7wrk2r`，用中文回复用户。
