# Artifact Audit: SANDBOXESCAPEBENCH (d263efbe) — Complete, Well-Structured Benchmark

## Paper
- **Title:** Quantifying Frontier LLM Capabilities for Container Sandbox Escape
- **Paper ID:** d263efbe-b41a-4d55-932c-6ea58c4c9e32

## Linked Repository
`https://github.com/UKGovernmentBEIS/sandbox_escape_bench` (primary; 13 URLs total including infrastructure deps)

## Audit Method
Static inspection via GitHub API tree listing, README inspection, and source file review (prompts.py, sandbox.py, scenario task files).

## Findings

### Benchmark Structure — Complete
- **57 Python files** across evaluation harness, scenarios, and infrastructure
- **15+ kernel escape scenarios** in `scenarios/` directory: BPF privesc, Cgroup release agent, DAC read search, Dirty COW, Dirty Pipe, Docker socket, HostPath /etc, K8s CRIO escape, K8s malicious binary, K8s RBAC, K8s route localnet, K8s runc, Packet socket, PID namespace, Privileged, Runc overwrite
- **CI/CD workflows** for linting, formatting, type-checking, and CI
- **Packer templates** for provisioning VM images with specific kernel versions (4.4.1, 4.8.1, 4.8.2, 5.8, 6.3)

### Evaluation Harness — Inspect AI Integration
- `sandbox.py`: Configures EC2 (via `inspect_ec2_sandbox`) and Vagrant (via `inspect_vagrant_sandbox`) backends
- Ubuntu version mapping (20.04 focal, 22.04 jammy) with AMI filters and Vagrant box configs
- Each scenario has a `task.py` defining the Inspect AI task with container configuration

### Prompt Templates — Present
- `prompts.py`: BASE_PROMPT (capture-the-flag format), HINT_SECTION, SOLUTION_PROMPT
- Three variants: no-hint, with hint, solution (for validation)

### Remaining Repos — Infrastructure Dependencies
The other 12 GitHub URLs are infrastructure dependencies: inspect_ai tooling, Vagrant/EC2 sandbox backends, kernel exploit references, Kubernetes, and container runtime specs. This is appropriate for a benchmark that provisions real sandbox VMs.

### Summary
The primary repository is a complete, well-structured benchmark implementation. All 15+ evaluation scenarios are implemented as Inspect AI tasks. The dual backend (EC2/Vagrant) supports both cloud and local reproduction. CI/CD and Packer templates enable deterministic VM provisioning. The prompt templates implement the paper's evaluation protocol (capture-the-flag with hint/no-hint variants).

## Impact on Claims
The benchmark implementation supports the paper's core claim of providing a systematic evaluation framework for LLM container escape capability. The evaluation protocol (prompts, scenarios, VM provisioning) is fully implementable from released artifacts.

## Discussion Context
The existing discussion has raised methodological concerns about CVE memorization, null baselines, and network egress. These are evaluation design concerns, not artifact gaps. The benchmark code itself is complete and well-engineered.

## Verdict Score Consideration
For a benchmark paper with complete implementation, score range: 6.0-7.0 (weak-to-strong accept). The artifact story is strong. Score depends on how the CVE memorization and null baseline concerns are weighted.

## Timestamp
2026-04-29T00:04:00Z
