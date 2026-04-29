# Code Artifact Audit: TurningPoint-GRPO (edba3ae8)

## Audit Method
Static inspection of cloned repository `YunzeTong/TurningPoint-GRPO` (commit `994d26a`).
File listing, import verification, and structural analysis. No code execution.

## Repository Structure
- 70+ files including:
  - Training scripts for SD3 and Flux with TP-GRPO (`scripts/my_train_*_with_op3.py`, 1654 lines each)
  - Reward scorers (PickScore, ImageReward, GenEval, UnifiedReward, aesthetic, CLIP, DeQA, OCR)
  - Diffusers pipeline patches with logprob computation
  - Dataset processing for multiple image generation benchmarks
  - Single-node and multi-node accelerate/DeepSpeed configs
  - TP-GRPO turning-point detection logic implemented in `op3` training scripts

## Concrete Findings

### 1. Zero automated tests
No unit tests, integration tests, or CI workflows exist anywhere in the repository. A system whose central claim is reward signal effectiveness has no automated correctness verification. Regression protection is absent.

### 2. Broken OCR import (reward scorer unreachable)
`flow_grpo/rewards.py:130` imports `from flow_grpo.ocr_mine import OcrScorer`. The file `flow_grpo/ocr_mine.py` does not exist in the repository. Only `flow_grpo/ocr.py` is present. The `ocr_score` function, which is registered in the `multi_score` dispatch dict at line 524, would raise `ModuleNotFoundError` at runtime.

### 3. Missing dreambooth training patches (confirmed)
`flow_grpo/diffusers_patch/train_dreambooth_lora_sd3.py` and `train_dreambooth_lora_flux.py` are imported by all four training scripts (`my_train_sd3_fast.py:27`, `my_train_sd3_fast_with_op3.py:27`, `my_train_flux_fast.py:27`, `my_train_flux_fast_with_op3.py:29`) but neither file exists in the repository. The `encode_prompt` function they provide is required for model loading — training cannot proceed from the released artifact alone.

### 4. Hardcoded internal paths (confirming prior audit)
`config/my_grpo.py` and `flow_grpo/rewards.py` contain hardcoded paths to Alibaba internal filesystems (e.g., `/mnt/workspace/tyz/A_MODELS/...`). No path-substitution manifest is provided. External researchers must reverse-engineer model paths from the README.

## Assessment
The repository is substantially more than a placeholder — the TP-GRPO turning-point detection, SDE/ODE reward computation, and multi-reward dispatch are all implemented. However, three concrete breakages (zero tests, broken OCR import, missing dreambooth patches) plus hardcoded internal paths mean the released artifact cannot reproduce the paper's training pipeline without reconstructing missing files. The method implementation is inspectable but not runnable.
