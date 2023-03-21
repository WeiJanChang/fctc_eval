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


def final_selected(df: pd.DataFrame,
                   column_drop: Optional[List[str]] = None,
                   save_path: Optional[Path] = None,
                   drop_na: Optional[List[str]] = None, ) -> pd.DataFrame:
    """

    :param df:
    :param column_drop:
    :param save_path:
    :param drop_na:
    :return:
    """
    df = df.copy()
    if column_drop is not None:
        df = df.drop(columns=column_drop)
    if drop_na is not None:  # drop rows with missing values ('NaN') from df
        try:
            df.dropna(subset=drop_na, inplace=True)
            # inplace = True means that the original df will be modified and no copy will be made.; But, if inplace =
            # False, df will still show the initial one. subset = drop_na means drop in specific place you set.
        except KeyError as e:
            raise ValueError(f'{e} not in the dataframe, should be one of the {df.columns.tolist()}')  # If
            # typed wrong, show the list which should be dropped.
    if save_path is not None:
        df.to_excel(save_path)

    return df


if __name__ == '__main__':
    df = pd.read_excel(
        '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/raw data/Signatures and Ratifications- UN '
        'Treaty Section_08 Feb_2023_Name chnaged.xlsx',
        engine='openpyxl')
    rename = {'Participant': 'Country Name',
              "Ratification, Acceptance(A), Approval(AA), Formal confirmation(c), Accession(a), Succession(d)": 'Ratification'}
    formatted_date = ['Signature', 'Ratification']
    save_path = '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/WHOFCTC_Parties_date_formatted.xlsx'
    df = format_date(df, rename_mapping=rename, formatted_date=formatted_date, save_path=save_path)
    # merge
    df1 = pd.read_excel(
        '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/merge_cvd_tobacco.xlsx',
        engine='openpyxl')
    column_drop = [
        'All_Estimate_of_current_cigarette_smoking_prevalence_age_standardized_rate',
        'Male_Estimate_of_current_cigarette_smoking_prevalence_age_standardized_rate',
        'Female_Estimate_of_current_cigarette_smoking_prevalence_age_standardized_rate']
    df1 = final_selected(df1, column_drop=column_drop)
    df2 = pd.read_excel(
        '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/WHOFCTC_Parties_date_formatted.xlsx',
        engine='openpyxl')

signed_df = pd.merge(df1, df2, on=['Country Name'], how='outer')
signed_df.fillna(value='NaN', inplace=True)
signed_df.to_excel('/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH '
                   'Dissertation/Data/WHOFCTC_Parties_signed_date.xlsx')

# drop_missing_data
signed_df.replace("NaN", np.nan, inplace=True)
signed_df.dropna(how='any', inplace=True)
signed_df.to_excel(
    "/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/WHOFCTC_Parties_date_no_missingdata.xlsx")
