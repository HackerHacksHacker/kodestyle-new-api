import base64
import requests
def update_file(owner, repo_name, file_path, new_content, commit_message, branch, token):
    api_url = f"https://api.github.com/repos/{owner}/{repo_name}/contents/{file_path}"
    headers = {
        'Authorization': f"bearer {token}",
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.get(api_url, headers=headers)
    print('checking new', new_content)
    if response.status_code == 200:
        current_content = response.json()['content']
        new_content_base64 = base64.b64encode(new_content.encode()).decode()
        payload = {
            'message': commit_message,
            'content': new_content_base64,
            'branch': branch,
            'sha': response.json()['sha']
        }
        update_response = requests.put(api_url, json=payload, headers=headers)
        if update_response.status_code == 200:
            print("File updated successfully.")
        else:
            print("Failed to update file:", update_response.text)
    else:
        print("Failed to fetch file:", response.text)