from telegram.ext import Updater, MessageHandler , Filters
from downloader import download_vid
from twitterclient import post_to_twitter
import traceback
import config
import re

# Accept only full post/reel/tv URLs (ask user to send the specific post URL)
INSTAGRAM_REGEX = r"(https?://(?:www\.)?instagram\.com/(?:p|reel|reels|tv)/[A-Za-z0-9_\-\.]+(?:/)?(?:\S*)?)"

def handle_message(update, context):
    text = update.message.text
    
    match = re.search(INSTAGRAM_REGEX, text)

    if not match:
        update.message.reply_text("Send me an Instagram post or reel URL (example: https://www.instagram.com/p/XXXXXXXX/ or /reel/)")
        return

    ig_url = match.group(1)
    update.message.reply_text("Downloading video...")

    # Download step
    try:
        path = download_vid(ig_url)
    except Exception as e:
        tb = traceback.format_exc()
        print("Download failed:\n", tb)
        update.message.reply_text(f"Download failed: {e}")
        return

    # Post step
    update.message.reply_text("Posting to Twitter...")
    try:
        post_to_twitter(path)
    except Exception as e:
        tb = traceback.format_exc()
        print("Twitter post failed:\n", tb)
        update.message.reply_text(f"Twitter post failed: {e}")
        return

    update.message.reply_text("Done")

def main():
    token = config.TELEGRAM_BOT_TOKEN
    if not token:
        raise ValueError("TELEGRAM_BOT_TOKEN environment variable not set")
    
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher

    if dp:
        dp.add_handler(MessageHandler(Filters.text, handle_message))
    updater.start_polling()
    print("Bot started")
    updater.idle()

if __name__ == "__main__":
    main()    