"""
Generic plain-text translator — fallback for backends that don't have a
dedicated translator yet (aider, codex, opencode). Shares the same paragraph-
buffering logic as gemini_cli.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Iterator

from reva.atif import TrajectoryBuilder

_STATE_KEY = "plain_text"


def translate(
    agent_dir: Path,
    lines: Iterable[str],
    builder: TrajectoryBuilder,
) -> Iterator[dict[str, Any]]:
    state = builder.state.setdefault(_STATE_KEY, {"buf": [], "seeded_user": False})
    buf: list[str] = state["buf"]

    if not state["seeded_user"]:
        state["seeded_user"] = True
        initial_path = agent_dir / "initial_prompt.txt"
        if initial_path.exists():
            initial = initial_path.read_text(encoding="utf-8").strip()
            if initial:
                yield builder.add_user_message(message=initial)

    for raw in lines:
        line = raw.rstrip("\r\n")
        stripped = line.strip()

        if not stripped:
            if buf:
                text = "\n".join(buf).strip()
                buf.clear()
                if text:
                    yield builder.add_agent_message(message=text)
            continue

        if line.startswith("[reva]"):
            if buf:
                text = "\n".join(buf).strip()
                buf.clear()
                if text:
                    yield builder.add_agent_message(message=text)
            yield builder.add_system_message(message=stripped)
            continue

        buf.append(line)
