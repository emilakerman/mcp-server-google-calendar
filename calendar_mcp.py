
from typing import Any
from mcp.server.fastmcp import FastMCP
import datetime
import random
from calendar_event import CalendarEvent


# Google Calendar API imports
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build


print("[calendar_mcp.py] Calendar MCP server starting...")
mcp = FastMCP("calendar")


SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_PATH = "service_account.json"


def get_calendar_service():
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_PATH,
        scopes=SCOPES
    )
    service = build("calendar", "v3", credentials=creds)
    return service

def get_month_range():
    now = datetime.datetime.now()
    start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if now.month == 12:
        end = start.replace(year=now.year+1, month=1)
    else:
        end = start.replace(month=now.month+1)
    return start.isoformat() + 'Z', end.isoformat() + 'Z'



@mcp.tool()
async def create_calendar_event(calendarEvent: CalendarEvent) -> str:
    """Create a Google Calendar event with the given details."""
    try:
        service = get_calendar_service()
        event = {
            'summary': calendarEvent.summary,
            'location': calendarEvent.location,
            'description': calendarEvent.description + (f"\nLivestream: {calendarEvent.livestream_url}" if calendarEvent.livestream_url else ""),
            'start': {'dateTime': calendarEvent.start_time, 'timeZone': 'UTC'},
            'end': {'dateTime': calendarEvent.end_time, 'timeZone': 'UTC'},
        }
        created_event = service.events().insert(calendarId='rustyjimmies@gmail.com', body=event).execute()
        return f"Event created: {created_event.get('htmlLink')}"
    except Exception as e:
        return f"Error creating event: {e}"


@mcp.tool()
async def summarize_upcoming_events() -> str: 
    """Summarize upcoming Google Calendar events for this month."""
    print("[calendar_mcp.py] summarize_upcoming_events called")
    try:
        service = get_calendar_service()
        start, end = get_month_range()
        events_result = service.events().list(
            calendarId='rustyjimmies@gmail.com', timeMin=start, timeMax=end,
            singleEvents=True, orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        if not events:
            print("[calendar_mcp.py] No events returned from API.")
            return "No upcoming events found for this month."
        summary = []
        for event in events:
            start_time = event['start'].get('dateTime', event['start'].get('date'))
            summary.append(f"- {event.get('summary', 'No Title')} at {start_time}")
        return f"Upcoming events for this month:\n" + "\n".join(summary)
    except Exception as e:
        print(f"[calendar_mcp.py] Error in summarize_upcoming_events: {e}")
        return f"Error fetching events: {e}"

@mcp.tool()
async def delete_random_event() -> str:
    """Delete a random upcoming Google Calendar event for this month."""
    print("[calendar_mcp.py] delete_random_event called")
    try:
        service = get_calendar_service()
        start, end = get_month_range()
        events_result = service.events().list(
            calendarId='rustyjimmies@gmail.com', timeMin=start, timeMax=end,
            singleEvents=True, orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        if not events:
            print("[calendar_mcp.py] No events returned from API for deletion.")
            return "No upcoming events to delete for this month."
        event = random.choice(events)
        event_id = event['id']
        event_summary = event.get('summary', 'No Title')
        event_time = event['start'].get('dateTime', event['start'].get('date'))
        service.events().delete(calendarId='rustyjimmies@gmail.com', eventId=event_id).execute()
        return f"Deleted event: {event_summary} at {event_time}"
    except Exception as e:
        print(f"[calendar_mcp.py] Error in delete_random_event: {e}")
        return f"Error deleting event: {e}"



if __name__ == "__main__":
    mcp.run()