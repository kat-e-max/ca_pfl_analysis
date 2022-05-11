# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 09:59:54 2022

@author: katmax

Script 3 of 8
Purpose: to read in and clean the PFL claimant demographic data

"""

#%% Read in the data

import pandas as pd

# Read in data
    # header will be Female, Male, Unknown, Total of each claim type
    # thousands keyword to deal with the commas in the numbers
claimant = pd.read_csv("Claimant Demographics-DE_2530_Rev.5_1-22.csv", 
                       header=2,
                       thousands =',')

print( '\nClaimant is a DataFrame object:', type(claimant) )
print(claimant)
#%% Clean up the dataframe

# rename year column
claimant = claimant.rename(columns = {'Unnamed: 0' : "Year"})

# drop extra row
claimant = claimant.dropna(subset = "Year")

# ensure year is a string
claimant["Year"] = claimant["Year"].astype(int)

# Set index to year
claimant = claimant.set_index("Year")

# Pick out blocks of columns
cols = claimant.columns
bonding = claimant[cols[ :4]]
care = claimant[cols[4:8]]
total = claimant[cols[8:12]]

#%%
# check data types
claimant.dtypes

# convert dataframe from float to integer
claimant = claimant.astype(int)

# confirm change
claimant.dtypes

# Export to CSV
claimant.to_csv("claimant.csv")
