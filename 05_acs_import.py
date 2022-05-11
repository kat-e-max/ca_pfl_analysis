# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 14:00:35 2022

@author: katmax

Script 5 of 8
Purpose: to import data from the American Community Survey (ACS) using an API call

"""

#%% Setup

import requests
import pandas as pd

# read in the list of desired variables - Excel file
var_info = pd.read_excel("ACS2018_var.xlsx") 

# want to keep description
uniqueid = var_info["UniqueID"].dropna()
uniqueid = uniqueid + "E" 

# convert Pandas Series into a simple list
var_name = uniqueid.to_list()

# tell the API to return the official Census name of 
# the geographic entity in each row of the results
var_list = ['NAME'] + var_name

# count the number of variables in the list
# max is 50

numvar = len(var_list)

if numvar <= 50:
    print("Okay to proceed!")
else:
    print("There are currently", numvar - 50, "too many variables in the list.")

# create the variable list of the API call
# concatenate the elements of var_list into a single string
# should be separated by commas
var_string = ','.join(var_list)

#%%

# set API to the desired endpoint
api = 'https://api.census.gov/data/2018/acs/acs5'

# set for-clause
    # left: what kind of geographic unit should be returned
    # right: will be used to select subsets of possible records
    # asterisk is wildcard
for_clause = 'tract:*'

# set in-clause
    # limits selected geographic units, here counties in CA
in_clause = 'state:06'

# set key value
    # will be Census API key
key_value = "a0225738d55ced7dc6b7d7c572499f948c373ca5"

# set payload to a new dictionary
    # parameters you want to pass to the server, in the form of a dictionary. 
    # Keys are parameters API allows - here, 'get', 'for', and 'key'
    # values are what you would like parameters to be set to
payload = {'get' : var_string, # the desired variables
           'for' : for_clause, # for county/tract
           'in' : in_clause, # for state of CA
           'key' : key_value} # API key

# build an HTTPS query string, send to API endpoint, collect response
response = requests.get(api, payload)

# confirm success
if response.status_code == 200:
    print("Request succeeded!")
else: # print some details about what went wrong
    print('Status:', response.status_code)
    print(response.text)
    assert False 
    # stop the script immediately

# parse JSON returned by Census server
# return a list of rows
row_list = response.json()

# set column names to the first row
colnames = row_list[0]  

# set rows to the subsequent rows
datarows = row_list[1:]

# convert data to Pandas dataframe
acs = pd.DataFrame(columns = colnames, data = datarows)

# rename 'Name' column to Tract
acs = acs.rename(columns = {'NAME' : 'Tract'})

#%%
# make column names with variables more comprehensible
rename_info = {
               'B13012_001E' : "total_w16-50",
               'B13012_002E' : "total_w16-50_b12",
               'B13012_003E' : "ma_w16-50_b12",
               'B13012_004E' : "ma_lf_b12",
               'B13012_005E' : "ma_nolf_b12",
               'B13012_006E' : "un_w16-50_b12",
               'B13012_007E' : "un_w16-50_b12_lf",
               'B13012_008E' : "un_w16-50_b12_nolf",
               'B13012_009E' : "w_nobl12",
               'B13012_010E' : "w_nobl12_ma",
               'B13012_011E' : "w_nobl12_ma_lf",
               'B13012_012E' : "w_nobl12_ma_nolf",
               'B13012_013E' : "w_nobl12_un",
               'B13012_014E' : "w_nobl12_un_lf",
               'B13012_015E' : "w_nobl12_un_nolf"
                   } 

acs = acs.rename(columns = rename_info)
#%%
# construct full GEOID for the tract - will help with mapping

acs["GEOID"] = acs["state"] + acs["county"] + acs["tract"]

# set index to county and tract (will be #'s)
acs = acs.set_index("GEOID")

#%%
# write out dataframe to CSV file
acs.to_csv("acs-data.csv") 
