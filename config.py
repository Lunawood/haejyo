import os

HF_API_KEY = "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"
HF_SUMMARY_MODEL_URL = (
    "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
)
HF_EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# 서버 설정
DEBUG = True
SSL_CERT_FILE = "server.crt"
SSL_KEY_FILE = "server.key"

# 벡터 데이터베이스 설정
VECTOR_DB_PATH = "vector_database.faiss"

# 로깅 설정
LOG_LEVEL = "DEBUG"
