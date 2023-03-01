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
    format_date(df, rename_mapping=rename, formatted_date=formatted_date, save_path=save_path)

# merge
df1 = pd.read_excel('/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/merge_cvd_tobacco.xlsx',
                    engine='openpyxl')
df2 = pd.read_excel('/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/WHOFCTC_Parties_date_formatted.xlsx',
                    engine='openpyxl')

signed_df = pd.merge(df1, df2, on=['Country Name'], how='outer')
signed_df.fillna(value='NaN', inplace=True)
signed_df.to_excel('/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH '
                   'Dissertation/Data/WHOFCTC_Parties_signed_date.xlsx')
column_drop = ['All_Estimate_of_current_cigarette_smoking_prevalence_age_standardized_rate',
               'Male_Estimate_of_current_cigarette_smoking_prevalence_age_standardized_rate',
               'Female_Estimate_of_current_cigarette_smoking_prevalence_age_standardized_rate']
drop_na = ['Unnamed: 0_x', 'Unnamed: 0_y', 'All_Number_of_Cause_Specific_Deaths',
           'Female_Number_of_Cause_Specific_Deaths',
           'Male_Number_of_Cause_Specific_Deaths', 'All_Total_Number_of_Deaths',
           'Female_Total_Number_of_Deaths', 'Male_Total_Number_of_Deaths',
           'All_Total_Percentage_of_Cause_Specific_Deaths_Out_Of_Total_Deaths',
           'Female_Total_Percentage_of_Cause_Specific_Deaths_Out_Of_Total_Deaths',
           'Male_Total_Percentage_of_Cause_Specific_Deaths_Out_Of_Total_Deaths',
           'All_Estimate_of_Current_Tobacco_Use_Prevalence_age_standardized_rate',
           'Male_Estimate_of_Current_Tobacco_Use_Prevalence_age_standardized_rate',
           'Female_Estimate_of_Current_Tobacco_Use_Prevalence_age_standardized_rate',
           'All_Estimate_of_Current_Tobacco_Smoking_Prevalence_age_standardized_rate',
           'Male_Estimate_of_Current_Tobacco_Smoking_Prevalence_age_standardized_rate',
           'Female_Estimate_of_Current_Tobacco_Smoking_Prevalence_age_standardized_rate',
           'Signature', 'Ratification']
save_path = (
    '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/WHOFCTC_Parties_signed_date_no_cigarettesmoking.xlsx')
new_df = final_selected(signed_df, column_drop=column_drop, drop_na=drop_na, save_path=save_path)

new_df.replace("NaN", np.nan, inplace=True)
new_df.dropna(how='any', inplace=True)
new_df.to_excel("/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/WHOFCTC_Parties_date_no_missingdata.xlsx")
new_df1 = new_df
new_df1.replace("Nan", np.nan, inplace=True)
new_df1.dropna(how='any', inplace=True)
new_df1.to_excel(
    "/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/WHOFCTC_ratified Parties_no_missingdata.xlsx")
print(new_df1['Country Name'].unique(), len(new_df1['Country Name'].unique()), new_df1.shape, new_df1.columns.tolist())

counts_df = new_df1['Country Name'].value_counts().to_frame()

counts_df.columns = ['count']
counts_df.to_excel("/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/count_country.xlsx")

# select specific country in df
# 找出所有包含指定值的行
result_df = new_df1[new_df1.isin(
    ['Iceland', 'Netherlands', 'Spain', 'Germany', 'Czechia', 'Lithuania', 'Mauritius', 'Kazakhstan', 'Latvia',
     'Costa Rica', 'Estonia', 'Ecuador', 'Serbia', 'Georgia', 'Slovenia', 'Guatemala', 'Mexico', 'Austria',
     'Singapore']).any(axis=1)].dropna(how='all')

result_df.to_excel("/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/19_ratified_country.xlsx")

