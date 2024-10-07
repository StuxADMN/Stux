from moviepy.editor import VideoFileClip, AudioFileClip
from pytubefix import YouTube
import subprocess
import re
import os

def clean_title_for_filename(title):
    cleaned_filename = re.sub(r'[^A-Za-z0-9_() ]', '', title)
    cleaned_name = re.sub(r'_+', '_', cleaned_filename.replace(" ", "_"))
    return cleaned_name.strip('_')
    
class YouTubeDownloader:
    def __init__(self, url):
        self.url = url
        self.yt = YouTube(url, on_progress_callback=self.progress_callback)
        self.progress = 0
        self.length = self.yt.length
        self.title = self.yt.title
        self.author = self.yt.author
        self.desc = self.yt.description
    
    def progress_callback(self, stream, chunk, bytes_remaining):
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        self.progress = percentage_of_completion
    
    def get_info(self,):
        ys = self.yt.streams
        resolutions = []
        for stream in ys:
            try:
                res = stream.resolution
                if "p" in res:
                    res = res.replace("p", "")
                    if int(res) not in resolutions:
                        resolutions.append(int(res))
            except Exception: pass
            
        return {
            "filename": clean_title_for_filename(self.yt.title),
            "title": self.yt.title,
            "author": self.yt.author,
            "desc": self.yt.description,
            "length": self.yt.length,
            "resolutions": sorted(resolutions, reverse=True),
            "url": self.url
        }

    def download(self, filename, quality='1080p'): 
        video_output_path = f"static/content/{filename}"
        video_stream = None
        audio_stream = None
        video_stream = self.yt.streams.filter(file_extension='mp4', res=quality).first()
        audio_stream = self.yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        if video_stream and audio_stream:
            video_file = video_stream.download(output_path="static/cache/", filename=filename)
            audio_file = audio_stream.download(output_path="static/cache/", filename=f"{filename}.mp3")
            command = [
                'ffmpeg', '-i', video_file, '-i', audio_file, 
                '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', video_output_path
            ]
            subprocess.run(command)
            os.file.remove(f"static/cache/{filename}")
            os.file.remove(f"static/cache/{filename}.mp3")
