from reva.safe_post_comment import (
    ExistingComment,
    duplicate_reason,
    jaccard_similarity,
    normalize_content,
)


def test_normalize_content_removes_markdown_and_case():
    assert normalize_content("### Hello, WORLD!") == "hello world"


def test_jaccard_similarity_detects_near_overlap():
    left = "training code missing evaluation scripts absent"
    right = "evaluation scripts absent and training code missing"
    assert jaccard_similarity(left, right) > 0.75


def test_duplicate_reason_blocks_existing_top_level():
    comments = [
        ExistingComment(
            comment_id="c1",
            author_id="me",
            parent_id=None,
            content_markdown="Original top-level comment",
        )
    ]
    reason = duplicate_reason(
        comments=comments,
        my_actor_id="me",
        parent_id=None,
        content_markdown="Different new content",
    )
    assert "already have top-level" in reason


def test_duplicate_reason_allows_first_top_level():
    reason = duplicate_reason(
        comments=[],
        my_actor_id="me",
        parent_id=None,
        content_markdown="New content",
    )
    assert reason is None


def test_duplicate_reason_blocks_same_parent_reply():
    comments = [
        ExistingComment(
            comment_id="c1",
            author_id="me",
            parent_id="parent",
            content_markdown="Earlier reply",
        )
    ]
    reason = duplicate_reason(
        comments=comments,
        my_actor_id="me",
        parent_id="parent",
        content_markdown="Another reply",
    )
    assert "already replied" in reason


def test_duplicate_reason_blocks_near_duplicate_content():
    comments = [
        ExistingComment(
            comment_id="c1",
            author_id="me",
            parent_id="other",
            content_markdown="The repository has no training code and no evaluation scripts",
        )
    ]
    reason = duplicate_reason(
        comments=comments,
        my_actor_id="me",
        parent_id="parent",
        content_markdown="No training code or evaluation scripts exist in the repository",
    )
    assert "near duplicate" in reason


def test_duplicate_reason_ignores_other_authors():
    comments = [
        ExistingComment(
            comment_id="c1",
            author_id="other",
            parent_id=None,
            content_markdown="Same point",
        )
    ]
    reason = duplicate_reason(
        comments=comments,
        my_actor_id="me",
        parent_id=None,
        content_markdown="Same point",
    )
    assert reason is None
