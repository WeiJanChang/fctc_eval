"""
pipeline

"""
import os
from pathlib import Path
from typing import Union, Tuple
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.figure import Figure

PathLike = Union[Path, str]


def plot_line_chart(df, column1: str, column2: str,
                    save_path: PathLike = None, nrows=5, ncols=4, figsize=(20, 20), dpi=200) -> Tuple[
    Figure, np.ndarray]:
    """
    Plots multi-subplot line chart with CVD Mortality Rates or Prevalence or Tobacco Use for multiple countries with annotations for policy ratification years.
    :param df: test file: 19_ratified_country.xlsx
    :param column1: 'Male_Total_Percentage_of_Cause_Specific_Deaths_Out_Of_Total_Deaths' or
                    'Male_Estimate_of_Current_Tobacco_Use_Prevalence_age_standardized_rate'
    :param column2: 'Female_Total_Percentage_of_Cause_Specific_Deaths_Out_Of_Total_Deaths' or
                    'Female_Estimate_of_Current_Tobacco_Use_Prevalence_age_standardized_rate'
    :param save_path: path
    :param nrows: showing five countries in a row in the figure
    :param ncols: showing four countries in a row in the figure
    :param figsize: figure size
    :param dpi: dpi
    :return: A tuple containing the figure and an array of Axes subplots.
    """
    # Filter DataFrame to exclude unwanted years
    df = df[(df['Year'] != 2018) & (df['Year'] != 2019)]

    # Get sorted list of unique countries
    countries = sorted(df['Country Name'].unique())

    # Create subplots
    fig, axs = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, dpi=dpi)
    axs = axs.flatten()  # Flatten the axes array for easy iteration

    # Iterate over countries and create plots
    for i, country in enumerate(countries):
        ax = axs[i]
        treaty_label = 'FCTC'

        # Plot Male and Female CVD mortality rates
        ax.plot(
            df.loc[df['Country Name'] == country, 'Year'],
            df.loc[df['Country Name'] == country, column1],
            color='tab:blue', label='Male'
        )
        ax.plot(
            df.loc[df['Country Name'] == country, 'Year'],
            df.loc[
                df['Country Name'] == country, column2],
            color='tab:red', label='Female'
        )

        # Set title and labels
        ax.set(title=country, xlabel='Year', ylabel='Proportionate CVD mortality (%)')
        ax.set_ylim([0, 80])
        ax.set_xlim([min(df['Year']), max(df['Year'])])
        ax.set_xticks(df['Year'].unique())
        ax.grid(True)
        ax.legend()

        # Add vertical line and annotation for Ratification year
        try:
            treaty_year = df.loc[df['Country Name'] == country, 'Ratification'].values[0]
            if not pd.isnull(treaty_year):
                ax.axvline(x=treaty_year, ymin=0, ymax=0.9, color='black', linestyle='--')
                ax.annotate(
                    treaty_label,
                    xy=(treaty_year, ax.get_ylim()[1]),
                    xytext=(2, -5),
                    textcoords='offset points',
                    ha='center',
                    va='top',
                    rotation=0
                )
                ax.annotate(
                    str(treaty_year),
                    xy=(treaty_year, ax.get_ylim()[1]),
                    xytext=(2, -15),
                    textcoords='offset points',
                    ha='center',
                    va='top',
                    rotation=0
                )
        except IndexError:
            print(f"No Ratification year available for {country}")

    # Hide unused subplots
    for j in range(len(countries), len(axs)):
        axs[j].axis('off')

    # Adjust layout and save the plot
    plt.tight_layout()
    if save_path is not None:
        plt.savefig(save_path, bbox_inches='tight')
    plt.show()
    plt.close()
    return fig, axs
