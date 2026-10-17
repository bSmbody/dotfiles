# Training-free open-vocabulary semantic segmentation from frozen foundation models

## Problem definition
Given frozen pretrained vision-language and vision foundation models (e.g. CLIP / SigLIP, DINOv2 / DINOv3, SAM) and an arbitrary list of class names, assign a class label to every pixel of an image without training on any segmentation labels and without fine-tuning any weights. Input: image and class-name list. Output: per-pixel label map. Standard evaluation: mIoU on VOC, Pascal Context, COCO-Object, COCO-Stuff, Cityscapes, ADE20K.

## Challenge
CLIP-style models are trained to align a global image embedding with text; their patch tokens are spatially noisy (attention concentrates on a few global or "sink" tokens), so dense patch–text similarity gives blurry, mislocalised masks. Training-free remedies — rewriting the last attention layer (self-self or neighbourhood attention), borrowing affinities from DINO, refining with SAM, sliding windows — are largely heuristic, can add large inference cost, and still fail on small objects, stuff classes and many-class benchmarks; results on ADE20K and COCO-Stuff remain far below weakly supervised methods. Concrete failure: on a street scene with "pole", "traffic sign", "person", "road", thin poles and small signs are absorbed into the surrounding road or building class even after attention modification.

## Constraints
- **Venue and deadline**: CVPR 2027 main track. Paper deadline 2026-11-16 AoE (registration 2026-11-10). Today is 2026-10-17, so every experiment must finish by about 2026-11-09: roughly three weeks of compute.
- **Compute**: at most 2–4 consumer GPUs with 24 GB each (RTX 3090 / 4090) on a shared lab cluster; no NVLink, no multi-node; single-GPU jobs. The whole paper (method, baselines, ablations, evaluation) must fit in ≤ 40 GPU-days. In practice: training-free / inference-time methods, or light fine-tuning (e.g. LoRA, ≤ 2 GPU-days per run) of public pretrained models that fit in 24 GB (diffusion/flow models up to ~3B parameters in bf16; larger ones only for inference with offloading; VLMs up to ~8B).
- **Team and assets**: a small group experienced with diffusion transformers and RL post-training. Already deployed: Wan2.1-T2V-1.3B, Flow-GRPO training code, HPSv3, VideoAlign, RAFT optical flow, VBench evaluation. Assets are a plus, not a requirement.
- **Evaluation**: public benchmarks and metrics computable within the budget; at most a small human study (~150 pairwise judgements).
- **Literature**: no cutoff — search up to today. arXiv work from the last 12 months counts as prior or concurrent work for novelty.
