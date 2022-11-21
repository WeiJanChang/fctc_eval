from pathlib import Path
from typing import Optional, List

import pandas as pd

from who_membership import WHO_MEMBERSHIP

__all__ = ['select_df']


def select_df(df: pd.DataFrame,
              column_drop: Optional[List[str]] = None,
              year: int = 2000,
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

    year_mask = df['Year'] > year
    entity_mask = [country in WHO_MEMBERSHIP for country in df['Entity']]
    ret = df[year_mask & entity_mask].reset_index(drop=True)

    if save_path is not None:
        ret.to_csv(save_path)

    return ret
