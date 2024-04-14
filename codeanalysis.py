import json
import re
import requests

url = "https://api.cloudflare.com/client/v4/accounts/2e92eb4614a4e9031da13af6d2619fab/ai/run/@cf/google/gemma-7b-it-lora"

def code_analysis(token, code):
    payload = {
        "max_tokens": 999,
        "prompt": f"Analyse this code: {code}",
        "raw": False,
        "stream": False
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    answer = response_data['result']['response']
    return answer

def code_score(token, code):
    payload = {
        "max_tokens": 999,
        "prompt": f"Give this code a score from 1 to 10, please give a score, a score is must to be given for coding practices, only 1 word is required which is score: score/10, and no other word should be replied, the code is: {code}",
        "raw": False,
        "stream": False
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    score = response_data['result']['response']
    # Extract score using regular expression
    match = re.search(r"\b(\d+)\b(?=\s*/10)", score)
    if match:
        return int(match.group(1))
    else:
        return None
