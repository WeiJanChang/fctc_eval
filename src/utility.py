"""
pipeline

MPH Thesis: To compare the relationship between the prevalence of tobacco and CVD mortality before and after the
implementation of a tobacco treaty in WHO FCTC ratified parties by gender

Step 1: Download raw data from open access database
        a. df1 = WHO Mortality database
        https://platform.who.int/mortality/themes/theme-details/topics/topic-details/MDB/cardiovascular-diseases
        b. df2 = WHO The Global Health Observatory
        https://www.who.int/data/gho/data/themes/topics/sdg-target-3_a-tobacco-control

Step 2:

Step 3: select the info I need and drop info I don't need.
        df1 (raw data): ['Region Code', 'Region Name', 'Country Code', 'Country Name', 'Year', 'Sex', 'Age group code', 'Age Group', 'Number', 'Percentage of cause-specific deaths out of total deaths', 'Age-standardized death rate per 100 000 standard population', 'Death rate per 100 000 population', 'Unnamed: 12']
        **114 (297066, 13)**

        df1 (after select): ['Region Code', 'Region Name', 'Country Code', 'Country Name', 'Year', 'Sex', 'Age Group', 'Number', 'Percentage of cause-specific deaths out of total deaths', 'Age-standardized death rate per 100 000 standard population', 'Death rate per 100 000 population']
        **111 (111401, 11)**

        df2(raw data): ['Location', 'Period', 'Indicator', 'Dim1', 'First Tooltip']
        **165 (9351, 5)**

        df2 (after select and rename):['Country Name', 'Year', 'Indicator', 'Sex', 'Prevalence']
        **165 (9351, 5)**

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
        modified_df.to_excel(save_path)

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
    :param drop_na: drop Age_Group <15 year-old
    :param save_path: save modified dataframe to another excel
    :return: df
    """

    # Sum of number of death in each age group
    numbers = df['Number']
    percentage = df['Percentage of cause-specific deaths out of total deaths']
    df["Total Number of Cause-Specific Deaths"] = numbers * 100 / percentage
    total_number_of_death = df["Total Number of Cause-Specific Deaths"]
    mask_nan = np.isnan(total_number_of_death)  # type: pd.Series[bool] # if value is NaN, NaN = True

    df.loc[
        mask_nan, "Total Number of Cause-Specific Deaths"] = 0  # search location of df. if index ('Total number of death') is
    # NaN, change NaN to 0. ( if no.loc :SettingWithCopyWarning: A value is trying to be set on a copy of a slice
    # from a DataFrame
    df["Total Number of Cause-Specific Deaths"] = df["Total Number of Cause-Specific Deaths"].astype(
        int)  # astype can cast/change multiple types (
    # change type to int)
    if drop_na is not None:  # drop rows with missing values ('NaN') from df
        df = df.mask(df['Age Group'].isin(['[0]', '[1-4]', '[5-9]', '[10-14]']), np.nan)
        df.dropna(subset=['Age Group'], inplace=True)

    if save_path is not None:
        df.to_excel(save_path)
    return df


def create_age_grouping(df: pd.DataFrame,
                        save_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Calculate: Total percentage of CVD of total deaths = Sum of number/ Sum of Total number of cause-specific deaths
    * 100 (Male/ Female/ All in each year and country)
    grouping_age: Age groups --> one age group (greater 15 y/o)
    create a new df and save it to excel

    :param df: df after select_df and preprocess_cvd
    :param save: save modified dataframe to another excel
    :return: new df
    """

    if 'Total Number of Cause-Specific Deaths' not in df.columns:
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
    total_number_of_death = group['Total Number of Cause-Specific Deaths']
    # noinspection PyTypeChecker todo: wt is it?
    dy['Number'] = np.array(numbers.sum())
    dy['Total Number of Cause-Specific Deaths'] = np.array(total_number_of_death.sum())
    dy['Total Percentage of Cause-Specific Deaths Out Of Total Deaths'] = np.array(
        numbers.sum() / total_number_of_death.sum() * 100)

    _df = pd.DataFrame.from_dict(dy)  # creates a new_df from the dy dictionary.

    # change layout
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
            'Prevalence'])

    changed_df.reset_index(drop=True, inplace=True)

    changed_df = changed_df.drop(['Sex', 'Prevalence', 'Indicator'], axis=1)
    changed_df = changed_df.groupby(['Country Name', 'Year']).first().reset_index()
    print(changed_df)
    if save_path is not None:
        changed_df.to_excel(save_path)
    return changed_df


if __name__ == '__main__':
    raw_who_cvd_df = pd.read_csv('/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/raw '
                                 'data/WHOMortalityDatabase_Deaths_sex_age_a_country_area_year-Cardiovascular '
                                 'diseases_7th February 2023.csv')
column_drop = ['Age group code', 'Unnamed: 12']
na_header = ['Number',
             'Percentage of cause-specific deaths out of total deaths',
             'Death rate per 100 000 population']
save_path = (
    '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/WHO_Cardiovascular_Disease_Mortality_Database.xlsx')
who_cvd_df = select_df(raw_who_cvd_df, column_drop=column_drop, drop_na=na_header,
                       save_path=save_path)
who_cvd_df = pd.read_excel(
    '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/WHO_Cardiovascular_Disease_Mortality_Database.xlsx')
# “xlrd” supports old-style Excel files (.xls).“openpyxl” supports newer Excel file formats.
drop_na = ['Age Group']
save_path = (
    '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/WHO_Cardiovascular_Disease_Mortality_Database_preprocess.xlsx')
who_cvd_df_preprocess = preprocess_cvd(who_cvd_df, drop_na=drop_na,
                                       save_path=save_path)  # assign a who_cvd_df after preprocess_cvd

who_cvd_df_preprocess = pd.read_excel(
    '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/WHO_Cardiovascular_Disease_Mortality_Database_preprocess.xlsx')
who_cvd_df_preprocess = preprocess_cvd(who_cvd_df_preprocess)
save_path = (
    '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/new_WHO_Cardiovascular_Disease_Mortality_Database.xlsx')
new_df = create_age_grouping(who_cvd_df_preprocess, save_path=save_path)

raw_tobacco_df = pd.read_csv(
    '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/raw data/Estimate of current tobacco smoking '
    'prevalence(%)(age-standardized rate)_17 Jan 2022.csv')

rename = {'Location': 'Country Name', 'Period': 'Year', 'Dim1': 'Sex', 'First Tooltip': 'Prevalence'}

save_path = '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/Prevalence of Tobacco use_modified.xlsx'
tobacco_df = select_df(raw_tobacco_df, rename_mapping=rename, save_path=save_path)

tobacco_df = pd.read_excel(
    '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/Prevalence of Tobacco use_modified.xlsx')
save_path = '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/Prevalence of Tobacco use_Changed_layout.xlsx'
changed_df = tobacco_layout_modified(tobacco_df, save_path=save_path)

# merge df1 & df2 test
df1 = new_df
df2 = changed_df

cvd_tobacco = pd.merge(df1, df2, on=['Country Name', 'Year'], how='outer')
cvd_tobacco.fillna(value='NaN',
                   inplace=True)  # inplace = True means that 'value = 'NaN'' will inplace original value in df. 'Nan' can changed what you want to instead of.
cvd_tobacco.to_excel('/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/merge_cvd_tobacco.xlsx')
