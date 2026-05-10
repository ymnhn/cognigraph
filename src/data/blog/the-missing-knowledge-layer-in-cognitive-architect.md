---
pubDatetime: 2026-04-13T12:05:30.000Z
title: "The Missing Knowledge Layer in Cognitive Architectures for AI Agents"
link: "https://arxiv.org/abs/2604.11364v1"
koreanSummary: "AI 에이전트를 위한 인지 아키텍처에서 누락된 지식 계층"
---

The two most influential cognitive architecture frameworks for AI agents, CoALA [21] and JEPA [12], both lack an explicit Knowledge layer with its own persistence semantics. This gap produces a category error: systems apply cognitive decay to factual claims, or treat facts and experiences with identical update mechanics. We survey persistence semantics across existing memory systems and identify eight convergence points, from Karpathy's LLM Knowledge Base [10] to the BEAM benchmark's near-zero contradiction-resolution scores [22], all pointing to related architectural gaps. We propose a four-layer decom position (Knowledge, Memory, Wisdom, Intelligence) where each layer has fundamentally different persistence semantics: indefinite supersession, Ebbinghaus decay, evidence-gated revision, and ephemeral inference respectively. Companion implementations in Python and Rust demonstrate the architectural separation is feasible. We borrow terminology from cognitive science as a useful analogy (the Knowledge/Memory distinction echoes Tulving's trichotomy), but our layers are engineering constructs justified by persistence-semantics requirements, not by neural architecture. We argue that these distinctions demand distinct persistence semantics in engineering implementations, and that no current framework or system provides this.
