"""
pipeline

Research Questions:
    i. Is there a relationship between the prevalence of tobacco use and CVD mortality before and after the
    implementation of a tobacco treaty in WHO FCTC ratified countries?

    ii. Is there a relationship between tobacco associated CVD, in terms of mortality and morbidity, and gender,
    pre and post implementation of FCTC?

Step 1: select 19 countries ratified in WHO FCTC
Step 2: select the year which countries ratified the treaty and compare CVD mortality in before and after the treaty
Step 3: Use statistical method to analysis
        i) Interrupted Time Series Analysis

        This method can be used to assess the impact of an intervention (WHO FCTC) on causal relationships,
        including analyzing trends in epidemiological indicators (Prevalence of Tobacco Use and CVD mortality)
        before and after the intervention.

        Note:
            When setting the lag parameter in Autocorrelation analysis, it's important to make sure that the
            lag intervals are consistent with the time intervals of your data.
        Step 1:
            Exclude year 2018, 2019


        ii) Correlation Analysis

        This method can be used to evaluate the correlation between smoking rates and CVD mortality,
        as well as whether the intervention (WHO FCTC) has changed this relationship.

        iii) Multivariate Regression Analysis

        This method can be used to evaluate complex interactions between smoking, gender, and CVD mortality,
        including the impact of the intervention (WHO FCTC) on the relationships between these factors.
"""
import os
from pathlib import Path
from typing import Optional, List, Union
import matplotlib.pyplot as plt
import pandas as pd

PathLike = Union[Path, str]


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


def select_ratified_country(df: pd.DataFrame, output_path: PathLike = None) -> pd.DataFrame:
    interval_df = consistent_year(df, year_mask=[2018, 2019])
    count_df = interval_df['Country Name'].value_counts().to_frame()
    count_df.columns = ['count']  # choose the most datapoint of countries
    df = interval_df.copy()
    selected_19_countries = ['Estonia', 'Costa Rica', 'Mexico', 'Czechia', 'Netherlands', 'Georgia', 'Spain',
                             'Singapore', 'Latvia', 'Germany', 'Guatemala', 'Kazakhstan', 'Austria', 'Serbia',
                             'Lithuania', 'Ecuador', 'Iceland', 'Slovenia', 'Mauritius', ]
    selected_19_df = df[df.isin(selected_19_countries).any(axis=1)].dropna(how='all')

    if output_path is not None:
        selected_19_df.to_excel(output_path, index=False)
    return selected_19_df


def plot_relationship(df: pd.DataFrame,
                      select_country: Optional[List[str]] = None,
                      variable_1: Optional[str] = None,
                      variable_2: Optional[str] = None,
                      variable_3: Optional[str] = None,
                      variable_4: Optional[str] = None,
                      x_label: Optional[str] = None,
                      y_label: Optional[str] = None,
                      save_path: Optional[str] = None) -> None:
    """

    :param df: selected_19_df
    :param select_country: df['Country Name'].unique()
    :param variable_1: 'Male_Estimate_of_Current_Tobacco_Use_Prevalence_age_standardized_rate'
    :param variable_2: 'Male_Total_Percentage_of_Cause_Specific_Deaths_Out_Of_Total_Deaths'
    :param variable_3: 'Female_Estimate_of_Current_Tobacco_Use_Prevalence_age_standardized_rate'
    :param variable_4: 'Female_Total_Percentage_of_Cause_Specific_Deaths_Out_Of_Total_Deaths'
    :param x_label: 'Year'
    :param y_label:
    :param save_path: output path
    :return:
    """
    selected_19_df = select_ratified_country(df)
    df = selected_19_df.copy()
    # convert 'Year' column to string type
    df['Year'] = df['Year'].astype(str)
    # filter by selected countries
    if select_country is not None:
        for country in select_country:
            country_df = df[df['Country Name'] == country]
            # create a new figure with 2 subplots
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))
            # plot variable_1 and variable_2 on the first subplot
            ax1.plot(country_df['Year'], country_df[variable_1], color='b')
            ax1.plot(country_df['Year'], country_df[variable_2], color='r')
            ax1.set_xlabel(x_label or 'Year')
            ax1.set_ylabel('Prevalence of Tobacco Use & CVD Mortality', color='k')
            ax1.tick_params(axis='y', labelcolor='k')
            ax1.legend(['Prevalence of Tobacco Use in Males (%)', 'CVD Mortality in Males (%)'], loc='upper left')
            # plot variable_3 and variable_4 on the second subplot
            ax2.plot(country_df['Year'], country_df[variable_3], color='g')
            ax2.plot(country_df['Year'], country_df[variable_4], color='m')
            ax2.set_xlabel(x_label or 'Year')
            ax2.set_ylabel('Prevalence of Tobacco Use & CVD Mortality', color='k')
            ax2.tick_params(axis='y', labelcolor='k')
            ax2.legend(['Prevalence of Tobacco Use in Females (%)', 'CVD Mortality in Females (%)'], loc='upper left')
            # set titles and axis labels for the figure
            plt.suptitle(f'{country} Statistics')
            plt.xticks(country_df['Year'])

            if y_label is not None:
                fig.text(0.06, 0.5, y_label, va='center', rotation='vertical')
            if save_path is not None:
                if not os.path.exists(os.path.dirname(save_path)):
                    os.makedirs(os.path.dirname(save_path))
                fig.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.show()
