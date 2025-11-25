import subprocess
import os
import glob

def download_vid(url):
    """Download Instagram video using yt-dlp.

    This avoids external download APIs and is more reliable when network
    connectivity to third-party APIs is flaky.
    """
    output_template = "video.%(ext)s"
    try:
        # Run yt-dlp to download the best available video/format.
        # Do not pass a format selection so yt-dlp can decide and merge
        # audio/video when needed.
        result = subprocess.run(
            [
                "yt-dlp",
                # Use a cookies file to bypass Instagram's login wall.
                # This is more reliable than --cookies-from-browser.
                # You must export your cookies from a logged-in browser session.
                "--cookies", "cookies.txt",
                "-o", output_template, url
            ],
            capture_output=True, text=True, timeout=180
        )

        if result.returncode != 0:
            # Include stderr to help debugging unsupported URLs
            stderr = (result.stderr or result.stdout or "").strip()
            raise Exception(f"yt-dlp error: {stderr}")

        # Find the downloaded file (video.<ext>) and normalize to video.mp4
        files = glob.glob("video.*")
        for f in files:
            if f.endswith((".mp4", ".mov", ".mkv", ".webm")):
                if f != "video.mp4":
                    try:
                        os.replace(f, "video.mp4")
                    except Exception:
                        # If replace fails, just return the found file
                        return f
                return "video.mp4"

        raise Exception("yt-dlp did not produce a video file")

    except FileNotFoundError:
        raise Exception("yt-dlp not found. Install it with: `.venv\\Scripts\\pip install yt-dlp` or `pip install yt-dlp`")
    except Exception as e:
        # Surface the yt-dlp stderr for debugging
        raise
