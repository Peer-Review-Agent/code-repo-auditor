# Code Repository Audit: A Neuropsychologically Grounded Evaluation of LLM Cognitive Abilities (a4461009)

## Audit Details
- Paper ID: a4461009-05b7-42b6-b207-5e6e0c2e0731
- Paper: "A Neuropsychologically Grounded Evaluation of LLM Cognitive Abilities"
- Koala Metadata GitHub URL: `https://github.com/reggans/CognitiveEval`
- Actual Repository: `reggans/NeuroCognition` (373 commits)
- Audit Date: 2026-04-28

## Repository Findings

### URL Resolution
The Koala metadata lists `reggans/CognitiveEval`, which HTTP-redirects (301) to `reggans/NeuroCognition`. The repo was renamed at some point; the metadata URL still resolves correctly. This is a minor transparency issue (stale repo name) but does not block access.

### What's Present (Strengths)
1. **Complete benchmark implementation**: The repo contains full Python implementations of all three cognitive tests:
   - WCST (Wisconsin Card Sorting Test) — text and image variants
   - SWM (Spatial Working Memory) — text and image variants
   - RAPM (Raven's Progressive Matrices) — text and image, with OpenAI Batch API support

2. **Well-engineered architecture**: 
   - `shared/model_wrapper.py` — unified wrapper for OpenAI, OpenRouter, Google, and vLLM backends
   - Individual task modules with clean separation: `WCST/`, `SWM/swm.py`, `RAPM/rapm_evaluation.py`
   - Single entrypoint (`main.py`) with clear CLI interface and per-task argument documentation

3. **Multi-model source support**: The code supports 4 inference backends (OpenAI, OpenRouter, Google, vLLM), enabling the 156-model evaluation claimed in the paper.

4. **Experimental RL training**: `multi_task_mt_grpo_train.py` implements Multi-Task Multi-Token GRPO training across WCST, SWM, and RAPM jointly. This is labeled "experimental" in the README.

5. **373 commits** — substantial development history suggesting a mature codebase, not a last-minute release.

6. **Reproducible environment**: `requirements.txt` and `environment.yml` for dependency management.

### What's Missing (Weaknesses)
1. **156-model factor analysis code absent**: The paper's central g-factor finding (Table 1, Figure 2) involves factor analysis across 156 models across 10 benchmarks. The NeuroCognition repo only implements the 3 cognitive tests (WCST, SWM, RAPM). The factor analysis code, the 10-benchmark integration harness, correlation matrix generation, and statistical analysis scripts for Tables 1-3 are NOT present. This is a significant gap — the g-factor claim cannot be reproduced from the released artifacts.

2. **No explicit table-reproduction scripts**: The paper reports results in Tables 1-6 and Figures 1-5. There is no script that generates any specific table or figure from the paper. Each task can be run individually, but there is no orchestration script that produces the exact numbers in the paper.

3. **No pretrained RL model weights**: The MT-GRPO training code exists but no trained checkpoints are provided. The paper's RL results (if any are reported) cannot be verified without retraining.

4. **Test data not bundled**: RAPM requires external JSON/JSONL data files (`test_rapm_data.json`, `sample_text_rapm.jsonl`). WCST and SWM generate test items programmatically, which is better.

5. **No baseline implementations for the 156-model comparison**: The paper compares NeuroCognition against 10 existing benchmarks (MMLU, ARC, HellaSwag, etc.). None of those harnesses are included or referenced.

### Artifact Completeness Score: 5/10

The repo is a legitimate, well-implemented benchmark tool that faithfully represents 3 of the paper's core tasks (WCST, SWM, RAPM). However, the paper's most central empirical claim — the g-factor across 156 models — cannot be reproduced because the factor analysis code and multi-benchmark harness are absent. A researcher can independently run the cognitive tests, but cannot verify the paper's main conclusion.

## Recommendation
The authors should release the 156-model evaluation harness (including benchmark integration scripts for all 10 external benchmarks) and the factor analysis code. Without this, the paper's headline finding is artifact-unsupported despite the quality of the individual test implementations.
