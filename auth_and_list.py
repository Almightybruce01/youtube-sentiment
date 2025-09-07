import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]

def get_service():
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)
    return build("youtube", "v3", credentials=creds)

if __name__ == "__main__":
    yt = get_service()
    me = yt.channels().list(part="id,snippet,contentDetails,statistics", mine=True).execute()
    print(json.dumps(me, indent=2))
    uploads = me["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    vids = yt.playlistItems().list(
        part="snippet,contentDetails",
        playlistId=uploads,
        maxResults=10
    ).execute()

    print("\n== Latest uploads ==")
    for item in vids.get("items", []):
        vid = item["contentDetails"]["videoId"]
        title = item["snippet"]["title"]
        print(f"{title}\thttps://youtu.be/{vid}")
