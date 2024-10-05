from flask import Flask, redirect, render_template, request, session
import sqlite3

# database class, will maybe turn into a module
class database():
    def __init__(self) -> None:
        self.connection = sqlite3.connect('database.db')
        self.cursor = self.connection.cursor()
    
    def init_db(self,):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                thumbnail_path TEXT,
                video_path TEXT NOT NULL,
                author TEXT NOT NULL,
                length INTEGER NOT NULL,
                upload_date TEXT DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
            );
        ''')
        self.connection.commit()

    def add_video(self, title, description, thumbnail_path, video_path, author, length):
        insert_query = '''
        INSERT INTO videos (title, description, thumbnail_path, video_path, author, length)
        VALUES (?, ?, ?, ?, ?, ?);
        '''
        self.cursor.execute(insert_query, (title, description, thumbnail_path, video_path, author, length))
        self.connection.commit()

    def remove_video(self, id):
        delete_query = '''
            DELETE FROM videos WHERE id = ?;
        '''
        self.cursor.execute(delete_query, (id,)) 
        self.connection.commit()

    def get_videos(self,):
        select_query = '''
            SELECT * FROM videos
        '''
        self.cursor.execute(select_query)
        return self.cursor.fetchall()

    def get_search(self, term):
        select_query = '''
            SELECT * FROM videos
        '''
        self.cursor.execute(select_query)
        videos = self.cursor.fetchall()
        videos_to_show = []
        for video in videos:
            if term in video:
                videos_to_show.append(video) 
    
    def get_video(self, id):
        select_query = '''
            SELECT * FROM videos WHERE id = ?;
        '''
        self.cursor.execute(select_query, (id,))
        return self.cursor.fetchall()[0]

    def insert_user(self, username, firstname, lastname):
        insert_query = '''
            INSERT INTO users (name, firstname, lastname) VALUES (?, ?, ?)
        '''
        self.cursor.execute(insert_query, (username, firstname, lastname))
        self.connection.commit()
        
    def delete_user(self, id):
        delete_query = '''
            DELETE FROM users WHERE id = ?;
        '''
        
    
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


@app.route("/login", methos=["POST", "GET"])
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
