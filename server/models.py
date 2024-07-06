from openai import OpenAI
import faiss
import numpy as np
from config import OPENAI_API_KEY
import certifi
import ssl
import os
import httpx

# SSL 컨텍스트 생성
ssl_context = ssl.create_default_context(cafile=certifi.where())

# httpx 클라이언트 생성
http_client = httpx.Client(verify=ssl_context)

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY, http_client=http_client)


class RAGModel:
    def __init__(self):
        self.index = None
        self.text_chunks = []

    def create_index(self, texts, risks, summaries):
        self.text_chunks = [
            {"text": text, "risk": risk, "summary": summary}
            for text, risk, summary in zip(texts, risks, summaries)
        ]
        embeddings = self._get_embeddings(texts)
        dimension = len(embeddings[0])  # 첫 번째 임베딩의 길이를 사용
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype("float32"))

    def _get_embeddings(self, texts):
        embeddings = []
        for text in texts:
            response = client.embeddings.create(
                model="text-embedding-3-small", input=text
            )
            embeddings.append(response.data[0].embedding)
        return embeddings

    def search(
        self, query, top_k=3, distance_threshold=0.3, relative_distance_threshold=1.2
    ):
        if not self.index or not self.text_chunks:
            raise ValueError("Index or text chunks not initialized")

        query_embedding = self._get_embeddings([query])[0]
        distances, indices = self.index.search(
            np.array([query_embedding]).astype("float32"), top_k * 2
        )

        # valid_indices = [i for i in indices[0] if 0 <= i < len(self.text_chunks)]
        # return [self.text_chunks[i] for i in valid_indices]
        results = []
        min_distance = float("inf")

        for i, dist in zip(indices[0], distances[0]):
            if 0 <= i < len(self.text_chunks):
                min_distance = min(min_distance, dist)

        for i, dist in zip(indices[0], distances[0]):
            if 0 <= i < len(self.text_chunks):
                # 절대적 거리 임계값과 상대적 거리 임계값을 모두 확인
                if (
                    dist <= distance_threshold
                    and dist <= min_distance * relative_distance_threshold
                ):
                    results.append((self.text_chunks[i], dist))
        results.sort(key=lambda x: x[1])

        # results의 0번 인덱스인 textchunks들만 반환한다.
        sorted_chunks = [result[0] for result in results]

        return sorted_chunks[:top_k]

    def add_texts(self, new_texts, new_risks, new_summaries):
        new_embeddings = self._get_embeddings(new_texts)
        self.index.add(np.array(new_embeddings).astype("float32"))
        self.text_chunks.extend(
            [
                {"text": text, "risk": risk, "summary": summary}
                for text, risk, summary in zip(new_texts, new_risks, new_summaries)
            ]
        )


rag_model = RAGModel()
