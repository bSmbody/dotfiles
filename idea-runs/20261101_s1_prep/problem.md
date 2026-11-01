# Preparation for GPT ideation: KV-cache compression for long chain-of-thought serving

## Problem definition
Compress the KV cache during the decode phase of long chain-of-thought (16K-64K generated tokens) so that reasoning models, served at memory-saturated batch, spend less wall-clock time and memory per correctly solved problem. Accuracy parity alone is not enough: generated length, loop and length-cap rates must not grow, and the method must beat FP8/FP4 KV on cost per correct answer.

## Challenge
The area is crowded and moves monthly. The newest strong baseline TaSQ (2610.03027, ~1.25-bit KV, SGLang, batch 6->84) keeps output length near BF16 but loses 17.8 AIME25 points on Qwen3-4B-Thinking and 14 NIAH points at 64K. An earlier scouting pass missed it. This run's job is complete coverage of prior work, not ideation.

## Constraints
- Compute ~1 TB H200; not binding. Newcomer student plus kernel help.
- Venue NeurIPS / ICML / ICLR / MLSys. Literature through 2026-11-01; the last 6 months matter most.
