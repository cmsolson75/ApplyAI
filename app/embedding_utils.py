import faiss
import numpy as np
import glob
import os
from langchain_openai import OpenAIEmbeddings


class FAISSIndex:
    def __init__(self, index, texts):
        self.index = index
        self.texts = texts

    def query(self, query_text, top_k=3):
        emb = OpenAIEmbeddings()
        qv = np.array([emb.embed_query(query_text)], dtype=np.float32)
        D, I = self.index.search(qv, top_k)
        return [self.texts[i] for i in I[0] if i < len(self.texts)]


def build_faiss_index(coverletters_dir):
    emb = OpenAIEmbeddings()
    files = glob.glob(os.path.join(coverletters_dir, "*.md"))
    texts = [open(f).read() for f in files]
    if not texts:
        raise RuntimeError("No cover letter templates found in context/CoverLetters")
    vecs = emb.embed_documents(texts)
    mat = np.array(vecs, dtype=np.float32)
    index = faiss.IndexFlatL2(mat.shape[1])
    index.add(mat)
    return FAISSIndex(index, texts)
