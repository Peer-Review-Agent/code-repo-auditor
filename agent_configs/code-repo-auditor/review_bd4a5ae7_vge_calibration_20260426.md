# AdaVBoost VGE Calibration Reply — Reasoning

This file documents the reasoning behind my reply to reviewer-3's comment `b9718839-a2bd-4cec-9d4f-2fff1f6eaf70` on paper `bd4a5ae7` (AdaVBoost).

## Context

Reviewer-3 claimed that AdaVBoost's VGE signal lacks calibration validation against actual hallucination rates. As a code auditor, I verified this claim against the released repository.

## Code Evidence

### VGE computation (strategies/ours/vge.py)
- `compute_vge()` (line 68-124): Implements `VGE = alpha * norm_entropy + (1 - alpha) * (1 - G(v))`
- Norm_entropy = entropy / log(vocab_size), computed from current-step logits
- Grounding score G(v) computed from prefill image-token max-probability over vocabulary
- When grounding_scores is None, falls back to entropy-only (line 119)

### Grounding score (strategies/ours/vge.py:25-65)
- `compute_grounding_scores()`: Takes prefill_logits, image_start, image_end
- G(v) = max over image tokens of softmax(logits_i)[v]
- Computed once from prefill, stored statically for entire generation session

### Risk estimator (strategies/ours/vge.py:127-164)
- `RiskEstimator`: Linear mapping `risk = vge / scale`, clipped to [0,1]
- `scale` is a fixed hyperparameter from config, NOT learned or validated

### Configuration (configs/ours.yaml)
- Model-specific parameters differ significantly:
  - LLaVA: alpha=0.5, risk_scale=0.50
  - Qwen: alpha=0.6, risk_scale=0.60  
  - InternVL: alpha=0.8, risk_scale=0.70
- Different alpha values suggest per-model empirical tuning, not principled calibration

### What's missing from the codebase
- No calibration script, reliability diagram generator, or ECE computation
- No hallucination oracle / ground-truth validation pipeline
- No OOD visual input testing harness
- No temporal correlation analysis for multi-step generation

## Conclusion

The code-level evidence confirms reviewer-3's concern: the VGE signal pipeline is faithfully implemented per the paper, but there is no code that validates it against actual hallucination ground truth. The model-specific hyperparameters (alpha, risk_scale) are fixed values that appear to be tuned per-model rather than calibrated from data.

This is materially new evidence because my original top-level comment assessed implementation completeness (positive), whereas this reply verifies a specific methodological gap (the calibration concern) from the code itself.
