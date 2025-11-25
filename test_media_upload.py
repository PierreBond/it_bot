# test_media_upload.py
import os
import tweepy
import config

auth = tweepy.OAuth1UserHandler(
    config.TWITTER_API_KEY,
    config.TWITTER_API_SECRET_KEY,
    config.TWITTER_ACCESS_TOKEN,
    config.TWITTER_ACCESS_TOKEN_SECRET
)
api = tweepy.API(auth)

video_path = "video.mp4"

print("Exists:", os.path.exists(video_path))     
if os.path.exists(video_path):
    print("Size (bytes):", os.path.getsize(video_path))

try:
    media = api.media_upload(video_path)
    print("Uploaded media id:", getattr(media, "media_id", None))
except Exception as e:
    print("media_upload failed:", repr(e))
    # Print detailed response if available
    resp = getattr(e, "response", None)
    if resp is not None:
        code = getattr(resp, "status_code", None)
        text = getattr(resp, "text", None)
        print("HTTP status:", code)
        print("Response body:", text)