#util,utility
from pathlib import Path
from typing import Optional, List

import pandas as pd

from who_membership import WHO_MEMBERSHIP

__all__ = ['select_df'] #__ __ python習慣用法


def select_df(df: pd.DataFrame,
              column_drop: Optional[List[str]] = None,
              year: int = 2000, #default 2000
              save_path: Optional[Path] = None) -> pd.DataFrame:
    """
    TODO write by yourself xxx
    :param df:
    :param column_drop:
    :param year:
    :param save_path:
    :return:
    """
    df = df.copy()
    if column_drop is not None:
        df = df.drop(columns=column_drop)

    year_mask: pd.Series[bool] = df['Year'] > year #type is list of bool; 比較df["year"]有沒有> default 的year
    entity_mask :List[bool]= [country in WHO_MEMBERSHIP for country in df['Entity']] 
        #在df裡Entity 裡的country有沒有也在who membership 裡，有的就True.
    ret:pd.DataFrame = df[year_mask & entity_mask].reset_index(drop=True) 
        #使用新的索引 df.reset_index; 把drop掉的也不要加進去新df裡(drop=True), ret=return

    if save_path is not None:
        ret.to_csv(save_path)

    return ret
