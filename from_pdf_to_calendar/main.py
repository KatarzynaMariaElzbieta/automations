import datetime
import logging
from tkinter.filedialog import askopenfilename

import pandas as pd
import tabula

from from_pdf_to_calendar.const_config import GROUPS_CALENDARS
from insert_event_to_calendar import insert_event
from list_events import select_to_remove
from remove_old_events import remove_events

from const_config import COLUMNS_NAMES


def change_group_name(row):
    if row['Przedmiot'] == 'JĘZYK ANGIELSKI':
        return row['Grupa'] + row['Przedmiot']
    return row['Grupa']


def get_file():
    """
    Function that converts open pdf to pandas data frame
    :return: data frame
    """
    filename = askopenfilename()
    if not filename.endswith(".pdf"):
        logging.error("wrong file format")
    dfs = tabula.read_pdf(filename, pages="all")
    return pd.concat(dfs)


def prepare_time_col(df, column_name):
    df[column_name] = df["Data"] + " " + df[column_name]
    df[column_name] = pd.to_datetime(df[column_name], format="%d.%m.%Y %H:%M")
    return df


def prepare_data(df):
    """
    A function that prepares data for use in subsequent functions.
    :param df: data frame with events
    :return: processed data frame with events
    """
    df = df.rename(columns={"Unnamed: 0": "Przedmiot"})
    df[["start_date", "end_date"]] = df["Godzina"].str.split("-", expand=True)
    df["start_date"] = df["Data"] + " " + df["start_date"]
    df["end_date"] = df["Data"] + " " + df["end_date"]
    df["start_date"] = pd.to_datetime(df["start_date"], format="%d.%m.%Y %H:%M")
    df["end_date"] = pd.to_datetime(df["end_date"], format="%d.%m.%Y %H:%M")
    df['grupa'] = df.apply(change_group_name, axis=1)

    df = df[df["start_date"] > datetime.datetime.now()]
    df = df.rename(columns=COLUMNS_NAMES)
    return df


if __name__ == "__main__":
    data_frame = get_file()
    data_frame = prepare_data(data_frame)
    for group, values in GROUPS_CALENDARS.items():
        df_g = data_frame.copy()
        df_g = df_g[df_g['grupa'].isin(values['groups'])]
        ro_rm = select_to_remove(calendar_id=values['calendar'])
        insert_event(values['calendar'], df_g)
        if ro_rm:
            remove_events(values['calendar'], ro_rm)
        logging.info(f"The data in {values['calendar']} has been updated")
