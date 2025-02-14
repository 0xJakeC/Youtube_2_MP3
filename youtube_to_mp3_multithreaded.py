import os
import subprocess
from yt_dlp import YoutubeDL
import concurrent.futures

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
    # Input multiple YouTube URLs
    youtube_urls = input("Enter the YouTube URLs (separated by commas): ").strip().split(',')

    # Directory to save the downloaded files and MP3s
    output_directory = "downloads"

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # Use ThreadPoolExecutor to handle multiple downloads concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Submit tasks to the executor
        futures = [
            executor.submit(download_youtube_audio, url.strip(), output_directory)
            for url in youtube_urls
        ]

        # Wait for all tasks to complete and print results
        for future in concurrent.futures.as_completed(futures):
            try:
                audio_file = future.result()
                print(f"MP3 file saved at: {audio_file}")
            except Exception as e:
                print(f"Error processing URL: {e}")

if __name__ == "__main__":
    main()
