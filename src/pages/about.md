---
layout: ../layouts/AboutLayout.astro
title: "About CogniGraph"
---

**CogniGraph** is an automated research dashboard that curates the latest academic papers in cognitive science, computational neuroscience, and related fields.

## How it works

Every day, a GitHub Actions pipeline fetches new preprints from [arXiv](https://arxiv.org), scores them for semantic relevance against a target concept using a sentence-transformer model (`all-MiniLM-L6-v2`), and publishes the top-scoring papers as posts on this site.

Papers are scored against this anchor concept:

> *Cognitive science research involving neural representations, computational modeling, active inference, and brain functions.*

Only papers that clear the relevance threshold are published — so everything here is directly on-topic.

## Topics covered

- Computational cognitive science
- Neural manifolds and representational geometry
- Active inference and predictive coding
- Brain-computer interfaces
- Artificial intelligence & human cognition
- Memory, attention, and decision-making

## Features

- **Daily updates** — fresh papers every morning via a scheduled GitHub Action
- **Semantic filtering** — only relevant papers make the cut
- **Full-text search** — powered by [PageFind](https://pagefind.app/)
- **Tag browsing** — explore by topic
- **RSS feed** — subscribe at [/rss.xml](/rss.xml)
- **Dark mode** — toggle in the header

## Source

The full source code is on [GitHub](https://github.com/ymnhn/cognigraph). Pull requests and issues are welcome.
