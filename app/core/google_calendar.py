import os
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv
from typing import Optional
from googleapiclient import errors

load_dotenv()

CREDENTIALS_FILE = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
COMMON_CALENDAR_ID = os.getenv("COMMON_CALENDAR_ID")


SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Initialise la connexion avec le Compte de Service Google."""
    if not CREDENTIALS_FILE or not os.path.exists(CREDENTIALS_FILE):
        raise ValueError(f"Fichier credentials introuvable: {CREDENTIALS_FILE}")
        
    creds = service_account.Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES)
    return build('calendar', 'v3', credentials=creds)


def add_user_to_common_calendar(user_email: str):
    """Ajoute un utilisateur au calendrier commun de l'organisation."""
    if not COMMON_CALENDAR_ID:
        print("Erreur : COMMON_CALENDAR_ID non configuré dans le .env")
        return
        
    service = get_calendar_service()
    
    rule = {
        'scope': {
            'type': 'user',
            'value': user_email,
        },
        'role': 'writer'
    }
    
    service.acl().insert(
        calendarId=COMMON_CALENDAR_ID, 
        body=rule, 
        sendNotifications=True
    ).execute()



def export_task_to_calendar(
    calendar_id: str, 
    title: str, 
    description: Optional[str] = None, 
    due_date: Optional[datetime.datetime] = None,
    color_id: Optional[str] = None
):
    service = get_calendar_service()
    
    target_date = due_date if due_date else datetime.datetime.now()
    date_str = target_date.strftime("%Y-%m-%d")
    end_date_str = (target_date + datetime.timedelta(days=1)).strftime("%Y-%m-%d")

    event = {
        'summary': title,
        'description': description or "",
        'start': {'date': date_str},
        'end': {'date': end_date_str},
        'colorId': color_id
    }

    created_event = service.events().insert(calendarId=calendar_id, body=event).execute()
    return {
        "id": created_event.get('id'),
        "link": created_event.get('htmlLink')
    }
    
def delete_calendar_event(calendar_id: str, event_id: str):
    if not calendar_id or not event_id:
        return
        
    service = get_calendar_service()
    try:
        service.events().delete(
            calendarId=calendar_id, 
            eventId=event_id
        ).execute()
    except Exception as e:
        if "404" in str(e):
            return
        raise e