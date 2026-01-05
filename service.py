from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import pickle
from email.mime.text import MIMEText
import base64

# Authenticate and the Gmail API service

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.compose']

def authenticate_gmail():
   creds = None
   if os.path.exists('token.pickle'):
       with open('token.pickle', 'rb') as token:
           creds = pickle.load(token)
   if not creds or not creds.valid:
       if creds and creds.expired and creds.refresh_token:
           creds.refresh(Request())
       else:
           flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
           try:
               creds = flow.run_local_server(port=0)
           except Exception:
               # If the local server approach fails (firewall, selector issues, headless),
               # fall back to the console auth flow where the user pastes the code.
               creds = flow.run_console()
       with open('token.pickle', 'wb') as token:
           pickle.dump(creds, token)
   return build('gmail', 'v1', credentials=creds, cache_discovery=False)
