from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# إعدادات GitHub API
GITHUB_API_URL = "https://api.github.com/repos"

@app.route('/')
def index():
    # عرض الصفحة الرئيسية
    return render_template('index.html')

@app.route('/fetch-repo', methods=['POST'])
def fetch_repo():
    data = request.json
    repo_url = data.get('url', '').strip()
    
    if not repo_url:
        return jsonify({"error": "الرجاء إدخال رابط صحيح"}), 400

    try:
        # تحليل الرابط لاستخراج المالك واسم المستودع
        # مثال: https://github.com/owner/repo
        parts = repo_url.rstrip('/').split('/')
        if 'github.com' not in parts or len(parts) < 5:
            return jsonify({"error": "تنسيق رابط GitHub غير صحيح"}), 400
        
        owner = parts[-2]
        repo = parts[-1]
        path = data.get('path', '')

        # طلب البيانات من GitHub API
        api_url = f"{GITHUB_API_URL}/{owner}/{repo}/contents/{path}"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            return jsonify(response.json())
        elif response.status_code == 404:
            return jsonify({"error": "المستودع أو الملف غير موجود"}), 404
        else:
            return jsonify({"error": "حدث خطأ أثناء جلب البيانات من GitHub"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # تشغيل التطبيق في الوضع التجريبي
    app.run(debug=True)

