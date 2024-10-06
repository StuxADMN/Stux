from pytube import YouTube

class YouTubeDownloader:
    def __init__(self, url):
        self.url = url
        self.yt = YouTube(url)
    
    def download(self, quality='1080p'):
        stream = None
        stream = self.yt.streams.filter(file_extension='mp4', res=quality).first()

        if stream:
            stream.download(output_path="static/content/")
