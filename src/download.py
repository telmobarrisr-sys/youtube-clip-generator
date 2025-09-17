# download.py
import os
import random
import time
from tenacity import retry, stop_after_attempt, wait_exponential
import yt_dlp

def get_random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0'
    ]
    return random.choice(user_agents)

@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=4, max=60))
def download_video_with_retry(url, output_path="downloads"):
    ydl_opts = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'best',
        'user_agent': get_random_user_agent(),
        'cookiefile': 'cookies.txt' if os.path.exists('cookies.txt') else None,
        'retries': 10,
        'fragment_retries': 10,
        'referer': 'https://www.youtube.com/',
        'socket_timeout': 30,
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None

# Función principal que usa clip_generator.py
def download_video(url, output_path="downloads"):
    return download_video_with_retry(url, output_path)
