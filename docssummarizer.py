import requests
from bs4 import BeautifulSoup

def scrape_text_only(link, prompt, token):
    try:
        # Send a GET request to the provided link
        response = requests.get(link)
        response.raise_for_status()  # Raise an exception for HTTP errors
        # Parse HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract all text content
        text_content = soup.get_text()
        # Truncate the text content if it exceeds the limit
        text_content = text_content[:6044]
        print(text_content)
        get_docs(prompt=prompt, token=token, text_content=text_content)
        
    except requests.RequestException as e:
        print(f"Error occurred during HTTP request: {str(e)}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

url = "https://api.cloudflare.com/client/v4/accounts/2e92eb4614a4e9031da13af6d2619fab/ai/run/@cf/openchat/openchat-3.5-0106"

def get_docs(prompt, token, text_content):
    try:
        payload = {
            "max_tokens": 9000,
            "prompt": f"How to {prompt}, docs reference: {text_content}",
            "raw": False,
            "stream": False
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}"
        }

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors

        parsed_data = response.json()
        print(parsed_data)
        docs_answer = parsed_data['result']['response']
        print(docs_answer)
        return docs_answer
    except requests.RequestException as e:
        print(f"Error occurred during HTTP request: {str(e)}")
    except Exception as e:
        print(f"Error occurred: {str(e)}")

scrape_text_only(link="https://www.twilio.com/docs/conversations/api/conversation-resource", prompt="create a conservation resource", token="CtAkepOQnTdha1SYMUE568yT-dq9srpBUeXuWB9c")
