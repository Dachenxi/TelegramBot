import instaloader
from urllib.parse import urlparse
import os, re

def extract_shortcode(url: str) -> str:
    path = urlparse(url).path
    patterns = [r"/p/([^/?]+)", r"/reel/([^/?]+)", r"/reels/([^/?]+)"]
    for pattern in patterns:
        match = re.search(pattern, path)
        if match:
            return match.group(1)
    return None

def download_instagram_post(url: str):
    L = instaloader.Instaloader()
    shortcode = extract_shortcode(url)
    if not shortcode:
        raise ValueError("URL tidak valid.")
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    L.download_post(post, target="temp")
    return [os.path.join("temp", file) for file in os.listdir("temp") if file.endswith((".jpg", ".mp4"))]
