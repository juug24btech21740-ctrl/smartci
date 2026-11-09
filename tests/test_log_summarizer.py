import pytest
from src.log_summarizer import summarize_build_log


def test_empty_log():
    with pytest.raises(ValueError):
        summarize_build_log("")


def test_missing_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ValueError):
        summarize_build_log("ERROR: Build failed")


def test_successful_summary(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        def json(self):
            return {
                "choices": [
                    {
                        "message": {
                            "content": "Build failed due to missing dependency."
                        }
                    }
                ]
            }

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")

    def fake_post(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(
        "src.log_summarizer.requests.post",
        fake_post
    )

    result = summarize_build_log("ERROR: Missing dependency")
    assert "missing dependency" in result
