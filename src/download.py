import yt_dlp
import yaml

def download_video(youtube_url, output_path="video_descargado.mp4"):
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': output_path,
        'merge_output_format': 'mp4',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    return output_path

if __name__ == "__main__":
    with open('config/params.yaml', 'r') as f:
        config = yaml.safe_load(f)
    download_video(config['youtube_url'])
