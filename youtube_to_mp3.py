import os
import subprocess
from yt_dlp import YoutubeDL

def download_youtube_audio(url, output_path="."):
    # Set options for yt-dlp
    ydl_opts = {
        'format': 'bestaudio/best',  # Download the best quality audio
        'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),  # Output file name
        'postprocessors': [{  # Convert to MP3 using ffmpeg
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,  # Suppress output (set to False for debugging)
    }

    # Download the audio
    with YoutubeDL(ydl_opts) as ydl:
        print(f"Downloading: {url}...")
        info_dict = ydl.extract_info(url, download=True)
        audio_file = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        print(f"Download complete: {audio_file}")
        return audio_file

def main():
    # Input YouTube URL
    youtube_url = input("Enter the YouTube URL: ")

    # Directory to save the downloaded file and MP3
    output_directory = "downloads"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Download the YouTube video as audio and convert to MP3
    audio_file = download_youtube_audio(youtube_url, output_directory)

    print(f"MP3 file saved at: {audio_file}")

if __name__ == "__main__": 
    main()
