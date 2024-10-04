from flask import Flask, redirect, render_template
import sqlite3

class database():
    def __init__(self) -> None:
        self.connection = sqlite3.connect('videos.db')
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
                upload_date TEXT DEFAULT CURRENT_TIMESTAMP,
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
        self.cursor.execute(delete_query, id) 
        self.connection.commit()





app = Flask(__name__)


def main():
    db = database()
    db.init_db()
    
    
    app.run(host="0.0.0.0", port=80)


if __name__=="__main__".
    main()

