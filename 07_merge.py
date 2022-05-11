# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 10:48:30 2022

@author: katmax

Script 7 of 8
Purpose: to merge the data on big counties with their corresponding geographic data (tracts and places)

"""

#%% Setup

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os

#%% Read in data

# read in the ACS data from the previous script with the correct variable types
fips = { 'county' : str , 'GEOID' : str, 'tract' : str}
big = pd.read_csv("big.csv", dtype = fips) 

# Import TIGER/Line data for tract geometries
tracts = gpd.read_file("tl_2018_06_tract.zip")

# trim columns to those listed
tracts = tracts[['STATEFP', 'COUNTYFP', 'TRACTCE', 'GEOID', 'ALAND', 'AWATER', 'geometry']]

# rename GEOID column to be clear it's coming from the tracts dataset
tracts = tracts.rename(columns = {"GEOID" : "GEOID_tract"})

# Import TIGER/Line data for place geometries
places = gpd.read_file("tl_2018_06_place.zip")

# trim columns to those listed 
places = places[['PLACEFP', 'GEOID', 'NAME', 'geometry']]

# rename GEOID column to be clear it's coming from the places dataset
places = places.rename(columns = {"GEOID" : "GEOID_place"})

#%% Intersect the tracts and places

inter = tracts.overlay(places,
                       how = "union",
                       keep_geom_type = True)

#%% Select a place as an example - here, Culver City

sm_tr = inter.query('NAME == "Culver City"')

sm_pl = places.query('NAME == "Culver City"')

# plot it
fig, ax1 = plt.subplots(dpi = 300)
sm_pl.boundary.plot(color = 'black', ax = ax1)
sm_tr.plot(edgecolor = 'yellow', ax = ax1)
ax1.axis('off')

#%% Join the ACS data of big counties ('big') onto the intersected data ('inter').

# rename GEOID in the 'big' dataset to prepare for joining
big = big.rename(columns = {"GEOID" : "GEOID_tract"})

joined = inter.merge(big, 
                      on = "GEOID_tract", # join on GEOID
                      how = "left", # left merge
                      validate = "m:1", # it's a many-to-one merge
                      # many tracts can correspond to 1 place
                      indicator = True)

# print merge indicator
print( joined['_merge'].value_counts() )

# drop duplicate columns
joined = joined.drop(columns = ["_merge", "county", "tract"])

#%% Some cleaning up of the joined dataframe before exporting

# drop tracts where ALAND is 0 (i.e., tracts in big counties that are all water)

land = joined [joined["ALAND"] > 0]
print(len(joined) - len(land), "all-water tracts dropped.")

#%% Set projection and write out to geopackage file

# set the projection
utm11n = 32611
land = land.to_crs(utm11n)

# set the name of the output file
out_file = "merge.gpkg"

# delete file if it already exists
if os.path.exists(out_file):
    os.remove(out_file)

# export the geodataframe
land.to_file(out_file, layer = "state", index = False) 

