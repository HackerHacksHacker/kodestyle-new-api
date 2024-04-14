import requests
import base64
from textcompletion import make_readme
from codeanalysis import code_analysis, code_score
from createimage import create_image
from socialmediamanagement import create_social_media_post
from flask import Flask, request, jsonify
from flask_cors import CORS
from codeanalysis import code_score
from github import update_file

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})



new_readme = "" 
owner_name = ""
my_repo_name = ""

@app.route('/readme_creator', methods=['POST'])
def readme_creator():
    data = request.get_json()
    repo_url = data.get('repo_url')
    tone = data.get('tone')
    description = data.get('description')
    my_token = data.get('token')
    owner, repo_name = extract_owner_repo(repo_url)
    repo_info = get_repo_info(owner, repo_name, my_token)
    if repo_info:
        repo_name,  some_value, contributors,readme_content = repo_info
        languages = get_languages(owner=owner, repo_name=repo_name, token=my_token)
        new_readme = make_readme(repo_name=repo_name, readme_content=readme_content, repo_contributors=contributors, repo_description=description, tone=tone, languages = languages)
        print(new_readme)
        return jsonify({'new_readme': new_readme}), 200
    else:
        return jsonify({'error': 'Repo information not found'}), 404

@app.route('/update_readme', methods=['POST'])
def update_readme():
    data = request.get_json()
    repo_url = data.get('repo_url')
    owner, repo_name = extract_owner_repo(repo_url)
    my_token = data.get('token')
    readme = data.get("readme")
    repo_info = get_repo_info(owner, repo_name, my_token)
    if repo_info:
        repo_name,  some_value, contributors,readme_content = repo_info
        my_token = data.get('token')
        update_file(owner=owner, repo_name=repo_name, file_path="README.md", new_content=readme, commit_message="Updated README.md", branch="main", token = my_token)
        return jsonify({'message': 'Readme updated successfully'}), 200

@app.route('/analyse_code', methods=['POST'])
def analyse_the_code():
    data = request.get_json()
    code = data.get('code')
    analysis = code_analysis(token="CtAkepOQnTdha1SYMUE568yT-dq9srpBUeXuWB9c", code=code)
    score = code_score(token="CtAkepOQnTdha1SYMUE568yT-dq9srpBUeXuWB9c",code=code)
    return jsonify({'analysis': analysis, 'code_score': score}), 200


@app.route('/get_social_media_post', methods=['POST'])
def get_social_media_post():
    data = request.get_json()
    repo_url = data.get('repo_url')
    tone = data.get('tone')
    my_token = data.get('token')
    user_description = data.get('description')
    owner, repo_name = extract_owner_repo(repo_url)
    repo_info = get_repo_info(owner, repo_name, my_token)
    if repo_info:
        repo_name, description, contributors, readme_content = repo_info
        link = create_image(prompt=f"{repo_name}")
        post = create_social_media_post(repo_name=repo_name, repo_owner_name=owner, description=description, image_link=link,token="CtAkepOQnTdha1SYMUE568yT-dq9srpBUeXuWB9c", tone=tone, repo_description=description)
        return jsonify({'post': post}), 200
    else:
        return jsonify({'error': 'Repo information not found'}), 404
        

# =========================================================================================================================================


def extract_owner_repo(repo_url):
    parts = repo_url.strip("/").split("/")
    owner = parts[-2]
    repo_name = parts[-1]
    return owner, repo_name

def get_repo_info(owner, repo_name, token=None):
    api_url = f"https://api.github.com/repos/{owner}/{repo_name}"
    headers = {}
    if token:
        headers['Authorization'] = f"token {token}"
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        contributors_url = data.get('contributors_url')
        contributors = get_contributors(contributors_url, headers)
        readme_content = get_readme_content(owner, repo_name, headers)
        return data.get('name'), data.get('description'), contributors, readme_content
    else:
        print("Failed to fetch repository information.")
        return None, None, None, None

def get_contributors(contributors_url, headers):
    response = requests.get(contributors_url, headers=headers)
    if response.status_code == 200:
        contributors_data = response.json()
        contributors = [contributor['login'] for contributor in contributors_data]
        return contributors
    else:
        print("Failed to fetch contributors.")
        return []

def get_readme_content(owner, repo_name, headers):
    readme_url = f"https://api.github.com/repos/{owner}/{repo_name}/readme"
    response = requests.get(readme_url, headers=headers)
    if response.status_code == 200:
        readme_data = response.json()
        readme_content = readme_data.get('content')
        if readme_content:
            decoded_content = base64.b64decode(readme_content).decode('utf-8')
            return decoded_content
        else:
            print("README file is empty.")
            return None
    else:
        print("Failed to fetch README content.")
        return None

def get_languages(owner, repo_name, token=None):
    api_url = f"https://api.github.com/repos/{owner}/{repo_name}/languages"
    headers = {}
    if token:
        headers['Authorization'] = f"token {token}"
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        languages = list(data.keys())
        return languages
    else:
        print("Failed to fetch repository languages.")
        return []



# Example usage


if __name__ == '__main__':
    app.run(debug=True)
