# Synthetic sanity check of G-C2 (Operator-Coupled KV Rounding), 2026-11-01

Synthetic data: d=128, 2048 tokens = 16 blocks of 128; K with log-normal channel scales plus 4 outlier channels (x8);
V standard normal; K per-channel 2/3-bit grids per block (KIVI-style), V per-token 2/1-bit grids. Attention sharpness
set by scaling scores (entropy ~7.2 / ~4.0 / ~0.8 nats; uniform = 7.6). "Rotated" = random orthogonal rotation of K and q
(stand-in for Hadamard; scores unchanged before quantization). Metrics: forward KL(p || p_hat) for K; relative readout
error ||p(V_hat - V)||^2 / ||pV||^2 for V. Scripts: c2sim.py (8 trials), c2sim_k.py and c2sim_rot.py (60 trials, medians).
This is NOT real-model evidence; it only tests the candidate's local claims and the choice of comparator.

## K: attention forward-KL (median of 60 trials)
| setting | RTN | independent SR | coupled SR (C2) | coupled < indep | coupled < RTN |
|---|---|---|---|---|---|
| K2, no rotation, diffuse | 0.098 | 0.200 | 0.189 | 65% | 0% |
| K2, no rotation, medium | 0.809 | 1.694 | 1.695 | 55% | 2% |
| K2, no rotation, sharp | 2.062 | 4.769 | 5.977 (mean 6.75 vs 5.37) | 40% | 25% |
| K2, rotated, diffuse | 0.128 | 0.252 | 0.259 | 52% | 0% |
| K2, rotated, medium | 0.954 | 2.129 | 2.095 | 57% | 5% |
| K2, rotated, sharp | 4.681 | 7.819 | 6.106 | 52% | 37% |
| K3, rotated, diffuse | 0.019 | 0.037 | 0.032 | 65% | 0% |
| K3, rotated, medium | 0.180 | 0.352 | 0.366 | 43% | 7% |
| K3, rotated, sharp | 0.469 | 0.572 | 0.794 | 52% | 37% |

## V: relative readout error (mean of 8 trials)
| setting | RTN | independent SR | dependent rounding (C2) |
|---|---|---|---|
| V2, diffuse | 0.248 | 0.520 | 0.272 |
| V2, medium | 0.239 | 0.482 | 0.495 |
| V2, sharp | 0.266 | 0.523 | 0.533 |
| V1, diffuse | 3.849 | 5.476 | 2.899 |
| V1, medium | 3.746 | 5.752 | 5.650 |
| V1, sharp | 3.883 | 6.160 | 6.036 |

## Reading
1. RTN beats both stochastic schemes on K by about 2x KL in every setting; coupling vs independent SR is roughly a coin flip
   (40-65% wins) and is worse in mean at sharp attention without rotation. The candidate's own kill condition
   ("stop if C2 beats only independent SR, not RTN/KVarN") would very likely fire on K.
2. V dependent rounding only helps when attention is diffuse (block-sum preservation then matters): it nearly matches RTN at
   V2 and beats RTN at V1. With medium or sharp attention it equals independent SR and loses to RTN.
3. The only regime with a possible win is V1 under diffuse attention, which is exactly where V precision matters least;
   retrieval heads and once-stated facts (sharp attention) get no benefit. V1 errors are large (>280% relative) in all
   variants with a naive min/max per-token grid.
