"""
pipeline

MPH Thesis: To Investigate the effects of tobacco control treaty on cardiovascular disease mortality in males and females
between Parties and Nonparties of the World Health Organization (WHO) Framework Convention on Tobacco Control (FCTC)

Step 1: Download raw data from open access database
        a. df1 = WHO Mortality database
        https://platform.who.int/mortality/themes/theme-details/topics/topic-details/MDB/cardiovascular-diseases
        b. df2 = Our World in Data
        https://ourworldindata.org/smoking#smoking-by-gender

Step 2: select df2['Entity'] which in WHO member states.

Step 3: select the info I need and drop info I don't need.

        df1: Region Name, Year (>=2000), Sex (All, Females, Males), Age Group(>=15 y/o), Number,
        Percentage of cause-specific deaths out of total deaths, Death rate per 100,000 population
        drop : Country Code, Region Code, Region Name, Age-standardized death rate per 100 000 standard population,
        Unnamed: 12.

        df2: Entity, Year, Prevalence of current tobacco use, males (% of male adults),
        Prevalence of current tobacco use, females (% of female adults), Population (historical estimates)
        drop: Continent, Code

Step 4: drop na from the remaining column.
        save it to modified_df

Step 5: finished the final version of Tobacco Use (df2). Next step is to do some calculations on df1

Step 6: df1:
        calculate 'sum of the number of death in a specific year in All/ Females/Males age-specific, respectively.'
        calculate 'Total number of Death (Not only the death of CVD) in a specific year in All/ Females/Males
        age-specific, respectively.'
        formula:percentage of cause-specific deaths out of total deaths =
                Number of deaths from a specific cause / Number of total deaths) x 100

Step 7: df1:
        calculate 'Total percentage of CVD deaths out of total deaths = Sum of the number/ Sum of the Total number of
        death * 100' (All/Females/Males in each year and country; no age-specific)

Step 8: df1:
        age grouping: each age groups --> one age group (>= 15 y/o)
        create a new df: groupby ['Entity','Year', 'Sex']
        and added new col: ['Number'], ['Total number of death'],['Total percentage of CVD']
        save it to excel

Step 9: df1:
        change layout.
        Sex (All, Female, and Male) combined to header(Number/ Tot Num/ Tot %) respectively
        Left only a unique year in col.

Step 10:
        ** df1(CVD Mortality):
        Header: Entity, Year, Sex, Number, Total Number of death, Total percentage of CVD

        ** df2(Tobacco Use):
        Header: Entity, Year, Prevalence of current tobacco use, males (% of male adults),
        Prevalence of current tobacco use, females (% of female adults), Population (historical estimates)

        merge df1 and df2, show NaN if some values are empty, don't drop
        save it to excel
"""

from pathlib import Path  # pathlib: module, Path: class. Checking if a path exist
from typing import Optional, List, Dict, Tuple  # typing: support for type hint
import pandas as pd
import numpy as np
import collections  # This module contains different datatype to process the data: dict, list, set, and tuple.
from pprint import pprint  # pprint.pprint() can use when you need to examine the structure of a large or complex
# data structure. this output reveals more readable and structured way.
from who_member_states import WHO_MEMBER_STATES

__all__ = ['select_df']  # only import 'select_df'


# test data should <10 MB

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

    :param df: input dataframe
    :param rename_mapping: both df have countries but the header is different
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
    modified_df: pd.DataFrame = df[year_mask & entity_mask].reset_index(
        drop=True)  # create a new df that only meet both
    # year_mask and entity_mask. df.reset_index(drop = True) means new index created, old index don't added in new df.

    if drop_na is not None:  # drop rows with missing values ('NaN') from df
        modified_df = _df.mask(_df['Age Group'].isin(['[0]', '[1-4]', '[5-9]', '[10-14]']), np.nan)
        try:
            modified_df.dropna(subset=drop_na, inplace=True)
            modified_df.dropna(subset=['Age Group'], inplace=True)
        # inplace = True means that the original df will be modified and no copy will be made.; But, if inplace = False,
        # df will still show the initial one. subset = drop_na means drop in specific place you set.
        except KeyError as e:
            raise ValueError(f'{e} not in the dataframe, should be one of the {_df.columns.tolist()}')  # If
            # typed wrong, show the list which should be dropped.
    if save_path is not None:
        modified_df.to_csv(Path)

    return modified_df


def preprocess_cvd(df: pd.DataFrame,
                   save_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Dataframe of WHO_CVD_Mortality_Age over 15_Year over 2000.xlsx need to modify:
    - grouping if set kwarg `grouping_age` as true todo: kwarg?
    - Calculate Total number of death
    - save as another dataframe

    :param df: input dataframe (WHO_CVD_Mortality_Age over 15_Year over 2000.xlsx)
    :param save_path: save modified dataframe to another excel
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

    if save_path is not None:
        df.to_excel(Path)
    return df


def create_age_grouping(df: pd.DataFrame,
                        save: bool = True) -> pd.DataFrame:
    """
    Calculate: Total percentage of CVD of total deaths = Sum of number/ Sum of Total number of
    death * 100 (Male/ Female/ All in each year and country)
    grouping_age: Age groups --> one age group (greater 15 y/o)
    create a new df and save it to excel

    :param df: df after select_df and preprocess_cvd
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
    # noinspection PyTypeChecker todo: wt is it?
    dy['Number'] = np.array(numbers.sum())
    dy['Total number of death'] = np.array(total_number_of_death.sum())
    dy['Total percentage of CVD'] = np.array(numbers.sum() / total_number_of_death.sum() * 100)

    new_df = pd.DataFrame.from_dict(dy)  # creates a new_df from the dy dictionary.
    if save:
        new_df.to_excel('Final_WHO_CVD_Mortality.xlsx')
    return new_df


def merge_df(df1: pd.DataFrame,
             df2: pd.DataFrame,
             based_on: Optional[List[str]] = None,
             save_path: Optional[Path] = None) -> pd.DataFrame:
    """

    :param df1: Final_WHO_CVD_Mortality_modified.xlsx
    :param df2: Tobacco_use_in_WHO_MEMBER_STATES.xlsx
    :param based_on: based on Entity and Year to combine to dataframe
    :param save_path: save combined dataframe to excel
    :return: merge_df
    """
    if based_on is not None:
        merge_df = pd.merge(df1, df2, on=based_on, how='outer')
        merge_df.fillna(value='NaN', inplace=True)  # inplace = True means that 'value = 'NaN'' will inplace original
        # value in df. 'Nan' can changed what you want to instead of.
    if save_path is not None:
        merge_df.to_excel('merged_test.xlsx', index=False)  # don't show index in excel
    return merge_df


if __name__ == '__main__':
    df = pd.read_csv(
        '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/MPH Dissertation/raw '
        'data/WHO_Cardiovascular_Disease_Mortality_Database.csv')

rename = {'Country Name': 'Entity'}
column_drop = ['Age group code', 'Country Code', 'Region Name', 'Region Code',
               'Age-standardized death rate per 100 000 standard population', 'Unnamed: 12']
na_header = ['Number',
             'Percentage of cause-specific deaths out of total deaths',
             'Death rate per 100 000 population']

df = select_df(df, rename_mapping=rename, column_drop=column_drop, drop_na=na_header)

df = pd.read_excel(
    '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/MPH '
    'Dissertation/WHO_CVD_Mortality_Age over 15_Year over 2000.xlsx',
    engine='openpyxl')
df = preprocess_cvd(df)
new_df = create_age_grouping(df)
print(new_df)

df1 = pd.read_excel(
    "/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/MPH Dissertation/Final_WHO_CVD_Mortality_modified.xlsx")
df2 = pd.read_excel(
    '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/MPH Dissertation/Tobacco_use_in_WHO_MEMBER_STATES.xlsx')
based_on = ['Entity', 'Year']
save_path = 'merged_test.xlsx'
merge_df = merge_df(df1, df2, based_on, save_path)
