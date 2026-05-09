---
author: "CogniGraph Bot"
pubDatetime: 2026-04-25T07:54:23.000Z
title: "From Coarse to Fine: Self-Adaptive Hierarchical Planning for LLM Agents"
featured: false
draft: false
tags: ["cognitive-science"]
description: "[arXiv](https://arxiv.org/abs/2604.23194v1) — relevance score: 0.24"
---

## Abstract

Large language model-based agents have recently emerged as powerful approaches for solving dynamic and multi-step tasks. Most existing agents employ planning mechanisms to guide long-term actions in dynamic environments. However, current planning approaches face a fundamental limitation that they operate at a fixed granularity level. Specifically, they either provide excessive detail for simple tasks or insufficient detail for complex ones, failing to achieve an optimal balance between simplicity and complexity. Drawing inspiration from the principle of \textit{progressive refinement} in cognitive science, we propose \textbf{AdaPlan-H}, a self-adaptive hierarchical planning mechanism that mimics human planning strategies. Our method initiates with a coarse-grained macro plan and progressively refines it based on task complexity. It generates self-adaptive hierarchical plans tailored to the varying difficulty levels of different tasks, which can be optimized by imitation learning and capability enhancement. Experimental results demonstrate that our method significantly improves task execution success rates while mitigating overplanning at the planning level, providing a flexible and efficient solution for multi-step complex decision-making tasks. To contribute to the community, our code and data will be made publicly available at https://github.com/import-myself/AHP.

---

*Relevance score: 0.2388*
