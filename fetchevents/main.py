#!/usr/bin/env python3
# *_* coding: utf-8 *_*
# Created by nb18422 at 09/03/2021
import tabulate

from fetchevents.meetupcrawl import meetup_ds_hamburg
from fetchevents.indico import indico_requests
from fetchevents.scrapedyncontt import crawl_ahoi
from fetchevents.scraper_ahoi import crawl_ai
import pandas as pd

def combine_sources():
    df1 = meetup_ds_hamburg()
    df2 = indico_requests()
    # df3 = crawl_ahoi()
    df4 = crawl_ai()
    df5 = meetup_ds_hamburg(url='https://www.meetup.com/de-DE/artificial-intelligence-center-hamburg-workshops-events/events/')
    df = pd.concat([df1,df2,df4,df5]).reset_index(drop=True)
    return df

def save_df_to_md(df, filename = "./fetchevents/ds_events.md", overwrite = "w"):
    tbdf = tabulate.tabulate(df.values, df.columns, tablefmt="pipe")
    # print(tbdf)
    # tbdf = df.to_markdown()
    # print(tbdf)
    f = open(filename, overwrite)
    f.write(tbdf)
    f.close()
    return None


if __name__ == "__main__":
    # meetup_ds_hamburg()
    df = combine_sources()
    print(df)
    # df.to_html('ds_events.html')
    save_df_to_md(df,filename = "ds_events.md")

