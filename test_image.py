import os, tweepy, config

auth = tweepy.OAuth1UserHandler(
    config.TWITTER_API_KEY,
    config.TWITTER_API_SECRET_KEY,
    config.TWITTER_ACCESS_TOKEN,
    config.TWITTER_ACCESS_TOKEN_SECRET
)
api = tweepy.API(auth)

img = "test.png"
print("Exists:", os.path.exists(img))
if os.path.exists(img):
    print("Size:", os.path.getsize(img))
try:
    # Step 1: Upload the media
    print("Uploading image...")
    media = api.media_upload(img)    
    print("Uploaded media id:", getattr(media, "media_id", None))

    # Step 2: Post the tweet with the media attached
    tweet_text = "This is a test tweet with an image posted via the API."
    print(f"Posting tweet: '{tweet_text}'")
    api.update_status(status=tweet_text, media_ids=[media.media_id])
    print("Successfully posted tweet with image to your timeline.")

except Exception as e:
    print("An error occurred:", repr(e))
    resp = getattr(e, "response", None)
    if resp is not None:
        print("HTTP status:", getattr(resp, "status_code", None))
        print("Response body:", getattr(resp, "text", None))