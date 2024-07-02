from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from dotenv import load_dotenv

app = Flask(__name__)
CORS(app)

# 환경 변수 로드
load_dotenv()

# 모델 api 로드
API_URL = "https://api-inference.huggingface.co/models/google/pegasus-xsum"
API_KEY = os.getenv("HUGGINGFACE_API_KEY")
headers = {"Authorization": f"Bearer {API_KEY}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text')

    # 입력 텍스트 요약
    response = query({"inputs": text})
    summary = response[0]['summary_text']

    # 텍스트에서 위험을 판단하는 간단한 로직 (예시)
    risk = 'High' if 'share' in text.lower() or 'third party' in text.lower() else 'Low'

    response_data = {
        'text': text,
        'summary': summary,
        'risk': risk
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(ssl_context=('server.crt', 'server.key'), debug=True)
