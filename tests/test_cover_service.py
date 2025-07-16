import io
import builtins
import pytest
from app.services.cover_service import CoverLetterService

class DummyPrompt:
    def __or__(self, other):
        return DummyChain()

class DummyLLM:
    pass

class DummyChain:
    def invoke(self, inputs):
        return type("Obj", (object,), {
            "content": f"{inputs['job_title']}->{inputs['company']}"
        })

@pytest.fixture(autouse=True)
def patch_prompt_and_llm(monkeypatch):
    monkeypatch.setattr(
        "app.services.cover_service.PromptTemplate.from_template",
        lambda _: DummyPrompt()
    )
    monkeypatch.setattr(
        "app.services.cover_service.ChatOpenAI",
        lambda **kwargs: DummyLLM()
    )

    def fake_open(path, mode="r", encoding=None):
        if "prompt" in path:
            return io.StringIO("DUMMY PROMPT CONTENT")
        return builtins.open(path, mode, encoding=encoding)
    monkeypatch.setattr("builtins.open", fake_open)

def test_generate_builds_prompt_correctly():
    service = CoverLetterService("any/prompt/path.txt")
    result = service.generate("Engineer", "AcmeCorp", "JD", "ResumeTxt", "Examples")
    assert "Engineer" in result
    assert "AcmeCorp" in result