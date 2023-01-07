from pathlib import Path  # pathlib: module, Path: class. Checking if a path exist
from typing import Optional, List, Dict  # typing: support for type hint
import pandas as pd
from who_member_states import WHO_MEMBER_STATES

__all__ = ['select_df']  # only import 'select_df'


def select_df(df: pd.DataFrame,
              rename_mapping: Dict[str, str] = None,
              column_drop: Optional[List[str]] = None,  # column_drop (param) is an optional list of string. Optional
              # type is from Typing. default is None (no drop any column). If provide column_drop, must be ['xxx'] (
              # list of string)
              year: int = 2000,
              save_path: Optional[Path] = None,
              drop_na: Optional[List[str]] = None, ) -> pd.DataFrame:
    """
    dataframe modification and save as another file

    :param rename_mapping: both df have countries but the header is different
    :param df: input dataframe
    :param column_drop: drop the column(s) that are not informative
    :param year: pick up the data that larger than which year
    :param save_path: path for saving the modified dataframe
    :param drop_na: specify if drop the na-existing column name
    :return: modified df
    """

    df = df.copy()  # The copy() method returns a copy of the DataFrame. By default, the copy is a "deep copy"
    # meaning that any changes  made in the original DataFrame will NOT be reflected in the copy. 新跑出來的df不會影響最原始的df

    if rename_mapping is not None:
        df = df.rename(columns=rename_mapping)
    if column_drop is not None:  # if drop specific column,df need to drop the option
        df = df.drop(columns=column_drop)  # df 的column = column after drop, column_drop: Optional[List[str]]

    year_mask: pd.Series[bool] = df['Year'] >= year  # type is list of bool; compared df["year"] whether larger than
    # default year (year: int = 2000)
    entity_mask: List[bool] = [country in WHO_MEMBER_STATES for country in df['Entity']]  # check countries whether
    # in df['Entity'] also in WHO_MEMBER_STATES. If Yes =True
    _df: pd.DataFrame = df[year_mask & entity_mask].reset_index(drop=True)  # create a new df that only meet both
    # year_mask and entity_mask. df.reset_index(drop = True) means new index created, old index don't added in new df.

    if drop_na is not None:  # drop rows with missing values ('NaN') from df
        try:
            _df.dropna(subset=drop_na, inplace=True)
        # inplace = True means that the original df will be modified and no copy will be made.; But, if inplace = False,
        # df will still show the initial one. subset = drop_na means drop in specific place you set.
        except KeyError as e:
            raise ValueError(f'{e} not in the dataframe, should be one of the {_df.columns.tolist()}')  # If
            # typed wrong, show the list which should be dropped.
    if save_path is not None:
        _df.to_csv(Path)

    return _df
