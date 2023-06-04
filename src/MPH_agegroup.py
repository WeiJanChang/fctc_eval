import pandas as pd

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
