from reva.safe_post_verdict import (
    ExistingComment,
    citation_ids,
    verdict_validation_issues,
)


def test_citation_ids_extracts_distinct_comment_references():
    text = "Use [[comment:aaaaaaaa-1111-2222-3333-bbbbbbbbbbbb]] twice [[comment:aaaaaaaa-1111-2222-3333-bbbbbbbbbbbb]]."

    assert citation_ids(text) == ["aaaaaaaa-1111-2222-3333-bbbbbbbbbbbb"]


def test_verdict_validation_accepts_five_eligible_comments():
    comments = [
        ExistingComment(comment_id=f"c{i}", author_id=f"agent-{i}", author_name=f"agent-{i}")
        for i in range(5)
    ]
    text = " ".join(f"[[comment:c{i}]]" for i in range(5))

    assert verdict_validation_issues(
        content_markdown=text,
        comments=comments,
        my_actor_id="me",
        sibling_actor_ids={"sibling"},
    ) == []


def test_verdict_validation_rejects_own_sibling_and_missing_citations():
    own = "00000000-0000-4000-8000-000000000001"
    sib = "00000000-0000-4000-8000-000000000002"
    missing = "00000000-0000-4000-8000-000000000003"
    ok_ids = [
        "00000000-0000-4000-8000-000000000004",
        "00000000-0000-4000-8000-000000000005",
        "00000000-0000-4000-8000-000000000006",
        "00000000-0000-4000-8000-000000000007",
    ]
    comments = [
        ExistingComment(comment_id=own, author_id="me", author_name="Code Repo Auditor"),
        ExistingComment(comment_id=sib, author_id="sibling", author_name="Novelty-Scout"),
        ExistingComment(comment_id=ok_ids[0], author_id="other-1", author_name="Other 1"),
        ExistingComment(comment_id=ok_ids[1], author_id="other-2", author_name="Other 2"),
        ExistingComment(comment_id=ok_ids[2], author_id="other-3", author_name="Other 3"),
        ExistingComment(comment_id=ok_ids[3], author_id="other-4", author_name="Other 4"),
    ]
    text = " ".join(f"[[comment:{comment_id}]]" for comment_id in [own, sib, missing, *ok_ids])

    issues = verdict_validation_issues(
        content_markdown=text,
        comments=comments,
        my_actor_id="me",
        sibling_actor_ids={"sibling"},
    )

    assert f"cannot cite own comment {own}" in issues
    assert f"cannot cite sibling agent comment {sib}" in issues
    assert f"cited comment {missing} does not exist on this paper" in issues
    assert "only 4 eligible distinct citations; need at least 5" in issues
