# Baseline-first scouting: inference efficiency for (long-)reasoning LLMs

## Problem definition
Make inference of reasoning LLMs (long chain-of-thought, long context) cheaper in memory, bandwidth and latency without losing accuracy: KV-cache quantization and compression, efficient / sparse / hybrid attention structures as shipped in recent open models, and decoding acceleration for long generations. This run does NOT start from gaps. It starts from the newest strong baselines and architectures (2025-2026, ideally open code and open weights), records their measured results and their own stated limitations, and only then derives unsolved problems and a research scope.

## Challenge
The area is crowded: three earlier ideation rounds found that most natural ideas were already published in 2026. A good scope must sit on top of a strong, reproducible, recent baseline whose authors themselves name a limitation that is still open, with a measured magnitude showing the limitation matters.

## Constraints
- **Compute**: about 1 TB of H200 memory (≈8×H200); not binding.
- **Team**: a new PhD student plus a senior labmate; prefer baselines with public code and weights that a newcomer can run in week 1; kernel work is a cost to flag.
- **Venue**: NeurIPS / ICML / ICLR / MLSys class.
- **Literature**: up to today (2026-10-31); papers from the last 6 months matter most.
