"""
pipline
picture whether Age group affect CVD mortality
"""
import pandas as pd
import os
import matplotlib.pyplot as plt
cvd = pd.read_excel('/Users/wei/UCD-MPH/MPH Lecture/MPH Dissertation/Data (WHO CVD and Tobacco '
                   'Use)/WHO_Cardiovascular_Disease_Mortality_Database_preprocess.xlsx')

select_19_countries = cvd[cvd['Country Name'].isin(['Estonia', 'Costa Rica', 'Mexico', 'Czechia', 'Netherlands', 'Georgia',
                                              'Spain', 'Singapore', 'Latvia', 'Germany', 'Guatemala', 'Kazakhstan',
                                              'Austria', 'Serbia', 'Lithuania', 'Ecuador', 'Iceland', 'Slovenia',
                                              'Mauritius'])].dropna(how='all')
desired_years = [2000, 2005, 2010, 2015, 2020]
filtered_df = select_19_countries[select_19_countries['Year'].isin(desired_years)]

filtered_df.to_excel('/Users/wei/UCD-MPH/MPH Lecture/MPH Dissertation/Data (WHO CVD and Tobacco '
                            'Use)/WithoutAgeGrouping.xlsx')


# build line chart
countries = filtered_df['Country Name'].unique()

for country in countries:
    country_data = filtered_df[filtered_df['Country Name'] == country]

    male_data = country_data[country_data['Sex'] == 'Male'].reset_index(drop=True)
    female_data = country_data[country_data['Sex']== 'Female'].reset_index(drop=True)
    all_data = country_data[country_data['Sex'] == 'All'].reset_index(drop=True)

    # Male
    plt.figure()
    plt.title(country + ' - Male')
    for year in [2000, 2005, 2010, 2015, 2020]:
        year_data = male_data[male_data['Year'] == year]
        plt.plot(year_data['Age Group'], year_data['Percentage of cause-specific deaths out of total deaths'], label=str(year))

    plt.xlabel('Age Group')
    plt.ylabel('Cardiovascular disease mortality (%)')

    plt.legend()
    plt.show()

    # Female
    plt.figure()
    plt.title(country + ' - Female')
    for year in [2000, 2005, 2010, 2015, 2020]:
        year_data = female_data[female_data['Year'] == year]
        plt.plot(year_data['Age Group'], year_data['Percentage of cause-specific deaths out of total deaths'], label=str(year))

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
# todo: lines are weird???????