# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 17:19:10 2022

@author: katmax

Script 8 of 8
Purpose: to put each of the big counties and their corresponding places on their own layers, and prepares them for visualizing in QGIS

"""

#%%

import pandas as pd
import geopandas as gpd
import os
import fiona # GIS module that handles files

# set up file for output
out_file = "filter.gpkg"

# delete file if it already exists
if os.path.exists(out_file):
    os.remove(out_file)
    
#%% Filtering out big counties, making into its own layer

# reading in whole state layer, immediately write out
state = gpd.read_file("merge.gpkg", layer = "state")
state.plot() # this visualizes the entire state with census tracts in white
state.to_file(out_file, layer = "state", index = False)

# read in the ACS data on big counties from the previous script with the correct variable types
fips = { 'county' : str , 'GEOID_tract' : str, 'tract' : str}
big = pd.read_csv("big.csv", dtype = fips) 

# recreate the list of big counties by pulling from the big dataframe (unique values)
counties = big.county.unique().tolist()

# go through whole state, only select not those GEOIDs that are the islands in LA County
state = state.query("(GEOID_tract != '06037599100') & (GEOID_tract != '06037599000')")

# filter out big counties, make own dataframe    
is_big = state["COUNTYFP"].isin(counties) # T/F if the county is in the list of big counties
big_only = state [ is_big ]

# doing test plots to check where the counties are visually 
big_only.plot("COUNTYFP") # this plots each county on its own plot
big_only.plot() # this plots all big counties together on 1 plot 
    
# write out the layer of big counties to geopackage file
big_only.to_file(out_file, layer = "big_counties", index = False)
    
#%% Create 1 layer for each of the big counties

# create a dictionary with the county codes and county names
county_names = {'001' : 'Alameda',
                '067' : 'Sacramento',
                '085' : 'Santa Clara',
                '037' : 'Los Angeles',
                '073' : 'San Diego',
                '071' : 'San Bernardino',
                '065' : 'Riverside',
                '059' : 'Orange'}

# for loop to select individual counties, plot them, export as individual layers
# this creates 2 layers per county - one with place names, one with the Census data by tract
for code,name in county_names.items(): # return the key and value for each entry
    lname = name.lower().replace(' ','') # make a lower case name with no spaces
    selected = state.query( f"COUNTYFP == '{code}'") # select the county through a query of the entire state
    selected.plot("COUNTYFP") # plot each county individually
    selected.to_file(out_file, layer = f"{lname}", index = False) # write it out as its own layer
    # using the lowercase name defined earlier as the layer name
    places = selected.dissolve("NAME") # dissolve the tracts by county, based on place name
    places.to_file(out_file, layer = f"{lname}-places") # make it its own layer, write Index as part of layer 
#%% Checking our layers are all there
# should be state, big counties, each county, and each county-places

layers = fiona.listlayers(out_file)
print( f'Layers in {out_file}:', layers )
