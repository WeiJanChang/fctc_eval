"""
pipeline

Dissertation:
    To compare the relationship between the Prevalence of Tobacco Use and Cardiovascular Disease mortality before and
    after the implementation of a tobacco treaty in World Health Organization Framework Convention on Tobacco Control
    ratified parties and additionally whether there were gender differences

Research Questions:
    i. Is there a relationship between the prevalence of tobacco use and CVD mortality before and after the
    implementation of a tobacco treaty in WHO FCTC ratified countries?

    ii. Is there a relationship between tobacco associated CVD, in terms of mortality and morbidity, and gender,
    pre and post implementation of FCTC?


Step 1: select 19 countries ratified in WHO FCTC
Step 2: select the year which countries ratified the treaty and compare CVD mortality in before and after the treaty
Step 3: Use statistical method to analysis
        i) Time-series analysis
        ii) Difference analysis
        iii) t-tests or analysis of variance
        iv) Multivariate regression analysis
"""

import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional, List
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional, List, Union
from pathlib import Path
import os
import statsmodels.api as sm
from statsmodels.tsa.stattools import grangercausalitytests


def plot_relationship(df: pd.DataFrame,
                      select_country: Optional[List[str]] = None,
                      variable_1: Optional[List[str]] = None,
                      variable_2: Optional[List[str]] = None,
                      x_label: Optional[str] = None,
                      y_label: Optional[str] = None,
                      save_path: Optional[Path] = None) -> None:
    # convert 'Year' column to string type
    df['Year'] = df['Year'].astype(str)
    # filter by selected countries
    if select_country is not None:
        for country in select_country:
            country_df = df[df['Country Name'] == country]
            # check if both variables exist in the DataFrame
            if variable_1 is not None and variable_1[0] in country_df.columns and \
                    variable_2 is not None and variable_2[0] in country_df.columns:
                # plot the two variables on the same figure
                fig, ax1 = plt.subplots()
                ax1.plot(country_df['Year'], country_df[variable_1[0]], label=variable_1[0], color='b')
                ax1.set_xlabel(x_label or 'Year')
                ax1.set_ylabel(variable_1[0], color='b')
                ax1.tick_params(axis='y', labelcolor='b')

                ax2 = ax1.twinx()
                ax2.plot(country_df['Year'], country_df[variable_2[0]], label=variable_2[0], color='r')
                ax2.set_ylabel(variable_2[0], color='r')
                ax2.tick_params(axis='y', labelcolor='r')

                plt.title(f'CVD Mortality and Prevalence of Tobacco Use in {country}')
                plt.xticks(country_df['Year'], rotation=90)
                plt.title(f'CVD Mortality and Prevalence of Tobacco Use in {country}')
                if save_path is not None:
                    if not os.path.exists(os.path.dirname(save_path)):
                        os.makedirs(os.path.dirname(save_path))
                    fig.savefig(save_path, dpi=300, bbox_inches='tight')

        plt_country = plt.show()
        print(plt_country)
        return plt_country


if __name__ == '__main__':
    df = pd.read_excel(
        "/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/19_ratified_country.xlsx")
    select_country = df['Country Name'].unique()
    variable_1 = ['CVD Mortality in Male (%)']
    variable_2 = ['Prevalence of Tobacco use in Male (age_standardized_rate) (%)']
    x_label = 'Year'
    y_label = 'CVD Mortality & Prevalence of Tobacco Use'
    save_path = '/Users/wei/Python/MPHDissertation/test_file/plot.png'
    df = plot_relationship(df, select_country=select_country, variable_1=variable_1, variable_2=variable_2,
                           x_label=x_label, y_label=y_label, save_path=save_path)
    if save_path is not None and os.path.isfile(save_path):
        print(f"{save_path} exists.")
    else:
        print(f"{save_path} does not exist.")
