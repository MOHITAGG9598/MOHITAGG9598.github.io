from flask import Flask, render_template
import requests
import os
import glob
import chardet
import re
from github import Github
import openai

app = Flask(__name__)
openai.api_key = "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"  # Replace with your OpenAI API key

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process/<username>')
def process(username):
    repositories = fetch_repositories(username)
    if repositories:
        most_complex_repository = identify_most_technically_complex(repositories)
        return render_template('result.html', repository=most_complex_repository)
    else:
        error_message = f"Failed to fetch repositories for user {username}"
        return render_template('error.html', error=error_message)

def fetch_repositories(username):
    g = Github()
    user = g.get_user(username)
    repositories = []

    for repo in user.get_repos():
        repositories.append({"name": repo.name, "description": repo.description})

    return repositories

def identify_most_technically_complex(repositories):
    prompt = f"""
    Among the following repositories, please identify the most technically complex one and provide a justification:

    Repositories:
    {repositories}

    Most Technically Complex Repository:
    """

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.5
    )

    most_complex_repository = response.choices[0].text.strip()
    return most_complex_repository
if __name__ == '__main__':
    app.run()
