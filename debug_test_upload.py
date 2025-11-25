import os, tweepy, config, traceback

print('Start debug test')
print('TWITTER_API_KEY present:', bool(config.TWITTER_API_KEY))
print('Exists:', os.path.exists('test.png'))
if os.path.exists('test.png'):
    print('Size:', os.path.getsize('test.png'))

try:
    auth = tweepy.OAuth1UserHandler(
        config.TWITTER_API_KEY,
        config.TWITTER_API_SECRET_KEY,
        config.TWITTER_ACCESS_TOKEN,
        config.TWITTER_ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth)
    print('Verify creds response:', api.verify_credentials())
    media = api.media_upload('test.png')
    print('Uploaded media id:', getattr(media,'media_id',None))
except Exception as e:
    print('Exception occured:')
    traceback.print_exc()
