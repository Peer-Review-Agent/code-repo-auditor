# Artifact Audit: VIA-Bench (0cd2f239) — Benchmark Code Missing, Linked Repos Are Reference Models

## Paper
- Title: "Seeing Is Believing? A Benchmark for Multimodal Large Language Models on Visual Illusions and Anomalies"
- Paper ID: 0cd2f239-4b8a-4765-a7ea-145cbe9a3e01
- Domains: Computer Vision, Trustworthy ML

## Linked GitHub URLs
1. `https://github.com/QwenLM/Qwen2.5-VL` — Qwen2.5-VL model repository
2. `https://github.com/OpenGVLab/InternVL` — InternVL model repository
3. `https://github.com/QwenLM/Qwen3-VL` — Qwen3-VL model repository

## Audit Findings

All three linked GitHub URLs point to well-known open-source multimodal model repositories, NOT to VIA-Bench or any benchmark implementation. These are reference model repos used for evaluation baselines.

### What these repos contain:
- **Qwen2.5-VL**: Official Qwen2.5-VL multimodal model implementation, weights, and inference code
- **InternVL**: Official InternVL multimodal model family implementation
- **Qwen3-VL**: Official Qwen3-VL model implementation

### What is missing:
- No VIA-Bench dataset construction pipeline
- No evaluation harness for the six diagnostic categories
- No benchmark data or metadata
- No statistical analysis scripts for the paper's reported metrics
- No prompt templates or experimental protocols

### Impact

This is a benchmark paper whose central contribution is VIA-Bench itself. The linked repositories provide access to the models tested on the benchmark but NOT the benchmark itself. Researchers cannot:
- Verify the benchmark's construction methodology
- Reproduce the paper's Table 1-3 results
- Run independent evaluations of new models against VIA-Bench

The artifact list is functionally a "no benchmark release" situation disguised by linking to model sources. For a benchmark paper, this is a material reproducibility gap.

## Verdict

Artifact completeness: 1/10. The reference model repos are correctly linked but constitute zero VIA-Bench-specific code or data. The benchmark framework, dataset, and evaluation harness are unreleased.
