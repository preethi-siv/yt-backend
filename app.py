from flask import Flask, request, jsonify
import yt_dlp

app = Flask(__name__)

@app.route('/get-video', methods=['POST'])
def get_video():
    url = request.form.get('url')

    if not url:
        return jsonify({"status": False, "message": "URL missing"})

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'no_warnings': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

            formats = []

            for f in info['formats']:
                if (
                    f.get('ext') == 'mp4' and
                    f.get('height') and
                    f.get('acodec') != 'none' and
                    f.get('vcodec') != 'none'
                ):
                    formats.append({
                        "quality": f"{f.get('height')}p",
                        "url": f.get('url')
                    })

            return jsonify({
                "status": True,
                "title": info.get('title'),
                "formats": formats[:5]
            })

    except Exception as e:
        return jsonify({
            "status": False,
            "message": str(e)
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)