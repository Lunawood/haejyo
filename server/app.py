# flask

from flask import Flask, request, jsonify
from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration

app = Flask(__name__)

# Hugging Face API 키 설정
HF_API_KEY = "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"
HF_MODEL_URL = "https://api-inference.huggingface.co/models/google/pegasus-xsum"

headers = {"Authorization": f"Bearer {HF_API_KEY}"}


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    text = data.get("text")

    response = requests.post(HF_MODEL_URL, headers=headers, json={"inputs": text})
    summary = response.json()[0]["summary_text"]

    # 분석 결과 생성 (예시: 위험도 평가)
    risk = "High" if "share" in text.lower() or "third party" in text.lower() else "Low"

    response_data = {"text": text, "summary": summary, "risk": risk}

    return jsonify(response_data)


if __name__ == "__main__":
    app.run(debug=True)
