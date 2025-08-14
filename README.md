# YouTube API Explorer

A minimal project to fetch YouTube channel and video metadata using the YouTube Data API v3.  
Example scripts are included.

1. Get a YouTube API key  (Free, <2 min. setup)
2. Clone this repo  
3. Paste your key into `config/api_config.yaml`  
4. Run `yt_api_test.py` to test the API key  
5. Run `fetch_channel_metadata.py`  
6. Run `fetch_video_metadata.py`  
7. Inspect and analyze your data:

```
/output/alextheanalyst/channel_data.json  
/output/alextheanalyst/videos_data.json
```

---

## 1. YouTube API Setup

Follow Google’s guide:  
https://developers.google.com/youtube/v3/getting-started

Steps:

1. Sign in to your Google Account  
2. Create a project: https://console.developers.google.com  
   Suggested name: `youtube-api-explorer`  
3. Enable the **YouTube Data API v3**  
4. Create an API key: https://console.cloud.google.com/apis/credentials  
5. Copy your API key  

---

Here is the raw markdown:

## 2. Clone the Repository

```bash
git clone https://github.com/wguDataNinja/youtube-api-explorer.git
cd youtube-api-explorer
````
3. Install Requirements
```python
pip install -r requirements.txt
```

4. Configure Your API Key

Create a config file by copying the sample:
```bash
cp config/api_config.sample.yaml config/api_config.yaml

```

Then edit config/api_config.yaml and paste your YouTube API key:
```python
YOUTUBE_API_KEY: "your-api-key-here"
```



### 3. Test the API

Run:

```bash
python scripts/yt_api_test.py
```

If successful, you’ll see channel info for Alex the Analyst — confirming your API key works.

---

### 4. Fetch Channel Metadata (no quota cost)

Fetch metadata for a single channel using its handle or ID.

Edit the top of the script:

`scripts/fetch_channel_data.py`

Set:
Pick your own channel or use the example:
```python
CHANNEL_INPUT = "alextheanalyst"  # or a channel ID like "UC7cs8q-gJRlGwj4A8OmCmXg"
```

Then run:

```bash
python scripts/fetch_channel_data.py
```

Output:
- Saves to: `output/[channel_name]/channel_data.json`

Note:
- The channel is hardcoded in the script via `CHANNEL_INPUT`
- Does **not** consume API quota (free `channels.list` parts)

Reference:  
https://developers.google.com/youtube/v3/docs/channels

---

### 5. Inspect the Channel Data

Open:

```
output/alextheanalyst/channel_data.json
```

Example:

```json
{
  "id": "UC7cs8q-gJRlGwj4A8OmCmXg",
  "snippet": {
    "title": "Alex The Analyst"
  }
}
```
---

### 6. Fetch Video Metadata

Fetch recent video metadata for the same channel selected in step 4.

Edit the top of the script:

`scripts/fetch_video_metadata.py`

Set:

```python
CHANNEL_INPUT = "alextheanalyst"  # must match the channel used in script 4
MAX_RESULTS = 50                  # set to None for ALL videos (watch quota)
```

Then run:

```bash
python scripts/fetch_video_metadata.py
```

Output:
- Saves to: `output/alextheanalyst/videos_data.json`
- Prints video count and estimated quota usage

---

Note:  
This script uses quota due to two API calls:

1. **`playlistItems.list`** – Fetches video IDs from the channel's uploads playlist  
   → 1 unit per call, max 50 videos per call  
   → For 384 videos: 8 calls = **8 units**

2. **`videos.list`** – Retrieves video metadata  
   - Each part costs 1 unit per video  
     - `snippet,statistics,contentDetails` = 3 units per video  
     - `snippet` only = 1 unit per video

**Quota cost examples:**
- All 3 parts: 384 × 3 = **1,152** + 8 = **1,160 units**
- Snippet only: 384 × 1 = **384** + 8 = **392 units**

Daily quota limit: **10,000 units**  
Reference: [YouTube API Quota Calculator](https://developers.google.com/youtube/v3/determine_quota_cost)

---
### 7. Next Steps

Now that you have the raw JSON data, here are some ideas:

- Transform the data into an easier-to-read CSV  
- Load into a Pandas DataFrame for analysis  
- Run EDA in a Jupyter notebook  
- Improve the code for flexibility and robustness  

---

### Possible Improvements

1. **Command-Line Arguments**  
   Support `--channel` and `--max-results` as arguments instead of editing the script.

2. **Use Channel Title as Folder Name**  
   Automatically name the output folder using the channel’s `snippet.title`.

3. **Safe Folder Names**  
   Sanitize channel titles (replace spaces and special characters).

4. **Error Logging**  
   Log any API or processing errors to a `.log` file for debugging.

5. **Modularize Shared Functions**  
   Move shared logic like `load_api_key()` and `resolve_channel_id()` into `utils.py`.

6. **Quota Summary**  
   Print total estimated quota usage at the end of the run.

7. **Optional CSV Export**  
   Add a `--csv` flag to export video data as a CSV alongside JSON.

---

Next step: **Topic Analysis** *(To-Do)*

**Project complete** — data is now ready for exploration and analysis.

