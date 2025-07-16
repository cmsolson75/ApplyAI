# tests/test_workflow_runner.py
import os
import tempfile
from app.workflow_runner import WorkflowRunner

class DummyService:
    def __init__(self, output):
        self.output = output
    def generate(self, *args, **kwargs):
        return self.output

class DummyIndex:
    def query(self, text, top_k=3):
        return ["contextA", "contextB"]

def test_workflow_runner_creates_files(tmp_path):
    # Prepare runner with dummy services
    resume_service = DummyService("RESUME_CONTENT")
    cover_service = DummyService("COVER_CONTENT")
    index = DummyIndex()

    # Create a fake resume context
    context_path = tmp_path / "resume_full.md"
    context_path.write_text("BASE_RESUME")

    runner = WorkflowRunner(
        resume_service=resume_service,
        cover_service=cover_service,
        index=index,
        resume_context_path=str(context_path),
        output_dir=str(tmp_path)
    )

    result = runner.run("Engineer", "AcmeCorp", "Some Job Description")

    # Verify files exist
    assert os.path.exists(result["resume_path"])
    assert os.path.exists(result["cover_path"])

    # Verify file contents
    assert "RESUME_CONTENT" in open(result["resume_path"]).read()
    assert "COVER_CONTENT" in open(result["cover_path"]).read()