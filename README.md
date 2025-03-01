# YouTube Subtitle Downloader

A Python script to download subtitles from YouTube playlists and organize them into Excel files. Supports English, Other Languages, and auto-generated subtitles with error handling and rate limiting.

## Features
- Downloads subtitles from YouTube playlists without downloading videos and saves them into dataframes.
- Supports multiple languages (English, Other Languages and auto-generated).
- Saves subtitles in individual playlist Excel files and a master dataset.
- Handles private videos, rate limits, and errors gracefully.
- Uses a download archive to avoid reprocessing videos.


## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/youtube-subtitle-downloader.git
   cd youtube-subtitle-downloader
2. pip install -r requirements.txt
# Run
1. subtitle_downloader.py

# Working
Subtitles will be saved in the subtitles/ directory:
   Individual playlist files: subtitles/<playlist_name>.xlsx
   Master dataset: subtitles/all_playlists_subtitles.xlsx
## Configuration
Output Directory: Change OUTPUT_DIR in the script to customize the output folder.
Cookies File: Set COOKIES_FILE to the path of your cookies file if authentication is needed.
Rate Limiting: Adjust 'ratelimit' in ydl_opts to control download speed.

### Notes
The script skips private videos and continues processing the playlist.
Random sleep intervals are added to avoid detection by YouTube.
Duplicate videos are avoided using a unique archive file per playlist.
This was meant to be only for subtitles, but audio and video can be added too.
