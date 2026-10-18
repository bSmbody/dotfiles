### C1 — Phrase-slot competition in the text-query rows of MM-DiT joint attention

- **Intuition**: Treat each noun phrase's text tokens in an MM-DiT as a "slot". In the text-query rows of joint attention, make the phrases compete for every image token, the way Slot Attention normalises attention over slots. A phrase's tokens can then absorb an image region only to the extent that they out-claim the other phrases for it. This routes the text stream per phrase and per block using the model's own affinities, with no layout, no extra pass and no latent gradients.

- **Gap it attacks**: Axis "attribute leakage and object omission through MM-DiT joint attention", Gap 1 (layout-free fixes treat each text token as a fixed carrier of its phrase). Take "a red apple and a green cup". In every joint block the "cup" tokens' attention over image tokens is normalised on its own, so nothing stops them from absorbing the apple's red region. In the next block they hand that content to the image tokens that read "cup". Today's layout-free fixes act only downstream:
  - EnMMDiT [2411.18301] and FOCUS [2510.02315] steer the latent.
  - DeLeaker [2510.15015] edits only the image-query rows.
  - Prompt Reinjection [2602.06886] applies one shared weight to every token.

  DreamRenderer [2503.12885] does route what each phrase's text tokens absorb, but only from user boxes. Closing the gap would give a zero-extra-NFE, layout-free control at the point where this leakage path is written: the early, text-dominated updates [2606.15796]. It would also show how much MM-DiT leakage travels through text-token updates. It leaves token keys free, so it can stack with key-side omission fixes such as OSI [2605.14270].

- **Source inspiration**: Object-centric learning and doubly stochastic attention.
  - **Slot Attention** [2006.15055]. Attention is normalised over the slots (the queries), not over the inputs. Each input's attention therefore has to be shared out among the slots, which makes them "compete for explaining parts of the input" and specialise to separate objects. When the softmax is put back on the input axis, as in ordinary attention, each slot's attention becomes "independent of all other slots", and performance "significantly" drops. A stripped soft-k-means version with no GRU and identity projections still reaches 75.5% ARI against 98.8% for the full module, so the competition itself does much of the grouping. The paper also recommends a separate background slot and shows that a rough upper bound on the number of slots is enough.
  - **Sinkformers** [2110.11773]. In trained softmax Transformers the column sums of attention drift toward 1 during training, so adding a normalisation over queries is close to the regime the model already learns.
  - **LOTFormer** [2509.23436]. Its plug-and-play protocol swaps doubly stochastic attention, including Sinkhorn, into a frozen trained translation encoder with no training. The cost is at most about 0.2 BLEU (33.40 to 33.36 for Sinkformer).

  Novelty type: recombination-of-distant-concepts.

- **How it maps to this problem**:
  - **Slots** are the token groups of each parsed noun phrase (noun plus its modifiers, found by a rule-based parser, so no LLM layout). One extra "rest of the prompt" group (relation words, padding and special tokens) plays the background slot.
  - **Inputs** are the image tokens of the joint sequence.
  - **Slot iterations** are the successive joint (double-stream) blocks and early steps, since each block's text-token update is a slot update.
  - **The competition** applies only in the text-query rows. Each image token's availability is first shared out across the phrases in proportion to their affinities for it. Each phrase's tokens then take their usual weighted mean over what they won, so a region claimed by "apple" stays mostly closed to "cup", while unclaimed background stays open to all.
  - **What stays as in the base model**:
    - The image-query rows already hold a competition: each image token's softmax runs over all text tokens.
    - The text-to-text part is left alone because DeLeaker found that hard cross-entity text-text suppression degrades results by 9–20% [2510.15015].
  - **Optional ablation**: other phrases' text tokens could later be treated as contested inputs in the same soft way.

- **Why it could work / feasibility**:
  - **Ownership assumption.** The mechanism assumes that each input mostly belongs to one object, and image patches of distinct objects mostly do. In FLUX, the image-text affinities already separate entities at the first step and only "blend by a middle step" in leakage cases [2510.15015]. Competition therefore has a correct early signal to keep sharp, rather than one to invent.
  - **The missing ingredient is exactly what Slot Attention adds.** In MM-DiT text-query rows each phrase normalises over image keys on its own: the softmax-over-inputs configuration that Slot Attention shows prevents specialisation [2006.15055].
  - **The leakage path runs through text-token updates.**
    - The FLUX cup-turns-red error traces to spurious red features in the text stream, and text-stream attribution dominates early steps (89.9% at step 0) [2606.15796].
    - T5 outputs mostly keep phrases apart (89% of items carry nothing from other items; "dog" encodes nothing of "green"), so cross-phrase attribute mixing is written inside the denoiser [2504.01137].
    - Per-instance routing of text-token absorption fixes binding, with larger gains as the instance count grows [2503.12885].
  - **A frozen model plausibly tolerates the change.** Query-axis normalisation sits near what trained attention already does [2110.11773], and it survives a training-free swap into a frozen model [2509.23436]. Here it touches only a few dozen phrase-token rows and is soft, with no minus-infinity masks, unlike the naive hard isolation that hurt quality in [2503.12885].
  - **Cost.** No extra NFE and no backpropagation, so SD3.5-M runs inside 24 GB and FLUX runs with offloading.
  - **Key assumption that must hold.** In the early joint blocks, a non-negligible share of each phrase token's update comes from image keys, and the text-to-image affinities already rank the right phrase highest on most of an object's tokens.

- **Novelty vs. closest in-domain work**: DeLeaker [2510.15015] is also layout-free FLUX attention reweighting. However, every edit it makes has an image token as the query. It uses hard thresholded masks frozen from early steps, and it does not control what text tokens absorb. C1 changes only the text-query rows, with no mask or threshold, and re-derives ownership by competition in every block. Two other near neighbours:
  - DreamRenderer [2503.12885] routes the text-query rows but needs user boxes.
  - FreeFuse [2510.23515] derives masks in a separate first pass and biases only the image-query rows.

- **Main risk**: When leakage is written (the first, text-dominated steps), the text-to-image affinities over still-noisy image tokens may not yet favour the right phrase. Competition would then be inert, or it would lock in a wrong early split and starve an omitted phrase of image support. This is DeLeaker's "cannot create a mask if not formed early" failure in another form.


- **Precision notes**:
  - **Ownership signal.** DeLeaker's early-step evidence [2510.15015] concerns image-query-to-text scores. Text-query-to-image scores come from a different query-key product, so whether they separate phrases equally early is the key assumption above. If they lag, the phrase shares can be read instead from the same block's image-query rows, which are already normalised over text tokens. That keeps the idea intact: phrases compete for image tokens, and only the text-query rows are changed.
  - **Follow the Flow statistic.** The 89% figure in [2504.01137] means that 89% of tokens, when generated alone, show no other prompt item. The "green dog" example is within one item: the T5 noun token does not even carry its own attribute. Both point to attribute binding, and its failures, being formed inside the denoiser.
