from cal_setup import get_calendar_service
from const_config import CALENDAR_ID


def remove_events(events_list):
    """
    Function removes events from the specified list from the calendar.
    :param events_list: List of events to be removed
    """
    service = get_calendar_service()
    for event in events_list:
        service.events().delete(calendarId=CALENDAR_ID, eventId=event["id"]).execute()
    print("Old removed")
