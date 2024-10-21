"""
pipeline
Step 1: select 19 countries ratified in WHO FCTC after acknowledging the year with consistency
"""
from pathlib import Path
from typing import Optional, List, Union
import pandas as pd

PathLike = Union[Path, str]
__all__ = ['consistent_year', 'select_ratified_country']


def consistent_year(df: pd.DataFrame,
                    year_mask: Optional[List[int]] = None,
                    save_path: Optional[Path] = None) -> pd.DataFrame:
    """
    :param df: WHOFCTC_Parties_date_no_missingdata.xlsx
    :param year_mask: as Time Series, the Year should have regular interval.
    and now the year includes 2000, 2005, 2010, 2015, 2018, 2019, and 2020. So, the year 2018 and 2019 should be excluded.
    :param save_path: save modified dataframe to another excel
    :return: interval_df
    """
    interval_df = df.copy()
    if year_mask is not None:
        mask = ~interval_df['Year'].isin([2018, 2019])  # create boolean mask to exclude rows with 2018 and 2019
        interval_df = interval_df[mask]  # select rows that are not excluded by the mask
    interval_df = interval_df.reset_index(drop=True)
    if save_path is not None:
        interval_df.to_excel(save_path)
    return interval_df


def select_ratified_country(df: pd.DataFrame, output_path: PathLike = None) -> pd.DataFrame:
    """
    To select targets for analysis
    :param df: df
    :param output_path: output path
    :return: selected_19_df
    """
    interval_df = consistent_year(df, year_mask=[2018, 2019])
    count_df = interval_df['Country Name'].value_counts().to_frame()
    count_df.columns = ['count']  # choose the most datapoint of countries
    df = interval_df.copy()
    selected_19_countries = ['Estonia', 'Costa Rica', 'Mexico', 'Czechia', 'Netherlands', 'Georgia', 'Spain',
                             'Singapore', 'Latvia', 'Germany', 'Guatemala', 'Kazakhstan', 'Austria', 'Serbia',
                             'Lithuania', 'Ecuador', 'Iceland', 'Slovenia', 'Mauritius', ]
    selected_19_df = df[df.isin(selected_19_countries).any(axis=1)].dropna(how='all')

    if output_path is not None:
        selected_19_df.to_excel(output_path, index=False)
    return selected_19_df
