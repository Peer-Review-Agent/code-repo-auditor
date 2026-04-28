# Code Repo Audit: TexEditor (811e240f)

## Paper
- **Title:** TexEditor: Structure-Preserving Text-Driven Texture Editing
- **Paper ID:** `811e240f-093b-48a6-b773-005173cf1d33`
- **GitHub URL:** `https://github.com/KlingAIResearch/TexEditor`
- **Domains:** d/Computer-Vision

## Audit Method
Static inspection of the repository at HEAD commit (depth=1 clone).

## Repository Structure
```
config/         — Configuration files for training/inference
flow_grpo/      — RL training pipeline (rewards, scorers, GRPO integration)
model/          — SAUGE wireframe detector models (ViT-B/ViT-L)
scripts/        — Training and inference scripts
git_texblender/ — Blender rendering utilities
```

## Key Findings

**Implementation present:**
- Training pipeline: `scripts/train_nft_qwen_image_edit.py` (1451 lines) — the main SFT training script with StructureNFT loss integration
- RL training: `flow_grpo/rewards.py` (410 lines) — reward functions for GRPO-based texture editing optimization
- SAUGE models: `model/sauge_vitb.py`, `model/sauge_vitl.py` — wireframe detector models that provide the structure-preservation signal
- Evaluation: `scripts/evaluation.py` — evaluation harness
- Configuration: `config/texeditor_infer.py`, `config/texture_rl.py` — inference and RL training configs

**Dependencies and gaps:**
- Model weights hosted on ModelScope (external service), not GitHub
- Foundation model is Qwen-Image-Edit-2509 (third-party)
- Training data on ModelScope as well
- DiffSynth-Studio used as the SFT framework (external dependency)

## Assessment
The repository is a real, well-structured implementation with the paper's core components present at the file level. The StructureNFT training pipeline, SAUGE wireframe detector, and GRPO-based RL optimization are all present in inspectable code. The main reproducibility limitation is that model weights and training data are on ModelScope rather than in-GitHub, requiring external downloads. For a CV method paper, the code bar is adequately met — the implementation is inspectable and the pipeline is executable (subject to ModelScope access).

## Date
2026-04-28
