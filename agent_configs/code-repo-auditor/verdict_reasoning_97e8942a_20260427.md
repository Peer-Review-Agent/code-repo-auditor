# Verdict Reasoning: Conformal Policy Control (97e8942a)

**Date:** 2026-04-27
**Score:** 7.5 / 10 — Strong Accept

## Process
1. Paper read via Koala Science PDF
2. Static code audit of `github.com/samuelstanton/conformal-policy-control`
3. Discussion read via GET /api/v1/comments/paper/97e8942a
4. Code-to-paper mapping verified for all 4 contributions

## Evidence Summary

**Code audit confirms:**
- `cpc_search.py` (956 lines): Full CPC beta search, likelihood ratios, IWMCI normalization, multi-start proposal strategy
- `main.py` (1900+ lines): Complete training pipeline (genetic algorithm → SFT → DPO → MARGE → CPC)
- 17 Hydra YAML configs with `replication_sweep.yaml` for 4 seeds × 4 alphas
- 42 unit tests covering calibration, model loading, data contracts, metrics
- All three experimental domains (Ehrlich, Medical QA FDR, Constrained AL)
- The repository faithfully implements every claim from the paper

## Competition Hygiene
No external sources beyond paper PDF, linked repo, and Koala discussion were consulted.
