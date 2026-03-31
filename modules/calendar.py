# -*- coding: utf-8 -*-
import os
import os.path
import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

PARTNER_EMAIL = os.getenv("PARTNER_EMAIL", "")

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

    def _date_range(self, start_raw, end_raw):
        """Returns list of all dates an event spans."""
        start_date = datetime.date.fromisoformat(start_raw.split('T')[0])
        if not end_raw:
            return [start_date]

        end_date = datetime.date.fromisoformat(end_raw.split('T')[0])

        # All-day events: Google sets end to day AFTER last day
        if 'T' not in start_raw:
            end_date -= datetime.timedelta(days=1)

        dates = []
        current = start_date
        while current <= end_date:
            dates.append(current)
            current += datetime.timedelta(days=1)
        return dates

    def get_upcoming_events(self):
        self.authenticate()
        service = build('calendar', 'v3', credentials=self.creds)

        now = datetime.datetime.utcnow().isoformat() + 'Z'
        events_result = service.events().list(
            calendarId='primary', timeMin=now,
            maxResults=50, singleEvents=True,
            orderBy='startTime').execute()

        events = events_result.get('items', [])
        colors_list = service.colors().get().execute().get('event', {})

        agenda_by_date = {}
        today = datetime.date.today()
        days_de = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

        for event in events:
            start_raw = event['start'].get('dateTime', event['start'].get('date'))
            end_raw = event['end'].get('dateTime', event['end'].get('date', None))

            # Get all days this event spans
            all_dates = self._date_range(start_raw, end_raw)

            # Detect partner events
            creator_email = event.get('creator', {}).get('email', '')
            is_partner = creator_email == PARTNER_EMAIL

            time_str = start_raw[11:16] if 'T' in start_raw else "Ganztag"
            color_id = event.get('colorId')
            bg_color = colors_list.get(color_id, {}).get('background', '#2ecc71')
            title = event.get('summary', 'Kein Titel')

            # Partner suffix
            if is_partner:
                title = title + " 💜"

            for event_date in all_dates:
                days_diff = (event_date - today).days
                if days_diff < 0:
                    continue

                date_str = event_date.isoformat()

                if days_diff == 0:
                    day_label = "Heute"
                elif days_diff == 1:
                    day_label = "Morgen"
                elif days_diff <= 6:
                    day_label = days_de[event_date.weekday()]
                else:
                    day_label = days_de[event_date.weekday()] + ", " + event_date.strftime("%d.%m.")

                if date_str not in agenda_by_date:
                    agenda_by_date[date_str] = {"label": day_label, "events": []}

                # For multi-day events show which day it is
                if len(all_dates) > 1:
                    day_num = (event_date - all_dates[0]).days + 1
                    display_title = f"{title} (Tag {day_num}/{len(all_dates)})"
                else:
                    display_title = title

                agenda_by_date[date_str]["events"].append({
                    "time": time_str if event_date == all_dates[0] else "↳",
                    "title": display_title,
                    "color": bg_color,
                    "is_partner": is_partner
                })

        # Sort chronologically
        agenda = {}
        for date_str in sorted(agenda_by_date.keys()):
            entry = agenda_by_date[date_str]
            agenda[entry["label"]] = entry["events"]

        return agenda