import datetime
from tkinter.filedialog import askopenfilename

import pandas as pd
import tabula
from insert_event_to_calendar import insert_event
from list_events import select_to_remove
from remove_old_events import remove_events

from from_pdf_to_calendar.const_config import COLUMNS_NAMES


def get_file():
    """
    Function that converts open pdf to pandas data frame
    :return: data frame
    """
    filename = askopenfilename()
    if not filename.endswith(".pdf"):
        print("wrong file format")
    dfs = tabula.read_pdf(filename, pages="all")
    return pd.concat(dfs)


def prepare_data(df):
    """
    A function that prepares data for use in subsequent functions.
    :param df: data frame with events
    :return: processed data frame with events
    """
    df[["start_date", "end_date"]] = df["Godzina"].str.split("-", expand=True)
    df["start_date"] = df["Data"] + " " + df["start_date"]
    df["end_date"] = df["Data"] + " " + df["end_date"]
    df["start_date"] = pd.to_datetime(df["start_date"], format="%d.%m.%Y %H:%M")
    df["end_date"] = pd.to_datetime(df["end_date"], format="%d.%m.%Y %H:%M")
    df = df[df["Grupa"].isin(["G", "GR2"])]
    df = df[df["start_date"] > datetime.datetime.now()]
    df = df.rename(COLUMNS_NAMES)
    return df


if __name__ == "__main__":
    data_frame = get_file()
    data_frame = prepare_data(data_frame)
    ro_rm = select_to_remove()
    insert_event(data_frame)
    remove_events(ro_rm)
    print("The data has been updated")
