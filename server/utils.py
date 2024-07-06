import requests
from config import HF_API_KEY, HF_SUMMARY_MODEL_URL
import logging
from openai import OpenAI
from config import OPENAI_API_KEY
import certifi
import ssl
import json
import httpx


logger = logging.getLogger(__name__)


# SSL 컨텍스트 생성
ssl_context = ssl.create_default_context(cafile=certifi.where())

# httpx 클라이언트 생성
http_client = httpx.Client(verify=ssl_context)

# OpenAI 클라이언트 초기화
client = OpenAI(api_key=OPENAI_API_KEY, http_client=http_client)

# client = OpenAI(api_key=OPENAI_API_KEY)


def analyze_for_customer(query, chunk):
    function_description = {
        "name": "analyze_relevance_and_content",
        "description": "Analyze the relevance of the text chunk to the query and provide a summary if relevant.",
        "parameters": {
            "type": "object",
            "properties": {
                "is_relevant": {
                    "type": "boolean",
                    "description": "Whether the chunk is relevant to the query",
                },
                "analysis": {
                    "type": "string",
                    "description": "Summary of the chunk from a customer's perspective in korean if relevant",
                },
            },
            "required": ["is_relevant", "analysis"],
        },
    }

    prompt = f"""
    As an agent reviewing terms and conditions or contracts from a customer's perspective, analyze the following query and related text chunk. Determine if the chunk is relevant to the query. If relevant, summarize the most crucial information for the customer. If not relevant, mark it as such.

    Query: {query}
    
    Text Chunk: {chunk}

    Provide a boolean indicating relevance and a concise korean summary focusing on key points that are important for the customer if relevant. If unrelated, set is_relevant to false and provide 'UNRELATED' as the analysis.
    """

    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that analyzes terms and conditions for customers.",
            },
            {"role": "user", "content": prompt},
        ],
        functions=[function_description],
        function_call={"name": "analyze_relevance_and_content"},
    )

    function_call = response.choices[0].message.function_call
    if function_call and function_call.name == "analyze_relevance_and_content":
        try:
            result = json.loads(function_call.arguments)
            is_relevant = result["is_relevant"]
            analysis = result["analysis"]

            if not is_relevant:
                return "UNRELATED"
            else:
                return analysis
        except json.JSONDecodeError:
            pass

    return "Invalid response"


def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that summarizes text.",
            },
            {
                "role": "user",
                "content": f"Please summarize the following text in korean within one line:\n\n{text}",
            },
        ],
    )
    return response.choices[0].message.content


def assess_risk(sentence):
    function_description = {
        "name": "get_risk_level",
        "description": "문장의 위험도를 평가하여 'High', 'Medium', 'Low' 중 하나를 반환합니다.",
        "parameters": {
            "type": "object",
            "properties": {
                "risk_level": {
                    "type": "string",
                    "enum": ["High", "Medium", "Low"],
                    "description": "평가된 위험 수준",
                }
            },
            "required": ["risk_level"],
        },
    }

    prompt = f"""
    Please analyze the following terms of service and evaluate the risk level from a consumer's perspective.
    Assign one of the following risk levels to each issue you identify: High, Medium, or Low.
    Then provide an overall risk level for the terms of service.
    다음 문장의 위험도를 평가하고 'High', 'Medium', 'Low' 중 하나만 선택하세요.
    다른 형태의 응답은 허용되지 않습니다.
    
    문장: "{sentence}"
    """

    response = client.chat.completions.create(
        model="gpt-4o-2024-05-13",
        messages=[
            {
                "role": "system",
                "content": "You are an expert in analyzing terms of service agreements. You must only respond using the get_risk_level function.",
            },
            {"role": "user", "content": prompt},
        ],
        functions=[function_description],
        function_call={"name": "get_risk_level"},
    )

    function_call = response.choices[0].message.function_call
    if function_call and function_call.name == "get_risk_level":
        try:
            risk_level = json.loads(function_call.arguments)["risk_level"]
            if risk_level in ["High", "Medium", "Low"]:
                return risk_level
        except json.JSONDecodeError:
            pass

    return "Invalid response"
