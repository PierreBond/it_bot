import tweepy, config
auth = tweepy.OAuth1UserHandler(
    config.TWITTER_API_KEY,
    config.TWITTER_API_SECRET_KEY,
    config.TWITTER_ACCESS_TOKEN,
    config.TWITTER_ACCESS_TOKEN_SECRET
)
api = tweepy.API(auth)
try:
    print(api.verify_credentials())
except Exception as e:
    print("verify_credentials failed:", e)