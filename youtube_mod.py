from pytubefix import YouTube
from pytubefix.cli import on_progress

class YouTubeDownloader:
    def __init__(self, url):
        self.url = url
        self.yt = YouTube(url)
    
    def get_resolutions(self,):
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

        return sorted(resolutions, reverse=True)
    
    def download(self, quality='1080p'):
        stream = None
        stream = self.yt.streams.filter(file_extension='mp4', res=quality).first()

        if stream:
            stream.download(output_path="static/content/")


if __name__=="__main__":
    from pytubefix import YouTube
    from pytubefix.cli import on_progress
    
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    yt = YouTube(url, on_progress_callback = on_progress)
    
    ys = yt.streams
    
    resolutions = []
    for stream in ys:
        try:
            res = stream.resolution
            if "p" in res:
                res = res.replace("p", "")
                if int(res) not in resolutions:
                    resolutions.append(int(res))

        except Exception as e: 
            pass

    print(sorted(resolutions, reverse=True))
