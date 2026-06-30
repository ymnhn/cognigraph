---
pubDatetime: 2026-06-28T11:12:52.000Z
title: "W4A4 Quantization for Inference on Wan2.2-I2V-A14B"
link: "https://arxiv.org/abs/2606.29337v1"
koreanSummary: "Wan2.2-I2V-A14B 추론을 위한 W4A4 양자화"
---

We summarize our submission to Sub-Challenge 1: W4A4 Quantization for Inference (HiF4 / MXFP4) of the ICME 2026 Low-Bit-width Large-Model Quantization Challenge. The sub-challenge targets 4-bit weight and 4-bit activation inference on Wan-AI/Wan2.2-I2V-A14B under HiF4 or MXFP4 numerical formats. We adapt two complementary ideas from LLM quantization, MixQ-style mixed precision for sparse activation outliers and SmoothQuant-style per-channel smoothing, together with block-wise HiF4 packing for Wan2.2 feed-forward linear layers. Calibration on representative OpenS2V-5M batches identifies heavy-tailed activation channels; smoothing rebalances dynamic range before W4A4 rounding; and a dual-branch GEMM preserves outlier columns in higher precision while the bulk of channels use strict W4A4. On official VBench I2V metrics, our pipeline stays within 2-3.5 percent of FP16 on most quality axes and improves motion smoothness, outperforming a native HiFloat4 baseline that degrades roughly 5 percent relative to FP16 across all reported scores.
