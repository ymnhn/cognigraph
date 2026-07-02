---
pubDatetime: 2026-05-23T17:03:42.000Z
title: "Measuring Reasoning Quality in LLMs: A Multi-Dimensional Behavioral Framework"
link: "https://arxiv.org/abs/2605.24661v3"
koreanSummary: "LLM의 추론 품질 측정: 다차원적 행동 프레임워크"
---

Despite remarkable progress on reasoning benchmarks, current LLM evaluation practice remains anchored to final-answer correctness, providing limited insight into how models reason, how reliably they behave under contextual variation, or how efficiently they reach conclusions. This paper proposes a unified multi-dimensional framework for measuring LLM reasoning quality from a behavioral perspective, operationalizing six theoretically grounded dimensions rooted in cognitive science: Correctness (CQ), Consistency (CS), Robustness (RS), Local Logical Coherence (LS), Efficiency (ES), and Stability (SS). The framework introduces deployment-aware aggregation, enabling context-specific model selection beyond accuracy-based leaderboards. Experiments across multiple LLMs and benchmarks reveal behaviors systematically concealed by single-metric evaluation, including the orthogonality of local logical coherence and correctness, deployment-context-dependent ranking inversions, and non-trivial dimensional profiles in small locally-deployed models. Discriminant validity analysis confirms that the proposed dimensions capture largely non-redundant signals. The resulting pipeline provides a foundation for diagnosing LLM reasoning behavior across deployment contexts, with domain-specific validation as a direction for future work.
