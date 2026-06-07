---
pubDatetime: 2026-06-03T14:24:53.000Z
title: "What Type of Inference is Active Inference?"
link: "https://arxiv.org/abs/2606.04935v1"
koreanSummary: "능동적 추론은 어떤 유형의 추론인가요?"
---

Active inference casts decision-making as inference, with the Expected Free Energy (EFE) unifying goal-directed and information-seeking behavior. Recent work showed that EFE minimization can be written as Variational Free Energy (VFE) minimization on a generative model augmented with epistemic priors. We prove that the VFE of the augmented model can be rewritten as the VFE of the predictive model plus explicit entropy-correction terms, making the EFE contribution transparent. We then show that proper EFE-based planning requires combining these epistemic corrections with a planning correction that turns marginal inference into policy optimization, yielding a full variational characterization of EFE-based planning. This clarifies which corrections are needed for cross-entropy planning and for full EFE-based planning. The same entropy-corrected formulation leads to a detailed message-passing scheme for EFE-based planning together with simpler ablations. Experiments on three grid-world environments show that the planning correction already helps when observations are decisive, whereas the additional observation-side epistemic corrections matter most when observations are merely suggestive.
