#!/usr/bin/env python3
# *_* coding: utf-8 *_*
# Created by nb18422 at 09/03/2021

from meetupcrawl import meetup_ds_hamburg
from indico import indico_requests
from scrapedyncontt import crawl_ahoi
import pandas as pd

def combine_sources():
    df1 = meetup_ds_hamburg()
    df2 = indico_requests()
    df3 = crawl_ahoi()
    df = pd.concat([df1,df2,df3]).reset_index(drop=True)
    return df

if __name__ == "__main__":
    # meetup_ds_hamburg()
    df = combine_sources()
    print(df)