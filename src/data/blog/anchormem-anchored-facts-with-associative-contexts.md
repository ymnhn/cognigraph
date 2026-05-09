---
author: "CogniGraph Bot"
pubDatetime: 2026-04-19T11:02:08.000Z
title: "AnchorMem: Anchored Facts with Associative Contexts for Building Memory in Large Language Models"
featured: false
draft: false
tags: ["cognitive-science"]
description: "[arXiv](https://arxiv.org/abs/2604.17377v1) — relevance score: 0.16"
---

## Abstract

While large language models have achieved remarkable performance in complex tasks, they still need a memory system to utilize historical experience in long-term interactions. Existing memory methods (e.g., A-Mem, Mem0) place excessive emphasis on organizing interactions by frequently rewriting them, however, this heavy reliance on summarization risks diluting essential contextual nuances and obscuring key retrieval features. To bridge this gap, we introduce AnchorMem, a novel memory framework inspired by the Proust Phenomenon in cognitive science, where a specific anchor triggers a holistic recollection. We propose a method that decouples the retrieval unit from the generation context. AnchorMem extracts atomic facts from interaction history to serve as retrieval anchors, while preserving the original context as the immutable context. To reveal implicit narrative cues, we construct an associative event graph that uses higher-order event links that bind sets of related facts into shared event representations, strengthening cross-memory integration without relying on generic entities as bridges. During retrieval, the system anchors queries to specific facts and events to locate relevant memories, but reconstructs the context using the associated raw chunks and events. Our method reconciles fine-grained retrieval with the contextual integrity of interactions. Experiments across three closed-source and open-source models on the LoCoMo benchmark demonstrate that AnchorMem significantly outperforms baselines. Code is available at https://github.com/RayNeo-AI-2025/AnchorMem.

---

*Relevance score: 0.1553*
