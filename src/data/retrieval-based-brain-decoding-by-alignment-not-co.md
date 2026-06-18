---
pubDatetime: 2026-06-17T13:52:38.000Z
title: "Retrieval-Based Brain Decoding by Alignment, not Complexity"
link: "https://arxiv.org/abs/2606.19081v1"
koreanSummary: "복잡성이 아닌 정렬을 통한 검색 기반 뇌 디코딩"
---

A prominent theory in cognitive science suggests that concepts in the brain are organized as high-dimensional vectors, with semantic meaning captured by directions and relative angles in this space. Brain decoding is the effort of reconstructing or retrieving stimuli (or their representations) from neural activity and involves finding a function that approximates how the brain represents concepts. This motivates the investigation of contrastive objectives as biologically plausible candidates to reverse the brain loss function. In this work, we study how functional MRI (fMRI) activity can generally be mapped with the embedding spaces of foundation models in vision, language, and audio. Although neural computations are highly non-linear at the microscale, fMRI measurements average signals across space and time, further smoothed by noise, effectively linearizing the observable representation. Consistent with these views, our experiments across multiple datasets demonstrate that linear contrastive decoders consistently outperform ridge regression and standard non-linear alternatives, and that these results generalize across images, text, and sound. These findings indicate that decoding gains arise more from the choice of training objective than from architectural complexity, pointing to contrastive-linear models as a principled strategy for brain decoding.
