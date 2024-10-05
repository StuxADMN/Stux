import sqlite3
import bcrypt

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(stored_hash: str, password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8'))

# database class for module
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
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                name TEXT NOT NULL UNIQUE,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                password TEXT NOT NULL
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

    def insert_user(self, username, firstname, lastname, password):
        insert_query = '''
            INSERT INTO users (name, firstname, lastname, password) VALUES (?, ?, ?, ?);
        '''
        password_hash = hash_password(password)
        self.cursor.execute(insert_query, (username, firstname, lastname, password_hash))
        self.connection.commit()
        
    def delete_user(self, id):
        delete_query = '''
            DELETE FROM users WHERE id = ?;
        '''
        self.cursor.execute(delete_query, (id,))
        self.connection.commit()
    
    def check_user_password(self, username, password):
        select_query = '''
            SELECT * FROM users WHERE username = ?;
        '''
        self.cursor.execute(select_query, (username,))
        user = self.cursor.fetchall()
        password_hash = user[4]
        if check_password(password_hash, password):
            return {
                "id": user[0],
                "name": user[1],
                "firstname": user[2],
                "lastname": user[3]                
            }
        return False

        
        
