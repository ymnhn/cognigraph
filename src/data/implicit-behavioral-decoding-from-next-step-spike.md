---
pubDatetime: 2026-05-13T04:55:03.000Z
title: "Implicit Behavioral Decoding from Next-Step Spike Forecasts at Population Scale"
link: "https://arxiv.org/abs/2605.12999v1"
koreanSummary: "인구 규모의 다음 단계 스파이크 예측에서 암시적 행동 디코딩"
---

Closed-loop brain-computer interfaces often require both a forecast of upcoming neural population activity and a readout of the animal's behavioral state. A single Mamba forecaster, trained only on next-step spike counts at Neuropixels scale, can deliver both in one forward pass. A lightweight per-session linear head reading the model's predicted rates decodes behavior better than the same linear classifier reading the raw spike counts, under matched temporal context. We test on the Steinmetz visual-discrimination benchmark, which spans 39 sessions, roughly 27,000 neurons, and 1,994 held-out trials. Across three training seeds, Mamba's predicted rates decode mouse choice at 75.7$\pm$0.2% trial vote, roughly 2.3 times chance level, and stimulus side at 66.1$\pm$0.6%, about twice chance. Compared to a matched 500 ms-context linear decoder on the raw spike counts, Mamba wins at trial vote by 4-6 pp on response and 4-6 pp on stimulus side. A session-start calibration block of about 100-150 trials brings the readout within 1-2 pp of asymptote, and the full pipeline fits inside the 50 ms bin budget on workstation-class GPUs typical of tethered chronic Neuropixels recordings.
