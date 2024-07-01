import json
from models import rag_model
from config import VECTOR_DB_PATH
import faiss


def load_terms_and_conditions():
    # 이용약관 및 개인정보 동의 내용을 로드하는 함수
    # 실제 구현에서는 파일이나 데이터베이스에서 데이터를 로드해야 합니다
    return [
        "이용약관 1: ...",
        "개인정보 동의 내용 1: ...",
        # 더 많은 텍스트 청크 추가
    ]


if __name__ == "__main__":
    texts = load_terms_and_conditions()
    rag_model.create_index(texts)
    faiss.write_index(rag_model.index, VECTOR_DB_PATH)
    print(f"Vector database initialized and saved to {VECTOR_DB_PATH}")
