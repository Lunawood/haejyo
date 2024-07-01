from flask import Flask, request, jsonify
import requests
import ssl
import traceback
import logging
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# 로깅 설정
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Hugging Face API 키 설정
HF_API_KEY = "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"
HF_MODEL_URL = "https://api-inference.huggingface.co/models/google/pegasus-xsum"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.json
        text = data.get("text")
        logger.info(f"Received text: {text}")

        response = requests.post(HF_MODEL_URL, headers=headers, json={"inputs": text})
        response.raise_for_status()  # HTTP 오류 발생 시 예외를 발생시킵니다.

        summary = response.json()[0]["summary_text"]
        logger.info(f"Generated summary: {summary}")

        # 분석 결과 생성 (예시: 위험도 평가)
        risk = (
            "High"
            if "share" in text.lower() or "third party" in text.lower()
            else "Low"
        )
        logger.info(f"Risk assessment: {risk}")

        response_data = {"text": text, "summary": summary, "risk": risk}
        return jsonify(response_data)

    except requests.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        return jsonify({"error": "Failed to communicate with Hugging Face API"}), 500

    except KeyError as e:
        logger.error(f"Failed to parse API response: {str(e)}")
        return jsonify({"error": "Failed to parse API response"}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        logger.error(traceback.format_exc())
        return jsonify({"error": "An unexpected error occurred"}), 500


if __name__ == "__main__":
    try:
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")

        app.run(debug=True, ssl_context=ssl_context)
    except Exception as e:
        logger.error(f"Failed to start server: {str(e)}")
        logger.error(traceback.format_exc())
