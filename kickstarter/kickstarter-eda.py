"""
EDA and visualization for the Kickstarter projects dataset. 

@author: Addison Klinke
Data from Kaggle (https://www.kaggle.com/kemical/kickstarter-projects)
"""

# Load required modules and data ----------------------------------------------
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

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
np.unique(df.launch_day.dt.year)

# TODO: drop the 1970's rows

# Split launch_time into hours, minutes, and seconds and convert to a single
# decimal respresentation. 
df[['h', 'm', 's']] = df.launch_time.astype(str).str.split(':', expand=True).astype(float)
df['launch_time'] = df.h.values + df.m.values / 60 + df.s.values / 3600
df.drop(columns=['h', 'm', 's'], inplace=True)

# We can also encode launch_day and deadline as integers representing day of 
# the year. Both of these transformations will make the data more suitable for 
# plotting and modeling. We can keep the year information from launch and 
# deadline dates in a single column since 


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

# How are projects distributed by category? 
main_categories = df.groupby('main_category').size().sort_values(ascending=False)
n_main = [i / 1000 for i in list(main_categories)]
labels_main = list(main_categories.index)

ind = np.arange(len(main_categories))
plt.bar(ind, n_main)
plt.ylabel('Count (Thousands)')
plt.xlabel('Main Category')
plt.title('Kickstarter Project Categories')
plt.xticks(ind, labels_main, rotation=90)
plt.show()

# Correlations for numeric variables
smaller = df[['goal_usd', 'pledged_usd', 'backers', 'duration', 'state']]
smaller.corr().unstack().sort_values().drop_duplicates()
# Strong correlation between pledged_usd and backers, which is to be expected
# since the more people backing the project, the more money it is likely to have
# raised. Other than this, correlations are fairly small

# How does sucess vary with factors like category, goal, country, duration,
# and time of day the project was launched? For duration, there are a few 
# outliers with over 14,000 days resulting from incorrect parsing of the launch
# date, so we will remove those first.
df.query('duration < 1000', inplace=True)
sns.distplot(df.query('state == 1').duration, hist=False, kde=True,
             kde_kws={'shade': True, 'linewidth': 3}, 
             label='Success', color='green')
sns.distplot(df.query('state == 0').duration, hist=False, kde=True,
             kde_kws={'shade': True, 'linewidth': 3}, 
             label='Failure', color='red') 
plt.legend(title='Project Status')
plt.xlabel('Project Duration (Days)')
plt.ylabel('Density')
plt.show()
# The vast majority of projects are 30 days long regardless of their status.
# The next largest peaks are at 60 and 45 days, indicating that projects tend 
# to be scheduled in terms of months (1, 1.5, 2, etc). There is a slight trend
# towards shorter durations leading to an increased chance of success - more 60
# day projects failed and more 15-25 day project succeeded.

# Now we can look at time of day the project funding goal (converted to USD for
# a fair comparison across all the currencies). Plotting on a log10 scale helps 
# compress the data into a viewable range since goals range from $0.01 up to 
# over $166,000,000
sns.distplot(np.log10(df.query('state == 1').goal_usd.values), hist=False, 
             kde=True, kde_kws={'shade': True, 'linewidth': 3}, 
             label='Success', color='green')
sns.distplot(np.log10(df.query('state == 0').goal_usd.values), hist=False, 
             kde=True, kde_kws={'shade': True, 'linewidth': 3}, 
             label='Failure', color='red') 
plt.legend(title='Project Status')
plt.xlabel('Project Funding Goal (log10 USD)')
plt.ylabel('Density')
plt.show()

# The distinction between failure and sucess is a more pronounced here than for
# duration - project with a larger funding goal failed more often. The most 
# common goals were around $10k USD

# What about time of day the project was launched? If people are most likely
# to hear about a project at its inception, it would be critical to launch at
# a time when people are available (for instance, weekday evenings).
smaller = df[['launch_time', 'state']]
smaller['h']
sns.tsplot()

# Insights on project name choices from an NLP perspective?