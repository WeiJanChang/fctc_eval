"""
pipeline

Step 1: select without missing data between CVD and Tobacco
??Step 2: select the year which countries sign the treaty and compare CVD mortality before and after the treaty
??Step 3: Use statistical method to analysis, which one???


"""

import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional, List
from pathlib import Path

# drop any nan in rows
df = pd.read_excel('/Users/wei/Python/MPHDissertation/test_file/CVD_Tobacco_merged_with_missingdata.xlsx')
df = df.dropna(how='any')  # drop the rows having Nan
# df.to_excel('no_missing_data.xlsx')
countries = df['Entity'].unique()
number_of_countries = len(countries)


# print(number_of_countries, countries)  # 85 countries

def plot_relationship(df: pd.DataFrame,
                      select_country: Optional[List[str]] = None,
                      variable_1: Optional[List[str]] = None,
                      variable_2: Optional[List[str]] = None,
                      x_label: str = None,
                      y_label: str = None,
                      save_path: Optional[Path] = None) -> pd.DataFrame:
    df['Year'] = df['Year'].astype(str)
    if select_country is not None:
        for country in select_country:
            country_df = df[df['Entity'] == country]
            if variable_1 is not None:
                plt.plot(country_df['Year'], country_df[variable_1[0]], label=variable_1[0])
            if variable_2 is not None:
                plt.plot(country_df['Year'], country_df[variable_2[0]], label=variable_2[0])
            if x_label is not None:
                plt.xlabel(x_label)
            if y_label is not None:
                plt.ylabel(y_label)
            plt.legend()
            plt.xticks(country_df['Year'], rotation=90)

            plt.title(f'CVD Mortality and Prevalence of Tobacco Use in {country}')
            plt_country = plt.show()

    if save_path is not None:
        plt_country.savefig(save_path, dpi=300, bbox_inches='tight')
    return df


if __name__ == '__main__':
    df = pd.read_excel(
        "/Users/wei/UCD-MPH/MPH-Lecture:Modules/MPH Dissertation/Data/CVD_Tobacco_Parties_ratified.xlsx")
    select_country = df['Entity'].unique()
    variable_1 = ['Female_total_percentage_of_CVD']
    variable_2 = ['Prevalence of current tobacco use, females (% of female adults)']
    x_label = 'Year'
    y_label = 'Total Percentage of CVD Mortality & Prevalence of Tobacco Use'
    save_path = '/Users/wei/Python/MPHDissertation/test_file/plot.png'
    for country in select_country:
        df = plot_relationship(df, select_country=[country], variable_1=variable_1, variable_2=variable_2,
                               x_label=x_label, y_label=y_label, save_path=save_path)
if save_path.exists():
    print(f"{save_path} exists.")
else:
    print(f"{save_path} does not exist.")
