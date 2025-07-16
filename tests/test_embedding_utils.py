import numpy as np
import tempfile
import os
import pytest
from app.embedding_utils import build_faiss_index

class DummyEmbeddings:
    def embed_query(self, text):
        return [1.0, 2.0, 3.0]  # fixed vector
    def embed_documents(self, texts):
        return [[0.1, 0.2, 0.3] for _ in texts]

@pytest.fixture(autouse=True)
def patch_openai_embeddings(monkeypatch):
    monkeypatch.setattr("app.embedding_utils.OpenAIEmbeddings", lambda : DummyEmbeddings())

def test_build_faiss_index_and_query(tmp_path):
    # Create dummy .md files
    (tmp_path / "a.md").write_text("doc A")
    (tmp_path / "b.md").write_text("doc B")

    # Build index
    index = build_faiss_index(str(tmp_path))
    assert len(index.texts) == 2

    # Query
    results = index.query("some query", top_k=1)
    assert len(results) == 1
    assert any("doc A" in r or "doc B" in r for r in results)