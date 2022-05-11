# -*- coding: utf-8 -*-
"""
Created on Mon Apr 18 12:37:55 2022

@author: katmax

Script 6 of 8
Purpose: to analyze and extract the desired American Community Survey (ACS) data to prepare for geomapping 

"""

#%% Setup

import pandas as pd

# ensure we read in the geographic variables as strings
fips = { 'state' : str, 'county' : str , 'GEOID' : str, 'tract' : str}

# import data from previous script
acs = pd.read_csv("acs-data.csv", dtype = fips) 

# get info on variables
acs.info()

# set index to necessary geographical information
acs = acs.set_index(["GEOID", "county", "tract"])

#%%

# calculate the total # of married and unmarried women in the labor force
# who had a birth in the last 12 months, by tract 
print("Total number of married & unmarried CA women in the labor force who gave birth in the last 12 months", 
      acs[["ma_lf_b12", "un_w16-50_b12_lf"]].sum())

# aggregate counts to county level - see what's interesting

# build new dataframe with the variables of interest
bycounty = acs[["ma_lf_b12", "un_w16-50_b12_lf"]].copy()

# add up in each county the #'s of married and unmarried women in the labor force
# who had a birth in the last 12 months
bycounty["total_lf_b12"] = bycounty["ma_lf_b12"] + bycounty["un_w16-50_b12_lf"]

# now we can group by county - don't need to reset index
grouped = bycounty.groupby("county")

# add up variables by county
grouped = grouped["total_lf_b12"].sum()

# grab counties where total women in labor force who had birth in last 12 months is over 10,000
topcounties = grouped[ grouped >= 10000 ]

print("There are", len(topcounties), "counties with high amounts of women in the labor force who have given birth in the last 12 months.")
     
# disaggregate counts to tract level for the top counties
# here, reset index to be able to access the county numbers to create the list
topcounties = topcounties.reset_index() 

# turn the column of county numbers into a list, print to check
counties_list = list(topcounties["county"])
print("The county numbers of these big counties are:", counties_list)

# create a dataframe of the big counties only, and their tracts
acs = acs.reset_index()
is_big = acs['county'].isin(counties_list) # gives True / False if the county # is in the counties list
big = acs[is_big].copy() # make dataframe, which is a subset of acs data for big counties, copy

big = big.set_index(["GEOID", "county", "tract"]) # set index of big to preserve necessary information 
big = big[["ma_lf_b12", "un_w16-50_b12_lf"]] # trim down to the variables of interest

# recompute the totals
big["total_lf_b12"] = big["ma_lf_b12"] + big["un_w16-50_b12_lf"]

# export to CSV
big.to_csv("big.csv")
