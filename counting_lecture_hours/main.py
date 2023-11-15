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
    print(dfs)
    return pd.concat(dfs)


def prepare_data(df):
    """
    A function that prepares data for use in subsequent functions.
    :param df: data frame with events
    :return: processed data frame with events
    """
    df[["start_date", "end_date"]] = df["Godzina"].str.split("-", expand=True)
    df["start_date"] = pd.to_datetime(df["start_date"], format="%H:%M")
    df["end_date"] = pd.to_datetime(df["end_date"], format="%H:%M")
    df["time"] = df["end_date"] - df["start_date"]
    df = df[df["Grupa"].isin(["G", "GR2"])]
    df_h = df[["Przedmiot", "time"]]
    df_h = df_h.groupby(["Przedmiot"]).sum()
    return df_h


if __name__ == "__main__":
    data_frame = get_file()
    data_frame = prepare_data(data_frame)
    data_frame['time'] = data_frame['time']

