import json
import requests
from dotenv import load_dotenv
import os

load_dotenv()

HF_API_KEY = os.getenv("HF_API_KEY")
print(HF_API_KEY)
headers = {"Authorization": f"Bearer {HF_API_KEY}"}
API_URL = (
    "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
)


def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", API_URL, headers=headers, data=data)
    return json.loads(response.content.decode("utf-8"))


data = query(
    {
        "inputs": {
            "source_sentence": "That is a happy person",
            "sentences": [
                "That is a happy dog",
                "That is a very happy person",
                "Today is a sunny day",
            ],
        }
    }
)

print(data)
"""
* 출력 결과
[0.6945773363113403, 0.9429150223731995, 0.256876140832901]
"""
