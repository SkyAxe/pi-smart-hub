# -*- coding: utf-8 -*-
import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

class CalendarModule:
    def __init__(self):
        self.scopes = ['https://www.googleapis.com/auth/calendar.readonly']
        self.creds = None
        self.creds_path = 'credentials.json'
        self.token_path = 'token.json'

    def authenticate(self):
        if os.path.exists(self.token_path):
            self.creds = Credentials.from_authorized_user_file(self.token_path, self.scopes)
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(self.creds_path, self.scopes)
                self.creds = flow.run_local_server(port=0)
            with open(self.token_path, 'w') as token:
                token.write(self.creds.to_json())

    def get_upcoming_events(self):
        self.authenticate()
        service = build('calendar', 'v3', credentials=self.creds)

        now = datetime.datetime.utcnow().isoformat() + 'Z'
        # Fetch more events — 50 to be safe
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=50, singleEvents=True,
            orderBy='startTime').execute()

        events = events_result.get('items', [])
        colors_list = service.colors().get().execute().get('event', {})

        agenda = {}
        today = datetime.date.today()
        days_de = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

        for event in events:
            start_raw = event['start'].get('dateTime', event['start'].get('date'))
            date_str = start_raw.split('T')[0]
            event_date = datetime.date.fromisoformat(date_str)

            days_diff = (event_date - today).days
            if days_diff < 0:
                continue
            # No hard limit on days — show as many as we have

            if days_diff == 0:
                day_label = "Heute"
            elif days_diff == 1:
                day_label = "Morgen"
            else:
                day_label = days_de[event_date.weekday()] + ", " + event_date.strftime("%d.%m.")

            if day_label not in agenda:
                agenda[day_label] = []

            time_str = start_raw[11:16] if 'T' in start_raw else "Ganztag"
            color_id = event.get('colorId')
            bg_color = colors_list.get(color_id, {}).get('background', '#2ecc71')

            agenda[day_label].append({
                "time": time_str,
                "title": event.get('summary', 'Kein Titel'),
                "color": bg_color
            })

        return agenda