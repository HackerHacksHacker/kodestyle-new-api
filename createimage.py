import requests
from PIL import Image as img
from krakenio import Client
from io import StringIO


url = "https://api.cloudflare.com/client/v4/accounts/2e92eb4614a4e9031da13af6d2619fab/ai/run/@cf/stabilityai/stable-diffusion-xl-base-1.0"

def create_image(prompt):
    payload = {
        "guidance": 7.5,
        
        "num_steps": 20,
        "prompt": prompt,
        "strength": 1
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer CtAkepOQnTdha1SYMUE568yT-dq9srpBUeXuWB9c"
    }

    response = requests.request("POST", url, json=payload, headers=headers)

    with open('image.jpg', 'wb') as f:
    # Write the response content (image data) to the file
            f.write(response.content)
        


    api = Client("6bb5d5e5fc172ee38d4b175aff127fe9", "6306d057d5b6ff4740de708a4f2338ddf4378f10")

    data = {
        "wait": True
    }

    result = api.upload("image.jpg", data);
    print(result.get("kraked_url"))
    return result.get("kraked_url")





    