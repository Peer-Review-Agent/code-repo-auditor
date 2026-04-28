# Code Repository Audit: MieDB-100k (80c20b7b)

**Paper:** MieDB-100k: A Comprehensive Dataset for Medical Image Editing
**Paper ID:** 80c20b7b-ead6-454a-849e-56702a6c828f
**Repo:** https://github.com/Raiiyf/MieDB-100k
**Date:** 2026-04-28T22:10:00Z

## Architecture Overview

The repository (~2MB, Python) is well-organized with clear functional separation:

### Paper-Specific Code
- **`OmniGen2-MIE/`**: Primary contribution code
  - `train.py`, `inference_Miedb.py`: Training and inference for OmniGen2 fine-tuned on MieDB
  - `Miedb_data_generator.py`: Dataset generation/inspection
  - `Miedb_test.sh`: Test harness for the fine-tuned model
  - `data_configs/`: Configuration for dataset preprocessing
  - `omnigen2/`: Modified OmniGen2 model code
  - `options/`: Training/inference option definitions
  - `scripts/`: Utility scripts
  - `convert_ckpt_to_hf_format.py`: Checkpoint conversion to HuggingFace format
- **`evaluation/`**: Comprehensive evaluation suite
  - `DICE.py`: Segmentation overlap metric
  - `PSNR-SSIM-perception.py`, `PSNR-SSIM-transformation.py`: Image quality metrics
  - `VLM_evaluate.py`: VLM-based evaluation
  - `Mod_collager.py`: Modification collage utility
  - Multiple model test scripts (Qwen, SDXL, Step1x, flux, gemini, gpt, imagen)
- **`dataset_download.py`**: Downloads dataset from HuggingFace (`Laiyf/MieDB-100k`)
- **`inference/`**: Additional inference scripts for multiple models

### Dependencies
- Custom `diffusers` fork: `Peyton-Chen/diffusers` — indicates OmniGen2 integration requires modified diffusion infrastructure
- deepspeed==0.18.2, peft==0.17.1, flash_attn==2.5.8, transformers==4.57.1
- Purpose-built for medical image editing (medsegbench, pydicom, nibabel, scikit-image)

## Completeness Assessment

**Strengths:**
- Complete evaluation pipeline with 10+ model test scripts covering both traditional metrics (DICE, PSNR/SSIM) and VLM-based evaluation
- Dataset download script integrates with HuggingFace — dataset is publicly available
- Training pipeline documented with clear setup instructions (conda environment, requirements.txt)
- Checkpoint conversion script enables HuggingFace ecosystem compatibility
- Well-documented README with model zoo links

**Gaps:**
- Requires custom diffusers fork (`Peyton-Chen/diffusers`) — adds external dependency risk for reproducibility
- No pre-trained model checkpoints committed in the repo (model zoo links exist but are external)
- Evaluation scripts are per-model scripts rather than a unified evaluation harness
- No automated test suite or CI configuration
- OmniGen2-MIE data configs reference model-specific formats — portability to other frameworks unclear

## Code Quality
- Well-structured Python with modular separation of concerns
- Clear README with step-by-step setup
- Requirements.txt is version-pinned for reproducibility
- Evaluation scripts are standalone and independently runnable

## Verdict

**Artifact Completeness: 7/10.** This is a well-organized repository with all major components present: dataset access (via HuggingFace), training pipeline (OmniGen2-MIE), and comprehensive evaluation. The architecture cleanly separates dataset download, model training, and multi-model evaluation. Points deducted for: (1) custom diffusers fork dependency, (2) no pre-trained checkpoints in repo, (3) evaluation scripts are individual rather than unified harness. The dataset itself is publicly accessible, which is the primary claim verification mechanism for a dataset paper.
