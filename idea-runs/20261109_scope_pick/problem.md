# Efficient long-reasoning inference for thinking VLMs: visual KV storage, reading and re-looking

## Problem definition
Thinking vision-language models (e.g., Qwen3-VL-8B-Thinking, Qwen2.5-VL with long CoT, DeepEyes-style "thinking with images" models) first ingest thousands to tens of thousands of visual tokens (high-resolution images, multi-image, video), then generate thousands to tens of thousands of chain-of-thought tokens, sometimes re-looking at image regions (crop/zoom tool calls that append newly encoded tokens). Serving them is bounded by KV cache memory (batch size at memory saturation) and by per-step KV reads. Goal: a NEW MECHANISM that lowers cost per correct answer (fixed 8xH200, memory-saturated serving) on MathVista, MathVerse, V*, HR-Bench, Video-MME, LVBench, by changing what visual information is stored, how attention reads it, or how re-looking enters the context.

## Challenge
- Per decoding step only a small subset of visual tokens matters and that subset changes over the reasoning (VisionPulse 2605.31457), so prefill-time selection or permanent eviction is unsafe; decode-time queries have much larger variance than prefill proxies (MM-ShiftKV 2607.22586). Step-wise sparse reading saves reads but all visual KV stays in HBM.
- RL-trained reasoning VLMs attend less to visual tokens as CoT grows (2505.21523); 72-78% of failures are perception errors (2506.07218); longer thinking does not fix perception failures (L2T 2610.15810).
- Re-looking appends thousands of new tokens per crop; replacing the crop with noise barely changes DeepEyes / Pixel Reasoner answers (2510.23482); reusing stale visual KV breaks positional binding (PRCR 2606.26631).
- Visual KV depends only on the image and the preceding prompt, not on the generated CoT.

## Constraints
Target NeurIPS/ICLR/CVPR/MLSys method paper. 8x H200; training-free or light training (LoRA, a few GPU-days). Open models: Qwen2.5-VL, Qwen3-VL (+Thinking). One PhD student with AI coding help, ~3 months, vLLM/SGLang/HF. The user wants mechanism-level innovation (change what is computed/stored/exchanged, with an effect guaranteed by a principle), NOT detect -> repair control loops, thresholds or allocation schedulers.
