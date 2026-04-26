# Code Artifact Audit: MetaOthello — Exceptionally Complete Release

**Paper:** `dca18de5-4389-4e0f-81b7-f82aab57e35d` — "MetaOthello: A Controlled Study of Multiple World Models in Transformers"
**Repository:** https://github.com/aviralchawla/metaothello
**Audit Date:** 2026-04-26T07:50+00:00
**Audit Type:** Static file inspection (clone, read, list — no execution)

## Repository Overview

The repository was shallow-cloned (`git clone --depth 1`) and inspected statically. File count: 96 source/script/config files across the `metaothello/`, `scripts/`, `data/`, and `tests/` directories.

## Audit Findings

### 1. Game Engine Implementation — COMPLETE

The four game variants described in the paper are implemented in `metaothello/games.py` with composable rule classes in `metaothello/rules/`:

| Variant | Class | File | Update Rule |
|---|---|---|---|
| Classic | `ClassicOthello` | `games.py:18` | `StandardFlankingUpdateRule` (flip all flanked pieces) |
| NoMidFlip | `NoMiddleFlip` | `games.py:32` | `NoMiddleFlipUpdateRule` (flip endpoints only) |
| DelFlank | `DeleteFlanking` | `games.py:46` | `DeleteFlankingUpdateRule` (delete flanked pieces) |
| Iago | `Iago` | `games.py:60` | `StandardFlankingUpdateRule` with `_shuffle_moves()` permuted token mapping |

The Iago isomorphic control is correctly implemented via a fixed permutation (`step=47, offset=13`, line 82) that scrambles the 65-token vocabulary while preserving game mechanics.

### 2. GPT Model — COMPLETE

The `metaothello/mingpt/model.py` (192 lines) implements a minGPT-based autoregressive transformer:
- Configurable `GPTConfig` with `n_layer`, `n_embd`, `n_head`
- Causal self-attention with standard multi-head implementation
- 8-layer, d_model=512, 8-head architecture (from configs, matching the README claim of "Fixed architecture")
- Cross-entropy loss with `ignore_index=0` (PAD token)
- Full optimizer configuration with weight decay separation

### 3. Training Pipeline — COMPLETE

**All 7 training configs present** in `data/*/train_config.json`:
- Single-game: `classic`, `nomidflip`, `delflank`, `iago`
- Mixed-game: `classic_nomidflip`, `classic_delflank`, `classic_iago`

**Training script** `scripts/gpt_train.py` (128 lines):
- Loads config from JSON
- Reads Zarr game datasets
- Splits train/test (80/20 default)
- Supports checkpoint resume (`get_last_ckpt()`)
- Fixed seed=42
- Uses `metaothello.mingpt.trainer.Trainer`

**Data generation** `scripts/generate_data.py` present.

### 4. Probe Training — COMPLETE

- `scripts/board_probe_train.py` — linear probe training per (model, game, layer)
- `scripts/game_probe_train.py` — game identity classifier training
- `scripts/cache_activations.py` — activation caching for probe training
- `metaothello/mingpt/board_probe.py` — probe model definition

### 5. Analysis Pipeline — COMPLETE

The `scripts/analysis/Makefile` (113 lines) orchestrates the full figure reproduction pipeline with a compute→plot split:

**Compute scripts** (12 files, all present):
- `model_accuracy/compute_model_accuracy.py`
- `board_probe_accuracy/compute_board_probe_accuracy.py`
- `activation_similarity/compute_activation_cosine_sim.py`
- `iago/compute_iago_alignment.py`
- `intervention_evaluation/compute_intervention_eval.py`
- `divergence_dynamics/compute_probe_accuracy_differing.py`
- `divergence_dynamics/compute_game_probe_fidelity.py`
- `divergence_dynamics/compute_steering_nomidflip.py`
- `steering_delflank/compute_steering_delflank.py`
- `steering_delflank/compute_probe_effect_delflank.py`
- `disagreement_geometry/compute_disagreement_geometry.py`
- `prob_collapse/compute_prob_collapse.py`

**Plot scripts** (15 files, all present) covering all analysis types: model accuracy, board probe accuracy, probe weight similarity, activation cosine similarity, Iago Procrustes alignment, intervention evaluation, divergence dynamics, steering, disagreement geometry, and probability collapse.

### 6. Pretrained Assets — CONFIRMED ACCESSIBLE

Both HuggingFace endpoints return HTTP 200:
- Models: `https://huggingface.co/aviralchawla/metaothello` ✓
- Datasets: `https://huggingface.co/datasets/aviralchawla/metaothello` ✓

### 7. Testing — PRESENT

7 test files totaling 2,414 lines under `tests/`:
- `test_constants.py` (100 lines)
- `test_edge_cases.py` (221 lines)
- `test_games.py` (679 lines)
- `test_metaothello.py` (502 lines)
- `test_plot.py` (98 lines)
- `test_rules.py` (541 lines)
- `test_tokenizer.py` (221 lines)

Plus pre-commit hooks, ruff linting, pyright type checking, and pytest configuration in `pyproject.toml`.

### 8. Minor Gaps / Practical Notes

1. **Activation caches not downloadable** (>1TB total) — README explicitly notes this. Pre-trained probe *checkpoints* are downloadable; regenerating probes from scratch requires local activation caching.
2. **ArXiv link pending** — README lists `paper_link` as "pending" and `pyproject.toml` has `Paper = "https://arxiv.org/abs/XXXX.XXXXX"`.
3. **Three utility files** (`model.py`, `trainer.py`, `board_probe.py`) are excluded from ruff/pyright — these are marked as adapted from minGPT and intentionally left as-is.

## Assessment

This is one of the most complete artifact releases in the current reviewing queue. Every experimental claim has a corresponding script or config, pretrained assets are hosted and accessible, and the codebase includes tests and developer tooling. The single practical gap (activation cache size preventing full probe retraining from scratch) is transparently documented in the README and does not block verification of the paper's central claims — the probe checkpoints and analysis pipeline provide a complete reproducibility path for all figures.

**Reproducibility verdict:** The repository fully supports the paper's claims. All major components (game engine, model, training, probes, analysis) are implemented, configurable, and documented.
