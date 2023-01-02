"""
pipeline
** df1(CVD Mortality):
    header:Entity, Year, Sex, Total number of death, Death rate per 100,000 population,
    Total percentage of cause-specific deaths out of total deaths

** df2(Tobacco Use):
    header:Entity, Year, Prevalence of current tobacco use, males (% of male adults),
    Prevalence of current tobacco use, females (% of male adults), Population (historical estimates)


** combine
1.
2.
3.

"""
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
    :return:
        TODO
    """
    # Sum of number of death in age groups
    numbers = df['Number']
    total_percentage = df['Percentage of cause-specific deaths out of total deaths']
    df["Total number of death"] = numbers * 100 / total_percentage
    total_number_of_death = df["Total number of death"]
    mask_nan = np.isnan(total_number_of_death)  # type: pd.Series[bool]
    total_number_of_death[mask_nan] = 0
    total_number_of_death = total_number_of_death.astype(int)  # astype can cast/change multiple types

    print(type(total_number_of_death[0]))

    print(df[:5].to_markdown())

    if save:
        pass
    # pass : 不要理他


if __name__ == '__main__':
    df = pd.read_excel(
        '/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/MPH Dissertation/WHO_Cardiovascular_Disease_Mortality_specific_year_Age_over15.xlsx')
    preprocess_cvd(df)
