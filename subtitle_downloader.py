import os
import pandas as pd
import numpy as np
import yt_dlp
import time
import random
from pathlib import Path

# Constants
OUTPUT_DIR = "subtitles"
MASTER_CSV = os.path.join(OUTPUT_DIR, "all_playlists_subtitles.xlsx")
# https://chromewebstore.google.com/detail/get-cookiestxt-locally
COOKIES_FILE = "cookies.txt"  # Optional: Add path to your cookies file for authentication

def download_subtitles(playlist_url):
    """Download subtitles from a YouTube playlist with authentication and rate limiting."""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)

    # Generate unique archive file based on playlist ID
    playlist_id = playlist_url.split('list=')[-1] if 'list=' in playlist_url else playlist_url.split('/')[-1]
    archive_file = os.path.join(OUTPUT_DIR, f"downloaded_videos_{playlist_id}.txt")

    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,
        'subtitleslangs': ['en', 'ur', 'auto'], # Optional: You can add more languages
        'skip_download': True,
        'outtmpl': f'{OUTPUT_DIR}/%(playlist_title)s/%(title)s.%(ext)s',
        'quiet': False,
        'ratelimit': 1000000,  # Limit download speed (bytes/second)
        'retries': 3,
        'fragment_retries': 3,
        'download_archive': archive_file,
        #'sleep_interval_requests': random.uniform(1, 2), # Optional: IF you want to add Sleep interval between video requests
        #'sleep_interval_subtitles': random.uniform(0,1 ), #Optional: If you want to add a sleep interval in between subtitle request for each video
        'noplaylist': False,
        'cookiefile': COOKIES_FILE if os.path.exists(COOKIES_FILE) else None,
        'ignoreerrors': True,
    }

    retry_attempts = 3 # Optional: Adjust retry attempts
    for attempt in range(retry_attempts):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(playlist_url, download=True)
                playlist_name = info.get('title', 'Unknown Playlist')
                print(f"✅ Processed playlist: {playlist_name}")
                return playlist_name, os.path.join(OUTPUT_DIR, playlist_name)
        except yt_dlp.utils.DownloadError as e:
            error_msg = str(e)
            print(f"Error downloading subtitles (Attempt {attempt + 1}/{retry_attempts}): {error_msg}")
            if "HTTP Error 429" in error_msg:
                wait_time = random.uniform(1, 10) * (attempt + 1) # Optional: Adjustment of sleep interval
                print(f"⚠️ Rate limit reached. Waiting {wait_time:.2f} seconds before retrying...")
                time.sleep(wait_time)
            elif "Private video" in error_msg or "Sign in if you've been granted access" in error_msg:
                print("⚠️ Skipping private video, continuing with playlist...")
                break
            else:
                print("⚠️ Unhandled error, but will attempt to resume from last point...")
                break
    return None

def read_subtitle_file(file_path):
    """Read subtitle file content or return None if unavailable."""
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None
    return None

def parse_subtitles(playlist_dir):
    """Parse downloaded subtitles and return DataFrame."""
    data = {
        'playlist_name': [], 'video_name': [], 
        'subtitles_en': [], 'subtitles_ur': [], 'subtitles_auto': []
    }

    playlist_name = os.path.basename(playlist_dir)
    for root, _, files in os.walk(playlist_dir):
        for file in files:
            if file.endswith('.vtt'):
                video_name = os.path.splitext(file)[0].replace('.en', '').replace('.ur', '').replace('.auto', '')
                data['playlist_name'].append(playlist_name)
                data['video_name'].append(video_name)

                en_path = os.path.join(root, f"{video_name}.en.vtt")
                ur_path = os.path.join(root, f"{video_name}.ur.vtt")
                auto_path = os.path.join(root, f"{video_name}.auto.vtt")

                data['subtitles_en'].append(read_subtitle_file(en_path) if os.path.exists(en_path) else np.nan)
                data['subtitles_ur'].append(read_subtitle_file(ur_path) if os.path.exists(ur_path) else np.nan)
                data['subtitles_auto'].append(read_subtitle_file(auto_path) if os.path.exists(auto_path) else np.nan)

    return pd.DataFrame(data)

def main():
    """Main function to download and process YouTube playlist subtitles."""
    playlist_urls = [
        'https://www.youtube.com/watch?v=8kPif5oSbw4&list=PLdZNFVCDo_1emqBpUQxOXU-fGZG3nVJKM',  # khai
        'https://www.youtube.com/watch?v=4L2V7KueDBs&list=PLb2aaNHUy_gEldBBBffyW-4Y56UtPon8C',  # mein
        'https://www.youtube.com/watch?v=XEPc2bUpC-c&list=PLb2aaNHUy_gEHFn5X2HQ7uIAkhqhqRcHI',  # rahe junoon
        # Add more playlists as needed
    ]

    # Load existing master dataset if it exists
    if os.path.exists(MASTER_CSV):
        df_master = pd.read_excel(MASTER_CSV)
    else:
        df_master = pd.DataFrame()

    for playlist_url in playlist_urls:
        print(f"\nProcessing playlist: {playlist_url}\n")
        playlist_result = download_subtitles(playlist_url)

        if playlist_result:
            playlist_name, playlist_dir = playlist_result
            df_temp = parse_subtitles(playlist_dir)

            # Save individual playlist Excel
            df_temp.to_excel(f"{OUTPUT_DIR}/{playlist_name}.xlsx", index=False)

            # Append to master DataFrame, avoiding duplicates
            df_master = pd.concat([df_master, df_temp]).drop_duplicates(subset=['playlist_name', 'video_name'], keep='last')
            print(f"✅ Subtitles for '{playlist_name}' saved successfully!\n")

            # Save updated master dataset
            df_master.to_excel(MASTER_CSV, index=False)
            print(f"📂 Master dataset updated at: {MASTER_CSV}\n")
        else:
            print(f"❌ Failed to download subtitles for {playlist_url}\n")

        sleep_time = random.uniform(1, 5)
        print(f"⏳ Sleeping for {sleep_time:.2f} seconds to avoid detection...\n")
        time.sleep(sleep_time)

    # Print summary
    print("\n📊 Final Summary:")
    print(f"Total videos processed: {len(df_master)}")
    print(f"English subtitles available: {df_master['subtitles_en'].notna().sum()}")
    print(f"Urdu subtitles available: {df_master['subtitles_ur'].notna().sum()}")
    print(f"Auto subtitles available: {df_master['subtitles_auto'].notna().sum()}")

if __name__ == "__main__":
    try:
        import yt_dlp, pandas, numpy
    except ImportError:
        print("Installing required packages...")
        os.system("pip install yt-dlp pandas numpy openpyxl")
    main()