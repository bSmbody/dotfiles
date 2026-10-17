# Lanes — "low-compute idea, any direction, ≥ 5/10"（2026-10-17）

用户要求：继续用 IdeaScientist，找低算力的 idea，方向不限，目标是模拟评审组给出 ≥ 5/10 的录用把握。
共同约束见各 lane 的 problem.md（CVPR 2027，11/16 截稿；2–4 张 24 GB 卡，全文 ≤ 40 卡·日）。

| Lane | 目录 | 为什么选 |
|---|---|---|
| 视频 DiT 的免训练运动质量 | 20261017_1140_video_motion | 纯推理；直接用上组里的 Wan2.1-1.3B、RAFT、VBench、VideoAlign；运动塌缩是组里已经摸熟的问题 |
| 扩散/流模型的推理期搜索 | 20261017_1140_inference_search | 纯推理，热门方向；HPSv3、VideoAlign 这些奖励模型现成可用 |
| 免训练开放词汇语义分割 | 20261017_1140_ov_seg | CVPR 的常规低算力赛道，标准基准齐全，单卡推理即可 |
| MM-DiT 文生图的免训练组合对齐 | 20261017_1140_mmdit_compose | 纯推理，标准基准（GenEval、T2I-CompBench++），用得上组里的 DiT 经验 |

挑选原则：一篇论文的全部实验能在约 3 周内跑完；评测用公开基准；不需要大规模训练。
3D 高斯等方向算力也低，但和组里的经验差得远，30 天内执行风险大，这一轮先不跑。
