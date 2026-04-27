from reva.redact_stream import redact_text


def test_redacts_koala_token_shape():
    text = "curl -H 'Authorization: Bearer cs_secret-token_123'"
    assert "cs_secret" not in redact_text(text)
    assert "REDACTED_KOALA_API_KEY" in redact_text(text)


def test_redacts_authorization_header_without_bearer():
    text = 'curl -H "Authorization: cs_secret-token_123" https://koala.science'
    redacted = redact_text(text)
    assert "cs_secret" not in redacted
    assert "Authorization: REDACTED_KOALA_API_KEY" in redacted


def test_keeps_non_secret_text():
    assert redact_text("hello world") == "hello world"
