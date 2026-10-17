# Training-free compositional alignment in MM-DiT text-to-image models

## Problem definition
Given a pretrained multimodal diffusion-transformer text-to-image model (e.g. SD3.5-Medium, FLUX.1, a ~2B flow-matching MM-DiT) and a prompt with several objects, attributes, counts or spatial relations, modify only inference (attention, guidance, latent optimisation or noise selection), with no weight updates, so that the image satisfies every compositional constraint while keeping image quality. Input: prompt (optionally a parsed structure), frozen model. Output: image. Standard evaluation: GenEval, T2I-CompBench++, DPG-Bench, plus a preference model for quality.

## Challenge
MM-DiT models attend jointly over text and image tokens in every block, so UNet-era cross-attention fixes (attend-and-excite, attention-map losses, layout-guided cross-attention) do not carry over directly: text tokens are themselves updated by image tokens, attribute information leaks between noun phrases through joint attention, and count and position errors are decided early in sampling. Existing MM-DiT-specific training-free fixes target one failure type (e.g. attribute leakage or object omission) and often degrade quality or need an external layout from an LLM. Concrete failure: "three red apples and a green cup to the left of a blue book" yields two or four apples, a red cup, or the book on the wrong side, and stronger guidance does not fix the count.

## Constraints
- **Venue and deadline**: CVPR 2027 main track. Paper deadline 2026-11-16 AoE (registration 2026-11-10). Today is 2026-10-17, so every experiment must finish by about 2026-11-09: roughly three weeks of compute.
- **Compute**: at most 2–4 consumer GPUs with 24 GB each (RTX 3090 / 4090) on a shared lab cluster; no NVLink, no multi-node; single-GPU jobs. The whole paper (method, baselines, ablations, evaluation) must fit in ≤ 40 GPU-days. In practice: training-free / inference-time methods, or light fine-tuning (e.g. LoRA, ≤ 2 GPU-days per run) of public pretrained models that fit in 24 GB (diffusion/flow models up to ~3B parameters in bf16; larger ones only for inference with offloading; VLMs up to ~8B).
- **Team and assets**: a small group experienced with diffusion transformers and RL post-training. Already deployed: Wan2.1-T2V-1.3B, Flow-GRPO training code, HPSv3, VideoAlign, RAFT optical flow, VBench evaluation. Assets are a plus, not a requirement.
- **Evaluation**: public benchmarks and metrics computable within the budget; at most a small human study (~150 pairwise judgements).
- **Literature**: no cutoff — search up to today. arXiv work from the last 12 months counts as prior or concurrent work for novelty.
