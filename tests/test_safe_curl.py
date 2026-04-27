from reva.safe_curl import (
    authorization_header,
    is_comment_post,
    load_payload,
    request_url,
)


def test_identifies_comment_post_with_payload_file():
    args = ["-s", "-X", "POST", "-d", "@/tmp/payload.json", "https://koala.science/api/v1/comments/"]
    assert is_comment_post(args)


def test_does_not_intercept_get_request():
    args = ["-s", "https://koala.science/api/v1/comments/paper/abc"]
    assert not is_comment_post(args)


def test_extracts_request_url_from_end():
    args = ["-H", "Authorization: key", "https://koala.science/api/v1/comments/"]
    assert request_url(args) == "https://koala.science/api/v1/comments/"


def test_authorization_header_strips_bearer():
    args = ["-H", "Authorization: Bearer cs_testtoken"]
    assert authorization_header(args) == "cs_testtoken"


def test_load_payload_from_json_string():
    payload = load_payload('{"paper_id": "p", "content_markdown": "c", "github_file_url": "u"}')
    assert payload["paper_id"] == "p"
