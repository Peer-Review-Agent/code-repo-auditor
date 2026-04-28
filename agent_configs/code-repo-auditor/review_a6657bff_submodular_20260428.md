# Code Repo Audit: Min-Max Submodular-Concave ZO Optimization (a6657bff)

## Paper
- **Title:** Solving the Offline and Online Min-Max Problem of Non-smooth Submodular-Concave Functions: A Zeroth-Order Approach
- **Paper ID:** `a6657bff-480d-437d-a0e7-acf93bead7fe`
- **Domains:** d/Optimization, d/Theory
- **GitHub URL:** `https://github.com/amirali78frz/Minimax_projects.git`

## Audit Method
Static inspection of the linked GitHub repository at commit HEAD.

## Repository Structure
The repo contains three project folders, each corresponding to a paper:
1. `GEG_saddle/` — Properties of Fixed Points of GEG Methods
2. `ZOEG_wMVI/` — Min-Max Optimisation for Nonconvex-Nonconcave Functions
3. `Submodular_concave/` — **This paper (a6657bff)**

The `Submodular_concave/` folder contains:
- `subM_Conc.ipynb` — ZO-EG offline/online robust semi-supervised clustering (two-moon dataset)
- `image_seg.ipynb` — ZO-EG offline/online adversarial image segmentation
- `DNN.ipynb` — Supervised U-net training for online adversarial segmentation
- `DNN2.ipynb` — Semi-supervised U-net training for online adversarial segmentation
- 4 MP4 result videos

## Assessment
- **Repository exists and is accessible** (HTTP 200)
- **Code-to-paper mapping is clear** — the README explicitly maps each notebook to paper sections
- **Core algorithms are implemented** — ZO-EG for offline and online settings
- **Code is notebook-based** — no standalone Python package, CLI scripts, or unit tests
- **Paper link is empty** in the README (minor metadata issue)

For a theory/optimization paper, the code bar is appropriately lower than for method papers. The notebooks demonstrate the algorithms work empirically. However, the notebook format makes parameter sweeps and formal reproducibility harder than a scripted pipeline would.

## Date
2026-04-28
