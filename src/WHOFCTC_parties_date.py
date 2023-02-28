"""
pipeline

Step 1:

        Download signature and ratification of FCTC raw data from UN
        https://treaties.un.org/pages/ViewDetails.aspx?src=TREATY&mtdsg_no=IX-4&chapter=9&clang=_en


Step 2:

        format date 'dd/mm/yy'
        header:['Country Name', 'Signature', 'Ratification']
        **188 (188, 3)**

Step 3:

        merge WHOFCTC_Parties_date_formatted.xlsx (n=188) and merge_cvd_tobacco.xlsx (n=89)
        drop_missing_data
        **82 (424, 22)**

step 4 :

        mask non-ratified parties
        **78 (400, 22)**


"""

import pandas as pd
from typing import Optional, List, Dict
from pathlib import Path
import numpy as np


def format_date(df: pd.DataFrame,
                rename_mapping: Dict[str, str] = None,
                formatted_date: Optional[List[str]] = None,
                save_path: Optional[Path] = None) -> pd.DataFrame:
    if rename_mapping is not None:
        df = df.rename(columns=rename_mapping)
    if formatted_date is not None:
        for col in formatted_date:
            df[col] = pd.to_datetime(df[col], infer_datetime_format=True)
            df[col] = df[col].dt.strftime("%d %b %Y")
    df.fillna(value='Nan', inplace=True)
    if save_path is not None:
        df.to_excel(save_path)
    return df


if __name__ == '__main__':
    df = pd.read_excel('/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/raw data/Signatures and '
                       'Ratifications- UN Treaty Section_08 Feb_2023 .xlsx', engine='openpyxl')
    rename = {'Participant': 'Country Name',
              "Ratification, Acceptance(A), Approval(AA), Formal confirmation(c), Accession(a), Succession(d)": 'Ratification'}
    formatted_date = ['Signature', 'Ratification']
    save_path = '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/WHOFCTC_Parties_date_formatted.xlsx'
    format_date(df, rename_mapping=rename, formatted_date=formatted_date, save_path=save_path)

# merge
df1 = pd.read_excel('/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/merge_cvd_tobacco.xlsx',
                    engine='openpyxl')
df2 = pd.read_excel('/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/WHOFCTC_Parties_date_formatted.xlsx',
                    engine='openpyxl')

signed_df = pd.merge(df1, df2, on=['Country Name'], how='outer')
signed_df.fillna(value='NaN', inplace=True)
signed_df.to_excel('/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/WHOFCTC_Parties_signed_date.xlsx')

# drop_missing_data
df = pd.read_excel('/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/WHOFCTC_Parties_signed_date.xlsx')
df = df.dropna(how='any')  # drop the rows having Nan
df = df.drop(columns=['Unnamed: 0', 'Unnamed: 0_x', 'Unnamed: 0_y'])
df.to_excel(
    '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/WHOFCTC_Parties_signed_date_no_missingdata.xlsx')

# mask non ratified parties

mask = df['Ratification'] != 'Nan'
df = df[mask]
df = df[df['Ratification'] != 'Nan']
df.to_excel('/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH '
            'Dissertation/Data/WHOFCTC_Parties_ratified_date_no_missingdata.xlsx')
