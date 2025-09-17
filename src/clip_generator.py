import yaml
from pytube import YouTube
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import os
import re

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
        yt = YouTube(url)
        stream = yt.streams.get_highest_resolution()
        filename = stream.download(output_path)
        print(f"Video descargado: {filename}")
        return filename
    except Exception as e:
        print(f"Error descargando video: {e}")
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
        print(f"Configuración cargada: {config}")
        
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
