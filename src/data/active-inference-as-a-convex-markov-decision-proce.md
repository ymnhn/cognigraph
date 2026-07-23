---
pubDatetime: 2026-07-22T13:52:40.000Z
title: "Active Inference as a Convex Markov Decision Process"
link: "https://arxiv.org/abs/2607.20152v1"
koreanSummary: "볼록 마르코프 결정 프로세스로서의 능동 추론"
---

Active Inference (AIF) frames adaptive behavior as the minimization of expected free energy (EFE), combining epistemic and pragmatic objectives within a single variational principle. We frame AIF as policy optimization and show that, for closed-loop control policies, EFE minimization can be formulated as a convex Markov decision process (MDP). In this formulation, the pragmatic terms are linear in the predictive state marginals and therefore equivalent to reward maximization in a latent MDP, while the epistemic value introduces a nonlinear component that distinguishes EFE minimization from standard reinforcement learning. This perspective further reveals the epistemic drive of active inference as a policy-dependent (performative) reward. We analyze finite-horizon, discounted, and average-reward formulations of EFE and derive a mirror descent (MD) algorithm that locally linearizes the objective around the current state marginals, yielding a policy-dependent reward that is compatible with actor-critic methods and dynamic programming. Finally, we argue that coupling world-model learning with policy optimization gives active inference the structure of performative reinforcement learning, providing a route toward grounding active inference within modern reinforcement learning and optimization theory, including convergence analysis and principled policy improvement guarantees.
