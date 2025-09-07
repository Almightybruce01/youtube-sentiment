import sys, csv, time
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

def get_service():
    creds = Credentials.from_authorized_user_file("token.json", ["https://www.googleapis.com/auth/youtube.readonly"])
    return build("youtube", "v3", credentials=creds)

def fetch_comments(video_id, max_items=1000):
    yt = get_service()
    out = []
    req = yt.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        order="time",
        textFormat="plainText"
    )
    while req and len(out) < max_items:
        res = req.execute()
        for item in res.get("items", []):
            top = item["snippet"]["topLevelComment"]["snippet"]
            out.append({
                "platform":"youtube",
                "video_id":video_id,
                "comment_id":item["snippet"]["topLevelComment"]["id"],
                "author":top.get("authorDisplayName"),
                "text":top.get("textDisplay","").replace("\n"," "),
                "published_at":top.get("publishedAt"),
                "like_count":top.get("likeCount",0)
            })
        req = yt.commentThreads().list_next(req, res)
        time.sleep(0.2)
    return out

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("Usage: python3 fetch_comments.py VIDEO_ID [MAX]"); sys.exit(1)
    vid = sys.argv[1]; limit = int(sys.argv[2]) if len(sys.argv)>2 else 1000
    rows = fetch_comments(vid, limit)
    out = "youtube_comments.csv"
    write_header = False
    try:
        open(out,"r",encoding="utf-8").close()
    except FileNotFoundError:
        write_header = True
    with open(out,"a",newline="",encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["platform","video_id","comment_id","author","text","published_at","like_count"])
        if write_header: w.writeheader()
        w.writerows(rows)
    print(f"Wrote {len(rows)} comments to {out}")
