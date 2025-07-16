import io
import os
import tempfile
import textwrap
from app.config_loader import load_config

def test_load_config_resolves_paths(tmp_path):
    # Create a temporary config.yaml with relative paths
    yaml_content = textwrap.dedent("""
        resume_prompt: prompts/prompt_resume.txt
        coverletter_prompt: prompts/prompt_coverletter.txt
        resume_context: context/Resume_Full.md
        cover_letter_context_folder: context/CoverLetters
    """)
    cfg_file = tmp_path / "config_test.yaml"
    cfg_file.write_text(yaml_content, encoding="utf-8")

    # Create dummy dirs/files to ensure normalization works (not strictly necessary)
    (tmp_path / "prompts").mkdir()
    (tmp_path / "context").mkdir()
    (tmp_path / "context" / "CoverLetters").mkdir()
    (tmp_path / "prompts" / "prompt_resume.txt").write_text("dummy")
    (tmp_path / "prompts" / "prompt_coverletter.txt").write_text("dummy")
    (tmp_path / "context" / "Resume_Full.md").write_text("dummy")

    # Run loader on this temp config
    cfg = load_config(str(cfg_file))

    # Assert keys exist
    assert "resume_prompt" in cfg
    assert "coverletter_prompt" in cfg
    assert "resume_context" in cfg
    assert "cover_letter_context_folder" in cfg

    # Assert the values are absolute paths (normalized)
    for key, path in cfg.items():
        assert os.path.isabs(path), f"{key} is not absolute: {path}"
        # optional: check the path points under tmp_path
        assert str(tmp_path) in path