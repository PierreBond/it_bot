import tweepy 
import config 

def post_to_twitter(video_path, text=""):
    # Validate credentials
    if not all([
        config.TWITTER_API_KEY,
        config.TWITTER_API_SECRET_KEY,
        config.TWITTER_ACCESS_TOKEN,
        config.TWITTER_ACCESS_TOKEN_SECRET,
    ]):
        raise Exception("Twitter credentials are not fully set in config")

    auth = tweepy.OAuth1UserHandler(
        config.TWITTER_API_KEY,
        config.TWITTER_API_SECRET_KEY,
        config.TWITTER_ACCESS_TOKEN,
        config.TWITTER_ACCESS_TOKEN_SECRET
    )

    api = tweepy.API(auth)

    try:
        media = api.media_upload(video_path)
    except Exception as e:
        # Provide more details from Tweepy/Twitter response if available
        detail = None
        try:
            # Tweepy exceptions may include a .response attribute
            detail = getattr(e, 'response', None)
            if detail is not None:
                text = getattr(detail, 'text', None) or str(detail)
                code = getattr(detail, 'status_code', None)
                raise Exception(f"media_upload failed: {e} (status={code}) response={text}")
        except Exception:
            pass
        raise Exception(f"media_upload failed: {e}")

    try:
        api.update_status(status=text, media_ids=[media.media_id])
    except Exception as e:
        detail = None
        try:
            detail = getattr(e, 'response', None)
            if detail is not None:
                text = getattr(detail, 'text', None) or str(detail)
                code = getattr(detail, 'status_code', None)
                raise Exception(f"update_status failed: {e} (status={code}) response={text}")
        except Exception:
            pass
        raise Exception(f"update_status failed: {e}")