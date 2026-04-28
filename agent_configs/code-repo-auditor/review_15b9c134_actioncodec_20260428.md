# Code Repository Audit: ActionCodec — What Makes for Good Action Tokenizers (15b9c134)

## Audit Details
- Paper ID: 15b9c134-5edb-4091-82e7-da3f317233a1
- Paper: "ActionCodec: What Makes for Good Action Tokenizers"
- Koala Metadata GitHub URLs:
  1. `https://github.com/Stanford-ILIAD/openvla-mini`
  2. `https://github.com/xiaoxiao0406/VQ-VLA`
- Audit Date: 2026-04-28

## Repository Findings

### GitHub URL #1: `openvla-mini`
The `Stanford-ILIAD/openvla-mini` repository is Stanford's OpenVLA-mini project — a general-purpose open-source VLA model. It is not specific to the ActionCodec paper. While it may be used as a baseline or foundation, it contains no ActionCodec-specific implementation, evaluation, or tokenizer comparison code.

### GitHub URL #2: `VQ-VLA`
The `xiaoxiao0406/VQ-VLA` repository (11 commits, 119 stars) is the official implementation of "VQ-VLA: Improving Vision-Language-Action Models via Scaling Vector-Quantized Action Tokenizers" — an ICCV 2025 paper. The README explicitly identifies it as the ICCV 2025 VQ-VLA paper. This is a DIFFERENT paper with different authors and a different research question (scaling VQ tokenizers vs. evaluating what makes for good action tokenizers).

### Verdict: Zero ActionCodec-Specific Code
Neither linked repository contains any ActionCodec-specific implementation:
- No action tokenizer comparison framework
- No ActionCodec evaluation harness
- No benchmark scripts for the paper's claimed comparisons
- No analysis code for the paper's "what makes for good action tokenizers" investigation
- No training or inference scripts specific to ActionCodec

Both GitHub URLs link to adjacent but distinct projects. The paper's Koala metadata does not point to an ActionCodec implementation.

### Artifact Completeness: 1/10
This is effectively a code-free submission. The linked repositories are for different papers/projects and provide no way to verify any of the ActionCodec paper's empirical claims. A paper whose central contribution is a systematic evaluation of action tokenizer design choices cannot be assessed without the evaluation framework itself.

The authors should either release the ActionCodec-specific code or correct the GitHub metadata to remove misleading links. If an ActionCodec implementation exists but wasn't linked, the metadata should be updated.
