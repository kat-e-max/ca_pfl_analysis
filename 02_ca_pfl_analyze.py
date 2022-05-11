# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 12:36:30 2022

@author: katmax

Script 2 of 8
Purpose: understand and visualize aspects of the CA PFL monthly data

"""

#%% Setup 

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# set nicer figure
plt.rcParams['figure.dpi'] = 300 
sns.set_theme(style="white")
#%% Import CA PFL monthly data

# Read in CSV
ca_pfl_data = pd.read_csv("ca_pfl_data.csv")

# set index to date
ca_pfl_data = ca_pfl_data.set_index("Date")

# check what data types are in the dataframe
ca_pfl_data.dtypes
    # we see that Pandas correctly classified the variables 

# get info on dataframe
ca_pfl_data.info()

#%% Getting a handle around the data - check that everything imported correctly

# How many records are there?
print("There are", len(ca_pfl_data), "records in the dataframe")

# group by month
by_month = ca_pfl_data.groupby("Month")
print("There are", len(by_month), "months in the dataframe")

# group by year
by_year = ca_pfl_data.groupby("Year")
print("There are", len(by_year), "years in the dataframe")

# convert months into month numbers to use for future dataframes
month_numbers = {
    'January': 1,
    'February': 2,
    'March': 3,
    'April': 4,
    'May': 5,
    'June': 6,
    'July': 7,
    'August': 8,
    'September': 9,
    'October' : 10,
    'November' : 11,
    'December' : 12
    }

# convert months to numbers for main dataframe
# get rid of index first
ca_pfl_data = ca_pfl_data.reset_index()
ca_pfl_data['month #'] = ca_pfl_data['Month'].replace(month_numbers)

# create list of month names, long and short form - to help with labeling axes
month_list = ["January", "February", "March", "April", "May", "June", "July",
              "August", "September", "October", "November", "December"]

s_month_list = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul",
              "Aug", "Sep", "Oct", "Nov", "Dec"]

#%% Analysis: look at data on mean # of first filed claims by month 

# describe data, sort by mean
# note: some months will have 17 years of data, others 18
first_filed = by_month["Total PFL First Claims Filed"].describe()
print(first_filed.sort_values("mean"))

# adding month numbers to dataframe to help with sorting in proper month order
first_filed = first_filed.reset_index()
first_filed['month #'] = first_filed['Month'].replace(month_numbers)

# plot: barplot
fig, ax1 = plt.subplots()
sns.barplot(data=first_filed,
            x='Month',
            y='mean',
            order = month_list,
            ax=ax1)
ax1.set_title("Mean PFL First Claims Filed, by Month (2004 - 2021)")
ax1.set_xticklabels(s_month_list, minor=False)
ax1.set_xlabel(None)
ax1.set_ylabel("# Claims")
fig.tight_layout()
fig.savefig('mean_month.png')

#%% Analysis: comparing claims paid vs. claims filed, as %

# create a new dataframe for this purpose
pvf = pd.DataFrame(index=ca_pfl_data.index)

# load in data: calculate percentages of PFL claims filed that were paid (high is good)
pvf = pd.DataFrame({'pvf_care' : ca_pfl_data["Care Claims Paid"] / ca_pfl_data["Care Claims Filed"]*100,
                      'pvf_bonding' : ca_pfl_data["Bonding Claims Paid"] / ca_pfl_data["Bonding Claims Filed"]*100,
                      'pvf_first' : ca_pfl_data["Total PFL First Claims Paid"] / ca_pfl_data["Total PFL First Claims Filed"]*100})

# round all data to 2 decimal places
pvf = pvf.round(2)

# add Date and Year columns from initial dataset
pvf["Date"] = ca_pfl_data["Date"]
pvf["Year"] = ca_pfl_data["Year"]

print(len(pvf))
# should be 210

# check if there are any records over 100% 
high = pvf.query("pvf_care >= 100 or pvf_bonding >= 100 or pvf_first >= 100")        
print("There are", len(high), "rows in which at least 1 value exceeds 100%.")

# decided not to convert those records over 100% to NA
# this could be because of an administrative backlog

#%% Plotting claims paid vs. claims filed

# triple panel plot
fig, (ax1, ax2, ax3) = plt.subplots(3,1)
    # 1st and 2nd argument indicate # of rows and columns of panels in the plot

# first plot    
pvf["pvf_care"].plot.line(ax = ax1)
    # index is x axis - here, date
ax1.set_title("% Care Claims Filed that Were Paid", fontsize = 10)
ax1.set_xlabel(None)
fig.tight_layout()

# second plot
pvf["pvf_bonding"].plot.line(ax = ax2)
    # index is x axis - here, date
ax2.set_title("% Bonding Claims Filed that Were Paid", fontsize = 10)
ax2.set_xlabel(None)
fig.tight_layout()

# third plot
pvf["pvf_first"].plot.line(ax = ax3)
    # index is x axis - here, date
ax3.set_title("% First Claims Filed that Were Paid", fontsize = 10)
ax3.set_xlabel(None)
fig.tight_layout()
fig.savefig('paidvfiled.png')