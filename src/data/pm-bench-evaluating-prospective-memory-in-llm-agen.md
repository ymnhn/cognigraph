---
pubDatetime: 2026-07-14T05:57:32.000Z
title: "PM-Bench: Evaluating Prospective Memory in LLM Agents"
link: "https://arxiv.org/abs/2607.12385v1"
koreanSummary: "PM-Bench: LLM 에이전트의 예상 메모리 평가"
---

A significant challenge in agentic AI is prospective memory: the ability to execute an intention at a specific future cue or state while other activities are ongoing. We introduce PM-Bench, a text-based benchmark for measuring prospective memory capabilities in modern LLM agents. Inspired by the Virtual Week paradigm from cognitive science, PM-Bench evaluates how well LLM agents maintain user intentions, execute delayed intentions, and monitor latent environment changes. Over the course of a simulated seven-day week, agents must continue an ongoing activity while deciding whether any deferred task is due. We compare eight state-of-the-art LLMs on PM-Bench under eight different agent configurations. PM-Bench proves challenging across all settings: the best method, a GPT-5.4 agent, reaches only 65.1\% F1 score under our evaluation. Furthermore, no single strategy for improving prospective memory dominates across models. We release PM-Bench as a controlled testbed for diagnosing these failures and developing training or inference-time interventions that support reliable prospective behavior.
