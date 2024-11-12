"""
pipeline

Plot the relationship

"""
import os
from pathlib import Path
from typing import Optional, List, Union
import matplotlib.pyplot as plt
import pandas as pd
from selected_countries import selected_19_countries
from preprocess_analysis import select_ratified_country

PathLike = Union[Path, str]


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


def plot_agegroup(df: pd.DataFrame, dir_path: PathLike):
    """
    picture whether Age group affect CVD mortality

    :param df:
    :return:
    """

    cvd = pd.read_excel(dir_path / 'WHO_Cardiovascular_Disease_Mortality_Database_preprocess.xlsx')
    select_19_countries = cvd[cvd['Country Name'].isin(selected_19_countries)].dropna(how='all')
    desired_years = [2000, 2005, 2010, 2015, 2020]
    filtered_df = select_19_countries[select_19_countries['Year'].isin(desired_years)]
    filtered_df.to_excel(dir_path / 'WithoutAgeGrouping.xlsx')

    # build line chart
    countries = filtered_df['Country Name'].unique()

    for country in countries:
        country_data = filtered_df[filtered_df['Country Name'] == country]

        male_data = country_data[country_data['Sex'] == 'Male'].reset_index(drop=True)
        female_data = country_data[country_data['Sex'] == 'Female'].reset_index(drop=True)
        all_data = country_data[country_data['Sex'] == 'All'].reset_index(drop=True)

        # Male
        plt.figure()
        plt.title(country + ' - Male')
        for year in [2000, 2005, 2010, 2015, 2020]:
            year_data = male_data[male_data['Year'] == year]
            plt.plot(year_data['Age Group'], year_data['Percentage of cause-specific deaths out of total deaths'],
                     label=str(year))

        plt.xlabel('Age Group')
        plt.ylabel('Cardiovascular disease mortality (%)')

        plt.legend()
        plt.show()

        # Female
        plt.figure()
        plt.title(country + ' - Female')
        for year in [2000, 2005, 2010, 2015, 2020]:
            year_data = female_data[female_data['Year'] == year]
            plt.plot(year_data['Age Group'], year_data['Percentage of cause-specific deaths out of total deaths'],
                     label=str(year))

        plt.xlabel('Age Group')
        plt.ylabel('Cardiovascular disease mortality (%)')

        plt.legend()
        plt.show()

        # All gender
        plt.figure()
        plt.title(country + ' - Both gender')
        for year in [2000, 2005, 2010, 2015, 2020]:
            year_data = all_data[all_data['Year'] == year]
            plt.plot(year_data['Age Group'], year_data['Percentage of cause-specific deaths out of total deaths'],
                     label=str(year))

        plt.xlabel('Age Group')
        plt.ylabel('Cardiovascular disease mortality (%)')

        plt.legend()
        plt.show()
# todo: test these code and present it on readme