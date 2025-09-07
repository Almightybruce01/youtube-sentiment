from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import sys

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def yt():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    return build("youtube","v3",credentials=creds)

if __name__ == "__main__":
    ids = sys.argv[1:]
    if not ids:
        print("Usage: python3 video_stats.py VIDEO_ID [VIDEO_ID ...]")
        sys.exit(1)
    y = yt()
    res = y.videos().list(part="snippet,statistics,status", id=",".join(ids)).execute()
    for it in res.get("items", []):
        vid = it["id"]
        title = it["snippet"]["title"]
        stats = it.get("statistics", {})
        status = it.get("status", {})
        cc = stats.get("commentCount", "0")
        m4k = status.get("madeForKids", False)
        privacy = status.get("privacyStatus", "unknown")
        print(f"{vid}\tcomments={cc}\tmadeForKids={m4k}\tprivacy={privacy}\ttitle={title}")
