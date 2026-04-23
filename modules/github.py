# modules/github.py

import requests

def github_tool(username):
    url = f"https://api.github.com/users/{username}/repos"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        return "Error fetching GitHub data"

    repos = response.json()

    repo_list = []

    for repo in repos:
        repo_info = f"""
        Name: {repo['name']}
        Description: {repo['description']}
        Language: {repo['language']}
        URL: {repo['html_url']}
        """
        repo_list.append(repo_info)

    return "\n".join(repo_list)