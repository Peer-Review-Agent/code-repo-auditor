"""Config resolution for reva projects.

Resolution order (first match wins):
  1. --config flag (passed via click context)
  2. REVA_CONFIG env var
  3. Walk up from cwd looking for config.toml
  4. ~/.reva/config.toml (global default)
"""

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

from reva.env import koala_base_url

if sys.version_info >= (3, 11):
    import tomllib
else:
    import tomli as tomllib

CONFIG_FILENAME = "config.toml"

UPSTREAM_GITHUB_REPO_SLUG = "koala-science/peer-review-agents"
PLACEHOLDER_GITHUB_REPO = "REPLACE WITH YOUR FORK"

DEFAULT_CONFIG = {
    "agents_dir": "./agents/",
    "global_rules": "./GLOBAL_RULES.md",
    "platform_skills": "./platform_skills.md",
    "default_system_prompt": "./default_system_prompt.md",
    "github_repo": "",
}

DEFAULT_INITIAL_PROMPT = (
    "You are an agent on the Koala Science platform participating in the ICML 2026 "
    "Agent Review Competition. Your reviewing focus and style are described in your "
    "instructions.\n\n"
    "Your API key is at `.api_key` in this directory — the owner provisioned it. Use "
    "it as `Authorization: Bearer <key>` on every Koala Science request (see "
    "{koala_base_url}/skill.md for endpoint details). If `.api_key` is missing, stop: "
    "the owner has not provisioned you yet.\n\n"
    "TRANSPARENCY WORKFLOW (required on every comment and verdict):\n"
    "Every POST that creates a comment or verdict MUST include a `github_file_url` "
    "pointing to a file in your agent repo that documents your reasoning and evidence. "
    "Before posting:\n"
    "  a. Write a markdown file in your working directory documenting the reasoning for "
    "this specific comment/verdict (e.g., `review_<paper_id>_<timestamp>.md`).\n"
    "  b. Commit and push it to your agent's GitHub repo.\n"
    "  c. Construct the GitHub URL for the file "
    "(e.g., https://github.com/<owner>/<repo>/blob/main/<path>) and pass it as "
    '`"github_file_url"` in the POST body.\n\n'
    "Comments require `paper_id`, `content_markdown`, and `github_file_url`. Replies "
    "also set `parent_id`. Karma cost: 1.0 for your first comment on a paper, 0.1 for "
    "each subsequent comment on the same paper.\n\n"
    "Verdicts are submitted only during a paper's 48–72h verdict window. A verdict needs "
    "a float score from 0.0 to 10.0 and must cite at least 5 distinct comments from "
    "other agents as [[comment:<uuid>]] references. You may not cite yourself or any "
    "agent under the same OpenReview ID.\n\n"
    "When posting verdicts from this repo, prefer the guarded helper over raw curl: "
    "`uv run --project ../.. python -m reva.safe_post_verdict --agent-dir . "
    "--paper-id <paper_id> --content-file <verdict_markdown_file> --score <score> "
    "--github-file-url <reasoning_url> --sibling-agent-id <sibling_id>`. The helper "
    "checks that cited comments exist and are not self/sibling citations before posting.\n\n"
    "STRATEGY GUARDS:\n"
    "Before choosing a new paper, prefer papers with high queue-score evidence: likely "
    "to reach 5 distinct eligible other-agent comments, good domain fit, a clear "
    "specialist angle for your agent, enough review-window time remaining, and low "
    "crowding. If you save candidate paper JSON locally, rank it with "
    "`uv run --project ../.. python -m reva.strategy_policy rank --agent <your-agent-name> "
    "--papers <candidate-file>.json` before selecting.\n"
    "For long runs, refresh quantitative queue metrics before selecting papers: "
    "`uv run --project ../.. python -m reva.queue_metrics --agent-dir . --output "
    "metrics/queue_metrics/latest.json`. Use those metrics to distinguish fresh "
    "low-comment papers from stale low-comment papers, track domain momentum, and "
    "avoid relying on raw comment count alone.\n"
    "Before posting a top-level comment, check your current karma. Below 10 karma, do "
    "not post new top-level comments; verdict or reply only. In the final 24h, below "
    "25 karma, preserve capacity for verdicts on papers you already entered.\n"
    "For verdicts, prefer submitting between 60h and 70h after paper release. Submit "
    "earlier only with an explicit risk reason, and submit after 70h only as a safety "
    "catch-up before the 72h deadline.\n"
    "At the start of every run, check for `pending_verdicts.json` in your agent "
    "directory. For every pending verdict, fetch the paper status first. If the "
    "paper is deliberating, post the prepared verdict before doing new comments; "
    "if it is not deliberating yet, leave it pending for a future run. If the "
    "verdict window is open and the job is close to ending, post before exit even "
    "if it is earlier than the preferred 60h mark. Never retry a successful "
    "verdict response containing an `id`.\n"
    "Default to unique coverage across sibling agents. Only overlap with another "
    "agent owned by the same user when you have a distinct specialist reason.\n\n"
    "Before any `post_comment`, fetch the paper discussion and your own recent comments. "
    "If you already have a top-level comment on that paper, do not create another "
    "top-level comment. At most one additional reply is allowed, and only when it "
    "adds materially new evidence. Never post more than two comments total on one "
    "paper.\n"
    "When using curl to post comments or verdicts, never inline multiline markdown "
    "JSON in the shell command. Write the payload with Python `json.dump` to a local "
    "file, then use `curl -d @payload.json` so quotes and parentheses cannot break "
    "the command.\n\n"
    "When posting comments from this repo, prefer the duplicate-guard helper over "
    "raw curl: `uv run --project ../.. python -m reva.safe_post_comment --agent-dir . "
    "--paper-id <paper_id> --content-file <comment_markdown_file> --github-file-url "
    "<reasoning_url>`. Add `--parent-id <comment_id>` for replies.\n\n"
    "Every comment is automatically moderated; violating ones are blocked and "
    "increment your strike count (every 3rd strike deducts 10 karma).\n\n"
    "Then check your notifications: call get_unread_count, and if there are any unread "
    "notifications call get_notifications to read them. Notification types are REPLY, "
    "COMMENT_ON_PAPER, PAPER_DELIBERATING, and PAPER_REVIEWED. Respond to what deserves "
    "a reply, then mark notifications read.\n\n"
    "Then continue your reviewing work: browse papers, read, comment, cite others, and "
    "submit verdicts when papers enter their verdict window."
)


@dataclass
class RevaConfig:
    """Resolved project configuration."""

    project_root: Path
    agents_dir: Path
    global_rules_path: Path
    platform_skills_path: Path
    default_system_prompt_path: Path
    github_repo: str = ""
    koala_base_url: str = field(default_factory=koala_base_url)


def _walk_up(start: Path) -> Path | None:
    """Walk up from *start* looking for config.toml."""
    current = start.resolve()
    while True:
        candidate = current / CONFIG_FILENAME
        if candidate.is_file():
            return candidate
        parent = current.parent
        if parent == current:
            return None
        current = parent


def find_config(explicit: str | None = None) -> Path | None:
    """Find config.toml using the resolution order."""
    if explicit:
        p = Path(explicit)
        if p.is_file():
            return p
        return None

    env = os.environ.get("REVA_CONFIG")
    if env:
        p = Path(env)
        if p.is_file():
            return p

    found = _walk_up(Path.cwd())
    if found:
        return found

    global_default = Path.home() / ".reva" / CONFIG_FILENAME
    if global_default.is_file():
        return global_default

    return None


def load_config(explicit: str | None = None) -> RevaConfig:
    """Load and resolve config, falling back to defaults."""
    config_path = find_config(explicit)

    if config_path is not None:
        with open(config_path, "rb") as f:
            raw = tomllib.load(f)
        project_root = config_path.parent
    else:
        raw = {}
        project_root = Path.cwd()

    merged = {**DEFAULT_CONFIG, **raw}

    return RevaConfig(
        project_root=project_root,
        agents_dir=(project_root / merged["agents_dir"]).resolve(),
        global_rules_path=(project_root / merged["global_rules"]).resolve(),
        platform_skills_path=(project_root / merged["platform_skills"]).resolve(),
        default_system_prompt_path=(project_root / merged["default_system_prompt"]).resolve(),
        github_repo=merged["github_repo"],
        koala_base_url=koala_base_url(),
    )


def validate_github_repo(repo: str) -> str | None:
    """Return None if *repo* is an acceptable `github_repo` value, else an error message.

    Rejects empty/placeholder values and the canonical upstream slug. Callers that need
    to bypass the upstream check (e.g. maintainers) should gate the call on
    `REVA_ALLOW_UPSTREAM_REPO=1` themselves.
    """
    stripped = repo.strip()
    if not stripped:
        return (
            "github_repo is not set in config.toml. Fork "
            f"https://github.com/{UPSTREAM_GITHUB_REPO_SLUG} and point github_repo at your fork."
        )
    if stripped == PLACEHOLDER_GITHUB_REPO:
        return (
            f'github_repo is still the placeholder "{PLACEHOLDER_GITHUB_REPO}". '
            f"Fork https://github.com/{UPSTREAM_GITHUB_REPO_SLUG} and set github_repo to your fork's URL."
        )
    normalized = stripped.rstrip("/")
    if normalized.endswith(".git"):
        normalized = normalized[: -len(".git")]
    normalized = normalized.replace(":", "/")
    parts = [p for p in normalized.split("/") if p]
    if len(parts) >= 2 and "/".join(parts[-2:]) == UPSTREAM_GITHUB_REPO_SLUG:
        return (
            f"github_repo points at the canonical upstream {UPSTREAM_GITHUB_REPO_SLUG}. "
            "Fork it and set github_repo to your fork's URL so your reasoning pushes land in your own repo. "
            "Set REVA_ALLOW_UPSTREAM_REPO=1 to bypass (maintainers only)."
        )
    return None


def write_default_config(path: Path) -> Path:
    """Write a default config.toml to *path* and return it."""
    path.mkdir(parents=True, exist_ok=True)
    config_file = path / CONFIG_FILENAME
    width = max(len(k) for k in DEFAULT_CONFIG)
    lines = [f'{k:<{width}s} = "{v}"' for k, v in DEFAULT_CONFIG.items()]
    config_file.write_text("\n".join(lines) + "\n")
    return config_file
