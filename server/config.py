from dotenv import load_dotenv
import os

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
HF_SUMMARY_MODEL_URL = os.getenv("HF_SUMMARY_MODEL_URL")
HF_EMBEDDING_MODEL = os.getenv("HF_EMBEDDING_MODEL")

DEBUG = os.getenv("DEBUG") == "True"
SSL_CERT_FILE = os.getenv("SSL_CERT_FILE")
SSL_KEY_FILE = os.getenv("SSL_KEY_FILE")

VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH")

LOG_LEVEL = os.getenv("LOG_LEVEL")
