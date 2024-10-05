from flask import Flask, redirect, render_template, request, session, Response, send_file
import os
os.chdir(os.path.abspath(os.path.dirname(__name__)))
from stuxbase import database
from youtube_mod import YouTubeDownloader

app = Flask(__name__)
app.secret_key = 'supersecretkey&RF/GDVB+Q"789630hnRT*Q()/RNF&W'

@app.route("/debug/<html>")
def debug(html):
    return render_template(html)

@app.route("/")
def feed():
    videos = db.get_videos()
    
    return render_template("feed.html", content=videos)

@app.route("/add-video", methods=["POST", "GET"])
def add_video():
    if request.method == "POST":
        url = request.form.get("url")
    
    return render_template("upload_video.html")


@app.route("/search/<term>")
def search(term):
    videos = db.get_search(term)

@app.route("/watch/<id>")
def watch(id):
    db = database()
    #video = db.get_video(id)
    video = " "
    return render_template("watch.html", video=video, filename="wohnmobil.mp4")

def get_video_range(file_path, start, length):
    with open(file_path, 'rb') as video:
        video.seek(start)
        data = video.read(length)
        return data

@app.route('/stream-video/<videofile>')
def video_stream(videofile):
    video_path = f'static/content/{videofile}'
    file_size = os.stat(video_path).st_size
    range_header = request.headers.get('Range', None)
    
    if range_header:
        byte_range = range_header.strip().split('=')[-1]
        byte_start, byte_end = byte_range.split('-')
        byte_start = int(byte_start)
        byte_end = int(byte_end) if byte_end else file_size - 1
        length = byte_end - byte_start + 1

        video_data = get_video_range(video_path, byte_start, length)

        response = Response(video_data, 206, mimetype='video/mp4', content_type='video/mp4')
        response.headers.add('Content-Range', f'bytes {byte_start}-{byte_end}/{file_size}')
        response.headers.add('Accept-Ranges', 'bytes')
    else:
        response = send_file(video_path, mimetype='video/mp4')
    
    return response

if __name__=="__main__":
    db = database()
    db.init_db()

    app.run(host="0.0.0.0", port=80, debug=True)
