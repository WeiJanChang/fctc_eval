# util,utility
from pathlib import Path
from typing import Optional, List

import pandas as pd

from who_membership import WHO_MEMBERSHIP

__all__ = ['select_df']


# __ __ python習慣用法


def select_df(df: pd.DataFrame,
              column_drop: Optional[List[str]] = None,
              year: int = 2000,
              save_path: Optional[Path] = None,
              drop_na: Optional[List[str]] = None) -> pd.DataFrame:
    """
    dataframe modification and save as another file

    :param df: input dataframe
    :param column_drop: drop the column(s) that are not informative
    :param year: pick up the data that larger than which year
    :param save_path: path for saving the modified dataframe
    :param drop_na: specify if drop the na-existing column name

    :return:
    """
    df = df.copy()
    if column_drop is not None:
        df = df.drop(columns=column_drop)

    # type is list of bool; 比較df["year"]有沒有> default 的year
    year_mask: pd.Series[bool] = df['Year'] > year
    # 在df裡Entity 裡的country有沒有也在who membership 裡，有的就True.
    entity_mask: List[bool] = [country in WHO_MEMBERSHIP for country in df['Entity']]
    # 使用新的索引 df.reset_index; 把drop掉的也不要加進去新df裡(drop=True), ret=return
    _df: pd.DataFrame = df[year_mask & entity_mask].reset_index(drop=True)

    if drop_na is not None:
        try:
            _df.dropna(subset=drop_na, inplace=True)
        except KeyError as e:
            raise ValueError(f'{e} not in the dataframe, should be one of the {_df.columns.tolist()}')


    if save_path is not None:
        _df.to_csv(save_path)

    return _df
