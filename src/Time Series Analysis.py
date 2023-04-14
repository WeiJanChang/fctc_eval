"""
pipeline

I. Plot the time series
todo: write only one function to run 4 different variables instead of using 4 functions

II. Check for stationary, seasonality, and trend

III. Check for autocorrelation

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
