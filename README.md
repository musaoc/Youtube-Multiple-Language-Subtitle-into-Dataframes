# YouTube Subtitle Downloader

A Python script to download subtitles from YouTube playlists and organize them into Excel files. Supports English, Other Languages, and auto-generated subtitles with error handling and rate limiting.

## Features
- Downloads subtitles from YouTube playlists without downloading videos.
- Supports multiple languages (English, Other Languages and auto-generated).
- Saves subtitles in individual playlist Excel files and a master dataset.
- Handles private videos, rate limits, and errors gracefully.
- Uses a download archive to avoid reprocessing videos.

## Prerequisites
- Python 3.6+
- Required libraries: `yt-dlp`, `pandas`, `numpy`, `openpyxl`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/youtube-subtitle-downloader.git
   cd youtube-subtitle-downloader
