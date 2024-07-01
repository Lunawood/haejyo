import requests
from config import HF_API_KEY, HF_SUMMARY_MODEL_URL


def summarize_text(text):
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    payload = {
        "inputs": text,
        "parameters": {"max_length": 150, "min_length": 50, "do_sample": False},
    }
    response = requests.post(HF_SUMMARY_MODEL_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()[0]["summary_text"]


def assess_risk(text):
    return (
        "High"
        if any(
            keyword in text.lower() for keyword in ["share", "third party", "collect"]
        )
        else "Low"
    )
