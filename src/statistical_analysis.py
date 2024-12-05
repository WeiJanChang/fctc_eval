import pandas as pd
from scipy.stats import pearsonr
from pathlib import Path
from typing import Union

PathLike = Union[Path, str]


def evaluate_correlation(df: pd.DataFrame, output_path: PathLike = None) -> pd.DataFrame:
    """
    Evaluate the correlation between smoking rates and CVD mortality before and after FCTC ratification for each country.
    :param df: df
    :return: df
    """
    results = {}
    df['Year'] = df['Year'].astype(str)
    df['Ratified Year'] = df['Ratification'].astype(str)

    for country, country_data in df.groupby(['Country Name']):
        # Find the year before and after FCTC ratification
        before_year = df['Year'] < df['Ratified Year']
        after_year = df['Year'] > df['Ratified Year']

        # Calculate the correlation between smoking rates and CVD mortality before FCTC ratification
        before_data = df[before_year]
        before_corr_F, _ = pearsonr(before_data['Female_Total_Percentage_of_Cause_Specific_Deaths_Out_Of_Total_Deaths'],
                                    before_data[
                                        'Female_Estimate_of_Current_Tobacco_Use_Prevalence_age_standardized_rate'])
        before_corr_M, _ = pearsonr(before_data['Male_Total_Percentage_of_Cause_Specific_Deaths_Out_Of_Total_Deaths'],
                                    before_data[
                                        'Male_Estimate_of_Current_Tobacco_Use_Prevalence_age_standardized_rate'])

        # Calculate the correlation between smoking rates and CVD mortality after FCTC ratification
        after_data = df[after_year]
        after_corr_F, _ = pearsonr(after_data['Female_Total_Percentage_of_Cause_Specific_Deaths_Out_Of_Total_Deaths'],
                                   after_data[
                                       'Female_Estimate_of_Current_Tobacco_Use_Prevalence_age_standardized_rate'])
        after_corr_M, _ = pearsonr(after_data['Male_Total_Percentage_of_Cause_Specific_Deaths_Out_Of_Total_Deaths'],
                                   after_data['Male_Estimate_of_Current_Tobacco_Use_Prevalence_age_standardized_rate'])

        # Store the results for the current country
        results[country] = {'Female_before_FCTC': before_corr_F, 'Female_after_FCTC': after_corr_F,
                            'Male_before_FCTC': before_corr_M, 'Male_after_FCTC': after_corr_M}

        result_df = pd.DataFrame.from_dict(results, orient='index').reset_index()
        result_df.rename(columns={'level_0': 'Country Name'}, inplace=True)
        # show country name in df

        if output_path is not None:
            result_df.to_excel(output_path, index=False)
    return result_df

