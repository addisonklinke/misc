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

os.chdir('/home/addison/Documents/git/portfolio/kickstarter')
df = pd.read_csv('kickstarter-projects.csv')

# EDA and cleaning ------------------------------------------------------------
print(df.shape)
summary = df.describe()
# First, we notice that there are two columns for the amount of money pledged:
# 'usd pledged' and 'usd_pledged_real'. According to documentation for the 
# dataset, the former was converted by Kickstarter and the later by the 
# fixer.io API. Looking at rows 1, 41, 43, and others we can see that the 
# amount in 'pledged' does not match 'usd pledged' even though the currency
# for the project is USD. Therefore, 'usd_pledged_real' is the more reliable
# column to use.


print(df.groupby('state').size())
# The majority of projects are either failed of successful. Canceled is the 
# next biggest category. We can simplify this to a binary classification
# problem with failed or canceled as 0 and successful as 1.

# Remove the unneeded rows and enocde classes
df = df[df.state.isin(['successful', 'failed', 'canceled'])]
df.state = df.state.replace({'successful':1, 'failed':0, 'canceled':0})
