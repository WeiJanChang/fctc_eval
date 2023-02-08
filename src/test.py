from pathlib import Path
from typing import Optional, List, Dict, Tuple
import pandas as pd
import numpy as np
import collections
from pprint import pprint  # pprint.pprint() can use when you need to examine the structure of a large or complex

from who_member_states import WHO_MEMBER_STATES

__all__ = ['select_df']


def select_df(df: pd.DataFrame,
              rename_mapping: Dict[str, str] = None,
              column_drop: Optional[List[str]] = None,
              year: int = 2000,
              save_path: Optional[Path] = None,
              drop_na: Optional[List[str]] = None, ) -> pd.DataFrame:
    df = df.copy()
    if rename_mapping is not None:
        df = df.rename(columns=rename_mapping)
    if column_drop is not None:
        df = df.drop(columns=column_drop)

    year_mask: pd.Series[bool] = df['Year'] >= year

    entity_mask: List[bool] = [country in WHO_MEMBER_STATES for country in df['Country Name']]

    modified_df: pd.DataFrame = df[year_mask & entity_mask].reset_index(
        drop=True)
    if drop_na is not None:
        try:
            modified_df.dropna(subset=drop_na, inplace=True)

        except KeyError as e:
            raise ValueError(f'{e} not in the dataframe, should be one of the {modified_df.columns.tolist()}')
    if save_path is not None:
        modified_df.to_excel(save_path)

    return modified_df


def preprocess_cvd(df: pd.DataFrame,
                   drop_na: Optional[List[str]] = None,
                   save_path: Optional[Path] = None) -> pd.DataFrame:
    numbers = df['Number']
    percentage = df['Percentage of cause-specific deaths out of total deaths']
    df["Total Number of Cause-Specific Deaths"] = numbers * 100 / percentage
    total_number_of_death = df["Total Number of Cause-Specific Deaths"]
    mask_nan = np.isnan(total_number_of_death)  # type: pd.Series[bool] # if value is NaN, NaN = True

    df.loc[
        mask_nan, "Total Number of Cause-Specific Deaths"] = 0

    df["Total Number of Cause-Specific Deaths"] = df["Total Number of Cause-Specific Deaths"].astype(
        int)
    if drop_na is not None:
        df = df.mask(df['Age Group'].isin(['[0]', '[1-4]', '[5-9]', '[10-14]']), np.nan)
        df.dropna(subset=['Age Group'], inplace=True)

    if save_path is not None:
        df.to_excel(save_path)
    return df


def create_age_grouping(df: pd.DataFrame,
                        save_path: Optional[Path] = None) -> pd.DataFrame:
    if 'Total Number of Cause-Specific Deaths' not in df.columns:
        raise RuntimeError('call preprocess_cvd in advance')

    dy: dict = collections.defaultdict(list)
    group = df.groupby(['Region Code', 'Region Name', 'Country Code', 'Country Name', 'Year', 'Sex'])
    info: List[Tuple] = list(group.groups.keys())

    for i, it in enumerate(info):
        dy['Region Code'].append(it[0])
        dy['Region Name'].append(it[1])
        dy['Country Code'].append(it[2])
        dy['Country Name'].append(it[3])
        dy['Year'].append(it[4])  # Year in [4]
        dy['Sex'].append(it[5])  # Sex in [5]

    numbers = group['Number']
    total_number_of_death = group['Total Number of Cause-Specific Deaths']

    dy['Number'] = np.array(numbers.sum())
    dy['Total Number of Cause-Specific Deaths'] = np.array(total_number_of_death.sum())
    dy['Total Percentage of Cause-Specific Deaths Out Of Total Deaths'] = np.array(
        numbers.sum() / total_number_of_death.sum() * 100)

    _df = pd.DataFrame.from_dict(dy)  #

    sex_values = ['All', 'Female', 'Male']
    new_df = _df.assign(
        All_Number=_df.query("Sex == 'All'")['Number'],
        Female_Number=_df.query("Sex == 'Female'")['Number'],
        Male_Number=_df.query("Sex == 'Male'")['Number'],
        All_Total_Number_of_Cause_Specific_Deaths=_df.query("Sex == 'All'")['Total Number of Cause-Specific Deaths'],
        Female_Total_Number_of_Cause_Specific_Deaths=_df.query("Sex == 'Female'")[
            'Total Number of Cause-Specific Deaths'],
        Male_Total_Number_of_Cause_Specific_Deaths=_df.query("Sex == 'Male'")['Total Number of Cause-Specific Deaths'],
        All_Total_Percentage_of_Cause_Specific_Deaths_Out_Of_Total_Deaths=_df.query("Sex == 'All'")[
            'Total Percentage of Cause-Specific Deaths Out Of Total Deaths'],
        Female_Total_Percentage_of_Cause_Specific_Deaths_Out_Of_Total_Deaths=_df.query("Sex == 'Female'")[
            'Total Percentage of Cause-Specific Deaths Out Of Total Deaths'],
        Male_Total_Percentage_of_Cause_Specific_Deaths_Out_Of_Total_Deaths=_df.query("Sex == 'Male'")[
            'Total Percentage of Cause-Specific Deaths Out Of Total Deaths'])
    new_df.reset_index(drop=True, inplace=True)

    new_df = new_df.drop(['Sex', 'Number', 'Total Number of Cause-Specific Deaths',
                          'Total Percentage of Cause-Specific Deaths Out Of Total Deaths'],
                         axis=1)  # axis = 1: specifies to drop columns

    new_df = new_df.groupby(['Region Code', 'Region Name', 'Country Code', 'Country Name',
                             'Year']).first().reset_index()  # The first method is then applied to
    # the grouped dataframe, which returns the first row of each group
    if save_path:
        new_df.to_excel(save_path)
    return new_df


raw_tobacco_df = pd.read_csv(
    '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/raw data/Estimate of current tobacco smoking '
    'prevalence(%)(age-standardized rate)_17 Jan 2022.csv')

rename = {'Location': 'Country Name', 'Period': 'Year', 'Dim1': 'Sex', 'First Tooltip': 'Prevalence'}

save_path = '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/Prevalence of Tobacco use_modified.xlsx'
tobacco_df = select_df(raw_tobacco_df, rename_mapping=rename, save_path=save_path)


def tobacco_layout_modified(df: pd.DataFrame,
                            save_path: Optional[Path] = None) -> pd.DataFrame:
    dy: dict = collections.defaultdict(list)
    group = df.groupby(['Country Name', 'Year', 'Indicator', 'Sex'])
    info: List[Tuple] = list(group.groups.keys())

    for i, it in enumerate(info):
        dy['Country Name'].append(it[0])
        dy['Year'].append(it[1])
        dy['Indicator'].append(it[2])
        dy['Sex'].append(it[3])
        dy['Prevalence'].append(group.get_group(it).Prevalence.mean())

    _df = pd.DataFrame.from_dict(dy)
    sex_values = ['Both sexes', 'Male', 'Female']
    indicator_values = ['Estimate of current tobacco use prevalence (%) (age-standardized rate)',
                        'Estimate of current tobacco smoking prevalence (%) (age-standardized rate)']

    changed_df = _df.assign(All_Estimate_of_Current_Tobacco_Use_Prevalence_age_standardized_rate=
                            _df.query(
                                "Sex == 'Both sexes'& Indicator =='Estimate of current tobacco use prevalence (%) (age-standardized rate)'")[
                                'Prevalence'],
                            Male_Estimate_of_Current_Tobacco_Use_Prevalence_age_standardized_rate=_df.query(
                                "Sex == 'Male'& Indicator =='Estimate of current tobacco use prevalence (%) (age-standardized rate)'")[
                                'Prevalence'],
                            Female_Estimate_of_Current_Tobacco_Use_Prevalence_age_standardized_rate=_df.query(
                                "Sex == 'Female'& Indicator =='Estimate of current tobacco use prevalence (%) (age-standardized rate)'")[
                                'Prevalence'],

                            All_Estimate_of_Current_Tobacco_Smoking_Prevalence_age_standardized_rate=_df.query(
                                "Sex == 'Both sexes'& Indicator =='Estimate of current tobacco smoking prevalence (%) (age-standardized rate)'")[
                                'Prevalence'],
                            Male_Estimate_of_Current_Tobacco_Smoking_Prevalence_age_standardized_rate=_df.query(
                                "Sex == 'Male'& Indicator =='Estimate of current tobacco smoking prevalence (%) (age-standardized rate)'")[
                                'Prevalence'],
                            Female_Estimate_of_Current_Tobacco_Smoking_Prevalence_age_standardized_rate=_df.query(
                                "Sex == 'Female'& Indicator =='Estimate of current tobacco smoking prevalence (%) (age-standardized rate)'")[
                                'Prevalence'])

    changed_df.reset_index(drop=True, inplace=True)

    changed_df = changed_df.drop(['Sex', 'Prevalence', 'Indicator'], axis=1)
    changed_df = changed_df.groupby(['Country Name', 'Year']).first().reset_index()
    print(changed_df)
    if save_path is not None:
        changed_df.to_excel(save_path)
    return changed_df


if __name__ == '__main__':
    tobacco_df  = pd.read_excel('/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/Prevalence of Tobacco use_modified.xlsx')
    save_path= '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/Prevalence of Tobacco use_Changed_layout.xlsx'
    changed_df= tobacco_layout_modified(tobacco_df,save_path=save_path)