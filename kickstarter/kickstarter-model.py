"""Machine learning models in scikit-learn to predict project success.

@author: Addison Klinke
"""
# Load required modules and data ----------------------------------------------
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.pipeline import Pipeline

os.chdir('/home/addisonklinke/Documents/git/portfolio/kickstarter') 
df = pd.read_csv('ks-projects-clean.csv', parse_dates=[4, 11, 12])

# Encode non-numeric data for modeling ----------------------------------------
df.drop(columns=['pledged', 'backers', 'pledged_usd', 'goal'], inplace=True)
df.dtypes
df.launch_time = np.cos(df.launch_time.astype('float') / 24 * 2 * np.pi)
df['launch_year'] = [d.year for d in df.launch_day]
df.launch_day = [np.cos(d.dayofyear / 365 * 2 * np.pi) for d in df.launch_day] 
df.deadline = [np.cos(d.dayofyear / 365 * 2 * np.pi) for d in df.deadline]
df.name = df.name.str.len()
df.dropna(inplace=True) # Some strings returned NA
categorical = df.select_dtypes(include=['object']).columns
df[categorical] = df[categorical].apply(LabelEncoder().fit_transform)
df.query("launch_year != 1970", inplace=True)
df.corr().unstack().sort_values().drop_duplicates()
# Currency and country are (unsurprisingly) highly correlated, so we will remove currency
df.drop(columns='currency', inplace=True)

# Initial Modeling ------------------------------------------------------------
seed = 1234
y = df.state.values
x = df.values[:, :-1]
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=seed)
models = [('LR', LogisticRegression()), ('LDA', LinearDiscriminantAnalysis()),
          ('KNN', KNeighborsClassifier()), ('CART', DecisionTreeClassifier()),
          ('SVC', SVC()), ('NB', GaussianNB())]
names = [n for n, m in models]
ctrl = KFold(n_splits=5, random_state=seed)
results = [cross_val_score(m, x_train, y_train, cv=ctrl, scoring='accuracy') for n, m in models]

fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results)
ax.set_xticklabels(names)
plt.show()

# Hyperparameter tuning -------------------------------------------------------

# Ensemble Modeling -----------------------------------------------------------

# Export Final Model ----------------------------------------------------------