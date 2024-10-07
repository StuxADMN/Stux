from flask import Flask, redirect, render_template, request, session, Response, send_file
import os
os.chdir(os.path.abspath(os.path.dirname(__name__)))
from stuxbase import database
from youtube_mod import YouTubeDownloader
import threading

global download_instances
download_instances = []

app = Flask(__name__)
app.secret_key = 'supersecretkey&RF/GDVB+Q"789630hnRT*Q()/RNF&W'

@app.route("/")
def feed():
    db = database()
    videos = db.get_videos()
    
    return render_template("feed.html", content=videos)

@app.route("/add-video", methods=["POST", "GET"])
def add_video():
    if request.method == "POST":
        if request.form.get("geturl") == "geturl":
            yt = YouTubeDownloader(request.form.get("url"))
            return render_template("add_video.html", video=yt.get_info(), get_url=False)
    
        def download_thread(url, resolution, filename):
            yt = YouTubeDownloader(url)
            db = database()
            download_instances.append(yt)
            try:
                yt.download(quality=resolution, filename=filename)
                db.add_video(title=yt.title, author=yt.author, length=yt.length, description=yt.desc, video_path=filename)
            except Exception as e: print(e)
            finally: download_instances.remove(yt)

        url_to_download = request.form.get("url")
        resolution_to_download = f"{request.form.get("resolution")}p"
        filename = request.form.get("title") + ".mp4"
        threading.Thread(target=download_thread, args=(url_to_download, resolution_to_download, filename)).start()

        return redirect("/downloads")
    
    return render_template("add_video.html", get_url=True)

@app.route("/delete-video/<id>")
def delete_video(id):
    db = database()
    video = db.get_video(id)
    db.remove_video(id)
    os.remove(f"static/content/{video["path"]}")
    return redirect("/settings")

@app.route("/search/<term>")
def search(term):
    videos = db.get_search(term)
    return redirect("/")

@app.route("/downloads", methods=["GET"])
def downloads():
    downloads_infos = []
    for download in download_instances:
        downloads_infos.append(
            {
                "title": download.title,
                "author": download.author,
                "progress": round(download.progress),
                "url": download.url
            }
        )
    return render_template("downloading.html", downloads=downloads_infos)

@app.route("/watch/<id>")
def watch(id):
    db = database()
    video = db.get_video(id)
    
    return render_template("watch.html", video=video)

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

@app.route("/settings", methods=["POST", "GET"])
def settings():
    db=database()
    videos = db.get_videos()
    
    
    return render_template("settings.html", videos=videos)

if __name__=="__main__":
    db = database()
    db.init_db()
    app.run(host="0.0.0.0", port=80, debug=True)
