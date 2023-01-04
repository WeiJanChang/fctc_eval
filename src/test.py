"""
pipeline
** df1(CVD Mortality):
    header:Entity, Year, Sex, Age group code, Age Group, Number, Percentage of cause-specific deaths out of total deaths,
    Total number of death, Death rate per 100,000 population,
    Total percentage of cause-specific deaths out of total deaths

** df2(Tobacco Use):
    header:Entity, Year, Prevalence of current tobacco use, males (% of male adults),
    Prevalence of current tobacco use, females (% of female adults), Population (historical estimates)


** combine
1. horizontal to vertical in df1  and combine to df2
2. if df has non value--> show Nan

"""
import collections
from pprint import pprint
from typing import Tuple, List

import numpy as np
import pandas as pd


# todo:test data 整理; notes; 不要的刪一刪; test data 檔案太大(<10 MB);engine='openpyxl'?

def preprocess_cvd(df: pd.DataFrame,
                   save: bool = True) -> pd.DataFrame:
    """
    Dataframe of WHO_CVD_mortality modify:
    - grouping if set kwarg `grouping_age` as true
    - Calculate total number of death
    - Calculate Total percentage of cause-specific deaths out of total deaths (%) =
    Sum of number of ALL n Males n Females/Sum of total number of death of ALL n Males n Females * 100
    - save as another dataframe

    :param df: input dataframe (WHO_CVD_mortality)
    :param save: save modified dataframe to another excel
    :return: df
    """

    # Sum of number of death in each age group
    numbers = df['Number']
    percentage = df['Percentage of cause-specific deaths out of total deaths']
    df["Total number of death"] = numbers * 100 / percentage
    total_number_of_death = df["Total number of death"]
    mask_nan = np.isnan(total_number_of_death)  # type: pd.Series[bool]
    # SettingWithCopyWarning: A value is trying to be set on a copy of a slice from a DataFrame 要改
    total_number_of_death[mask_nan] = 0
    total_number_of_death = total_number_of_death.astype(int)  # astype can cast/change multiple types
    df['Total number of death'] = total_number_of_death
    # print(type(total_number_of_death[0]))
    # print(df[:30].to_markdown())

    if save:
        pass  # pass : ignore it
    return df


def create_age_grouping(df: pd.DataFrame,
                        save: bool = True) -> pd.DataFrame:
    """
    Calculate: Total percentage of cause-specific deaths out of total deaths = Sum of number/ SUM of Total number of
    death * 100 (Male/ Female/ All in each year and country)
    grouping_age: age groups --> one age group (greater 15 y/o)

    :param df: df after preprocess_cvd
    :param save:
    :return: df
    """

    if 'Total number of death' not in df.columns:
        raise RuntimeError('call preprocess_cvd in advance')

    dy = collections.defaultdict(list)
    group = df.groupby(['Entity', 'Year', 'Sex'])
    info: List[Tuple] = list(group.groups.keys())

    for i, it in enumerate(info):
        dy['Entity'].append(it[0])
        dy['Year'].append(it[1])
        dy['Sex'].append(it[2])

    numbers = group['Number']
    total_number_of_death = group['Total number of death']
    # 為什麼reset index 還是不能加 df = df.reset_index(drop=True)
    # noinspection PyTypeChecker
    dy['total_percentage_of_cvd'] = np.array(numbers.sum() / total_number_of_death.sum() * 100)

    new_df = pd.DataFrame.from_dict(dy)
    if save:
        new_df.to_excel('test_.xlsx')
    return new_df


if __name__ == '__main__':
    df = pd.read_excel(
        '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/MPH '
        'Dissertation/WHO_Cardiovascular_Disease_Mortality_specific_year_Age_over15.xlsx', engine='openpyxl') #todo?

    df = preprocess_cvd(df)
    new_df=create_age_grouping(df)
    print(new_df)
