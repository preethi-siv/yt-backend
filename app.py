from flask import Flask, request, jsonify
from flask_cors import CORS
from pytube import YouTube

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

        yt = YouTube(url)

        streams = yt.streams.filter(file_extension='mp4').order_by('resolution').desc()

        formats = []
        used = set()

        for stream in streams:
            if stream.resolution and stream.resolution not in used:
                formats.append({
                    "quality": stream.resolution,
                    "url": stream.url
                })
                used.add(stream.resolution)

        return jsonify({
            "status": True,
            "title": yt.title,
            "formats": formats
        })

    except Exception as e:
        return jsonify({
            "status": False,
            "message": str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
