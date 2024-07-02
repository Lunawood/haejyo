from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from config import HF_EMBEDDING_MODEL


class RAGModel:
    def __init__(self):
        self.embedding_model = SentenceTransformer(HF_EMBEDDING_MODEL)
        self.index = None
        self.text_chunks = []

    def create_index(self, texts):
        self.text_chunks = texts
        embeddings = self.embedding_model.encode(texts)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)

    def search(self, query, top_k=3):
        if not self.index or not self.text_chunks:
            raise ValueError("Index or text chunks not initialized")

        query_embedding = self.embedding_model.encode([query])[0]
        distances, indices = self.index.search(
            np.array([query_embedding]).astype("float32"), top_k
        )

        # 유효한 인덱스만 반환
        valid_indices = [i for i in indices[0] if 0 <= i < len(self.text_chunks)]
        return [self.text_chunks[i] for i in valid_indices]


rag_model = RAGModel()
