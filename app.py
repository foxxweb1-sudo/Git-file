from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_repo_info(owner, repo):
    url = f'https://api.github.com/repos/{owner}/{repo}'
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    repo_url = ''
    branch = 'main'
    repo_info = None
    error = ''
    owner = ''
    repo = ''
    zip_url = ''
    if request.method == 'POST':
        repo_url = request.form['repo_url'].strip()
        branch = request.form.get('branch', 'main').strip()
        parts = repo_url.rstrip('/').split('/')
        if len(parts) >= 5:
            owner = parts[-2]
            repo = parts[-1]
            repo_info = get_repo_info(owner, repo)
            if repo_info:
                zip_url = f"https://github.com/{owner}/{repo}/archive/refs/heads/{branch}.zip"
            else:
                error = "لم يتم العثور على المستودع. تأكد من صحة الرابط."
        else:
            error = "يرجى إدخال رابط صحيح لشكل: https://github.com/owner/repo"
    return render_template('index.html', repo_url=repo_url, branch=branch, repo_info=repo_info, error=error, zip_url=zip_url)

if __name__ == '__main__':
    app.run(debug=True)