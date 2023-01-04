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


def preprocess_cvd(df: pd.DataFrame,
                   grouping_age: bool = True,
                   save: bool = True) -> pd.DataFrame:
    """
    Dataframe of WHO_CVD_mortality modify:
    - grouping if set kwarg `grouping_age` as true
    - Calculate total number of death
    - Calculate Total percentage of cause-specific deaths out of total deaths (%) =
    Sum of number of ALL n Males n Females/Sum of total number of death of ALL n Males n Females * 100
    - save as another dataframe

    :param df: input dataframe (WHO_CVD_mortality)
    :param grouping_age: 16 age groups --> one age group (greater 15 y/o)
    :param save: save modified dataframe to another excel
    :return: df
    """

    # Sum of number of death in each age group
    numbers = df['Number']
    percentage = df['Percentage of cause-specific deaths out of total deaths']
    df["Total number of death"] = numbers * 100 / percentage
    total_number_of_death = df["Total number of death"]
    mask_nan = np.isnan(total_number_of_death)  # type: pd.Series[bool]
    total_number_of_death[mask_nan] = 0
    total_number_of_death = total_number_of_death.astype(int)  # astype can cast/change multiple types
    df['Total number of death'] = total_number_of_death
    # mask_nan = np.isnan(total_percentage)  # type: pd.Series[bool]
    # total_percentage[mask_nan] = 0
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

    :param df: df after preprocess_cvd
    :param save:
    :return: df
    """


    try:
        total_number_of_death = df["Total number of death"]  # if this function can't find total_number_of_death.
    except KeyError:
        raise RuntimeError('call preprocess_cvd in advance')  # it will show error for u to fix it.

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
    # 為何不行 df['Total percentage of CVD'] = numbers.sum() / total_number_of_death.sum() * 100
    # total_percentage_of_cvd = df['Total percentage of CVD']
    # noinspection PyTypeChecker
    dy['total_percentage_of_cvd'] = np.array(numbers.sum() / total_number_of_death.sum() * 100)

    new_df = pd.DataFrame.from_dict(dy)
    new_df.to_excel('test_.xlsx')


    # new_df = pd.DataFrame({'Entity': df.groupby(['Entity'])['Entity'], 'Year': df.groupby(['Year'])['Year'], 'Sex':
    # df.groupby(['Sex'])['Sex'], 'Total percentage of CVD': total_percentage_of_cvd})
    # print(total_percentage_of_cvd)


    # df['Total percentage of CVD'] = total_percentage_of_cvd

    #    entity_list = df['Entity'].unique()
    #    year_list = df['Year'].unique()
    #    sex_list = df['Sex'].unique()
    #    for entity in entity_list:
    #        for year in year_list:
    #            for sex in sex_list:
    #                mask_a = df['Entity'] == entity
    #                mask_b = df['Year'] == year
    #                mask_c = df['Sex'] == sex

    #                mask_all = mask_a & mask_b & mask_c

    #                print(df[mask_all].shape[0])

    if save:
        pass
    return df


if __name__ == '__main__':
    df = pd.read_excel(
        '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/MPH '
        'Dissertation/WHO_Cardiovascular_Disease_Mortality_specific_year_Age_over15.xlsx', engine='openpyxl')

    df = preprocess_cvd(df)
    create_age_grouping(df)
