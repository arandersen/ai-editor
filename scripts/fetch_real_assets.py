#!/usr/bin/env python3
import json
import urllib.request
import urllib.parse
import os

HEADERS = {
    "User-Agent": "VoxEditorialVideoBot/1.0 (arthur@editorial-explainer.org)"
}

OUT_DIR = "/Users/arthurandersen/Documents/AI_Video_Editor_Gemini/VOX-TEST_race/02_assets/real_downloads"
os.makedirs(OUT_DIR, exist_ok=True)

queries = {
    "beat02_starter_gun.jpg": "starting pistol",
    "beat02_classroom.jpg": "exam hall university desks",
    "beat03_money.jpg": "banknotes stack money",
    "beat03_city.jpg": "vintage city skyline",
    "beat03_handshake.jpg": "handshake business agreement",
    "beat05_lap9_runner.jpg": "sprinter crossing finish line",
    "beat05_lap3_runner.jpg": "runner track race middle"
}

def search_wikimedia(query):
    url = (
        "https://commons.wikimedia.org/w/api.php?action=query&generator=search"
        f"&gsrnamespace=6&gsrsearch={urllib.parse.quote(query)}"
        "&gsrlimit=1&prop=imageinfo&iiprop=url|size|extmetadata&format=json"
    )
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=15) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        pages = data.get("query", {}).get("pages", {})
        for _, page in pages.items():
            info = page.get("imageinfo", [{}])[0]
            img_url = info.get("url")
            desc_url = info.get("descriptionurl")
            title = page.get("title")
            return img_url, desc_url, title
    return None, None, None

def download_file(url, out_path):
    # Strip utm parameters if present
    clean_url = url.split("?")[0]
    req = urllib.request.Request(clean_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30) as resp, open(out_path, "wb") as f:
        f.write(resp.read())

log_entries = []
for filename, q in queries.items():
    print(f"Searching for '{q}'...")
    try:
        img_url, desc_url, title = search_wikimedia(q)
        if img_url:
            out_file = os.path.join(OUT_DIR, filename)
            print(f"  Downloading {title} -> {out_file}...")
            download_file(img_url, out_file)
            log_entries.append(f"- **{filename}**: [{title}]({desc_url}) via Wikimedia Commons (Original: {img_url})")
            print(f"  ✅ Saved {filename}")
        else:
            print(f"  ❌ No result for {q}")
    except Exception as e:
        print(f"  ⚠️ Error for {q}: {e}")

print("\n--- Asset Log Entries ---")
for entry in log_entries:
    print(entry)
