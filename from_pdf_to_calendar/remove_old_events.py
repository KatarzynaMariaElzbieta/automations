import logging

from cal_setup import get_calendar_service


def remove_events(calendar_id, events_list):
    """
    Function removes events from the specified list from the calendar.
    :param calendar_id: ID of google calendar
    :param events_list: List of events to be removed
    """
    service = get_calendar_service()
    for event in events_list:
        service.events().delete(calendarId=calendar_id, eventId=event["id"]).execute()
    logging.info("Old removed")
