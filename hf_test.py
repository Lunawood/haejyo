import json
import requests
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()

# API 키와 모델 URL 설정
HF_API_KEY = os.getenv("HF_API_KEY")
SUMMARY_API_URL = (
    "https://api-inference.huggingface.co/models/lcw99/t5-large-korean-text-summary"
)

EMBEDDING_API_URL = "https://api-inference.huggingface.co/models/sentence-transformers/distiluse-base-multilingual-cased-v2"


headers = {"Authorization": f"Bearer {HF_API_KEY}"}


def summarize_text(text):
    payload = {"inputs": text}
    response = requests.post(SUMMARY_API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return "요약 실패"
    try:
        return response.json()[0]["generated_text"]
    except (KeyError, IndexError) as e:
        print(f"Unexpected response format: {response.json()}")
        return "요약 실패"


def get_embeddings(sentences):
    payload = {"inputs": sentences}
    response = requests.post(EMBEDDING_API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None
    return response.json()


def calculate_similarity(source_sentence, sentences):
    all_sentences = [source_sentence] + sentences
    embeddings = get_embeddings(all_sentences)
    if embeddings is None:
        return ["error"] * len(sentences)

    source_embedding = embeddings[0]
    sentence_embeddings = embeddings[1:]

    similarities = []
    for sent_emb in sentence_embeddings:
        similarity = cosine_similarity(source_embedding, sent_emb)
        similarities.append(similarity)

    return similarities


def cosine_similarity(v1, v2):
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude1 = sum(a * a for a in v1) ** 0.5
    magnitude2 = sum(b * b for b in v2) ** 0.5
    if magnitude1 * magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)


# 테스트 텍스트
test_sentences = [
    "회원 탈퇴 후 개인정보는 즉시 파기됩니다. 단, 관련 법령에 따라 일정 기간 보관이 필요한 정보는 해당 기간 동안 보관됩니다.",
    "서비스 이용 중 얻은 정보를 회사의 사전 승낙 없이 복제, 송신, 출판, 배포, 방송 등 기타 방법에 의하여 영리목적으로 이용하거나 제3자에게 이용하게 하여서는 안 됩니다.",
    "회사가 파산하는 경우, 개인정보 처리 방침에 따라 파기하거나 제3자에게 인계될 수 있습니다.",
]

# 요약 테스트
for sentence in test_sentences:
    summary = summarize_text(sentence)
    print(f"원문: {sentence}")
    print(f"요약: {summary}")
    print()

questions = [
    "회원 탈퇴 후 개인정보는 즉시 삭제됩니까?",
    "서비스에서 얻은 정보를 블로그에 공유해도 되나요?",
    "회사 파산 시 내 개인정보는 어떻게 되나요?",
    "오늘 날씨가 좋네요.",
]

for test_sentence in test_sentences:
    print(f"기준 문장: {test_sentence}")
    similarities = calculate_similarity(test_sentence, questions)
    for question, similarity in zip(questions, similarities):
        print(f"질문: {question}")
        print(f"유사도: {similarity}")
    print()
