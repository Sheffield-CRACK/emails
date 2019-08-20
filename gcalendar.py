from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import yagmail

user = 'astro.coffee.sheffield@gmail.com'   # address to download and send email from
pwd = 'crack_astro'
recipient = []
with open('crack_emails.txt') as f:
    recipient.extend(f.read().split())

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='sheffield.ac.uk_ghkciehdbqhtm6864g6o62c3k0@group.calendar.google.com',
                                        timeMin=now, maxResults=1, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        start = start[:-15]
        start = datetime.datetime.strptime(start, "%Y-%m-%d").date()
        if start == datetime.date.today():
            contents = '🚀🔭 Reminder: ' + event['summary'] + ' 🚀🔭'
            yag = yagmail.SMTP(user, pwd)
            yag.send(recipient, contents, contents) 

if __name__ == '__main__':
    main()


#calendarId='primary'