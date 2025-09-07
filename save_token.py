import json, os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Start a local server auth flow using your client_secret.json
    flow = InstalledAppFlow.from_client_secrets_file("client_secret.json", SCOPES)
    creds = flow.run_local_server(port=0)
    # Save the credentials so other scripts can reuse them
    with open("token.json","w") as f:
        f.write(creds.to_json())
    print("Wrote token.json at:", os.path.abspath("token.json"))

if __name__ == "__main__":
    main()
