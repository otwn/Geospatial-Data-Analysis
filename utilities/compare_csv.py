import numpy as np
import math
import pandas as pd
import geopandas as gpd
from metaflow import step


def find_diff_rows_number(df1, df2):
    result = f"The number of different rows between 2 df: {len(df1[~df1.apply(tuple,1).isin(df2.apply(tuple,1))])}"
    return result


def find_diff_rows_and_cells(df1, df2):
    stacked = (df1 != df2).stack()
    changed = stacked[stacked]
    changed.index.names = ['id', 'col']
    difference_locations = np.where(df1 != df2)
    changed_from = df1.values[difference_locations]
    changed_to = df2.values[difference_locations]
    diff_df = pd.DataFrame({'from': changed_from, 'to': changed_to}, index=changed.index)
    # even though both df1['col1'] and df2['col1'] are NaN, diff_df contains the rows. remove them.
    idx = diff_df.index[diff_df.notnull().all(axis=1)]
    non_df = diff_df.iloc[idx]
    return non_df


def compare_df(df1, df2, align_axis=1, keep_shape=False, keep_equal=False):
    """
    Using pandas function to compare two dataframes
    """
    return df1.compare(df2, align_axis, keep_shape, keep_equal)
    

def format_dataframe(df, sort_column):
    """
    df: pandas dataframe
    sort_column: a specific column name used for sorting
    
    This will return a formatted dataframe: column is sorted by name 
    and row is sorted by the specific column. Then drop the index.
    """
    df = df.reindex(sorted(df.columns), axis=1)
    df = df.sort_values(by=sort_column)
    df.reset_index(drop=True, inplace=True)
    return df


def remove_null_column(df):
    nn = df.nunique(axis=0)
    unique_index = [i for i in range(len(nn)) if nn[i] == 0]
    df2 = df.drop(nn.index[unique_index], axis=1)
    return df2


def check_duplicate(df):
    return df[df.duplicated() == True]


def wgs2utmEPSG(latitude:float, longitude:float):
    """
    Find the UTM Zone based on latitude/longitude in WGS84
    Input: latitude, longitude
    Return EPSG code 326xx in northern hemisphere, 327xx in southern hemisphere
    """
    if longitude > -180 and longitude < 180:
        utmzone = (math.floor((longitude + 180)/6) % 60) + 1
        if (latitude > -90 and latitude < 0):
            epsg = int("".join(("327",str(utmzone))))
        elif (latitude < 90 and latitude > 0):
            epsg = int("".join(("326", str(utmzone))))
        else:
            print(f"Latitude is out of range: {latitude}")
    else:
        print(f"Longitude is out of range: {longitude}")
        
    return epsg


def calculate_distance(row, dest_geom, src_col='geometry', target_col='distance'):
    """
    Calculates the distance between Point geometries.
    Assumed row and dest_gom are projected (e.g. UTM. Unit is meter)
    Parameters
    ----------
    dest_geom : shapely.Point
       A single Shapely Point geometry to which the distances will be calculated to.
    src_col : str
       A name of the column that has the Shapely Point objects from where the distances will be calculated from.
    target_col : str
       A name of the target column where the result will be stored.

    Returns
    -------
    Distance in meters that will be stored in 'target_col'.
    """

    # Calculate the distances
    dist = row[src_col].distance(dest_geom)

    # Convert into kilometers
    dist_km = dist / 1000

    # Assign the distance to the original data
    # row[target_col] = dist_km
    row[target_col] = round(dist,3)
    
    return row
