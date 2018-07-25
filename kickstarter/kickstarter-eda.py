#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 24 04:55:04 2018

@author: Addison Klinke

EDA and visualization for the Kickstarter projects dataset from Kaggle 
(https://www.kaggle.com/kemical/kickstarter-projects)
"""

# Load required modules and data ----------------------------------------------
import pandas as pd
import os

os.chdir('/home/addisonklinke/Documents/git/portfolio/kickstarter') 
df = pd.read_csv('ks-projects.csv', parse_dates=[5, 7])

# Data cleaning ---------------------------------------------------------------
df.shape
df.describe()
df.dtypes
# First, we notice that there are two columns for the amount of money pledged:
# 'usd pledged' and 'usd_pledged_real'. According to documentation for the 
# dataset, the former was converted by Kickstarter and the later by the 
# fixer.io API. Looking at rows 1, 41, 43, and others we can see that the 
# amount in 'pledged' does not match 'usd pledged' even though the currency
# for the project is USD. Therefore, 'usd_pledged_real' is the more reliable
# column to use.

# We will also drop the project ID since that is a random number which should
# have no correlation to the project's success.
df.drop(columns=['usd pledged', 'ID'], inplace=True)
df.rename(columns={'usd_pledged_real':'pledged_usd', 
                   'usd_goal_real':'goal_usd'}, inplace=True)

df.groupby('state').size()
# The majority of projects are either failed of successful. Canceled is the 
# next biggest category. We can simplify this to a binary classification
# problem with failed or canceled as 0 and successful as 1.

# Remove the unneeded rows and enocde classes
df = df[df.state.isin(['successful', 'failed', 'canceled'])]
df.state = df.state.replace({'successful':1, 'failed':0, 'canceled':0})

# Add a 'duration' variable which measures the length of the project. We will
# also split 'launched' into the day and time
df['launch_day'] = [d.date() for d in df.launched]
df['launch_time'] = [d.time() for d in df.launched]
df['duration'] = [(d - l).days for d, l in zip(df.deadline.dt.date, df.launch_day)]
df.drop(columns='launched', inplace=True)

# We will also move the 'state' column last so that splitting features and 
# target will be easy in sklearn
cols = list(df.columns)
cols.append(cols.pop(cols.index('state')))
df = df.reindex(columns=cols)

# Finally, write the modified dataframe to CSV so we don't have to repeat these
# steps in the future
df.to_csv('ks-projects-clean.csv', index=False)

# Exploratory Analysis --------------------------------------------------------
df = pd.read_csv('ks-projects-clean.csv', parse_dates=[4, 11, 12])

# How are projects distributed by category and sub-category?

# Variable correlations

# How does sucess vary with factors like category, goal, country, duration,
# and time of day the project was launched?

# Insights on project name choices?