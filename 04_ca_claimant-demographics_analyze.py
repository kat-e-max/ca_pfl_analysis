# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 15:18:56 2022

@author: katmax

Script 4 of 8
Purpose: to analyze the PFL claimant demographic data, and plot some visualizations

"""
    
#%% Setup

import pandas as pd
import matplotlib.pyplot as plt

#%% Read in data

# Read in claimant data
claimant = pd.read_csv("claimant.csv")

# set index to year
claimant = claimant.set_index("Year")

# set up same columns from last script
cols = claimant.columns
bonding = claimant[cols[ :4]]
care = claimant[cols[4:8]]
total = claimant[cols[8: 12]] 

# rename care columns
rename_care = { 
    "Female.1": "Female",
    "Male.1": "Male",
    "Unknown.1": "Unknown",
    "Total.1" : "Total"
    }

care = care.rename(columns=rename_care)

# rename total columns
rename_total = { 
    "Female.2": "Female",
    "Male.2": "Male",
    "Unknown.2": "Unknown",
    "Total.2" : "Total"
    }

total = total.rename(columns=rename_total)

#%% Analysis: what is share of female claims vs. male claims to total claims?
# multiply by 100 so values are percentages

# calculate share of care claims
share_f_care = (care["Female"] / care["Total"]*100)
share_m_care = (care["Male"] / care["Total"]*100)

# calculate share of bonding claims
share_f_bonding = (bonding["Female"] / bonding["Total"]*100)
share_m_bonding = (bonding["Male"] / bonding["Total"]*100)

# calculate share of total claims
share_f_total = (total["Female"] / total["Total"]*100)
share_m_total = (total["Male"] / total["Total"]*100)

# putting in its own dataframe
share = pd.DataFrame({'share_f_care' : share_f_care,
                      'share_m_care' : share_m_care,
                      'share_f_bonding' : share_f_bonding,
                      'share_m_bonding' : share_m_bonding,
                      'share_f_total' : share_f_total,
                      'share_m_total' : share_m_total})

share_pct = ["0%", "20%", "40%", "60%", "80%", "100%"]

#%% 2 panel plot: share of care claims filed vs. share of bonding claims filed

fig, (ax1, ax2) = plt.subplots(1,2)
    # 1 and 2 indicate # of rows and columns of panels in the plot
    
# plot left panel
share[["share_f_care", "share_m_care"]].plot.bar(stacked = True, ax = ax1)
    # index is x axis
ax1.set_title("Share of 1st PFL Care Claims Filed", fontsize = 10)
ax1.set_xlabel(None)
ax1.legend(["Female", "Male"], 
           bbox_to_anchor = (1, -0.2), prop = {'size' : 10}, frameon = False, ncol = 2)
ax1.set_yticklabels(share_pct, rotation=0)
fig.tight_layout()

# The f/m ratio of first PFL care claims has stayed relatively constant since 2004.

#plot right panel
share[["share_f_bonding", "share_m_bonding"]].plot.bar(stacked = True, ax = ax2)
ax2.set_title("Share of 1st PFL Bonding Claims Filed", fontsize = 10)
ax2.legend(["Female", "Male"], 
           bbox_to_anchor = (1, -0.2), prop = {'size' : 10}, frameon = False, ncol = 2)
ax2.set_yticklabels(share_pct, rotation=0)
#ax2.set_xticklabels(year_increments, rotation = 0)
ax2.set_xlabel(None)
fig.tight_layout()
fig.savefig('share-claims-bysex.png')

# The share of males filing first PFL bonding claims has increased by ~ 20 pct points.

#%% Next step: looking at raw numbers of claimants of each type, by sex

# create dataframe
raw_claims = pd.DataFrame({'f_care' : care["Female"],
                      'm_care' : care["Male"],
                      'total_care' : care["Total"],
                      'f_bonding' : bonding["Female"],
                      'm_bonding' : bonding["Male"],
                      "total_bonding" : bonding["Total"]})

# single panel plot
fig, ax1 = plt.subplots()
raw_claims[["f_care", "m_care", "f_bonding", "m_bonding"]].plot.line(stacked = True, ax = ax1)
    # index is x axis
ax1.set_title("Number of First PFL Claims Filed", fontsize = 10)
ax1.set_xlabel(None)
ax1.legend(["Female - Care", "Male - Care", "Female - Bonding", "Male - Bonding"], 
            frameon = False)
fig.tight_layout()
fig.savefig('first-claims-bytype-bysex.png')

#%% Bar plot: total first care and bonding claims by year

# set up dpi and theme
plt.rcParams['figure.dpi'] = 300 
    # how to improve resolution of graphics. Figure is the key. Set to 300 dpi.

ylab_total = ["0", "50,000", "100,000", "150,000", "200,000", "250,000", "300,000"]

# bar plot - would like to add tick marks if possible
fig, ax1 = plt.subplots()
total.plot.bar(y='Total', ax=ax1)
    # it will assume you want x as index
ax1.set_title("Total First PFL Care and Bonding Claims Filed, by Year")
ax1.set_ylabel(None)
ax1.set_yticklabels(ylab_total, rotation=0)
ax1.set_xlabel(None) 
ax1.legend().set_visible(False)
plt.xticks(rotation = 45)
fig.tight_layout()
fig.savefig('total-claims.png')

#%% Stacked bar plot: looking at bonding claims

ylab_bonding = ["0", "50,000", "100,000", "150,000", "200,000", "250,000"]

fig, ax1 = plt.subplots()
bonding[["Female", "Male", "Unknown"]].plot.bar(stacked = True, ax=ax1)
    # it will assume you want x as index
    # list of columns inside [] makes a temporary dataframe
ax1.set_title("PFL First Bonding Claims Filed, by Sex")
ax1.set_ylabel(None)
ax1.set_yticklabels(ylab_bonding, rotation=0)
ax1.set_xlabel(None)
plt.xticks(rotation = 45)
ax1.legend(#loc = "lower center", bbox_to_anchor = (0.5, -0.3), 
           prop = {'size' : 12}, frameon = False)
fig.tight_layout()
fig.savefig('bonding-claims.png')

#%% Stacked bar plot: looking at care claims

ylab_care = ["0", "5,000", "10,000", "15,000", "20,000", "25,000", "30,000", "35,000", "40,000"]

fig, ax1 = plt.subplots()
care[["Female", "Male", "Unknown"]].plot.bar(stacked = True, ax=ax1)
    # it will assume you want x as index
    # list of columns inside [] makes a temporary dataframe
ax1.set_title("PFL First Care Claims Filed, by Sex")
ax1.set_ylabel(None)
ax1.set_yticklabels(ylab_care, rotation=0)
ax1.set_xlabel(None)
plt.xticks(rotation = 45)
ax1.legend(#loc = "lower center", bbox_to_anchor = (0.5, -0.3), 
           prop = {'size' : 12}, frameon = False)
fig.tight_layout()
fig.savefig('care-claims.png')