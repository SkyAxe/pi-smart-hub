from google_auth_oauthlib.flow import InstalledAppFlow
import os

# Exactly the same settings as your module
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def get_creds():
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    # This will open ONE browser window and wait.
    creds = flow.run_local_server(port=0)
    
    with open('token.json', 'w') as token:
        token.write(creds.to_json())
    print("\n--- SUCCESS! token.json created. You can close this now. ---")

if __name__ == "__main__":
    get_creds()
