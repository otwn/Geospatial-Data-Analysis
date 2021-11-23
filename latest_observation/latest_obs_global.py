
import os
import requests
import numpy as np
import pandas as pd


# download latest_obs.txt using request
def download_latest_obs(url):
    response = requests.get(url)
    with open('latest_obs.txt', 'w') as f:
        f.write(response.text)


# read latest_obs.txt with pandas and return a dataframe
def get_latest_obs_df(filename):
    # read latest_obs.txt with pandas
    stations_df = pd.read_table(filename, delim_whitespace=True,\
        skiprows=[1])
    # replace "MM" with np.nan
    stations_df.replace('MM', np.nan, inplace=True)
    # convert to numeric
    stations_df = stations_df.apply(pd.to_numeric, errors='ignore')
    
    return stations_df


# save dataframe to csv
def save_df_to_csv(df, filename):
    df.to_csv(filename, index=False)


if __name__ == '__main__':
    url = 'https://ndbc.noaa.gov/data/latest_obs/latest_obs.txt'
    # download_latest_obs(url)

    stations = get_latest_obs_df(url)
    print(stations.head())

    save_df_to_csv(stations, 'latest_obs_global.csv')
        
