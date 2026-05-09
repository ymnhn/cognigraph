---
author: "CogniGraph Bot"
pubDatetime: 2026-04-30T14:34:31.000Z
title: "Flying by Inference: Active Inference World Models for Adaptive UAV Swarms"
featured: false
draft: false
tags: ["cognitive-science"]
description: "[arXiv](https://arxiv.org/abs/2604.27935v1) — relevance score: 0.21"
---

## Abstract

This paper presents an expert-guided active-inference-inspired framework for adaptive UAV swarm trajectory planning. The proposed method converts multi-UAV trajectory design from a repeated combinatorial optimization problem into a hierarchical probabilistic inference problem. In the offline phase, a genetic-algorithm planner with repulsive-force collision avoidance (GA--RF) generates expert demonstrations, which are abstracted into Mission, Route, and Motion dictionaries. These dictionaries are used to learn a probabilistic world model that captures how expert mission allocations induce route orders and how route orders induce motion-level behaviors. During online operation, the UAV swarm evaluates candidate actions by forming posterior beliefs over symbolic states and minimizing KL-divergence-based abnormality indicators with respect to expert-derived reference distributions. This enables mission allocation, route insertion, motion adaptation, and collision-aware replanning without rerunning the offline optimizer. Bayesian state estimators, including EKF and PF modules, are integrated at the motion level to improve trajectory correction under uncertainty. Simulation results show that the proposed framework preserves expert-like planning structure while producing smoother and more stable behavior than modified Q-learning. Additional validation using real-flight UAV trajectory data demonstrates that the learned world model can correct symbolic predictions under noisy and non-smooth observations, supporting its applicability to adaptive UAV swarm autonomy.

---

*Relevance score: 0.2115*
