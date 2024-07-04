from flask import Flask, request, jsonify
from flask_cors import CORS
import ssl
import traceback
import logging
from config import DEBUG, SSL_CERT_FILE, SSL_KEY_FILE, LOG_LEVEL, VECTOR_DB_PATH
from models import rag_model
from utils import summarize_text, assess_risk
import os
import faiss, json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

SSL_CERT_FILE = os.getenv("SSL_CERT_FILE")
SSL_KEY_FILE = os.getenv("SSL_KEY_FILE")
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
logging.basicConfig(level=getattr(logging, LOG_LEVEL), format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_vector_database():
    try:
        rag_model.index = faiss.read_index(VECTOR_DB_PATH)
        with open(VECTOR_DB_PATH + "_chunks.json", "r") as f:
            rag_model.text_chunks = json.load(f)
        logger.info(f"Vector database loaded from {VECTOR_DB_PATH}")
    except Exception as e:
        logger.error(f"Failed to load vector database: {str(e)}")
        raise

@app.route("/", methods=["GET"])
def home():
    return "AgreeSum"

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        text = data.get("text")
        logger.info(f"Received text: {text}")
        print(f"Received text: {text}")  # 테스트를 위해 텍스트 출력
        if rag_model.index is None:
            raise ValueError("Vector database not initialized")

        relevant_chunks = rag_model.search(text)
        relevant_text = " ".join(relevant_chunks)

        summary = summarize_text(relevant_text)
        logger.info(f"Generated summary: {summary}")

        risk = assess_risk(summary)
        logger.info(f"Risk assessment: {risk}")

        response_data = {"text": text, "summary": summary, "risk": risk}
        return jsonify(response_data)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "An unexpected error occurred"}), 500

if __name__ == "__main__":
    try:
        load_vector_database()  # 서버 시작 시 벡터 데이터베이스 로드
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")

        app.run(debug=DEBUG, ssl_context=ssl_context)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        logger.error(traceback.format_exc())
