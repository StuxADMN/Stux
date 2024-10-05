from pytube import YouTube

class YouTubeDownloader:
    def __init__(self, url):
        self.url = url
        self.yt = YouTube(url)
    
    def download(self, quality='medium'):
        stream = None
        
        if quality == 'low':
            stream = self.yt.streams.filter(file_extension='mp4', res="360p").first()
        elif quality == 'medium':
            stream = self.yt.streams.filter(file_extension='mp4', res="480p").first()
        elif quality == 'high':
            stream = self.yt.streams.filter(file_extension='mp4', res="720p").first()
        elif quality == 'ultra high':
            stream = self.yt.streams.filter(file_extension='mp4', res="1080p").first()
        else:
            raise ValueError("Quality has to be 'low', 'medium', 'high' or 'ultra high'")
        
        if stream:
            stream.download(output_path="static/content/")
