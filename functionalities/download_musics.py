from pytube import YouTube

def download_audio_from_youtube(url):
    try:
        yt = YouTube(url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        if audio_stream:
            print(f"Downloading audio from {yt.title}...")
            audio_stream.download(output_path="audio", filename=f"{yt.title}.mp3")
            print("Download completed successfully!")
        else:
            print(f"No audio stream found for {yt.title}")

    except Exception as e:
        print(f"Error occurred while downloading audio: {str(e)}")

if __name__ == "__main__":
    youtube_urls_file = "youtube_urls.txt"

    with open(youtube_urls_file, "r") as file:
        youtube_urls = file.readlines()

    youtube_urls = [url.strip() for url in youtube_urls]

    for url in youtube_urls:
        download_audio_from_youtube(url)
