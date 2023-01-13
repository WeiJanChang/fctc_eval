"""
pipeline
** df1(CVD Mortality):
    This .xlsx processed via utility.py
    header:Entity, Year, Sex, Age Group, Number, Percentage of cause-specific deaths out of total deaths,
    Death rate per 100,000 population

** df2(Tobacco Use):
    This .xlsx processed via utility.py
    header:Entity, Year, Prevalence of current tobacco use, males (% of male adults),
    Prevalence of current tobacco use, females (% of female adults), Population (historical estimates)

** combine
1. horizontal to vertical in df1  and combine to df2
2. if df has non value--> show Nan (don't drop)

"""
import collections  # This module contains different datatype to process the data: dict, list, set, and tuple.
from pprint import pprint
# pprint.pprint() can use when you need to examine the structure of a large or complex data structure. this output
# reveals more readable and structured way.
from typing import Tuple, List, Optional

import numpy as np
import pandas as pd


# todo:test data 整理; notes; test data 檔案太大(<10 MB)

def preprocess_cvd(df: pd.DataFrame,
                   save: bool = True) -> pd.DataFrame:
    """
    Dataframe of WHO_CVD_mortality modify:
    - grouping if set kwarg `grouping_age` as true todo: kwarg?
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
    mask_nan = np.isnan(total_number_of_death)  # type: pd.Series[bool] # if value is NaN, NaN = True

    df.loc[mask_nan, 'Total number of death'] = 0  # search location of df. if index ('Total number of death') is
    # NaN, change NaN to 0. ( if no.loc :SettingWithCopyWarning: A value is trying to be set on a copy of a slice
    # from a DataFrame
    df['Total number of death'] = df['Total number of death'].astype(int)  # astype can cast/change multiple types (
    # change type to int)

    # print(type(total_number_of_death[0]))
    # print(df[:30].to_markdown())

    if save:
        df.to_excel('test.xlsx')
    return df


def create_age_grouping(df: pd.DataFrame,
                        save: bool = True) -> pd.DataFrame:
    """
    Calculate: Total percentage of cause-specific deaths out of total deaths = Sum of number/ Sum of Total number of
    death * 100 (Male/ Female/ All in each year and country)
    grouping_age: age groups --> one age group (greater 15 y/o)
    create a new df and save it to excel

    :param df: df after preprocess_cvd
    :param save: save modified dataframe to another excel
    :return: new df
    """

    if 'Total number of death' not in df.columns:
        raise RuntimeError('call preprocess_cvd in advance')

    dy: dict = collections.defaultdict(list)  # defaultdict object in collections. datatype will be dict. Using list
    # as the default_factory to group a sequence of key-value pairs into a dictionary of lists
    group = df.groupby(['Entity', 'Year', 'Sex'])
    info: List[Tuple] = list(group.groups.keys())  # List[Tuple]: value is a list of tuple[()].looking for the keys in a
    # dict. The 'groups' attribute of the 'groupby' object is always dic type

    for i, it in enumerate(info):  # i = index ( starting from 0) , it = item (Entity, Year, Sex). enumerate can pair
        # index and item
        dy['Entity'].append(it[0])  # Entity in [0]
        dy['Year'].append(it[1])  # Year in [1]
        dy['Sex'].append(it[2])  # Sex in [2]

    numbers = group['Number']
    total_number_of_death = group['Total number of death']
    # noinspection PyTypeChecker
    dy['Number'] = np.array(numbers.sum())
    dy['Total number of death'] = np.array(total_number_of_death.sum())
    dy['Total percentage of CVD'] = np.array(numbers.sum() / total_number_of_death.sum() * 100)

    new_df = pd.DataFrame.from_dict(dy)  # creates a new_df from the dy dictionary.

    if save:
        new_df.to_excel('WHO_CVD_Mortality_test.xlsx')
    return new_df


if __name__ == '__main__':
    df = pd.read_excel(
        '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/MPH '
        'Dissertation/WHO_CVD_Mortality_Age over 15_Year over 2000.xlsx',
        engine='openpyxl')  # “xlrd” supports old-style Excel files (.xls).“openpyxl” supports newer Excel file formats.

df = preprocess_cvd(df)  # assign a df after preprocess_cvd
new_df = create_age_grouping(df)  # assign a new_df after create_age_grouping

"""
pipeline
** df1 (Final_WHO_CVD_Mortality.xlsx):
    Change layout.
    Sex (All, Female, and Male) combined to header(Number/ Tot Num/ Tot %) respectively
    Left only a unique year in col.
** df2 (Tobacco use.xlsx):
    Combine with df1 and show NaN if some values are empty, don't drop
"""

# todo: def modified_cvd(df: pd.DataFrame, save_path: Optional[Path] = None) -> pd.DataFrame:
"""

    :param df: Use new_df ( Final_WHO_CVD_Mortality.xlsx) to modify column, add new col. and change position.
    :param save_path: modified dataframe to another excel file
    :return: df
"""

df2 = pd.DataFrame(columns=['Entity', 'Year', 'All_number', 'Female_number', 'Male_number', 'All_total number of death',
                            'Female_total number of death', 'Male_total number of death', 'All_total percentage of CVD',
                            'Female_total percentage of CVD', 'Male_total percentage of CVD'])
df2['Entity'] = new_df['Entity']
df2['Year'] = new_df['Year']
df2['All_number'] = new_df[new_df['Sex'] == 'All']['Number']
df2['Female_number'] = new_df[new_df['Sex'] == 'Female']['Number']
df2['Male_number'] = new_df[new_df['Sex'] == 'Male']['Number']
df2['All_total number of death'] = new_df[new_df['Sex'] == 'All']['Total number of death']
df2['Female_total number of death'] = new_df[new_df['Sex'] == 'Female']['Total number of death']
df2['Male_total number of death'] = new_df[new_df['Sex'] == 'Male']['Total number of death']
df2['All_total percentage of CVD'] = new_df[new_df['Sex'] == 'All']['Total percentage of CVD']
df2['Female_total percentage of CVD'] = new_df[new_df['Sex'] == 'Female']['Total percentage of CVD']
df2['Male_total percentage of CVD'] = new_df[new_df['Sex'] == 'Male']['Total percentage of CVD']
df2.reset_index(drop=True, inplace=True)

df2.to_excel('df2_test.xlsx')

# merge test
df1 = pd.read_excel(
    "/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/MPH Dissertation/Final_WHO_CVD_Mortality_modified.xlsx")
df2 = pd.read_excel(
    '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/MPH Dissertation/Tobacco_use_in_WHO_MEMBER_STATES.xlsx')
merged_df = pd.merge(df1, df2, on=['Entity', 'Year'], how='outer')
merged_df.fillna(value='NaN', inplace=True)
merged_df.to_excel('merged_test.xlsx', index=False)

# todo: 把沒有同時符合entity, year符合的也要列出來
