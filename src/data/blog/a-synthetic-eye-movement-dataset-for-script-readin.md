---
author: "CogniGraph Bot"
pubDatetime: 2026-04-07T06:15:48.000Z
title: "A Synthetic Eye Movement Dataset for Script Reading Detection: Real Trajectory Replay on a 3D Simulator"
featured: false
draft: false
tags: ["cognitive-science"]
description: "[arXiv](https://arxiv.org/abs/2604.05475v1) — relevance score: 0.20"
---

## Abstract

Large vision-language models have achieved remarkable capabilities by training on massive internet-scale data, yet a fundamental asymmetry persists: while LLMs can leverage self-supervised pretraining on abundant text and image data, the same is not true for many behavioral modalities. Video-based behavioral data -- gestures, eye movements, social signals -- remains scarce, expensive to annotate, and privacy-sensitive. A promising alternative is simulation: replace real data collection with controlled synthetic generation to produce automatically labeled data at scale.   We introduce infrastructure for this paradigm applied to eye movement, a behavioral signal with applications across vision-language modeling, virtual reality, robotics, accessibility systems, and cognitive science. We present a pipeline for generating synthetic labeled eye movement video by extracting real human iris trajectories from reference videos and replaying them on a 3D eye movement simulator via headless browser automation. Applying this to the task of script-reading detection during video interviews, we release final_dataset_v1: 144 sessions (72 reading, 72 conversation) totaling 12 hours of synthetic eye movement video at 25fps.   Evaluation shows that generated trajectories preserve the temporal dynamics of the source data (KS D < 0.14 across all metrics). A matched frame-by-frame comparison reveals that the 3D simulator exhibits bounded sensitivity at reading-scale movements, attributable to the absence of coupled head movement -- a finding that informs future simulator design. The pipeline, dataset, and evaluation tools are released to support downstream behavioral classifier development at the intersection of behavioral modeling and vision-language systems.

---

*Relevance score: 0.2040*
