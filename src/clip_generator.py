from moviepy.editor import VideoFileClip
import yaml

def generate_clips(video_path, clips):
    for clip in clips:
        start_time = clip['start_time']
        end_time = clip['end_time']
        output_name = clip['output_name']
        
        # Convertir tiempos a segundos
        start_sec = sum(x * int(t) for x, t in zip([3600, 60, 1], start_time.split(":")))
        end_sec = sum(x * int(t) for x, t in zip([3600, 60, 1], end_time.split(":")))
        
        # Recortar el clip
        video = VideoFileClip(video_path).subclip(start_sec, end_sec)
        video.write_videofile(output_name, codec='libx264', audio_codec='aac')
        video.close()
        print(f"Clip guardado como {output_name}")

if __name__ == "__main__":
    with open('config/params.yaml', 'r') as f:
        config = yaml.safe_load(f)
    generate_clips("video_descargado.mp4", config['clips'])
