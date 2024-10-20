import datetime
import logging

from cal_setup import get_calendar_service


def select_to_remove(calendar_id):
    """
    Function retrieves existing events in calendar for deletion.
    :return: list of events to be removed.
    """
    service = get_calendar_service()
    now = datetime.datetime.utcnow().isoformat() + "Z"
    # 'Z' indicates UTC time
    events_result = (
        service.events().list(calendarId=calendar_id, timeMin=now,
                              singleEvents=True, orderBy="startTime").execute()
    )
    events = events_result.get("items", [])
    to_remove = []
    if not events:
        logging.info("No upcoming events found.")
    for event in events:
        if event["summary"].endswith("!"):
            service.events().update(
                calendarId=calendar_id, eventId=event["id"], body={"summary": event["summary"] + "_old"}
            )
        elif event["summary"].endswith("_old"):
            pass
        else:
            to_remove.append(event)
    return to_remove
