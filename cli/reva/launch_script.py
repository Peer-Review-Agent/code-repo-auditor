"""Shared helper that writes an agent's .reva_launch.sh and .reva_env.sh.

Both the tmux path (`reva.tmux.create_session`) and the cluster path
(`reva.cluster.submit_agent`) call this so they produce a byte-identical
.reva_launch.sh for the same agent + options.
"""

import os
from pathlib import Path

LAUNCH_FILENAME = ".reva_launch.sh"
ENV_FILENAME = ".reva_env.sh"
BIN_DIRNAME = ".reva_bin"

_ENV_PREFIXES = (
    "GEMINI_",
    "CLAUDE_",
    "ANTHROPIC_",
    "OPENAI_",
    "CODEX_",
    "OPENCODE_",
    "GOOGLE_",
    "COALESCENCE_",
)


def write_launch_files(agent_dir: str, launch_script: str) -> Path:
    """Write .reva_env.sh and .reva_launch.sh into *agent_dir*.

    The env file holds backend API keys forwarded from the current process's
    environment so the agent inherits them without the caller having to leak
    them on a command line. The launch file sources then removes the env
    file before executing the real body.

    Returns the path to the launch script.
    """
    working_dir = Path(agent_dir).resolve()
    bin_dir = working_dir / BIN_DIRNAME
    bin_dir.mkdir(exist_ok=True)
    curl_wrapper = bin_dir / "curl"
    curl_wrapper.write_text(
        "#!/bin/bash\n"
        "exec uv run --project ../.. python -m reva.safe_curl \"$@\"\n",
        encoding="utf-8",
    )
    curl_wrapper.chmod(0o755)

    env_keys = [k for k in os.environ if k.startswith(_ENV_PREFIXES)]
    env_path = working_dir / ENV_FILENAME
    env_lines = [f"export {k}={os.environ[k]!r}" for k in env_keys]
    env_path.write_text("\n".join(env_lines) + "\n", encoding="utf-8")
    env_path.chmod(0o600)

    script_path = working_dir / LAUNCH_FILENAME
    full_script = f"source {env_path}\nrm -f {env_path}\nexport PATH={bin_dir!s}:$PATH\n{launch_script}"
    script_path.write_text(full_script, encoding="utf-8")
    script_path.chmod(0o755)

    return script_path
