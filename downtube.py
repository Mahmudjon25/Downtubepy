from flask import Flask, render_template, request, send_file
import os
from yt_dlp import YoutubeDL

app = Flask(__name__)

DOWNLOAD_FOLDER = "downloads"
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return """
    <!DOCTYPE html>
    <html lang="tg">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Боргирии YouTube</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 0;
                background: linear-gradient(120deg, #84fab0, #8fd3f4);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                color: #333;
            }
            .container {
                background: white;
                padding: 30px;
                border-radius: 10px;
                box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
                width: 400px;
                text-align: center;
            }
            h1 {
                color: #007bff;
                font-size: 24px;
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin: 10px 0 5px;
                text-align: left;
            }
            input, select, button {
                width: 100%;
                padding: 10px;
                margin: 5px 0 15px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
            }
            button {
                background: #007bff;
                color: white;
                border: none;
                cursor: pointer;
            }
            button:hover {
                background: #0056b3;
            }
            footer {
                margin-top: 20px;
                font-size: 14px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Боргирии Видео ва MP3 аз YouTube</h1>
            <form action="/download" method="post">
                <label for="url">Суроғаи YouTube-ро ворид кунед:</label>
                <input type="text" id="url" name="url" placeholder="https://www.youtube.com/watch?v=..." required>

                <label for="format">Форматро интихоб кунед:</label>
                <select id="format" name="format" required>
                    <option value="video">Видео</option>
                    <option value="audio">MP3</option>
                </select>

                <label for="quality">Сифатро интихоб кунед:</label>
                <select id="quality" name="quality" required>
                    <option value="best">Беҳтарин</option>
                    <option value="high">Баланд</option>
                    <option value="medium">Миёна</option>
                    <option value="low">Паст</option>  
</select>

    <button type="submit">Боргирӣ</button>
            </form>
            <footer>
                &copy; 2024, Боргирии Видео. Ҳама ҳуқуқҳо ҳифз шудаанд.
            </footer>
        </div>
    </body>
    </html>
    """

@app.route('/download', methods=['POST'])
def download():
    url = request.form['url']
    format_type = request.form['format']
    quality = request.form['quality']
    ydl_opts = {}

    quality_map = {
        "best": "best",
        "high": "bestvideo[height<=1080]+bestaudio/best",
        "medium": "bestvideo[height<=720]+bestaudio/best",
        "low": "bestvideo[height<=480]+bestaudio/best"
    }

    if format_type == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        }
    elif format_type == 'video':
        ydl_opts = {
            'format': quality_map.get(quality, "best"),
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
        }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)
            if format_type == 'audio':
                file_name = os.path.splitext(file_name)[0] + '.mp3'

        return send_file(file_name, as_attachment=True)
    except Exception as e:
        return f"Хато рӯй дод: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)