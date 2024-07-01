from flask import Flask, request, jsonify
from flask_cors import CORS
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

app = Flask(__name__)
CORS(app)

# 모델 및 토크나이저 로드
tokenizer = AutoTokenizer.from_pretrained("google/pegasus-multi_news")
model = AutoModelForSeq2SeqLM.from_pretrained("google/pegasus-multi_news")

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text')

    # 입력 텍스트를 토큰화하고 모델에 입력
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding="longest")
    summary_ids = model.generate(inputs["input_ids"], max_length=60, num_beams=4, length_penalty=2.0, early_stopping=True)
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    # 텍스트에서 위험을 판단하는 간단한 로직 (예시)
    risk = 'High' if 'share' in text.lower() or 'third party' in text.lower() else 'Low'

    response_data = {
        'text': text,
        'summary': summary,
        'risk': risk
    }

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True)
