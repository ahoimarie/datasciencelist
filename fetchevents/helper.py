import datefinder
import pandas as pd


def split_datetime(text):
    """Find a datetime object in a textstring and return date and time separately"""

    try:
        matches = list(datefinder.find_dates(text))

        d = {'DateTime': [matches[0]]}
        df1 = pd.DataFrame(data=d)
        date = df1['DateTime'].dt.strftime('%Y-%m-%d')
        time = df1['DateTime'].dt.strftime('%H:%M')
    except IndexError:
        date, time = None, None

    return date,time