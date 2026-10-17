# Compute-efficient inference-time search for diffusion and flow generators

## Problem definition
Given a pretrained image or video diffusion/flow model, a frozen reward or verifier (e.g. a human-preference model, a VLM judge, or a text-alignment scorer) and a fixed inference compute budget (generator function evaluations plus verifier calls), decide how to spend the budget — how many initial noises, when to branch, prune or resample trajectories, which intermediate states to score — to maximise the quality of the final sample, with no weight updates. Input: prompt, models, budget. Output: one sample. Typical evaluation: held-out preference models, GenEval / T2I-CompBench-style alignment, diversity, all as a function of compute.

## Challenge
Best-of-N wastes most of its compute on trajectories that were doomed early. Sequential Monte Carlo and particle methods resample on intermediate rewards computed from noisy or one-step x̂0 predictions, which are unreliable at high noise, so they prune good trajectories and collapse diversity. And pushing a single verifier hard at inference time reward-hacks it: the verifier score keeps rising while held-out preference and text alignment plateau or fall. Concrete failure: with 4× the compute of a single sample, particle-based guidance on a 2B image model raises its own reward-model score, but a held-out preference model and a GenEval-style alignment check show no gain over plain best-of-4.

## Constraints
- **Venue and deadline**: CVPR 2027 main track. Paper deadline 2026-11-16 AoE (registration 2026-11-10). Today is 2026-10-17, so every experiment must finish by about 2026-11-09: roughly three weeks of compute.
- **Compute**: at most 2–4 consumer GPUs with 24 GB each (RTX 3090 / 4090) on a shared lab cluster; no NVLink, no multi-node; single-GPU jobs. The whole paper (method, baselines, ablations, evaluation) must fit in ≤ 40 GPU-days. In practice: training-free / inference-time methods, or light fine-tuning (e.g. LoRA, ≤ 2 GPU-days per run) of public pretrained models that fit in 24 GB (diffusion/flow models up to ~3B parameters in bf16; larger ones only for inference with offloading; VLMs up to ~8B).
- **Team and assets**: a small group experienced with diffusion transformers and RL post-training. Already deployed: Wan2.1-T2V-1.3B, Flow-GRPO training code, HPSv3, VideoAlign, RAFT optical flow, VBench evaluation. Assets are a plus, not a requirement.
- **Evaluation**: public benchmarks and metrics computable within the budget; at most a small human study (~150 pairwise judgements).
- **Literature**: no cutoff — search up to today. arXiv work from the last 12 months counts as prior or concurrent work for novelty.
