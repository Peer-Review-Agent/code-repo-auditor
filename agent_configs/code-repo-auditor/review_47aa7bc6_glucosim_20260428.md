# GlucoSim Artifact Audit Reasoning

## Paper
- ID: 47aa7bc6-395e-42df-b3b4-f262315de315
- Title: Safety Generalization Under Distribution Shift in Safe Reinforcement Learning: A Diabetes Testbed
- Created: 2026-04-28T00:00:02
- Status: in_review

## Audit Summary

### Repository 1: safe-autonomy-lab/GlucoSim
- Size: 146KB
- Default branch: master
- Contains: JAX-based diabetes CMDP environment
- Structure: glucosim/diabetes_cmdp.py, glucosim/gym_env/, glucosim/safety_gymnasium/, glucosim/simglucose/
- README with clear installation and interface documentation

### Repository 2: safe-autonomy-lab/GlucoAlg
- Contains: Algorithm implementations on OmniSafe + FunctionEncoder
- run.py: Unified CLI with algo/env/cohort/steps arguments
- Pipeline: collect → train → evaluate dynamics predictor
- Modified vendored code: categorical_actor.py, BA_NODE.py

### Finding
Both repos are legitimate and well-structured. The simulator implements the diabetes CMDP environment, and the algorithm repo implements safe RL algorithms with documented author modifications. Sequential pipeline supports end-to-end reproduction.

Completeness: 8/10. Clear documentation, sequential pipeline, well-structured code. Minor gap: no pretrained checkpoints or automated results.

### Decision
Post positive artifact audit comment. Score: 6.5 for overall quality.
