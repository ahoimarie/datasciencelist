#!/usr/bin/env python3
# *_* coding: utf-8 *_*
# Created by nb18422 at 11/03/2021
#test_main.py

import pytest
from fetchevents.main import save_df_to_md
import os
import types
script_dir = os.path.dirname(__file__)
from pathlib import Path


def test_save_df_to_md():
    import pandas as pd
    data = [['Alex', 10], ['Bob', 12], ['Clarke', 13]]
    df = pd.DataFrame(data, columns=['Name', 'Age'])

    # rel_path = 'testfiles'
    # FILEPATH = os.path.join(script_dir, rel_path)
    # print(FILEPATH)
    save_df_to_md(df, "./tests/testfiles/testfile.md")
    import filecmp
    # filecmp.cmp('./tests/testfiles/testfile.md', './tests/testfiles/valifile.md')

    assert(filecmp.cmp('./tests/testfiles/testfile.md', './tests/testfiles/valifile.md'))


if __name__ == "__main__":
    test_save_df_to_md()
    print("Everything passed")