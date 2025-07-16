import faiss
import numpy as np
import glob
import os
from typing import List
from langchain_openai import OpenAIEmbeddings


class FAISSIndex:
    """
    Wrapper for a FAISS vector index and its associated text corpus.
    """

    def __init__(self, index: faiss.Index, texts: List[str]) -> None:
        """
        Initialize a FAISSIndex.

        Args:
            index (faiss.Index): A FAISS index containing vector embeddings.
            texts (List[str]): Text documents corresponding to the vectors in the index.
        """
        self.index: faiss.Index = index
        self.texts: List[str] = texts

    def query(self, query_text: str, top_k: int = 3) -> List[str]:
        """
        Perform a similarity search against the index.

        Args:
            query_text (str): Input query text.
            top_k (int): Number of nearest neighbors to return.

        Returns:
            List[str]: Retrieved documents sorted by similarity.
        """
        emb = OpenAIEmbeddings()
        qv: np.ndarray = np.array([emb.embed_query(query_text)], dtype=np.float32)
        D, I = self.index.search(qv, top_k)
        return [self.texts[i] for i in I[0] if i < len(self.texts)]


def build_faiss_index(coverletters_dir: str) -> FAISSIndex:
    """
    Build a FAISS index from all markdown files in a given directory.

    Args:
        coverletters_dir (str): Path to directory containing .md files.

    Returns:
        FAISSIndex: Constructed FAISSIndex with embedded documents.

    Raises:
        RuntimeError: If no markdown files are found in the given directory.
    """
    emb = OpenAIEmbeddings()
    files: List[str] = glob.glob(os.path.join(coverletters_dir, "*.md"))
    texts: List[str] = [open(f, encoding="utf-8").read() for f in files]
    if not texts:
        raise RuntimeError("No cover letter templates found in context/CoverLetters")

    vecs: List[List[float]] = emb.embed_documents(texts)
    mat: np.ndarray = np.array(vecs, dtype=np.float32)
    index: faiss.IndexFlatL2 = faiss.IndexFlatL2(mat.shape[1])
    index.add(mat)
    return FAISSIndex(index, texts)