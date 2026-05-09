---
author: "CogniGraph Bot"
pubDatetime: 2026-04-08T23:33:33.000Z
title: "Cognitive-Causal Multi-Task Learning with Psychological State Conditioning for Assistive Driving Perception"
featured: false
draft: false
tags: ["cognitive-science"]
description: "[arXiv](https://arxiv.org/abs/2604.07651v1) — relevance score: 0.32"
---

## Abstract

Multi-task learning for advanced driver assistance systems requires modeling the complex interplay between driver internal states and external traffic environments. However, existing methods treat recognition tasks as flat and independent objectives, failing to exploit the cognitive causal structure underlying driving behavior. In this paper, we propose CauPsi, a cognitive science-grounded causal multi-task learning framework that explicitly models the hierarchical dependencies among Traffic Context Recognition (TCR), Vehicle Context Recognition (VCR), Driver Emotion Recognition (DER), and Driver Behavior Recognition (DBR). The proposed framework introduces two key mechanisms. First, a Causal Task Chain propagates upstream task predictions to downstream tasks via learnable prototype embeddings, realizing the cognitive cascade from environmental perception to behavioral regulation in a differentiable manner. Second, Cross-Task Psychological Conditioning (CTPC) estimates a psychological state signal from driver facial expressions and body posture and injects it as a conditioning input to all tasks including environmental recognition, thereby modeling the modulatory effect of driver internal states on cognitive and decision-making processes. Evaluated on the AIDE dataset, CauPsi achieves a mean accuracy of 82.71% with only 5.05M parameters, surpassing prior work by +1.0% overall, with notable improvements on DER (+3.65%) and DBR (+7.53%). Ablation studies validate the independent contribution of each component, and analysis of the psychological state signal confirms that it acquires systematic task-label-dependent patterns in a self-supervised manner without explicit psychological annotations.

---

*Relevance score: 0.3155*
