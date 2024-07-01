from flask import Flask, request, jsonify
from transformers import RagTokenizer, RagRetriever, RagSequenceForGeneration

app = Flask(__name__)

# RAG 모델 초기화
tokenizer = RagTokenizer.from_pretrained("facebook/rag-sequence-nq")
retriever = RagRetriever.from_pretrained("facebook/rag-sequence-nq")
model = RagSequenceForGeneration.from_pretrained("facebook/rag-sequence-nq")

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    text = data.get('text')
    
    inputs = tokenizer(text, return_tensors="pt")
    generated = model.generate(input_ids=inputs["input_ids"], num_return_sequences=1)
    output = tokenizer.batch_decode(generated, skip_special_tokens=True)

    response = {
        'text': text,
        'risk': 'High' if "high risk" in output[0].lower() else 'Low',
        'explanation': output[0]
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
