---
author: "CogniGraph Bot"
pubDatetime: 2026-04-27T01:01:32.000Z
title: "Towards Localizing Conversation Partners using Head Motion"
featured: false
draft: false
tags: ["cognitive-science"]
description: "[arXiv](https://arxiv.org/abs/2604.23927v1) — relevance score: 0.10"
---

## Abstract

Many individuals struggle to understand conversation partners in noisy settings, particularly amid background speakers or due to hearing impairments. Emerging wearables like smartglasses offer a transformative opportunity to enhance speech from conversation partners. Crucial to this is identifying the direction in which the user wants to listen, which we refer to as the user's acoustic zones of interest. While current spatial audio-based methods can resolve the direction of vocal input, they are agnostic to listening preferences and have limited functionality in noisy settings with interfering speakers. To address this, behavioral cues are needed to actively infer a user's acoustic zones of interest. We explore the effectiveness of head-orienting behavior, captured by Inertial Measurement Units (IMUs) on smartglasses, as a modality for localizing these zones in seated conversations. We introduce HALo, a head-orientation-based acoustic zone localization network that leverages smartglasses' IMUs to non-invasively infer auditory zones of interest corresponding to conversation partner locations. By integrating an a priori estimate of the number of conversation partners, our approach yields a 21% performance improvement over existing methods. We complement this with CoCo, which classifies the number of conversation partners using only IMU data, achieving 0.74 accuracy and a 35% gain over rule-based and generic time-series baselines. We discuss practical considerations for feature extraction and inference and provide qualitative analyses over extended sessions. We also demonstrate a minimal end-to-end speech enhancement system, showing that head-orientation-based localization offers clear advantages in extremely noisy settings with multiple conversation partners.

---

*Relevance score: 0.1018*
