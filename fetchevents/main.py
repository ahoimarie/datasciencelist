#!/usr/bin/env python3
# *_* coding: utf-8 *_*
# Created by nb18422 at 09/03/2021
import tabulate

from fetchevents.meetupcrawl import meetup_ds_hamburg
from fetchevents.indico import indico_requests
from fetchevents.scrapedyncontt import crawl_ahoi
import pandas as pd

def combine_sources():
    df1 = meetup_ds_hamburg()
    df2 = indico_requests()
    df3 = crawl_ahoi()
    df = pd.concat([df1,df2,df3]).reset_index(drop=True)
    return df

def save_df_to_md(df):
    tbdf = tabulate.tabulate(df.values, df.columns, tablefmt="pipe")
    # print(tbdf)
    # tbdf = df.to_markdown()
    print(tbdf)
    f = open("ds_events.md", "w")
    f.write(tbdf)
    f.close()
    return None


if __name__ == "__main__":
    # meetup_ds_hamburg()
    df = combine_sources()
    print(df)
    # df.to_html('ds_events.html')
    save_df_to_md(df)