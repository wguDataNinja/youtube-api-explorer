#!/usr/bin/env python3
"""
Fetch metadata for one YouTube channel using its handle or ID.
Does NOT use quota
Saves result to: output/<handle>/channel_data.json
"""

import sys
import json
import yaml
import requests
from pathlib import Path

API_BASE = "https://www.googleapis.com/youtube/v3"

# -------- CONFIG --------
CHANNEL_INPUT = "alextheanalyst"  # also ok: "UC7cs8q-gJRlGwj4A8OmCmXg"
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
        return handle_or_id  # already a channel ID

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

def fetch_channel_data(channel_id, api_key):
    url = f"{API_BASE}/channels"
    params = {
        "part": "snippet,statistics,contentDetails,topicDetails",  # all parts cost 0 for channels.list
        "id": channel_id,
        "key": api_key
    }
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    return r.json().get("items", [])

def save_channel_json(channel_obj, channel_label):
    out_dir = OUTPUT_DIR / channel_label
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "channel_data.json"
    with open(out_path, "w") as f:
        json.dump(channel_obj, f, indent=2)
    print(f"Saved {out_path}")

def main():
    api_key = load_api_key(CONFIG_PATH)
    channel_id = resolve_channel_id(CHANNEL_INPUT, api_key)
    items = fetch_channel_data(channel_id, api_key)

    if not items:
        print("No data returned.")
        return

    channel = items[0]
    snippet = channel.get("snippet", {})
    stats = channel.get("statistics", {})

    print("Channel Info")
    print("------------")
    print(f"Title:           {snippet.get('title')}")
    print(f"Description:     {snippet.get('description')[:80]}...")
    print(f"Subscribers:     {stats.get('subscriberCount')}")
    print(f"Total Videos:    {stats.get('videoCount')}")
    print(f"Total Views:     {stats.get('viewCount')}")

    save_channel_json(channel, CHANNEL_INPUT)


if __name__ == "__main__":
    main()