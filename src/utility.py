"""
pipeline

Step 1 Cleaning the WHO CVD mortality data:
- column drop: ['Age group code', 'Unnamed: 12', 'Age-standardized death rate per 100 000 standard population']
- drop na: ['Number','Percentage of cause-specific deaths out of total deaths', 'Death rate per 100 000 population']

Step 2 preprocess the WHO CVD mortality data:
- Calculate Total number of death
- only left age >15 years old

Step 3 preprocess the WHO CVD mortality data:
- Calculate 'Total Number of Cause-Specific Deaths'
    - formula: Total Number of Cause-Specific Deaths=Numbers* 100/Percentage of cause-specific deaths out of total deaths
- Calculate 'Total Percentage of Cause-Specific Deaths Out Of Total Deaths'
    - formula: Number of Cause-Specific Deaths/ Total Number of Cause-Specific Deaths * 100'
    (All/Females/Males in each year and country; no age-specific)
- Grouping age
- change layout

Step 4 preprocess the Tobacco data:
- raname column name
- {'Location': 'Country Name', 'Period': 'Year', 'Dim1': 'Sex', 'First Tooltip': 'Prevalence'}
- change layout

Step 5 merge CVD df and tobacco df:
- merge them based on Country Name and Year,show NaN if some values are empty
"""

from pathlib import Path  # pathlib: module, Path: class. Checking if a path exist
from typing import Optional, List, Dict, Tuple  # typing: support for type hint
import pandas as pd
import numpy as np
import collections  # This module contains different datatype to process the data: dict, list, set, and tuple.
from pprint import pprint  # pprint.pprint() can use when you need to examine the structure of a large or complex
# data structure. this output reveals more readable and structured way.
from who_member_states import WHO_MEMBER_STATES

__all__ = ['select_df',
           'preprocess_cvd',
           'create_age_grouping',
           'tobacco_layout_modified',
           'merge_df']


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
    #    entity_mask: List[bool] = [country in WHO_MEMBER_STATES for country in
    #                              df['Country Name']]  # check countries whether
    # in df['Entity'] also in WHO_MEMBER_STATES. If Yes =True
    modified_df: pd.DataFrame = df[year_mask].reset_index(
        drop=True)  # create a new df that only meet both
    # year_mask and entity_mask. df.reset_index(drop = True) means new index created, old index don't added in new df.

    if drop_na is not None:  # drop rows with missing values ('NaN') from df
        try:
            modified_df.dropna(subset=drop_na, inplace=True)
            # inplace = True means that the original df will be modified and no copy will be made.; But, if inplace =
            # False, df will still show the initial one. subset = drop_na means drop in specific place you set.
        except KeyError as e:
            raise ValueError(f'{e} not in the dataframe, should be one of the {modified_df.columns.tolist()}')  # If
            # typed wrong, show the list which should be dropped.
    if save_path is not None:
        modified_df.to_excel(save_path, index=False)

    return modified_df


def preprocess_cvd(df: pd.DataFrame,
                   drop_na: Optional[List[str]] = None,
                   save_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Dataframe of WHO_Cardiovascular_Disease_Mortality_Database.xlsx need to modify:
    - grouping if set kwarg `grouping_age` as true  # kwarg : keyword arguments
    - Calculate Total number of death
    - only left age >15 years old
    - save as another dataframe

    :param df: input dataframe (WHO_Cardiovascular_Disease_Mortality_Database.xlsx)
    :param drop_na: drop Age_Group <15-year-old
    :param save_path: save modified dataframe to another excel
    :return: df
    """

    # Sum of number of death in each age group
    numbers = df['Number']
    percentage = df['Percentage of cause-specific deaths out of total deaths']
    df["Total Number of Deaths"] = numbers * 100 / percentage
    total_number_of_death = df["Total Number of Deaths"]
    mask_nan = np.isnan(total_number_of_death)  # type: pd.Series[bool] # if value is NaN, NaN = True

    df.loc[
        mask_nan, "Total Number of Deaths"] = 0  # search location of df. if index ('Total number of death') is
    # NaN, change NaN to 0. ( if no.loc :SettingWithCopyWarning: A value is trying to be set on a copy of a slice
    # from a DataFrame
    df["Total Number of Deaths"] = df["Total Number of Deaths"].astype(
        int)  # astype can cast/change multiple types (
    # change type to int)
    if drop_na is not None:  # drop rows with missing values ('NaN') from df
        df = df.mask(df['Age Group'].isin(['[0]', '[1-4]', '[5-9]', '[10-14]', '[All]']), np.nan)
        df.dropna(subset=['Age Group'], inplace=True)

    if save_path is not None:
        df.to_excel(save_path, index=False)
    return df


def create_age_grouping(df: pd.DataFrame,
                        save_path: Optional[Path] = None) -> pd.DataFrame:
    """
    1. Calculate: Total percentage of CVD of total deaths = Sum of CVD death number/ Sum of Total number of deaths
    * 100 (Male/ Female/ All in each year and country)
    2. grouping_age: Age groups --> one age group (greater 15 y/o)
    3. change layout
    4. create a new df and save it to excel

    :param df: df after select_df and preprocess_cvd
    :param save: save modified dataframe to another excel
    :return: new df
    """

    if 'Total Number of Deaths' not in df.columns:
        raise RuntimeError('call preprocess_cvd in advance')

    dy: dict = collections.defaultdict(list)  # defaultdict object in collections. datatype will be dict. Using list
    # as the default_factory to group a sequence of key-value pairs into a dictionary of lists
    group = df.groupby(['Region Code', 'Region Name', 'Country Code', 'Country Name', 'Year', 'Sex'])
    info: List[Tuple] = list(group.groups.keys())  # List[Tuple]: value is a list of tuple[()].looking for the keys in a
    # dict. The 'groups' attribute of the 'groupby' object is always dic type

    for i, it in enumerate(info):  # i = index ( starting from 0) , it = item (Entity, Year, Sex). enumerate can pair
        # index and item
        dy['Region Code'].append(it[0])
        dy['Region Name'].append(it[1])
        dy['Country Code'].append(it[2])
        dy['Country Name'].append(it[3])
        dy['Year'].append(it[4])  # Year in [4]
        dy['Sex'].append(it[5])  # Sex in [5]

    numbers = group['Number']
    total_number_of_death = group['Total Number of Deaths']
    # noinspection PyTypeChecker todo: wt is it?
    dy['Number'] = np.array(numbers.sum())
    dy['Total Number of Deaths'] = np.array(total_number_of_death.sum())
    dy['Total Percentage of Cause-Specific Deaths Out Of Total Deaths'] = np.array(
        numbers.sum() / total_number_of_death.sum() * 100)

    _df = pd.DataFrame.from_dict(dy)  # creates a new_df from the dy dictionary.

    # change layout
    sex_values = ['All', 'Female', 'Male']
    new_df = _df.assign(
        All_Number_of_Cause_Specific_Deaths=_df.query("Sex == 'All'")['Number'],
        Female_Number_of_Cause_Specific_Deaths=_df.query("Sex == 'Female'")['Number'],
        Male_Number_of_Cause_Specific_Deaths=_df.query("Sex == 'Male'")['Number'],
        All_Total_Number_of_Deaths=_df.query("Sex == 'All'")['Total Number of Deaths'],
        Female_Total_Number_of_Deaths=_df.query("Sex == 'Female'")[
            'Total Number of Deaths'],
        Male_Total_Number_of_Deaths=_df.query("Sex == 'Male'")['Total Number of Deaths'],
        All_Total_Percentage_of_Cause_Specific_Deaths_Out_Of_Total_Deaths=_df.query("Sex == 'All'")[
            'Total Percentage of Cause-Specific Deaths Out Of Total Deaths'],
        Female_Total_Percentage_of_Cause_Specific_Deaths_Out_Of_Total_Deaths=_df.query("Sex == 'Female'")[
            'Total Percentage of Cause-Specific Deaths Out Of Total Deaths'],
        Male_Total_Percentage_of_Cause_Specific_Deaths_Out_Of_Total_Deaths=_df.query("Sex == 'Male'")[
            'Total Percentage of Cause-Specific Deaths Out Of Total Deaths'])
    new_df.reset_index(drop=True, inplace=True)

    new_df = new_df.drop(['Sex', 'Number', 'Total Number of Deaths',
                          'Total Percentage of Cause-Specific Deaths Out Of Total Deaths'],
                         axis=1)  # axis = 1: specifies to drop columns

    new_df = new_df.groupby(['Country Name', 'Year']).first().reset_index()  # The first method is then applied to
    # the grouped dataframe, which returns the first row of each group
    if save_path:
        new_df.to_excel(save_path, index=False)
    return new_df


def tobacco_layout_modified(df: pd.DataFrame,
                            column_drop: Optional[Path] = None,
                            save_path: Optional[Path] = None) -> pd.DataFrame:
    """
    run select_df first and then use this function to modify layout
    :param df:  Prevalence of Tobacco data
    :param column_drop: drop col
    :param save_path: path
    :return: df
    """
    df = df.copy()
    df = df.rename(columns={'Location': 'Country Name', 'Period': 'Year', 'Dim1': 'Sex', 'First Tooltip': 'Prevalence'})
    if column_drop is not None:
        df = df.drop(columns=column_drop)
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
                        'Estimate of current tobacco smoking prevalence (%) (age-standardized rate)',
                        'Estimate of current cigarette smoking prevalence (%) (age-standardized rate)']

    changed_df = _df.assign(
        All_Estimate_of_Current_Tobacco_Use_Prevalence_age_standardized_rate=_df.query(
            "Sex == 'Both sexes'& Indicator =='Estimate of current tobacco use prevalence (%) (age-standardized rate)'")[
            'Prevalence'],
        Male_Estimate_of_Current_Tobacco_Use_Prevalence_age_standardized_rate=_df.query(
            "Sex == 'Male'& Indicator =='Estimate of current tobacco use prevalence (%) (age-standardized rate)'")[
            'Prevalence'],
        Female_Estimate_of_Current_Tobacco_Use_Prevalence_age_standardized_rate=_df.query(
            "Sex == 'Female'& Indicator =='Estimate of current tobacco use prevalence (%) (age-standardized rate)'")[
            'Prevalence'],

        All_Estimate_of_Current_Tobacco_Smoking_Prevalence_age_standardized_rate=_df.query(
            "Sex == 'Both sexes'& Indicator =='Estimate of current tobacco smoking prevalence (%) (age-standardized "
            "rate)'")['Prevalence'],
        Male_Estimate_of_Current_Tobacco_Smoking_Prevalence_age_standardized_rate=_df.query(
            "Sex == 'Male'& Indicator =='Estimate of current tobacco smoking prevalence (%) (age-standardized rate)'")[
            'Prevalence'],
        Female_Estimate_of_Current_Tobacco_Smoking_Prevalence_age_standardized_rate=_df.query(
            "Sex == 'Female'& Indicator =='Estimate of current tobacco smoking prevalence (%) (age-standardized rate)'")[
            'Prevalence'],
        All_Estimate_of_current_cigarette_smoking_prevalence_age_standardized_rate=_df.query(
            "Sex == 'Both sexes'& Indicator =='Estimate of current cigarette smoking prevalence (%) (age-standardized rate)'")[
            'Prevalence'],
        Male_Estimate_of_current_cigarette_smoking_prevalence_age_standardized_rate=_df.query(
            "Sex == 'Male'& Indicator =='Estimate of current cigarette smoking prevalence (%) (age-standardized rate)'")[
            'Prevalence'],
        Female_Estimate_of_current_cigarette_smoking_prevalence_age_standardized_rate=_df.query(
            "Sex == 'Female'& Indicator =='Estimate of current cigarette smoking prevalence (%) (age-standardized rate)'")[
            'Prevalence'])

    changed_df.reset_index(drop=True, inplace=True)

    changed_df = changed_df.drop(['Sex', 'Prevalence', 'Indicator'], axis=1)
    changed_df = changed_df.groupby(['Country Name', 'Year']).first().reset_index()
    if save_path is not None:
        changed_df.to_excel(save_path, index=False)
    return changed_df


def merge_df(cvd_df: pd.DataFrame, tobacco_df: pd.DataFrame, column_name=Optional[List[str]],
             all_df_out: Optional[Path] = None) -> pd.DataFrame:
    """
    merge CVD df and tobacco df based on Country Name and Year
    :param cvd_df: cvd df
    :param tobacco_df: tobacco df
    :param column_name: country name and year
    :param all_df_out: output path
    :return: df
    """
    all_df = pd.merge(cvd_df, tobacco_df, on=column_name, how='outer')
    all_df.fillna(value='NaN', inplace=True)  # inplace = True means that 'value = 'NaN'' will inplace original value
    # in df. 'Nan' can be changed what you want to instead of.

    # drop no need indicators in Tobacco dataset
    columns_to_drop = [
        'Female_Estimate_of_current_cigarette_smoking_prevalence_age_standardized_rate',
        'Male_Estimate_of_current_cigarette_smoking_prevalence_age_standardized_rate',
        'All_Estimate_of_current_cigarette_smoking_prevalence_age_standardized_rate',
        'Female_Estimate_of_Current_Tobacco_Smoking_Prevalence_age_standardized_rate',
        'Male_Estimate_of_Current_Tobacco_Smoking_Prevalence_age_standardized_rate',
        'All_Estimate_of_Current_Tobacco_Smoking_Prevalence_age_standardized_rate'
    ]
    all_df = all_df.drop(columns=columns_to_drop)
    if all_df_out is not None:
        all_df.to_excel(all_df_out, index=False)

    return all_df
