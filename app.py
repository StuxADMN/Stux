from flask import Flask, redirect, render_template, request, session
import os
os.chdir(os.path.abspath(os.path.dirname(__name__)))
from stuxbase import database

app = Flask(__name__)


@app.route("/debug/<html>")
def debug(html):
    return render_template(html)


@app.route("/")
def feed():
    videos = db.get_videos()
    
    return render_template("feed.html", content=videos)

@app.route("/search/<term>")
def search(term):
    videos = db.get_search(term)

@app.route("/watch/<id>")
def watch(id):
    video = db.get_video(id)
        
    return render_template("watch", video=video)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        print(request.form)

    return render_template("login.html")

@app.route("/logout")
def logout():
    if "user_id" in session:
        session.pop()



if __name__=="__main__":
    db = database()
    db.init_db()
    
    
    app.run(host="0.0.0.0", port=80, debug=True)
