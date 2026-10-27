# Plan — efficient attention landscape (2026-10-27)

Goal of this run (user request): the user's senior labmate suggested a direction: standard attention pruning, variant attention pruning, hybrid attention architectures, memory matrices, and algorithms for variant attention. Map the current work and open problems so the user understands the area. Stop after MAP THE LANDSCAPE.

## Axes
1. KV cache and token pruning for standard softmax attention
2. Pruning and compression of variant attention mechanisms
3. Hybrid architectures mixing full attention with linear or recurrent layers
4. Memory matrix update rules in linear attention and fast-weight models
5. Hardware-efficient training and inference algorithms for linear and sparse attention

## Active direction
state: `forming`

## History
- `forming` at turn 1: wrote problem.md; spawning gap_finder on axes 1–5 in parallel (independent axes).
- `forming`: gap_finder axis 5 (hardware-efficient algorithms) returned, 2 gaps.
- `forming`: gap_finder axis 3 (hybrid architectures) returned, 2 gaps.
- `forming`: gap_finder axis 4 (memory matrix update rules) returned, 2 gaps.
