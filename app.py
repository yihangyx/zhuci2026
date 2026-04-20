from flask import Flask, request, jsonify, render_template
import requests
import re

app = Flask(__name__)

API_LIST = [
    "https://apis.jxcxin.cn/api/douyin",
    "https://api.lvxiaodong.com/api/dypro"
]

def extract_douyin_url(text):
    pattern = r'https?://v\.douyin\.com/[a-zA-Z0-9_-]+'
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    pattern2 = r'https?://www\.douyin\.com/[a-zA-Z0-9_-]+'
    match2 = re.search(pattern2, text)
    if match2:
        return match2.group(0)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/parse', methods=['POST'])
def parse_video():
    data = request.get_json()
    input_text = data.get('url', '').strip()

    if not input_text:
        return jsonify({"success": False, "error": "请输入内容！"}), 400

    url = extract_douyin_url(input_text)
    if not url:
        return jsonify({"success": False, "error": "未在文本中找到抖音链接！"}), 400

    for api_index, api_url in enumerate(API_LIST):
        try:
            response = requests.get(api_url, params={"url": url}, timeout=15)
            result_data = response.json()

            if api_index == 0:
                if result_data.get("code") == 200:
                    item = result_data["data"]
                    video_url = item.get("url", "")

                    return jsonify({
                        "success": True,
                        "title": item.get('title', '无'),
                        "author": item.get('author', '无'),
                        "like": item.get('like', '无'),
                        "time": item.get('time', '无'),
                        "video_url": video_url,
                        "cover": item.get("cover", ""),
                        "music": item.get("music", {}).get("url", "") if item.get("music") else ""
                    })
            elif api_index == 1:
                if result_data.get("code") == 0:
                    item = result_data["data"]["item"]
                    video_url = item.get("url", "")

                    return jsonify({
                        "success": True,
                        "title": item.get('title', '无'),
                        "author": item.get('author', '无'),
                        "video_url": video_url,
                        "cover": item.get("cover", ""),
                        "music": item.get("music", "")
                    })

        except Exception as e:
            continue

    return jsonify({"success": False, "error": "解析失败，请检查链接是否有效"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)