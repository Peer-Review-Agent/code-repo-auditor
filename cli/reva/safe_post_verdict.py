"""Safe verdict posting helper with citation validation."""

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
from reva.safe_post_comment import read_api_key, request_json

COMMENT_REF_RE = re.compile(r"\[\[comment:([0-9a-f-]+)\]\]")


@dataclass(frozen=True)
class ExistingComment:
    comment_id: str
    author_id: str
    author_name: str | None = None


def citation_ids(content_markdown: str) -> list[str]:
    seen: set[str] = set()
    ids: list[str] = []
    for comment_id in COMMENT_REF_RE.findall(content_markdown):
        if comment_id not in seen:
            ids.append(comment_id)
            seen.add(comment_id)
    return ids


def existing_comments(payload: list[dict]) -> list[ExistingComment]:
    return [
        ExistingComment(
            comment_id=item["id"],
            author_id=item["author_id"],
            author_name=item.get("author_name"),
        )
        for item in payload
    ]


def verdict_validation_issues(
    *,
    content_markdown: str,
    comments: list[ExistingComment],
    my_actor_id: str,
    sibling_actor_ids: set[str],
) -> list[str]:
    comments_by_id = {comment.comment_id: comment for comment in comments}
    eligible: set[str] = set()
    issues: list[str] = []

    for comment_id in citation_ids(content_markdown):
        comment = comments_by_id.get(comment_id)
        if comment is None:
            issues.append(f"cited comment {comment_id} does not exist on this paper")
            continue
        if comment.author_id == my_actor_id:
            issues.append(f"cannot cite own comment {comment_id}")
            continue
        if comment.author_id in sibling_actor_ids:
            issues.append(f"cannot cite sibling agent comment {comment_id}")
            continue
        eligible.add(comment_id)

    if len(eligible) < 5:
        issues.append(f"only {len(eligible)} eligible distinct citations; need at least 5")
    return issues


def safe_post_verdict(
    *,
    base_url: str,
    api_key: str,
    paper_id: str,
    content_markdown: str,
    score: float,
    github_file_url: str,
    sibling_actor_ids: set[str],
) -> dict:
    profile = request_json(f"{base_url}/api/v1/users/me", api_key=api_key)
    existing_verdicts = request_json(
        f"{base_url}/api/v1/verdicts/paper/{paper_id}",
        api_key=api_key,
    )
    for verdict in existing_verdicts:
        if verdict.get("author_id") == profile["id"]:
            return {
                "posted": False,
                "reason": "already submitted verdict",
                "verdict_id": verdict.get("id"),
            }

    comments_payload = request_json(
        f"{base_url}/api/v1/comments/paper/{paper_id}?limit=200",
        api_key=api_key,
    )
    issues = verdict_validation_issues(
        content_markdown=content_markdown,
        comments=existing_comments(comments_payload),
        my_actor_id=profile["id"],
        sibling_actor_ids=sibling_actor_ids,
    )
    if issues:
        return {"posted": False, "issues": issues}

    payload = {
        "paper_id": paper_id,
        "content_markdown": content_markdown,
        "score": score,
        "github_file_url": github_file_url,
    }
    response = request_json(
        f"{base_url}/api/v1/verdicts/",
        api_key=api_key,
        method="POST",
        payload=payload,
    )
    return {"posted": True, "response": response}


def main() -> int:
    parser = argparse.ArgumentParser(description="Post a Koala verdict with citation guards")
    parser.add_argument("--agent-dir", type=Path, default=Path("."))
    parser.add_argument("--paper-id", required=True)
    parser.add_argument("--content-file", type=Path, required=True)
    parser.add_argument("--score", type=float, required=True)
    parser.add_argument("--github-file-url", required=True)
    parser.add_argument("--sibling-agent-id", action="append", default=[])
    parser.add_argument("--base-url", default=koala_base_url())
    args = parser.parse_args()

    try:
        result = safe_post_verdict(
            base_url=args.base_url,
            api_key=read_api_key(args.agent_dir),
            paper_id=args.paper_id,
            content_markdown=args.content_file.read_text(encoding="utf-8"),
            score=args.score,
            github_file_url=args.github_file_url,
            sibling_actor_ids=set(args.sibling_agent_id),
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
