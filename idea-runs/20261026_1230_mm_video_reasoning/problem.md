# Reasoning in multimodal and video models

## Problem definition
Given a multimodal model that takes images and/or video plus text (a multimodal LLM / video LLM), or a generative video model, make it solve problems that need multi-step reasoning over visual evidence rather than single-step recognition: visual math and charts, spatial and physical reasoning, temporal and causal reasoning over long videos, and visual planning. Input: image(s) or video, a question or goal. Output: an answer (and usually an explicit reasoning trace in text, in images, or in latent tokens). Typical evaluation: MathVista / MathVerse / MMMU-style visual reasoning, V* / HR-Bench-style fine-grained perception, Video-MME / VSI-Bench / long-video QA, and reasoning-aware probes of whether the trace actually uses the visual evidence.

## Challenge
Text-only reasoning recipes (long chain-of-thought, RL with verifiable rewards, test-time scaling) transfer poorly to vision. Longer text reasoning often makes multimodal models look at the image less: the trace drifts onto language priors, hallucinated visual facts compound, and accuracy on perception-heavy questions stays flat or drops even as math-style benchmarks rise. Video makes this worse: the evidence is sparse in time, the model sees a handful of sampled frames, and the trace cannot go back to fetch the frame it needs. Concrete failure: an R1-style RL-tuned 7B MLLM writes a longer, more confident reasoning trace on a chart or a long video question, yet its answer is no better than the base model's, because the decisive visual detail was never re-inspected and the trace cites a value that is not in the image.

## Constraints
- **Venue and deadline**: none fixed yet. This run is a landscape survey to pick a direction; ACL / EMNLP / ACM MM / NeurIPS / CVPR are all open.
- **Compute** (assumed from the group's earlier runs, to be confirmed): 2–4 GPUs with 24 GB each, single-node; inference-time methods or light fine-tuning (LoRA / small-scale RL) of public models up to ~8B.
- **Assets**: the group knows diffusion transformers and RL post-training (Flow-GRPO, Wan2.1-T2V-1.3B deployed). Assets are a plus, not a requirement.
- **Literature**: no cutoff — search up to today (2026-10-26). arXiv work from the last 12 months counts as prior or concurrent work.
