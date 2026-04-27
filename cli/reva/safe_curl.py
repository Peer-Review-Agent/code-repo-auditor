"""A tiny curl-compatible guard for Koala comment posts.

Non-comment requests are delegated to the real curl binary. POST requests to
`/api/v1/comments/` are routed through `reva.safe_post_comment` so agents cannot
accidentally bypass duplicate protection.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

from reva.safe_post_comment import safe_post_comment


def real_curl() -> str:
    return os.environ.get("REVA_REAL_CURL", "/usr/bin/curl")


def value_after(args: list[str], flag: str) -> str | None:
    for index, item in enumerate(args):
        if item == flag and index + 1 < len(args):
            return args[index + 1]
        if item.startswith(flag) and item != flag:
            return item[len(flag) :]
    return None


def all_values_after(args: list[str], flag: str) -> list[str]:
    values = []
    index = 0
    while index < len(args):
        item = args[index]
        if item == flag and index + 1 < len(args):
            values.append(args[index + 1])
            index += 2
            continue
        if item.startswith(flag) and item != flag:
            values.append(item[len(flag) :])
        index += 1
    return values


def request_url(args: list[str]) -> str | None:
    for item in reversed(args):
        if item.startswith("http://") or item.startswith("https://"):
            return item
    return None


def is_comment_post(args: list[str]) -> bool:
    url = request_url(args)
    if url is None:
        return False
    path = urlparse(url).path.rstrip("/")
    method = (value_after(args, "-X") or "").upper()
    has_payload = value_after(args, "-d") is not None or value_after(args, "--data") is not None
    return path.endswith("/api/v1/comments") and (method == "POST" or has_payload)


def authorization_header(args: list[str]) -> str:
    for header in all_values_after(args, "-H"):
        if header.lower().startswith("authorization:"):
            return header.split(":", 1)[1].strip().replace("Bearer ", "")
    env_key = os.environ.get("COALESCENCE_API_KEY")
    if env_key:
        return env_key
    raise RuntimeError("missing Authorization header or COALESCENCE_API_KEY")


def payload_arg(args: list[str]) -> str:
    payload = value_after(args, "-d") or value_after(args, "--data")
    if payload is None:
        raise RuntimeError("missing -d/--data payload for comment POST")
    return payload


def load_payload(payload: str) -> dict:
    if payload.startswith("@"):
        return json.loads(Path(payload[1:]).read_text(encoding="utf-8"))
    return json.loads(payload)


def delegate(args: list[str]) -> int:
    return subprocess.run([real_curl(), *args]).returncode


def main() -> int:
    args = sys.argv[1:]
    if not is_comment_post(args):
        return delegate(args)

    try:
        payload = load_payload(payload_arg(args))
        result = safe_post_comment(
            base_url=request_url(args).split("/api/v1/comments", 1)[0],
            api_key=authorization_header(args),
            paper_id=payload["paper_id"],
            content_markdown=payload["content_markdown"],
            github_file_url=payload["github_file_url"],
            parent_id=payload.get("parent_id"),
        )
    except Exception as exc:
        print(json.dumps({"posted": False, "error": str(exc)}, indent=2))
        return 1

    print(json.dumps(result.get("response", result), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
