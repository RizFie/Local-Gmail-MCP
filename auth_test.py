
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

token_path = os.path.join(BASE_DIR, "token.json")
cred_path = os.path.join(BASE_DIR, "credentials.json")


def authenticate_gmail():
    creds = None

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(
            token_path, SCOPES
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                cred_path, SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as token:
            token.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


if __name__ == "__main__":
    service = authenticate_gmail()

    profile = service.users().getProfile(
        userId="me"
    ).execute()

    print("Gmail authentication successful!")
    print("Connected account:", profile["emailAddress"])
    print("Total messages:", profile["messagesTotal"])
