from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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
            'skip_download': True,
            'cookiefile': 'cookies.txt'
        }
    
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        formats = []
        used = set()

        for f in info['formats']:
            if f.get('height') and f.get('url'):
                quality = f"{f['height']}p"

                if quality not in used:
                    formats.append({
                        "quality": quality,
                        "url": f['url']
                    })
                    used.add(quality)

        return jsonify({
            "status": True,
            "title": info.get('title'),
            "formats": formats[:6]  # limit for clean UI
        })

    except Exception as e:
        return jsonify({
            "status": False,
            "message": str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
