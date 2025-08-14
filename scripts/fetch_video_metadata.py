#!/usr/bin/env python3
"""
Fetch metadata for recent videos on a given YouTube channel.
Saves result to: output/<handle>/videos_data.json

NOTE:
- This script DOES use quota.
"""

import sys
import json
import yaml
import requests
from pathlib import Path

API_BASE = "https://www.googleapis.com/youtube/v3"

# -------- CONFIG --------
CHANNEL_INPUT = "alextheanalyst"  # or None to skip
MAX_RESULTS = 50                 # set to None for ALL videos (watch quota)
# ------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "api_config.yaml"
OUTPUT_DIR = PROJECT_ROOT / "output"

def load_api_key(config_path: Path) -> str:
    with open(config_path, "r") as f:
        key = yaml.safe_load(f).get("YOUTUBE_API_KEY")
    if not key:
        raise RuntimeError("Missing YOUTUBE_API_KEY")
    return key

def resolve_channel_id(handle_or_id, api_key):
    if handle_or_id.startswith("UC"):
        return handle_or_id
    url = f"{API_BASE}/channels"
    params = {
        "part": "id",
        "forHandle": handle_or_id,
        "key": api_key
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    items = r.json().get("items", [])
    if not items:
        raise ValueError("No channel found for that handle.")
    return items[0]["id"]

def get_uploads_playlist_id(channel_id, api_key):
    url = f"{API_BASE}/channels"
    params = {
        "part": "contentDetails",
        "id": channel_id,
        "key": api_key
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    items = r.json().get("items", [])
    return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]

def fetch_recent_video_ids(playlist_id, api_key, max_results):
    video_ids = []
    url = f"{API_BASE}/playlistItems"
    params = {
        "part": "contentDetails",
        "playlistId": playlist_id,
        "maxResults": min(50, max_results),
        "key": api_key
    }

    while True:
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        data = r.json()
        for item in data.get("items", []):
            video_ids.append(item["contentDetails"]["videoId"])
            if len(video_ids) >= max_results:
                return video_ids
        if "nextPageToken" in data:
            params["pageToken"] = data["nextPageToken"]
        else:
            break
    return video_ids

def fetch_video_metadata(video_ids, api_key):
    metadata = []
    url = f"{API_BASE}/videos"

    # Each part adds 1 quota unit per video
    params_template = {
        "part": "snippet,statistics,contentDetails",  # Each part costs 1 quota unit per video
        "key": api_key
    }

    for i in range(0, len(video_ids), 50):
        chunk = video_ids[i:i+50]
        params = params_template.copy()
        params["id"] = ",".join(chunk)
        r = requests.get(url, params=params, timeout=20)
        r.raise_for_status()
        metadata.extend(r.json().get("items", []))
    return metadata

def save_video_data(video_data, label):
    out_dir = OUTPUT_DIR / label
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "videos_data.json"
    with open(out_path, "w") as f:
        json.dump(video_data, f, indent=2)
    print(f"Saved {out_path}")

def main():
    if not CHANNEL_INPUT:
        print("CHANNEL_INPUT is None. Exiting.")
        return

    api_key = load_api_key(CONFIG_PATH)
    channel_id = resolve_channel_id(CHANNEL_INPUT, api_key)
    playlist_id = get_uploads_playlist_id(channel_id, api_key)
    video_ids = fetch_recent_video_ids(playlist_id, api_key, MAX_RESULTS)
    print(f"Found {len(video_ids)} videos (limit = {MAX_RESULTS})")
    video_data = fetch_video_metadata(video_ids, api_key)
    save_video_data(video_data, CHANNEL_INPUT)

if __name__ == "__main__":
    main()