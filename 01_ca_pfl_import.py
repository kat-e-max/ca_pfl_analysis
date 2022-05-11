# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 09:50:59 2022

@author: katmax

Script 1 of 8
Purpose: download and prepare the CA PFL monthly data

"""

# Note: Since the API only imports 100 of the 210 needed records, download the CSV file from the website instead.
# Website link: https://data.ca.gov/dataset/paid-family-leave-pfl-monthly-data/resource/918a5226-0794-4e3e-a9a1-c82e11e0c164
    
#%%
import pandas as pd

# read in the CSV downloaded from the above website
ca_pfl_data = pd.read_csv("Paid_Family_Leave__PFL__-_Monthly_Data.csv")

# basic data cleaning

# remove columns not needed: Area Type, California, _id
ca_pfl_data = ca_pfl_data.drop(columns = ["Area Type", "Area Name"])

# rename columns for ease of use
# Source: page 14 of https://edd.ca.gov/siteassets/files/pdf_pub_ctr/de2530.pdf

rename_info = {"Average Duration": "Average Duration (weeks)",
              "PFL Average Weekly Benefit Amount (AWBA)": "PFL Average Weekly Benefit Amount (AWBA) ($)",
              "Total Benefits Authorized": "Total Benefits Authorized (millions of $)",
              "Average Weekly Benefits Paid": "Average Weekly Benefits Paid ($)",
                "Total PFL First Claims Filled": "Total PFL First Claims Filed"}

ca_pfl_data = ca_pfl_data.rename(columns=rename_info)

# write to CSV, take out index
ca_pfl_data.to_csv("ca_pfl_data.csv", index = False)
