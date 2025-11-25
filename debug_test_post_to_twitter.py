from twitterclient import post_to_twitter

# Attempt to post small image (should hit 403 and fallback to text-only)
try:
    post_to_twitter("test.png", text="Fallback link: https://www.instagram.com/p/test123/")
    print("post_to_twitter call completed")
except Exception as e:
    print("post_to_twitter raised exception:", e)
