"""
gemini-cli → ATIF translator.

Gemini CLI (invoked non-interactively with `-p`) emits plain text, not JSON.
We translate by:

  1. Emitting the initial prompt (from initial_prompt.txt) as a single user
     step the first time we're called on an empty trajectory.
  2. Buffering subsequent output lines into paragraphs (blank-line separated),
     emitting each paragraph as an agent step.
  3. Recognizing reva harness lines (``[reva] ...``) and flushing the current
     paragraph immediately, then emitting the harness line as a system step.

Caveats:
  - Gemini CLI does not expose structured tool-call output, so every model turn
    lands in `message` with no `tool_calls`/`observation`.
  - Token usage / cost are not reported and stay zero in final_metrics.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Iterator

from reva.atif import TrajectoryBuilder

_STATE_KEY = "gemini_cli"
_NOISY_PREFIXES = (
    "YOLO mode is enabled",
    "Loaded cached credentials",
    "Data collection is disabled",
)


def translate(
    agent_dir: Path,
    lines: Iterable[str],
    builder: TrajectoryBuilder,
) -> Iterator[dict[str, Any]]:
    state = builder.state.setdefault(_STATE_KEY, {"buf": [], "seeded_user": False})
    buf: list[str] = state["buf"]

    # Seed the user step from initial_prompt.txt on first invocation
    if not state["seeded_user"]:
        state["seeded_user"] = True
        initial_path = agent_dir / "initial_prompt.txt"
        if initial_path.exists():
            initial = initial_path.read_text(encoding="utf-8").strip()
            if initial:
                yield builder.add_user_message(message=initial)
        if not builder.trajectory["agent"].get("model_name"):
            builder.set_agent_metadata(model_name="gemini")

    for raw in lines:
        line = raw.rstrip("\r\n")
        stripped = line.strip()

        if not stripped:
            if buf:
                step = _flush_paragraph(builder, buf)
                if step is not None:
                    yield step
            continue

        if line.startswith("[reva]"):
            if buf:
                step = _flush_paragraph(builder, buf)
                if step is not None:
                    yield step
            yield builder.add_system_message(message=stripped)
            continue

        if any(stripped.startswith(p) for p in _NOISY_PREFIXES):
            yield builder.add_system_message(message=stripped)
            continue

        buf.append(line)


def _flush_paragraph(builder: TrajectoryBuilder, buf: list[str]) -> dict[str, Any] | None:
    text = "\n".join(buf).strip()
    buf.clear()
    if not text:
        return None
    return builder.add_agent_message(message=text)
