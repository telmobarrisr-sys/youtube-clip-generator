import yaml
import yt_dlp
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
import re
import random

def load_config():
    with open('config/params.yaml', 'r') as file:
        return yaml.safe_load(file)

def convert_time_to_seconds(time_str):
    """Convierte tiempo en formato HH:MM:SS a segundos"""
    if isinstance(time_str, (int, float)):
        return time_str
    
    parts = list(map(int, time_str.split(':')))
    if len(parts) == 3:  # HH:MM:SS
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    elif len(parts) == 2:  # MM:SS
        return parts[0] * 60 + parts[1]
    else:  # SS
        return parts[0]

def download_video(url, output_path="downloads/"):
    os.makedirs(output_path, exist_ok=True)
    try:
        # Configuración para evitar bloqueos de YouTube
        ydl_opts = {
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'format': 'best[height<=720]',
            'quiet': False,
            'no_warnings': False,
            'ignoreerrors': True,
            'retries': 3,
            'fragment_retries': 3,
            'skip_unavailable_fragments': True,
            'extract_flat': False,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Accept-Encoding': 'gzip,deflate',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                'Connection': 'keep-alive',
                'Referer': 'https://www.youtube.com/',
            },
            'socket_timeout': 30,
            'no_check_certificate': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Intentar descargar
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            print(f"Video descargado: {filename}")
            return filename
            
    except Exception as e:
        print(f"Error descargando video: {e}")
        # Intentar método alternativo si falla
        return download_video_alternative(url, output_path)

def download_video_alternative(url, output_path):
    """Método alternativo si el primero falla"""
    try:
        print("Intentando método alternativo de descarga...")
        
        ydl_opts = {
            'outtmpl': os.path.join(output_path, 'video.%(ext)s'),
            'format': 'worst[height>=360]',  # Calidad más baja para evitar detección
            'quiet': False,
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            },
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            print(f"Video descargado (método alternativo): {filename}")
            return filename
            
    except Exception as e:
        print(f"Error también en método alternativo: {e}")
        raise

def create_clip(video_path, start_time, end_time, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=output_path)
        print(f"Clip creado: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error creando clip: {e}")
        raise

def main():
    try:
        config = load_config()
        print(f"Configuración cargada")
        
        # Descargar el video
        print("Descargando video...")
        video_path = download_video(config['youtube_url'])
        
        # Crear clips
        for clip in config['clips']:
            print(f"\nProcesando clip: {clip['output_name']}")
            
            # Convertir tiempos a segundos
            start_seconds = convert_time_to_seconds(clip['start_time'])
            end_seconds = convert_time_to_seconds(clip['end_time'])
            
            print(f"Tiempo: {start_seconds}s - {end_seconds}s")
            
            # Crear el clip
            output_path = f"clips/{clip['output_name']}"
            clip_path = create_clip(video_path, start_seconds, end_seconds, output_path)
            
            print(f"✓ Clip creado exitosamente: {clip_path}")
        
        print("\n🎉 Todos los clips han sido creados exitosamente!")
        
    except Exception as e:
        print(f"❌ Error en el proceso: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    main()
