"""Redact secrets from backend output before it reaches agent.log."""

from __future__ import annotations

import re
import sys

KOALA_TOKEN_RE = re.compile(r"cs_[A-Za-z0-9_-]+")
AUTH_HEADER_RE = re.compile(
    r"(Authorization:\s*(?:Bearer\s*)?)([^\"'\n\r]+)",
    re.IGNORECASE,
)


def redact_text(text: str) -> str:
    redacted = KOALA_TOKEN_RE.sub("REDACTED_KOALA_API_KEY", text)
    return AUTH_HEADER_RE.sub(r"\1REDACTED_KOALA_API_KEY", redacted)


def main() -> int:
    for line in sys.stdin:
        sys.stdout.write(redact_text(line))
        sys.stdout.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
