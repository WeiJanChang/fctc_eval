"""
pipeline

Setup dates in a uniform format

"""

import pandas as pd
from typing import Optional, List
from pathlib import Path


def format_date(df: pd.DataFrame,
                uniform_date: Optional[List[str]] = None,
                save_path: Optional[Path] = None) -> pd.DataFrame:
    if uniform_date is not None:
        for col in uniform_date:
            df[col] = pd.to_datetime(df[col], infer_datetime_format=True)
            df[col] = df[col].dt.strftime('%d/%m/%Y')
    if save_path is not None:
        df.to_excel(save_path)
    return df

"""
if __name__ == '__main__':
    df = pd.read_excel('/Users/wei/Python/MPHDissertation/test_file/WHO_FCTC_Parties_date_filter .xlsx')
    uniform_date = ['Signature',
                    'Ratification, Acceptance(A), Approval(AA), Formal confirmation(c), Accession(a), Succession(d)']
    save_path = '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/WHOFCTC_Parties_date_filter.xlsx'
    format_date(df, uniform_date=uniform_date, save_path=save_path)

"""