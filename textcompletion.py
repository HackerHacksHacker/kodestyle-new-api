import requests
import json
from github import update_file



url = "https://api.cloudflare.com/client/v4/accounts/2e92eb4614a4e9031da13af6d2619fab/ai/run/@cf/google/gemma-7b-it-lora"

def make_readme(repo_name, repo_description, repo_contributors, readme_content, tone, languages):
    payload = {
        "max_tokens": 5000,
        "prompt": f"Please help me make a readme.md file for {repo_name}, description: {repo_description}, contributors: {repo_contributors}, present content of the file: {readme_content}, I want to have in the .md format, the tone of the file must be {tone}, languages: {languages}",
        "raw": False,
        "stream": False
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer CtAkepOQnTdha1SYMUE568yT-dq9srpBUeXuWB9c"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    parsed_data = json.loads(response.text)
    readme_response = parsed_data['result']['response']
    return readme_response


def push_to_github(owner_name, repo_name, file_path, new_content, commit_message, branch, token):
    update_file(owner=owner_name, repo_name=repo_name, file_path=file_path, content=new_content, commit_message=commit_message, branch=branch, token=token)