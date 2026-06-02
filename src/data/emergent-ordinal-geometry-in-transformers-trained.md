---
pubDatetime: 2026-05-31T14:44:54.000Z
title: "Emergent Ordinal Geometry in Transformers Trained on Local Comparisons"
link: "https://arxiv.org/abs/2606.01269v1"
koreanSummary: "로컬 비교를 통해 훈련된 변압기의 새로운 서수 기하학"
---

Transitive inference is the challenge of inferring that A < C from knowing only adjacent relations (A < B, B < C). It is solved by humans and animals not through logical chaining but via an analogue mental number line, whose signature is the symbolic distance effect: distant comparisons are easier than nearby ones. We ask whether Transformers acquire the same primitive, training small models exclusively on adjacent comparisons from a hidden total order and evaluating generalization to unseen distant pairs. We find that out-of-distribution generalization emerges alongside a striking geometric reorganization: entity embeddings collapse onto a one-dimensional manifold whose principal axis recovers the hidden rank order with near-perfect fidelity, and this structure is sensitive to optimization in ways that produce grokking-like transient dynamics. Critically, even when accuracy is at ceiling, decision confidence and geometric separation both scale monotonically with rank distance, directly mirroring the symbolic distance effect observed across decades of behavioural experiments on humans, primates, and rodents. These results ground a 50-year-old behavioural regularity in the geometry of learned representations, offering a mechanistic account of transitive inference that bridges cognitive science and modern neural networks.
