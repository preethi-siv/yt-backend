from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "Backend is running"

@app.route('/get-video', methods=['POST'])
def get_video():
    try:
        data = request.get_json()
        url = data.get('url')

        if not url:
            return jsonify({"status": False, "message": "No URL provided"})

        ydl_opts = {
            'quiet': True,
            'skip_download': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        video_url = None

        # Find only 360p
        for f in info['formats']:
            if f.get('height') == 360 and f.get('url'):
                video_url = f['url']
                break

        if not video_url:
            return jsonify({
                "status": False,
                "message": "360p not available"
            })

        return jsonify({
            "status": True,
            "title": info.get('title'),
            "url": video_url
        })

    except Exception as e:
        return jsonify({
            "status": False,
            "message": str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
