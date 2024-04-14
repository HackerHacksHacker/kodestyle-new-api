import json
import requests

url = "https://api.cloudflare.com/client/v4/accounts/2e92eb4614a4e9031da13af6d2619fab/ai/run/@cf/meta/llama-2-7b-chat-fp16"

def create_social_media_post(repo_name, repo_owner_name, repo_description, description, token, image_link, tone):
    payload = {
        "max_tokens": 999,
        "prompt": f"Please create an amazing post for social media for the repo: {repo_name}, repo owner name as : {repo_owner_name}, repo description as: {repo_description}, normal description as: {description}, also insert this image in between (must): {image_link}, and the tone must be {tone}, the content length must not exceed 260 characters",
        "raw": False,
        "stream": False
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    response = requests.request("POST", url, json=payload, headers=headers)
    parsed_data = json.loads(response.text)
    post = parsed_data['result']['response']
    return post

# Call the function to create the social media post
post = create_social_media_post(repo_name="Whatsapp clone", repo_owner_name="0Armaan025", repo_description="It's a whatsapp clone in Flutter", description="Hey, I want to make a post for my whatsapp upcoming clone in flutter that I'm trying my best to make, it's incomplete yet", token="CtAkepOQnTdha1SYMUE568yT-dq9srpBUeXuWB9c", tone="Informal", image_link="https://dl.kraken.io/api/7e/81/bb/0666c59da206f3ba8e4cdf1bec/image.jpg")

# # Write the post to a file
# with open("new.txt", "w", encoding="utf-8") as file:
#     file.write(post)
