import os
import json

from .google.auth.transport.requests import Request
from .google.oauth2             import credentials
from .google_auth_oauthlib.flow import InstalledAppFlow
from .googleapiclient.discovery import build
from .googleapiclient.errors import HttpError

def authenticate(SCOPES, CACHE=False):

    # initialize credentials object from 'google.oauth2'
    creds = None

    # get state of credentials
    if os.path.exists('token.json'):
        creds = credentials.Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # Check credentials valid, or empty
    if not creds or not creds.valid:

        # if credentials valid, but expired
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        # Initalialize, if not valid
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'desktop.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        if CACHE == True:
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

    return json.loads(creds.to_json())


