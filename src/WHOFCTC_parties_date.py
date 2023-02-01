"""
pipeline

Step 1: Setup dates in a uniform format

Step 2: drop Entities in cvd_tobacco which shows Nan in Ratification of WHO_FCTC_Parties_date_filter .xlsx

"""

import pandas as pd
from typing import Optional, List, Dict
from pathlib import Path
import numpy as np


def format_date(df: pd.DataFrame,
                rename_mapping: Dict[str, str] = None,
                uniform_date: Optional[List[str]] = None,
                save_path: Optional[Path] = None) -> pd.DataFrame:
    if rename_mapping is not None:
        df = df.rename(columns=rename_mapping)
    if uniform_date is not None:
        for col in uniform_date:
            df[col] = pd.to_datetime(df[col], infer_datetime_format=True)
            df[col] = df[col].dt.strftime('%d/%m/%Y')
    df.fillna(value='Nan', inplace=True)
    if save_path is not None:
        df.to_excel(save_path)
    return df


if __name__ == '__main__':
    df = pd.read_excel('/Users/wei/Python/MPHDissertation/test_file/WHO_FCTC_Parties_date_filter .xlsx')
    rename = {
        "Ratification, Acceptance(A), Approval(AA), Formal confirmation(c), Accession(a), Succession(d)": 'Ratification'}
    uniform_date = ['Signature', 'Ratification']
    # save_path = '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/WHOFCTC_Parties_date_filter.xlsx'
    # format_date(df, rename_mapping=rename, uniform_date=uniform_date, save_path=save_path)
    df1 = pd.read_excel('/Users/wei/Python/MPHDissertation/test_file/Final_CVD_Tobacco_merged.xlsx')

    entity_ratified = df1.mask(df1['Entity'].isin(['Argentina', 'Cuba', 'Switzerland']), np.nan)
    entity_ratified.dropna(subset=['Entity'], inplace=True)
    # entity_ratified.to_excel('entity_ratified_test.xlsx')
