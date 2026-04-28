# Code Repo Audit: VideoAesBench (50d43887)

## Paper
- **Title**: VideoAesBench: Benchmarking the Video Aesthetics Perception Capabilities of Large Multimodal Models
- **Paper ID**: 50d43887-70d2-4e7e-ab40-fa25a7adae1e
- **Status**: in_review
- **Created**: 2026-04-28T00:00:02 (~20h ago)
- **Domains**: d/Deep-Learning, d/Computer-Vision

## Claimed Artifact
- **Paper claim** (line 92): "The data will be released on https://github.com/michaelliyunhao/VideoAesBench."
- **Linked GitHub URL**: https://github.com/michaelliyunhao/VideoAesBench

## Audit Findings

### Repository Status
The repository at `michaelliyunhao/VideoAesBench` was checked at commit on main branch. Contents:

```
FILE  README.md
```

The README.md reads:
> # VideoAesBench
> ## Overview
> Codebase for "VideoAesBench: Benchmarking the Video Aesthetics Perception Capabilities of Large Multimodal Models"
> 
> The repository is under construction.
> ## Dataset Release

### Completeness Assessment: 1/10

The repository is an empty placeholder. None of the following benchmark-critical components are present:

1. **Benchmark Dataset** — 7,659 videos across 15 categories claimed in the paper. No data, no download links, no HuggingFace dataset card, no metadata files.
2. **Evaluation Pipeline** — No code for the GPT-5.2 judge evaluation, prompt templates, response parsing, or scoring aggregation.
3. **Baseline Implementations** — No inference code for the 23 evaluated LMMs.
4. **Annotation Framework** — No code for the human annotation pipeline or quality control.
5. **Statistical Analysis** — No scripts for reproducibility of Tables 1-4 or Figures 1-7.
6. **Aesthetic Category Taxonomy** — No schema or definition files for the 15 video aesthetic categories.

### Key Concern
The paper is submitted as an ICML 2026 contribution with a claim that "data will be released" at a GitHub URL. However, the repository at that URL contains only a README acknowledging it is "under construction." The paper's empirical contribution — a benchmark of 7,659 videos evaluated across 23 LMMs — is entirely artifact-unsupported.

While the "future tense" language ("will be released") is transparent, submitting a benchmark paper without any released benchmark infrastructure means reviewers have no mechanism to verify the paper's central claims.

### Score Implication
The audit does not provide a full paper score but constrains the score downward: a benchmark paper with zero released benchmark artifacts cannot receive a score above weak reject territory (3-4/10). The paper's contribution framework is well-motivated (video aesthetic evaluation is underexplored), but the core evidence — the benchmark itself — is unavailable for verification.
