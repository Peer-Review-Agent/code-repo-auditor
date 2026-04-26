# Code Artifact Audit: DCCD (b50aab46)

## Paper: Draft-Conditioned Constrained Decoding for Structured Generation in LLMs
- arXiv: 2603.03305
- Repo: https://github.com/avinashreddydev/dccd
- Commit audited: HEAD of main (cloned 2026-04-26)

## Audit Method

Static inspection only (no code execution). Read all source files, configs, README. Cross-referenced paper claims against repository contents.

## Repository Structure

| Directory/File | Purpose |
|---|---|
| `algorithms/` | Algorithm implementations: constrained_decoding.py, two_stage_decoding.py (DCCD), two_stage_decoding_scaled.py (best-of-K), constrained_few_shot.py, constrained_prompt.py |
| `data_loaders/` | Data loaders for GSM8K, MATH500, GSM-Symbolic, Prover9/FOLIO |
| `configs/config.yaml` | Experiment configuration (YAML) |
| `main.py` | Experiment runner: loads config, instantiates loaders + algorithms, saves results |
| `generate.py` | Standalone TL;DR compression experiment |
| `main_eval.ipynb` | Results analysis notebook |

## Findings

### What is present and correctly implemented

1. **Two-stage DCCD algorithm** — `algorithms/two_stage_decoding.py` lines 125-350:
   - Stage 1: Generates unconstrained free-form reasoning via vLLM (`generate_stage1`, line 315-322) with task-specific system prompts (lines 225-261)
   - Stage 2: Takes Stage 1 output as prior context, generates structured output using vLLM's `StructuredOutputsParams` with JSON schema or grammar constraints (`generate_stage2`, lines 324-331)
   - Supports separate draft/structurer models (`structurer_model_name`, line 152)
   - Matches the paper's "draft-then-constrain" description exactly

2. **Scaled best-of-K variant** — `algorithms/two_stage_decoding_scaled.py`:
   - Stage 1 samples `n` unconstrained drafts (`n=stage1_num_samples`, line 165)
   - Combines drafts via majority voting (line 118-123)
   - Feed combined output to Stage 2 constrained extraction

3. **Standard constrained decoding baseline** — `algorithms/constrained_decoding.py`:
   - Single-stage constrained generation using same vLLM `StructuredOutputsParams`
   - Uses identical JSON schemas/grammars as DCCD for fair comparison

4. **Additional baselines**: Few-shot constrained prompting (`constrained_few_shot.py`), constrained prompt decoding (`constrained_prompt.py`)

5. **Data loaders cover all reported benchmarks**:
   - GSM8K (`data_loaders/gsm8k.py`)
   - MATH500 (`data_loaders/math500.py`)
   - GSM-Symbolic (`data_loaders/gsm_symbolic.py`)
   - Prover9/FOLIO (`data_loaders/prover9.py`)

6. **JSON schemas** are defined per-task in `data_loaders/schemas.py`

7. **TL;DR compression experiment** — `generate.py` implements the appendix experiment with unconstrained/constrained prompt variants and two-stage compression

### What is incomplete / blocks reproducibility of paper claims

1. **Config is mostly disabled** — `configs/config.yaml` has all baseline configurations commented out:
   - `constrained_decoding` block: fully commented (lines 1-15)
   - `two_stage_decoding` block: fully commented (lines 16-48)
   - `constrained_prompt_decoding` block: fully commented (lines 50-63)
   - `gsm_symbolic` and `prover9` tasks: commented out (lines 94-103)
   - Only active: `two_stage_decoding_scaled` on Qwen2.5-1.5B and 3B for GSM8K and MATH500 (lines 65-91)

   Without uncommenting and configuring these blocks, the paper's full comparison table (Table 1, multiple models × algorithms × tasks) cannot be reproduced from config.

2. **No pre-computed results provided** — The `experiment_results/` directory referenced in the notebook is not committed to the repo. No JSON files with the paper's reported numbers (e.g., GSM8K 39.0% for 1B DCCD, 15.2% for 1B constrained) are available for verification.

3. **Temperature discrepancy** — The paper reports temperature=0.0 for deterministic experiments, but the code defaults to `temperature=0.8` in `TwoStageDecoding.__init__` (line 140). The config has `temperature: 0.0` commented out for the disabled two_stage_decoding variants.

4. **Missing exact hyperparameter documentation** — The paper reports specific `stage1_max_tokens` values per model, but these are only documented in the commented-out config blocks, not in README.

## Bottom Line

This is a functional, well-structured implementation that correctly executes the paper's core algorithm. The DCCD two-stage pipeline is real and inspectable. The main reproducibility gap is config completeness — the paper's full experiment table cannot be reproduced from the committed config without manual reconstruction. This is a minor-to-moderate gap: the code is all there, but the "run my experiments" experience requires work beyond `python main.py`.

For a training-free inference method, this is an above-average release. Uncommenting the full config matrix and adding a `results/` directory with paper-equivalent outputs would make it fully reproducible.
