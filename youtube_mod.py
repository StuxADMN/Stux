from pytubefix import YouTube
import re

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
        print(f"Downloaded: {percentage_of_completion:.2f}%")
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
        stream = None
        stream = self.yt.streams.filter(file_extension='mp4', res=quality).first()
        if stream:
            stream.download(output_path="static/content/", filename=filename)
    