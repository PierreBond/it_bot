import tweepy
import config
from tweepy import TweepyException

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
    except TweepyException as e:
        # Add more detail to the exception
        response = getattr(e, "response", None)
        if response is not None:
            raise Exception(f"media_upload failed with status {response.status_code}: {response.text}") from e
        raise Exception(f"media_upload failed: {e}") from e

    try:
        api.update_status(status=text, media_ids=[media.media_id])
    except TweepyException as e:
        response = getattr(e, "response", None)
        if response is not None:
            resp_text = getattr(response, 'text', '')
            if "You currently have access to a subset of X API" in resp_text:
                 raise Exception(
                    "Posting tweet failed (403 Forbidden): Your Twitter Developer App access level is too low. "
                    "Please upgrade to the 'Basic' tier or higher in the developer portal to post tweets."
                ) from e
            raise Exception(f"update_status failed with status {response.status_code}: {resp_text}") from e
        raise Exception(f"update_status failed: {e}") from e