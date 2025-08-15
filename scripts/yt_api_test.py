import yaml
import requests
from pathlib import Path

# Absolute path to config
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = PROJECT_ROOT / "config" / "api_config.yaml"

def load_api_key():
    with open(CONFIG_PATH) as f:
        return yaml.safe_load(f)["YOUTUBE_API_KEY"]

def test_youtube_api():
    key = load_api_key()
    channel_id = "UC7cs8q-gJRlGwj4A8OmCmXg"  # Alex The Analyst

    url = (
        "https://www.googleapis.com/youtube/v3/channels"
        f"?part=snippet,statistics&id={channel_id}&key={key}"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json().get("items", [])
        if not data:
            print("❌ No data returned. Check if the channel ID is valid.")
            return

        snippet = data[0]["snippet"]
        stats = data[0]["statistics"]
        handle = snippet.get("customUrl", "N/A")

        print("✅ Connected to YouTube API")
        print("Channel Title:", snippet["title"])
        print("Handle:        {}".format(handle))
        print("Subscribers:   {}".format(stats.get("subscriberCount", "N/A")))
        print("Total Videos:  {}".format(stats.get("videoCount", "N/A")))

    except requests.exceptions.HTTPError as err:
        print("❌ HTTP Error:", err.response.status_code)
        print(err.response.text)
    except Exception as e:
        print("❌ Unexpected Error:", str(e))

if __name__ == "__main__":
    test_youtube_api()