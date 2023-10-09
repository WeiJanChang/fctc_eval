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
        df.to_excel(save_path)
    return df


def create_age_grouping(df: pd.DataFrame,
                        save_path: Optional[Path] = None) -> pd.DataFrame:
    """
    Calculate: Total percentage of CVD of total deaths = Sum of CVD death number/ Sum of Total number of deaths
    * 100 (Male/ Female/ All in each year and country)
    grouping_age: Age groups --> one age group (greater 15 y/o)
    create a new df and save it to excel

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

    new_df = pd.DataFrame.from_dict(dy)  # creates a new_df from the dy dictionary.

    """
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
    """
    new_df = new_df.groupby(
        ['Country Name', 'Year', 'Sex']).first().reset_index()  # The first method is then applied to
    # the grouped dataframe, which returns the first row of each group
    if save_path:
        new_df.to_excel(save_path)
    return new_df


def tobacco_layout_modified(df: pd.DataFrame,
                            column_drop: Optional[Path] = None,
                            save_path: Optional[Path] = None) -> pd.DataFrame:
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
    _df['Sex'] = _df['Sex'].replace('Both sexes', 'All')

    indicator_values = ['Estimate of current tobacco use prevalence (%) (age-standardized rate)',
                        'Estimate of current tobacco smoking prevalence (%) (age-standardized rate)',
                        'Estimate of current cigarette smoking prevalence (%) (age-standardized rate)']

    changed_df = _df.assign(
        Estimate_of_Current_Tobacco_Use_Prevalence_age_standardized_rate=_df.query(
            "Indicator =='Estimate of current tobacco use prevalence (%) (age-standardized rate)'")[
            'Prevalence'],
        Estimate_of_Current_Tobacco_Smoking_Prevalence_age_standardized_rate=_df.query(
            "Indicator =='Estimate of current tobacco smoking prevalence (%) (age-standardized "
            "rate)'")['Prevalence'],
        Estimate_of_current_cigarette_smoking_prevalence_age_standardized_rate=_df.query(
            "Indicator =='Estimate of current cigarette smoking prevalence (%) (age-standardized rate)'")[
            'Prevalence'])
    changed_df.reset_index(drop=True, inplace=True)

    changed_df = changed_df.drop(['Prevalence', 'Indicator'], axis=1)
    changed_df = changed_df.groupby(['Country Name', 'Year', 'Sex']).first().reset_index()
    print(changed_df)
    if save_path is not None:
        changed_df.to_excel(save_path)
    return changed_df


def consistent_year(df: pd.DataFrame,
                    year_mask: Optional[List[int]] = None,
                    save_path: Optional[Path] = None) -> pd.DataFrame:
    """
    :param df: WHOFCTC_Parties_date_no_missingdata.xlsx
    :param year_mask: as Time Series, the Year should have regular interval.
    and now the year includes 2000, 2005, 2010, 2015, 2018, 2019, and 2020. So, the year 2018 and 2019 should be excluded.
    :param save_path: save modified dataframe to another excel
    :return: interval_df
    """
    interval_df = df.copy()
    if year_mask is not None:
        mask = ~interval_df['Year'].isin([2018, 2019])  # create boolean mask to exclude rows with 2018 and 2019
        interval_df = interval_df[mask]  # select rows that are not excluded by the mask
    interval_df = interval_df.reset_index(drop=True)
    if save_path is not None:
        interval_df.to_excel(save_path)
    return interval_df


if __name__ == '__main__':
    raw_who_cvd_df = pd.read_csv(
        '/Users/wei/Documents/UCD_MPH/mph_lecture/mph_dissertation/data/raw_data'
        '/WHOMortalityDatabase_Deaths_sex_age_a_country_area_year-Cardiovascular diseases_7th February 2023.csv')
    column_drop = ['Age group code', 'Unnamed: 12', 'Age-standardized death rate per 100 000 standard population']
    na_header = ['Number',
                 'Percentage of cause-specific deaths out of total deaths',
                 'Death rate per 100 000 population']
    save_path = Path('/Users/wei/Documents/UCD_MPH/mph_lecture/mph_dissertation/data/test_whocvd.xlsx')

    who_cvd_df = select_df(raw_who_cvd_df, column_drop=column_drop, drop_na=na_header, save_path=save_path)

    save_path = Path('/Users/wei/Documents/UCD_MPH/mph_lecture/mph_dissertation/data/test_whocvd_selectedagegroup.xlsx')
    who_cvd_df_preprocess = preprocess_cvd(who_cvd_df, ['Age Group'],
                                           save_path=save_path)  # assign a who_cvd_df after preprocess_cvd

    save_path = Path('/Users/wei/Documents/UCD_MPH/mph_lecture/mph_dissertation/data/test_whocvd_agegrouping.xlsx')
    age_grouping_df = create_age_grouping(who_cvd_df_preprocess, save_path=save_path)

    raw_tobacco_df = pd.read_csv(
        '/Users/wei/Documents/UCD_MPH/mph_lecture/mph_dissertation/data/raw_data/Estimate of current tobacco smoking '
        'prevalence(%)(age-standardized rate)_17 Jan 2022.csv')

    rename = {'Location': 'Country Name', 'Period': 'Year', 'Dim1': 'Sex', 'First Tooltip': 'Prevalence'}

    save_path = Path('/Users/wei/Documents/UCD_MPH/mph_lecture/mph_dissertation/data/test_renametobacco.xlsx')
    tobacco_df = select_df(raw_tobacco_df, rename_mapping=rename, save_path=save_path)

    save_path = Path('/Users/wei/Documents/UCD_MPH/mph_lecture/mph_dissertation/data/test_new_tobacco.xlsx')
    new_tobacco = tobacco_layout_modified(tobacco_df, save_path=save_path)

    # merge df1 & df2 test
    df1 = age_grouping_df
    df2 = new_tobacco

    cvd_tobacco = pd.merge(df1, df2, on=['Country Name', 'Year', 'Sex'], how='outer')
    cvd_tobacco.fillna(value='NaN',
                       inplace=True)  # inplace = True means that 'value = 'NaN'' will inplace original value
    # in df. 'Nan' can changed what you want to instead of.

    # drop no need indicators in Tobacco dataset
    columns_to_drop = [
        'Estimate_of_current_cigarette_smoking_prevalence_age_standardized_rate',
        'Estimate_of_Current_Tobacco_Smoking_Prevalence_age_standardized_rate', ]
    cvd_tobacco = cvd_tobacco.drop(columns=columns_to_drop)
    # drop NaN
    cvd_tobacco.replace('NaN', np.nan, inplace=True)
    cvd_tobacco = cvd_tobacco.dropna(axis=0)
    cvd_tobacco.to_excel(
        '/Users/wei/Documents/UCD_MPH/mph_lecture/mph_dissertation/data/test_cvd_tobacco.xlsx')

    # merge parties date
    who_tobacco_member = pd.read_excel(
        '/Users/wei/Documents/UCD_MPH/mph_lecture/mph_dissertation/data/WHOFCTC_Parties_date_formatted.xlsx',
        engine='openpyxl')

    signed_df = pd.merge(cvd_tobacco, who_tobacco_member, on=['Country Name'], how='outer')
    signed_df.fillna(value='NaN', inplace=True)
    # drop_missing_data
    signed_df.replace("NaN", np.nan, inplace=True)
    signed_df = signed_df.dropna(axis=0)
    signed_df.to_excel('/Users/wei/Documents/UCD_MPH/mph_lecture/mph_dissertation/data/test_signed_member.xlsx')

    # 19 countries selected

    result_df = signed_df[signed_df.isin(
        ['Estonia', 'Costa Rica', 'Mexico', 'Czechia', 'Netherlands', 'Georgia', 'Spain', 'Singapore', 'Latvia',
         'Germany',
         'Guatemala', 'Kazakhstan', 'Austria', 'Serbia', 'Lithuania', 'Ecuador', 'Iceland', 'Slovenia', 'Mauritius',
         ]).any(axis=1)].dropna(how='all')

    result_df.to_excel("/Users/wei/Documents/UCD_MPH/mph_lecture/mph_dissertation/data/19_finaltest.xlsx")

    year_mask = [2018, 2019]
    save_path = Path('/Users/wei/Documents/UCD_MPH/mph_lecture/mph_dissertation/data/19_finaltest,5yrs interval.xlsx')
    new_df = consistent_year(result_df, year_mask=year_mask, save_path=save_path)
