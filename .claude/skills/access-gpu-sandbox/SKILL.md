---
name: access-gpu-sandbox
description: Access the McGill-NLP shared GPU sandbox (8x RTX A6000, 384GB VRAM) via SSH. Each skill/agent gets its own dedicated user account — NEVER use the shared `sandbox` user.
---

# GPU Sandbox (8x NVIDIA RTX A6000, 384GB VRAM)

## ⚠️ Never SSH as `sandbox`

The `sandbox` user is the Docker host's internal account. **Every agent/skill must have its own named user** provisioned via the API below. If you find yourself typing `ssh sandbox@...` — stop.

## SSH Key

This skill owns a dedicated SSH key pair stored in `.ssh/` within the skill directory:
- Private key: `${CLAUDE_SKILL_DIR}/.ssh/id_rsa`
- Public key: `${CLAUDE_SKILL_DIR}/.ssh/id_rsa.pub`

The private key is gitignored; the public key is committed.

## Current user

This skill is provisioned as user **`xlu41agent`**.

## Connecting

```bash
ssh -p 2222 xlu41agent@ec2-35-182-158-243.ca-central-1.compute.amazonaws.com \
    -i ${CLAUDE_SKILL_DIR}/.ssh/id_rsa -o StrictHostKeyChecking=no
```

To run a one-shot command:

```bash
ssh -p 2222 xlu41agent@ec2-35-182-158-243.ca-central-1.compute.amazonaws.com \
    -i ${CLAUDE_SKILL_DIR}/.ssh/id_rsa -o StrictHostKeyChecking=no "nvidia-smi"
```

## Creating a new user (API workflow)

The sandbox exposes a public key-submission API at `https://gpu-sandbox-keys-upload.mcgill-nlp.org`. Endpoints:

| Method | Path | Auth | Purpose |
|--------|------|------|---------|
| `GET`  | `/api/info` | none | Show SSH host, port, GPU config |
| `POST` | `/api/keys` | none | Submit a new user + key (usually auto-approved) |
| `GET`  | `/api/keys/<username>` | none | Check status of a request |
| `POST` | `/api/keys/<username>/approve` | admin | Approve pending request |
| `POST` | `/api/keys/<username>/revoke` | admin | Revoke access |

To create a new user, POST to `/api/keys` with:
- `name`: full name of the human owner
- `email`: contact email
- `username`: 3-32 chars, lowercase, starts with a letter, `[a-z0-9_]`
- `public_key`: an ssh-rsa / ssh-ed25519 public key

Example:

```bash
PUBKEY=$(cat ${CLAUDE_SKILL_DIR}/.ssh/id_rsa.pub)
curl -sS -X POST https://gpu-sandbox-keys-upload.mcgill-nlp.org/api/keys \
  -H "Content-Type: application/json" \
  -d "$(jq -nc --arg key "$PUBKEY" '{
    name: "Your Name",
    email: "you@example.com",
    username: "myusername",
    public_key: $key
  }')"
```

The response will indicate `"status": "approved"` and include the exact `ssh_command` to use.

If you need to regenerate the SSH key: `ssh-keygen -t rsa -b 4096 -N "" -C "gpu-sandbox-skill" -f ${CLAUDE_SKILL_DIR}/.ssh/id_rsa`, then POST it via the API above.

## Usage notes

- 8x NVIDIA RTX A6000 GPUs (48GB VRAM each, 384GB total).
- CUDA 12.5 driver. Use PyTorch compiled for CUDA 12.4 (`pip install torch==2.5.1+cu124 --index-url https://download.pytorch.org/whl/cu124`).
- Python 3.10 available. `transformers`, `torch`, and `accelerate` are pre-installed (but may be too new for the driver — reinstall `torch==2.5.1+cu124` if you hit CUDA errors).
- Persistent data should go under `/data` to survive container restarts.

## Manual (human) setup — for reference

Humans can also upload keys via the web UI at https://gpu-sandbox-keys-upload.mcgill-nlp.org (shared password: `O8zF1-BP27u7E9Ut`).
