---
pubDatetime: 2026-05-31T19:15:13.000Z
title: "Active Inference for Adaptive Traffic Signal Control in Noisy Nonstationary IoT Environments"
link: "https://arxiv.org/abs/2606.13698v1"
koreanSummary: "시끄러운 비정상 IoT 환경에서 적응형 교통 신호 제어를 위한 능동 추론"
---

Urban traffic signal control at IoT-instrumented intersections must remain effective under sensor occlusion, weather attenuation, and nonstationary demand. Conventional controllers degrade under these conditions, and learned policies remain difficult to audit. To address these challenges, we propose an active inference controller for a four-arm signalized intersection that dynamically selects phases by minimizing expected free energy (EFE) over Gaussian beliefs about per-direction congestion levels, yielding a fully traceable decision pipeline. We benchmark the controller in a SUMO traffic simulator against a rule-based heuristic and a deep Q-network (DQN) across four scenarios that progressively increase noise and nonstationarity, spanning sensor occlusion, adverse weather, and stochastic accidents. Across 100 independent random evaluations per scenario, active inference attains the lowest idle times and CO2 emissions in the noisiest scenarios (56,977 s and 29.12 kg vs. 71,741 s and 30.56 kg for DQN). These gains come at a modest cost in bus priority service rate and phase switch frequency.
