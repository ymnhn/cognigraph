---
pubDatetime: 2026-05-16T16:15:59.000Z
title: "PyraVid: Hierarchical Multimodal Memory for Long-Horizon Video Reasoning"
link: "https://arxiv.org/abs/2605.17065v1"
koreanSummary: "PyraVid: 장거리 비디오 추론을 위한 계층적 다중모달 메모리"
---

Memory has become an increasingly important component of agentic systems, as these systems are expected to reason over long-term experience. However, prior work has largely focused on unimodal memory, leaving multimodal memory relatively underexplored despite its central role in real-world applications. Compared with unimodal settings, multimodal memory introduces additional challenges, including heterogeneous input integration, person-centric information alignment, and evidence aggregation across different granularities. We present PyraVid, a hierarchical multimodal memory framework inspired by Event Segmentation Theory from cognitive science. PyraVid organizes long videos into a coarse-to-fine pyramid structure, enabling structured memory access and effective evidence aggregation. It further supports structure-guided memory expansion with pruning, allowing the retrieval of related events with strong causal connectivity but low semantic similarity while reducing noise. Experiments on multiple long-video understanding benchmarks show that PyraVid consistently improves performance across datasets, model scales, and question types, highlighting the effectiveness of hierarchical multimodal memory for long-horizon reasoning.
