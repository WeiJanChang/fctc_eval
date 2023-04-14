"""
pipeline

I. Plot the time series
todo: write only one function to run 4 different variables instead of using 4 functions

II. Check for stationary, seasonality, and trend

III. Check for autocorrelation
todo: write only one function to run 4 different variables instead of using 4 functions

IV. Decompose the time series

V. Plot the decomposition

VI. Forecast future values

"""
import matplotlib
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from jedi.api.refactoring import inline

path = '/Users/wei/Python/MPHDissertation/test_file/19 ratified countries_21 March 23.xlsx'
df = pd.read_excel(path)


# Ia. CVD Mortality in Males
def plot_df(df, country, title="", xlabel='Year', ylabel='Male_Total Percentage of CVD Deaths', dpi=100):
    fig, ax = plt.subplots(figsize=(15, 4), dpi=dpi)
    ax.plot(df.loc[df['Country Name'] == country, 'Year'],
            df.loc[df['Country Name'] == country, 'Male_Total Percentage of CVD Deaths'], color='tab:red')
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.set_ylim([0, 100])
    ax.set_xlim([min(df['Year']), max(df['Year'])])
    ax.set_xticks(df['Year'].unique())
    ax.grid(True)


countries = df['Country Name'].unique()

fig, axs = plt.subplots(nrows=5, ncols=4, figsize=(20, 20), dpi=100)

for i in range(len(countries)):
    row = i // 4
    col = i % 4
    country = countries[i]
    ax = axs[row][col]
    ax.plot(df.loc[df['Country Name'] == country, 'Year'],
            df.loc[df['Country Name'] == country, 'Male_Total Percentage of CVD Deaths'], color='tab:red')
    ax.set(title='CVD Mortality Rate in Males in {}'.format(country), xlabel='Year',
           ylabel='Male_Total Percentage of CVD Deaths')
    ax.set_ylim([0, 100])
    ax.set_xlim([min(df['Year']), max(df['Year'])])
    ax.set_xticks(df['Year'].unique())
    ax.grid(True)
    # cause-specific mortality rate
plt.tight_layout()
plt.savefig('CVD Mortality Rate in Males.png')


# Ib. CVD Mortality in Females
def plot_df(df, country, title="", xlabel='Year', ylabel='Female_Total Percentage of CVD Deaths', dpi=100):
    fig, ax = plt.subplots(figsize=(15, 4), dpi=dpi)
    ax.plot(df.loc[df['Country Name'] == country, 'Year'],
            df.loc[df['Country Name'] == country, 'Female_Total Percentage of CVD Deaths'], color='tab:red')
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.set_ylim([0, 100])
    ax.set_xlim([min(df['Year']), max(df['Year'])])
    ax.set_xticks(df['Year'].unique())
    ax.grid(True)


countries = df['Country Name'].unique()

fig, axs = plt.subplots(nrows=5, ncols=4, figsize=(20, 20), dpi=100)

for i in range(len(countries)):
    row = i // 4
    col = i % 4
    country = countries[i]
    ax = axs[row][col]
    ax.plot(df.loc[df['Country Name'] == country, 'Year'],
            df.loc[df['Country Name'] == country, 'Female_Total Percentage of CVD Deaths'], color='tab:red')
    ax.set(title='CVD Mortality Rate in Females in {}'.format(country), xlabel='Year',
           ylabel='Female_Total Percentage of CVD Deaths')
    ax.set_ylim([0, 100])
    ax.set_xlim([min(df['Year']), max(df['Year'])])
    ax.set_xticks(df['Year'].unique())
    ax.grid(True)
    # cause-specific mortality rate
plt.tight_layout()
plt.savefig('CVD Mortality Rate in Females.png')


# Ic. Estimate of Tobacco Use Prevalence (%)(age-standardized rate) in Males
def plot_df(df, country, title="", xlabel='Year',
            ylabel='Male_Prevalence of Current Tobacco Use Estimated (ASR)', dpi=100):
    fig, ax = plt.subplots(figsize=(15, 4), dpi=dpi)
    ax.plot(df.loc[df['Country Name'] == country, 'Year'],
            df.loc[df['Country Name'] == country, 'Male_Prevalence of Current Tobacco Use Estimated (ASR)'],
            color='tab:red')
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.set_ylim([0, 100])
    ax.set_xlim([min(df['Year']), max(df['Year'])])
    ax.set_xticks(df['Year'].unique())
    ax.grid(True)


countries = df['Country Name'].unique()

fig, axs = plt.subplots(nrows=5, ncols=4, figsize=(20, 20), dpi=100)

for i in range(len(countries)):
    row = i // 4
    col = i % 4
    country = countries[i]
    ax = axs[row][col]
    ax.plot(df.loc[df['Country Name'] == country, 'Year'],
            df.loc[df['Country Name'] == country, 'Male_Prevalence of Current Tobacco Use Estimated (ASR)'],
            color='tab:red')
    ax.set(title='Prevalence of Tobacco Use in Males in {}'.format(country), xlabel='Year',
           ylabel='Male_Prevalence of Current Tobacco Use Estimated (ASR)')
    ax.set_ylim([0, 100])
    ax.set_xlim([min(df['Year']), max(df['Year'])])
    ax.set_xticks(df['Year'].unique())
    ax.grid(True)
    # cause-specific mortality rate
plt.tight_layout()
plt.savefig('Prevalence of Tobacco Use in Males.png')


# Id. Estimate of Tobacco Use Prevalence (%)(age-standardized rate) in Females
def plot_df(df, country, title="", xlabel='Year',
            ylabel='Female_Prevalence of Current Tobacco Use Estimated (ASR)', dpi=100):
    fig, ax = plt.subplots(figsize=(15, 4), dpi=dpi)
    ax.plot(df.loc[df['Country Name'] == country, 'Year'],
            df.loc[df['Country Name'] == country, 'Female_Prevalence of Current Tobacco Use Estimated (ASR)'],
            color='tab:red')
    ax.set(title=title, xlabel=xlabel, ylabel=ylabel)
    ax.set_ylim([0, 100])
    ax.set_xlim([min(df['Year']), max(df['Year'])])
    ax.set_xticks(df['Year'].unique())
    ax.grid(True)


countries = df['Country Name'].unique()

fig, axs = plt.subplots(nrows=5, ncols=4, figsize=(20, 20), dpi=100)

for i in range(len(countries)):
    row = i // 4
    col = i % 4
    country = countries[i]
    ax = axs[row][col]
    ax.plot(df.loc[df['Country Name'] == country, 'Year'],
            df.loc[df['Country Name'] == country, 'Female_Prevalence of Current Tobacco Use Estimated (ASR)'],
            color='tab:red')
    ax.set(title='Prevalence of Tobacco Use in Females in {}'.format(country), xlabel='Year',
           ylabel='Female_Prevalence of Current Tobacco Use Estimated (ASR)')
    ax.set_ylim([0, 100])
    ax.set_xlim([min(df['Year']), max(df['Year'])])
    ax.set_xticks(df['Year'].unique())
    ax.grid(True)
    # cause-specific mortality rate
plt.tight_layout()
plt.savefig('Prevalence of Tobacco Use in Females.png')

# II. Test for Stationarity
# ADF test
from statsmodels.tsa.stattools import adfuller
import sys

series = df.loc[:, 'Male_Total Percentage of CVD Deaths'].values
df.plot(figsize=(14, 8), legend=None, title='CVD Mortality in Males from 2000 to 2020')

# Open a file for writing
with open('ADF_test.txt', 'w') as f:
    # Redirect the standard output to the file
    sys.stdout = f

    # Loop over each country in the dataframe
    for country in df['Country Name'].unique():
        # Subset the data for the current country
        country_data = df[df['Country Name'] == country]['Male_Total Percentage of CVD Deaths']
        # Perform the ADF test
        result = adfuller(country_data, autolag='AIC')
        # Print the results to the console
        print(f'Country Name: {country}')
        print(f'ADF Statistic: {result[0]}')
        print(f'p-value: {result[1]}')
        print(f'n_lags: {result[2]}')
        for key, value in result[4].items():
            print(f'Critical Values: {key}, {value}')

    # Reset the standard output
    sys.stdout = sys.__stdout__

# III.Check for Autocorrelation
# IIIa.Autocorrelation_CVD Mortality in Males
from pandas.plotting import autocorrelation_plot

# Create a 5x4 grid of subplots
fig, axs = plt.subplots(nrows=5, ncols=4, figsize=(20, 20))
axs = axs.ravel()  # flatten the subplot array

# Draw plot for each city
for i, (city, group) in enumerate(df.groupby('Country Name')):
    autocorrelation_plot(group['Male_Total Percentage of CVD Deaths'].tolist(), ax=axs[i])
    axs[i].set_title(f'CVD Mortality in Males in {city}', fontsize=16)

# Adjust spacing between subplots
plt.tight_layout()
plt.savefig('Autocorrelation_CVD Mortality in Males.png')

# IIIb. Autocorrelation_CVD Mortality in Females
fig, axs = plt.subplots(nrows=5, ncols=4, figsize=(20, 20))
axs = axs.ravel()
for i, (city, group) in enumerate(df.groupby('Country Name')):
    autocorrelation_plot(group['Female_Total Percentage of CVD Deaths'].tolist(), ax=axs[i])
    axs[i].set_title(f'CVD Mortality in Females in {city}', fontsize=16)

plt.tight_layout()
plt.savefig('Autocorrelation_CVD Mortality in Females.png')

# IIIc. Estimate of Tobacco Use Prevalence (%)(age-standardized rate) in Males
fig, axs = plt.subplots(nrows=5, ncols=4, figsize=(20, 20))
axs = axs.ravel()
for i, (city, group) in enumerate(df.groupby('Country Name')):
    autocorrelation_plot(group['Male_Prevalence of Current Tobacco Use Estimated (ASR)'].tolist(), ax=axs[i])
    axs[i].set_title(f'Prevalence of Tobacco Use in Males in {city}', fontsize=14.5)

plt.tight_layout()
plt.savefig('Autocorrelation_Tobacco use in Males.png')

# IIId. Estimate of Tobacco Use Prevalence (%)(age-standardized rate) in Females
fig, axs = plt.subplots(nrows=5, ncols=4, figsize=(20, 20))
axs = axs.ravel()

for i, (city, group) in enumerate(df.groupby('Country Name')):
    autocorrelation_plot(group['Female_Prevalence of Current Tobacco Use Estimated (ASR)'].tolist(), ax=axs[i])
    axs[i].set_title(f'Prevalence of Tobacco Use in Females in {city}', fontsize=14.5)

plt.tight_layout()
plt.savefig('Autocorrelation_Tobacco use in Females.png')

# Autocorrelation and Partial Autocorrelation Functions
# 1.Autocorrelation is simply the correlation of a series with its own lags. If a series is significantly
# autocorrelated, that means, the previous values of the series (lags) maybe helpful in predicting the current value.
# 2.Partial Autocorrelation also conveys similar information but it conveys the pure correlation of a series and
# its lag, excluding the correlation contributions from the intermediate lags.

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

# Draw Plot
# Create a new figure and set the size
# 1. ACF and PACF_CVD Mortality in Males
# Create a new figure and set the size
fig, axes = plt.subplots(len(df.groupby('Country Name')), 2, figsize=(12, 40), dpi=100)

# Loop through the countries and add subplots to the figure
for i, (country, group) in enumerate(df.groupby('Country Name')):
    # Plot the ACF and PACF on the subplots
    plot_acf(group['Male_Total Percentage of CVD Deaths'].tolist(), lags=4, ax=axes[i, 0])
    plot_pacf(group['Male_Total Percentage of CVD Deaths'].tolist(), lags=1, method='ywm', ax=axes[i, 1])

    # Set the titles for the subplots
    axes[i, 0].set_title(f'{country} ACF-CVD Mortality in Males')
    axes[i, 1].set_title(f'{country} PACF-CVD Mortality in Males')

# Adjust the layout of the subplots and save the figure as a PNG file
plt.tight_layout()
plt.savefig('ACF and PACF_CVD Mortality in Males.png', dpi=100)

# 2. ACF and PACF_CVD Mortality in Females
fig, axes = plt.subplots(len(df.groupby('Country Name')), 2, figsize=(12, 40), dpi=100)

for i, (country, group) in enumerate(df.groupby('Country Name')):
    plot_acf(group['Female_Total Percentage of CVD Deaths'].tolist(), lags=4, ax=axes[i, 0])
    plot_pacf(group['Female_Total Percentage of CVD Deaths'].tolist(), lags=1, method='ywm', ax=axes[i, 1])

    axes[i, 0].set_title(f'{country} ACF-CVD Mortality in Females')
    axes[i, 1].set_title(f'{country} PACF-CVD Mortality in Females')
plt.tight_layout()
plt.savefig('ACF and PACF_CVD Mortality in Females.png', dpi=100)

# 3. ACF and PACF_Tobacco Use Prevalence in Males
fig, axes = plt.subplots(len(df.groupby('Country Name')), 2, figsize=(12, 40), dpi=100)

for i, (country, group) in enumerate(df.groupby('Country Name')):
    plot_acf(group['Male_Prevalence of Current Tobacco Use Estimated (ASR)'].tolist(), lags=4, ax=axes[i, 0])
    plot_pacf(group['Male_Prevalence of Current Tobacco Use Estimated (ASR)'].tolist(), lags=1, method='ywm',
              ax=axes[i, 1])

    axes[i, 0].set_title(f'{country} ACF-Prevalence of Tobacco Use in Males')
    axes[i, 1].set_title(f'{country} PACF-Prevalence of Tobacco Use in Males')

plt.tight_layout()
plt.savefig('ACF and PACF_Prevalence of Tobacco Use in Males.png', dpi=100)

# 4. ACF and PACF_Tobacco Use Prevalence in Females
fig, axes = plt.subplots(len(df.groupby('Country Name')), 2, figsize=(12, 40), dpi=100)

for i, (country, group) in enumerate(df.groupby('Country Name')):
    plot_acf(group['Female_Prevalence of Current Tobacco Use Estimated (ASR)'].tolist(), lags=4, ax=axes[i, 0])
    plot_pacf(group['Female_Prevalence of Current Tobacco Use Estimated (ASR)'].tolist(), lags=1, method='ywm',
              ax=axes[i, 1])

    axes[i, 0].set_title(f'{country} ACF-Prevalence of Tobacco Use in Females')
    axes[i, 1].set_title(f'{country} PACF-Prevalence of Tobacco Use in Females')

plt.tight_layout()
plt.savefig('ACF and PACF_Prevalence of Tobacco Use in Females.png', dpi=100)

# IV. Decompose the time series
from statsmodels.tsa.seasonal import seasonal_decompose
from dateutil.parser import parse

# ValueError: x must have 2 complete cycles requires 60 observations. x only has 5 observation(s)
