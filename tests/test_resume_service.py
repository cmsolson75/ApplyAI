import io
import builtins
import pytest
from app.services.resume_service import ResumeService

# Dummy classes
class DummyPrompt:
    def __or__(self, other):
        return DummyChain()

class DummyLLM:
    pass

class DummyChain:
    def invoke(self, inputs):
        return type("Obj", (object,), {
            "content": f"{inputs['job_title']}|{inputs['company']}"
        })

@pytest.fixture(autouse=True)
def patch_prompt_and_llm(monkeypatch):
    # Patch the prompt and LLM classes to avoid real init logic
    monkeypatch.setattr(
        "app.services.resume_service.PromptTemplate.from_template",
        lambda _: DummyPrompt()
    )
    monkeypatch.setattr(
        "app.services.resume_service.ChatOpenAI",
        lambda **kwargs: DummyLLM()
    )

    # Patch open() only for prompt_path, return a dummy file-like object
    def fake_open(path, mode="r", encoding=None):
        if "prompt" in path:
            return io.StringIO("DUMMY PROMPT CONTENT")
        return builtins.open(path, mode, encoding=encoding)
    monkeypatch.setattr("builtins.open", fake_open)

def test_generate_builds_prompt_correctly():
    service = ResumeService("any/prompt/path.txt")  # uses patched open
    result = service.generate("Engineer", "AcmeCorp", "Some JD", "FullResume")
    assert "Engineer" in result
    assert "AcmeCorp" in result