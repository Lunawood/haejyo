from flask import Flask, request, jsonify
from flask_cors import CORS
import ssl
import traceback
import logging
from config import DEBUG, SSL_CERT_FILE, SSL_KEY_FILE, LOG_LEVEL, VECTOR_DB_PATH
from models import rag_model
from utils import summarize_text, assess_risk, analyze_for_customer
import faiss, json, os
from initialize_db import load_terms_and_conditions


app = Flask(__name__)
CORS(app)

logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger(__name__)

# 애플리케이션 로거 설정

# logger.setLevel(logging.WARNING)  # DEBUG와 INFO 로그는 표시되지 않음

# 또는 완전히 비활성화
# logger.disabled = True


def update_database(new_texts, new_risks, new_summaries):
    # 새 텍스트 추가
    if len(new_risks) != 0:
        rag_model.add_texts(new_texts, new_risks, new_summaries)

    # 업데이트된 인덱스 저장
    faiss.write_index(rag_model.index, VECTOR_DB_PATH)

    # 업데이트된 text_chunks 저장
    with open(VECTOR_DB_PATH + "_chunks.json", "w") as f:
        json.dump(rag_model.text_chunks, f)

    print(f"Vector database updated and saved to {VECTOR_DB_PATH}\n\n")


MAX_INPUT_LENGTH = 512  # 모델이 지원하는 최대 길이로 설정

@app.route("/", methods=["GET"])
def home():
    return "AgreeSum Server"

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        query = data.get("text")
        logger.info(f"Received text: {query}")
        if rag_model.index is None:
            raise ValueError("Vector database not initialized")

        relevant_chunks = rag_model.search(query)
        # print("relevant chunks: ", relevant_chunks)
        relevant_summaries = []
        for chunk in relevant_chunks:
            # customer_analysis = analyze_for_customer(query, chunk["text"])

            # if customer_analysis != "UNRELATED":
            relevant_summaries.append(
                {
                    "query": query,
                    "summary": chunk["summary"],
                    "risk": chunk["risk"],
                    # "customer_analysis": customer_analysis,
                }
            )

        logger.info(f"Generated summaries and risks: {relevant_summaries}")

        return jsonify(relevant_summaries)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "An unexpected error occurred"}), 500


if __name__ == "__main__":
    try:
        # 초기 데이터베이스 생성 (이미 있다면 로드)
        if os.path.exists(VECTOR_DB_PATH):
            rag_model.index = faiss.read_index(VECTOR_DB_PATH)
            with open(VECTOR_DB_PATH + "_chunks.json", "r") as f:
                rag_model.text_chunks = json.load(f)
        else:
            initial_texts = load_terms_and_conditions()
            initial_risks = [
                assess_risk(text) for text in initial_texts
            ]  # Assess initial risks
            initial_summaries = [summarize_text(text) for text in initial_texts]

            rag_model.create_index(initial_texts, initial_risks, initial_summaries)
            update_database([], [], [])  # 초기 저장
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile=SSL_CERT_FILE, keyfile=SSL_KEY_FILE)

        app.run(debug=DEBUG, ssl_context=ssl_context)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        logger.error(traceback.format_exc())
