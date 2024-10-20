import datetime
from tkinter.filedialog import askopenfilename

import pandas as pd
import tabula
import numpy as np


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


def change_group(row):
    if row['Przedmiot'] == 'JĘZYK ANGIELSKI':
        if row['Grupa'] == 'GR1':
            return 'GR2'
        elif row['Grupa'] == 'GR2':
            return 'GR1'
    return row['Grupa']

def prepare_data(df):
    """
    A function that prepares data for use in subsequent functions.
    :param df: data frame with events
    :return: processed data frame with events
    """
    df = df.rename(columns={"Unnamed: 0": "Przedmiot"})
    df[["start_date", "end_date"]] = df["Godzina"].str.split("-", expand=True)
    # df["start_date"] = df["Data"] + " " + df["start_date"]
    # df["end_date"] = df["Data"] + " " + df["end_date"]
    df["start_date"] = pd.to_datetime(df["start_date"], format="%H:%M")
    df["end_date"] = pd.to_datetime(df["end_date"], format="%H:%M")
    df["time"] = df["end_date"] - df["start_date"]
    print(df)

    df['grupa'] = df.apply(change_group, axis=1)
    print(df)
    df = df[df["Grupa"].isin(["G", "GR1"])]
    df_h = df[["Przedmiot", "time"]]
    df_h = df_h.groupby(["Przedmiot"]).sum()
    # df = df[df["start_date"] > datetime.datetime.now()]
    # df = df.rename(columns=COLUMNS_NAMES)
    return df_h


if __name__ == "__main__":
    data_frame = get_file()
    print('-'*60)
    print(data_frame.columns)
    print('-'*60)
    data_frame = prepare_data(data_frame)
    data_frame['time'] = (data_frame['time'].dt.total_seconds()/60)/45
    print(data_frame)
    print(data_frame.dtypes)
