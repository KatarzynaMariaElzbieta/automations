from cal_setup import get_calendar_service
from const_config import ATTENDEES, CALENDAR_ID


def insert_event(data_df, description_text=""):
    """
    Function to add events with data frame to the calendar
    :param data_df:data frame with event data
    :param description_text: optional text to describe the event
    """
    service = get_calendar_service()
    for index, row in data_df.iterrows():
        start_date = row["start_date"]
        end_date = row["end_date"]
        service.events().insert(
            calendarId=CALENDAR_ID,
            body={
                "summary": row["summary"],
                "location": row["location"],
                "description": f'{description_text} {row["description"]}',
                "start": {"dateTime": start_date.isoformat(), "timeZone": "Europe/Warsaw"},
                "end": {"dateTime": end_date.isoformat(), "timeZone": "Europe/Warsaw"},
                # "attendees": ATTENDEES,
            },
        ).execute()
