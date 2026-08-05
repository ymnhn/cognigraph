---
pubDatetime: 2026-08-03T16:20:11.000Z
title: "Intention Inference Under Execution Noise: Separating Aleatoric and Epistemic Uncertainty in Social Dilemmas"
link: "https://arxiv.org/abs/2608.02440v1"
koreanSummary: "실행 소음 하에서 의도 추론: 사회적 딜레마에서 우연적 불확실성과 인식론적 불확실성 분리"
---

In noisy social dilemmas, intended actions are stochastically corrupted before execution, so an observed defection may reflect hostile intent or action error. Standard Markov Decision Process (MDP) formulations treat executed actions as states, structurally precluding this distinction and causing systematic over-retaliation. We introduce a Partially Observable MDP (POMDP) formulation encoding opponent intentions as latent states and executed actions as noisy observations, solved within the active inference (AIF) framework with a cost function that decomposes into epistemic and pragmatic components that jointly address inferring current intent and learning how intent evolves. In the Iterated Prisoner's Dilemma with symmetric noise, we derive a critical noise threshold governing cooperation collapse, connecting it to a fixed-point condition on learned priors. Experiments reveal that the value of intention inference is context-dependent: the POMDP provides consistent advantages against conditionally cooperative opponents, but mutual intention inference under sufficient noise produces correlated belief-driven collapse. The advantage is specific to games where intent attribution is decision-relevant.
