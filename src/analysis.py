"""
pipeline

Step 1: select without missing data between CVD and Tobacco
Step 2: select the year which countries sign the treaty and compare CVD mortality before and after the treaty
Step 3: Use statistical method to analysis, which one???


"""

import pandas as pd

df = pd.read_excel('/Users/wei/Python/MPHDissertation/test_file/Merge_CVD_Tobacco.xlsx')
df = df.dropna(how='any')  # drop the rows having Nan
# df.to_excel('no_missing_data.xlsx')
countries = df['Entity'].unique()
number_of_countries = len(countries)
# print(number_of_countries, countries)  # 85 countries
