# from_pdf_to_calendar
The project allows you to enter events read from pdf into google calendar as a table.

The pdf is loaded into a pandas data frame - which should be
adjusted accordingly by changing the prepare_data function
so that it contains columns:
- start_date, 
- end_date,
- summary,
- location,
- description.

#### Note future events existing so far in the calendar will be deleted (unless they end with ! or _old).
Then new events will be added with duration dates corresponding to the range between 
start_date and end_date, name from the summary field, location from location,
and description -optional custom text + content from the description column.

## Before you start
Before you start prepare:
- the pdf you want to process - the data in it should be in the form of a table
- Make sure you have tkinter installed
  - If not `sudo apt-get install python3-tk`.
- Get `oauth 2.0 client credentials ` - place the client_secret file in the folder from_pdf_to_callendar.
- In the const_config.py file put:
  - the name of the client_secret file,
  - the id of the calendar on which the changes will be made,
  - the list of dictionaries with the emails of the meeting participants
  