import sqlite3

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
                video_path TEXT NOT NULL,
                author TEXT NOT NULL,
                length INTEGER NOT NULL
            );
        ''')
        self.connection.commit()

    def add_video(self, title, description, video_path, author, length):
        insert_query = '''
        INSERT INTO videos (title, description, video_path, author, length)
        VALUES (?, ?, ?, ?, ?);
        '''
        self.cursor.execute(insert_query, (title, description, video_path, author, length))
        self.connection.commit()

    def remove_video(self, id):
        delete_query = '''
            DELETE FROM videos WHERE id = ?;
        '''
        self.cursor.execute(delete_query, (id,)) 
        self.connection.commit()

    def get_videos(self,):
        videos_info = []
        select_query = '''
            SELECT * FROM videos
        '''
        self.cursor.execute(select_query)
        videos = self.cursor.fetchall()
        for video in videos:
            videos_info.append(
                {
                    "id": video[0],
                    "title": video[1],
                    "desc": video[2],
                    "path": video[3],
                    "author": video[4],
                    "length": f"{video[5] // 60:02}:{video[5] % 60:02}",
                }
            )
        
        
        return videos_info

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
        video = self.cursor.fetchall()[0]
        video_info = {
            "id": video[0],
            "title": video[1],
            "desc": video[2],
            "path": video[3],
            "author": video[4],
            "length": f"{video[5] // 60:02}:{video[5] % 60:02}",
        }
        
        return video_info
