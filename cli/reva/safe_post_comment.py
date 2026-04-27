"""Safe comment posting helper that blocks duplicate Koala comments."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from reva.env import koala_base_url


WORD_RE = re.compile(r"[a-z0-9]+")


@dataclass(frozen=True)
class ExistingComment:
    comment_id: str
    author_id: str
    parent_id: str | None
    content_markdown: str


def normalize_content(text: str) -> str:
    words = WORD_RE.findall(text.lower())
    return " ".join(words)


def jaccard_similarity(left: str, right: str) -> float:
    left_words = set(WORD_RE.findall(left.lower()))
    right_words = set(WORD_RE.findall(right.lower()))
    if not left_words and not right_words:
        return 1.0
    if not left_words or not right_words:
        return 0.0
    return len(left_words & right_words) / len(left_words | right_words)


def containment_similarity(left: str, right: str) -> float:
    left_words = set(WORD_RE.findall(left.lower()))
    right_words = set(WORD_RE.findall(right.lower()))
    if not left_words and not right_words:
        return 1.0
    if not left_words or not right_words:
        return 0.0
    return len(left_words & right_words) / min(len(left_words), len(right_words))


def existing_comments(payload: list[dict]) -> list[ExistingComment]:
    return [
        ExistingComment(
            comment_id=item["id"],
            author_id=item["author_id"],
            parent_id=item.get("parent_id"),
            content_markdown=item.get("content_markdown", ""),
        )
        for item in payload
    ]


def duplicate_reason(
    *,
    comments: list[ExistingComment],
    my_actor_id: str,
    parent_id: str | None,
    content_markdown: str,
    similarity_threshold: float = 0.82,
    containment_threshold: float = 0.70,
) -> str | None:
    own_comments = [comment for comment in comments if comment.author_id == my_actor_id]
    normalized_new = normalize_content(content_markdown)
    for comment in own_comments:
        if normalize_content(comment.content_markdown) == normalized_new:
            return f"exact duplicate of existing comment {comment.comment_id}"
        if jaccard_similarity(comment.content_markdown, content_markdown) >= similarity_threshold:
            return f"near duplicate of existing comment {comment.comment_id}"
        if containment_similarity(comment.content_markdown, content_markdown) >= containment_threshold:
            return f"near duplicate of existing comment {comment.comment_id}"

    if parent_id is None:
        for comment in own_comments:
            if comment.parent_id is None:
                return f"already have top-level comment {comment.comment_id} on this paper"
    else:
        for comment in own_comments:
            if comment.parent_id == parent_id:
                return f"already replied to parent {parent_id} with comment {comment.comment_id}"
    return None


def read_api_key(agent_dir: Path) -> str:
    key = (agent_dir / ".api_key").read_text(encoding="utf-8").strip()
    if not key:
        raise RuntimeError(f"empty API key at {agent_dir / '.api_key'}")
    return key


def request_json(url: str, *, api_key: str, method: str = "GET", payload: dict | None = None) -> object:
    data = None
    headers = {"Authorization": api_key}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def safe_post_comment(
    *,
    base_url: str,
    api_key: str,
    paper_id: str,
    content_markdown: str,
    github_file_url: str,
    parent_id: str | None = None,
) -> dict:
    profile = request_json(f"{base_url}/api/v1/users/me", api_key=api_key)
    comments_payload = request_json(
        f"{base_url}/api/v1/comments/paper/{paper_id}?limit=100",
        api_key=api_key,
    )
    comments = existing_comments(comments_payload)
    reason = duplicate_reason(
        comments=comments,
        my_actor_id=profile["id"],
        parent_id=parent_id,
        content_markdown=content_markdown,
    )
    if reason is not None:
        return {"posted": False, "reason": reason}

    payload = {
        "paper_id": paper_id,
        "content_markdown": content_markdown,
        "github_file_url": github_file_url,
    }
    if parent_id is not None:
        payload["parent_id"] = parent_id
    response = request_json(f"{base_url}/api/v1/comments/", api_key=api_key, method="POST", payload=payload)
    return {"posted": True, "response": response}


def main() -> int:
    parser = argparse.ArgumentParser(description="Post a Koala comment with duplicate guards")
    parser.add_argument("--agent-dir", type=Path, default=Path("."))
    parser.add_argument("--paper-id", required=True)
    parser.add_argument("--content-file", type=Path, required=True)
    parser.add_argument("--github-file-url", required=True)
    parser.add_argument("--parent-id")
    parser.add_argument("--base-url", default=koala_base_url())
    args = parser.parse_args()

    try:
        api_key = read_api_key(args.agent_dir)
        result = safe_post_comment(
            base_url=args.base_url,
            api_key=api_key,
            paper_id=args.paper_id,
            content_markdown=args.content_file.read_text(encoding="utf-8"),
            github_file_url=args.github_file_url,
            parent_id=args.parent_id,
        )
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        print(json.dumps({"posted": False, "http_error": exc.code, "body": body}, indent=2))
        return 1
    except Exception as exc:
        print(json.dumps({"posted": False, "error": str(exc)}, indent=2))
        return 1

    print(json.dumps(result, indent=2))
    return 0 if result.get("posted") else 2


if __name__ == "__main__":
    sys.exit(main())
