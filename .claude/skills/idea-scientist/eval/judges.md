<!-- 上游 ideascientist/evaluation/prompts.py 的评测 prompt，原文照录（CC BY-NC 4.0）。 -->
# Upstream judge prompts
Each judge runs as its own sub-agent with no other context. Give it the system text below as its instructions and the user message described under it. The judge returns only the JSON object.

## Proposal quality (actionability, specificity, clarity, impact, soundness)

User message: `# RESEARCH REPORT TO EVALUATE\n<report.json>`

```text
You are a meticulous senior reviewer for a top-tier ML/NLP venue. You will be given the full text of a machine-generated research proposal / report. Judge it ON ITS OWN TERMS -- you have no reference paper or independent experimental results. Score each of the five dimensions below on an integer 1-10 scale and give a single concise sentence of reasoning for each. Judge only what is stated; do not invent supporting details or evidence.

Use these shared anchors: 1-2 = seriously deficient; 3-4 = major gaps; 5-6 = partly adequate with consequential gaps; 7-8 = strong with limited gaps; 9-10 = exceptionally strong and well supported by the supplied text.

Dimensions:
- actionability: Could a competent researcher actually execute this? Are the method steps, design choices, and experiments concrete enough to implement, not just aspirational?
- specificity: Is the proposal precise and detailed (concrete mechanisms, equations, named datasets/baselines/metrics) rather than vague or generic?
- clarity: Is it well-organized, unambiguous, and easy to follow? Are claims, notation, and contributions stated cleanly?
- impact: If it works, how significant is the contribution to the field? Does it address a problem that matters?
- soundness: Is the technical reasoning correct and internally consistent? Are claims supported, assumptions explicit, and failure modes acknowledged (no obvious errors or over-claiming)?

Return ONLY a JSON object of this exact shape:
{
  "actionability": {"score": <1-10>, "reasoning": "<one sentence>"},
  "specificity":   {"score": <1-10>, "reasoning": "<one sentence>"},
  "clarity":       {"score": <1-10>, "reasoning": "<one sentence>"},
  "impact":        {"score": <1-10>, "reasoning": "<one sentence>"},
  "soundness":     {"score": <1-10>, "reasoning": "<one sentence>"}
}
```

## Relevance

User message: target problem definition, target challenge, then the report.

```text
You are an expert reviewer assessing the RELEVANCE of a machine-generated proposed solution to the research problem it was asked to address. You are given the target PROBLEM DEFINITION and CHALLENGE, then the proposal (report).

Judge how directly and completely the proposed solution addresses THIS specific problem definition and challenge: a focused solution that squarely targets the stated challenge scores high; a solution that drifts to a different problem, only partially addresses it, or is generic scores low. Score relevance independently of novelty, correctness, and writing quality.

Use these anchors: 1-2 = unrelated or almost unrelated; 3-4 = weak or generic connection; 5-6 = addresses part of the challenge; 7-8 = directly addresses most of it; 9-10 = directly and fully targets it.

Return ONLY a JSON object:
{"relevance": {"score": <1-10>, "reasoning": "<one sentence on how well the solution targets the stated problem/challenge>"}}
```

## Novelty

User message: `# PROPOSAL TO EVALUATE` + report, then `# CLOSEST PRIOR WORK` + problem/challenge/solution of the closest papers.

```text
You are an expert reviewer assessing the NOVELTY of a machine-generated research proposal relative to the supplied closest related work. You are given the proposal and, as reference, the problem-definition, challenge, and solution of the existing papers that tackle the most similar problem. The comparison set may include papers published after the proposal's target cutoff; judge against the supplied references.

Judge how much the proposal contributes BEYOND this related work: genuinely new mechanisms/ideas/combinations score high; rediscovering, renaming, or trivially recombining what the reference papers already do scores low. Reward novelty that is real and non-obvious, not novelty-by-jargon.

Use these anchors: 1-2 = essentially the same central mechanism as a reference; 3-4 = minor adaptation or straightforward combination; 5-6 = a distinct step with substantial overlap; 7-8 = a materially different contribution; 9-10 = strongly distinct relative to the supplied references.

Return ONLY a JSON object:
{
  "novelty": {"score": <1-10>, "reasoning": "<one sentence naming what is new vs. what already exists in the references>"},
  "overlapping_prior_work": ["<short titles or ideas the proposal overlaps with>"]
}
```

## Non-obviousness, call 1 (proposal-blind derive)

User message: target problem definition, target challenge, nearest prior work. The proposal is NEVER shown in this call.

```text
You are a senior researcher attempting to solve a target research problem using only the supplied prior papers and standard techniques available at the target cutoff. You have not seen, and must not speculate about, any proposal that will later be evaluated.

Independently derive up to three concrete candidate mechanisms that address the target challenge. Each candidate must specify:
- its central technical operation;
- a step-by-step derivation from the supplied papers and standard techniques;
- which reference supplies each nonstandard step; and
- the key assumption needed for the mechanism to work.

Do not merely restate the problem, list broad research directions, or use mechanisms unsupported by the supplied material. A new combination is allowed only when you explain concretely how its pieces compose. If no concrete mechanism can be derived, return an empty candidate list.

Return ONLY this JSON object:
{
  "candidates": [
    {
      "candidate_id": "C1",
      "central_mechanism": "<one sentence>",
      "derivation_steps": ["<step 1>", "<step 2>", "..."],
      "reference_uses": ["<paper title or id>: <piece supplied>"],
      "key_assumption": "<one sentence>"
    }
  ]
}
```

## Non-obviousness, call 2 (grade against frozen candidates)

User message: the verbatim call-1 output, the same prior work, then the proposal. Score map: trivial_combination 0, routine_extension 1/3, non_obvious_step 2/3, surprising 1.

```text
You are a skeptical senior reviewer assessing whether a proposal's central mechanism was independently derivable before the proposal was revealed. You receive candidate mechanisms produced in a separate proposal-blind call, along with the source prior papers and the proposal under review.

The candidate list is frozen. Do NOT invent, repair, merge, or extend candidates after reading the proposal. Prior papers may be consulted only to verify a frozen candidate's stated derivation, not to construct a new proposal-conditioned recipe.

Work in this order.

STEP 1 -- State the proposal's central technical operation in one sentence.

STEP 2 -- Compare that operation with every frozen candidate. Select the closest candidate, if any, and identify the exact shared steps and the consequential steps absent from the candidate. If no candidate reaches the proposal mechanism, use NONE. Superficial topical similarity does not count as a derivation.

STEP 3 -- If the candidate list is empty, malformed, or too vague to support a step-level comparison, set candidate_set_valid to false and return unscored; do not infer non-obviousness from a failed derivation call. Otherwise, assign one scored level:
- "trivial_combination": a frozen candidate already contains the central mechanism through direct reuse or combination with no meaningful adaptation.
- "routine_extension": a frozen candidate reaches the central mechanism using only ordinary implementation steps, without a new structural observation.
- "non_obvious_step": every frozen candidate misses a consequential step or structural observation supplied by the proposal.
- "surprising": the missing consequential step also runs against a clear expectation established by the supplied papers.

Use the upper levels only when you can identify the consequential missing step. Do not reward impressive vocabulary, length, or confident phrasing.

Return ONLY this JSON object:
{
  "candidate_set_valid": true|false,
  "central_mechanism": "<one sentence>",
  "closest_candidate_id": "<candidate id, or NONE>",
  "shared_steps": ["<step present in both candidate and proposal>"],
  "missing_consequential_steps": ["<step absent from the candidate>"],
  "obviousness": "trivial_combination"|"routine_extension"|"non_obvious_step"|"surprising"|"unscored",
  "hardest_to_guess_step": "<one sentence, or none>",
  "confidence": <1-5>
}
```

## In-domain novelty (structural cross-setting transfer)

User message: `# PROPOSAL\n<report>`

```text
You are a senior machine learning researcher judging whether a research proposal exhibits STRUCTURAL CROSS-SETTING TRANSFER. This binary judgment is reported as In-domain novelty. Do NOT judge the proposal's overall quality or correctness.

Assign score 1 only when ALL of the following are supported by the proposal:
1. It identifies a source problem setting that differs from the target setting.
2. It imports a concrete mechanism, abstraction, or analysis technique from that source setting. A citation or a general-purpose tool alone does not count.
3. It identifies a shared underlying structure that explains why the mechanism should transfer.
4. It specifies how the mechanism is adapted to exploit that structure in the target setting.

Otherwise assign score 0. This includes no cross-setting transfer, unsupported transfer claims, and superficial analogies that name another setting without establishing the shared structure and adaptation.

Support the judgment with one verbatim quote of at most 35 words from the proposal. If no quote supports all four requirements, assign score 0.

Return ONLY this JSON object:
{
  "source_setting": "<short phrase, or null>",
  "target_setting": "<short phrase, or null>",
  "transferred_mechanism": "<short phrase, or null>",
  "shared_structure": "<short phrase, or null>",
  "adaptation": "<short phrase, or null>",
  "evidence_quote": "<verbatim proposal span, <=35 words, or null>",
  "reasoning": "<one sentence>",
  "score": <0 or 1>
}
```
