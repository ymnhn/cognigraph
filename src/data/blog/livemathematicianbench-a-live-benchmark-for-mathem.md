---
author: "CogniGraph Bot"
pubDatetime: 2026-04-02T08:22:17.000Z
title: "LiveMathematicianBench: A Live Benchmark for Mathematician-Level Reasoning with Proof Sketches"
featured: false
draft: false
tags: ["research", "cognitive-science"]
description: "[arXiv](https://arxiv.org/abs/2604.01754v1) — relevance score: 0.29"
---

## Abstract

Mathematical reasoning is a hallmark of human intelligence, and whether large language models (LLMs) can meaningfully perform it remains a central question in artificial intelligence and cognitive science. As LLMs are increasingly integrated into scientific workflows, rigorous evaluation of their mathematical capabilities becomes a practical necessity. Existing benchmarks are limited by synthetic settings and data contamination. We present LiveMathematicianBench, a dynamic multiple-choice benchmark for research-level mathematical reasoning built from recent arXiv papers published after model training cutoffs. By grounding evaluation in newly published theorems, it provides a realistic testbed beyond memorized patterns. The benchmark introduces a thirteen-category logical taxonomy of theorem types (e.g., implication, equivalence, existence, uniqueness), enabling fine-grained evaluation across reasoning forms. It employs a proof-sketch-guided distractor pipeline that uses high-level proof strategies to construct plausible but invalid answer choices reflecting misleading proof directions, increasing sensitivity to genuine understanding over surface-level matching. We also introduce a substitution-resistant mechanism to distinguish answer recognition from substantive reasoning. Evaluation shows the benchmark is far from saturated: Gemini-3.1-pro-preview, the best model, achieves only 43.5%. Under substitution-resistant evaluation, accuracy drops sharply: GPT-5.4 scores highest at 30.6%, while Gemini-3.1-pro-preview falls to 17.6%, below the 20% random baseline. A dual-mode protocol reveals that proof-sketch access yields consistent accuracy gains, suggesting models can leverage high-level proof strategies for reasoning. Overall, LiveMathematicianBench offers a scalable, contamination-resistant testbed for studying research-level mathematical reasoning in LLMs.

---

*Relevance score: 0.2884*
