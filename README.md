# portfolio

Example data science and machine learning projects

## Overview of Projects

See the `/projects` folder in this repository for Jupyter notebooks walking through each step of the project. These will include 

* Data Cleaning
* Exploratory Data Analysis (EDA)
* Data Transforms
* Feature Selection
* Model Development
* Hyperparameter Tuning
* Ensemble Modeling  

The primary notebook for each project is named `projectName-main.ipynb`. Other extensions such as `projectName-download.ipynb` are for supplementary steps. Often these are for cases where the files created exceed Github's 100 MB limit. Unless you need access to the original data files, I recommend just sticking with the main notebook for each project.


### kickstarter

Can we predict whether or not a project will succeed on Kickstarter given information such as the project name, category, launch and deadline dates, and target funding goal? Raw data obtained from Mickaël Mouillé on Kaggle (https://www.kaggle.com/kemical/kickstarter-projects). I use the 'ks-projects-201801.csv' version of the data.

### snowpack

Collecting, cleaning, and merging daily snowfall time series data from various mountainous weather stations in the western US. Raw data reports were obtained from the Deparment of Agriculture's Natural Resources Conservation Service API (https://wcc.sc.egov.usda.gov/reportGenerator/). The goal of this project is to predict the spring snow melt date using only information from the onset of the previous winter up to the peak snow accumulation. Personally, I am interested in these predictions to more reliably plan snow-free backpacking trips. However, in industry the same information could be used by ski resorts to predict the optimal time to change their lift chairs to catch the beginning of the summer mountain biking season.

## Authors

Addison G. Klinke  
Email: agk38@case.edu  
LinkedIn: https://www.linkedin.com/in/addison-klinke-28768b97/  
Resume: see 'Resume-AddisonKlinke.pdf' in this repository's root folder  

## Installation

Code in this repository was written in Python >= 3.6.5 (https://www.python.org/getit/). Package dependencies will depend on the specific project of interest, but I recommend installing with pip3 (https://pip.pypa.io/en/stable/installing/) or conda (https://conda.io/docs/user-guide/install/index.html).

## Conventions

Python objects are documented with numpy style docstrings (https://numpydoc.readthedocs.io/en/latest/format.html).

## Contributing

As this repository is a personal portfolio, pull requests and contributions will likely be minimal. However, I am always trying to improve and will gladly welcome polite feedback or constructive criticisms about the approaches used. 

## License

This project is licensed under the MIT License - see the LICENSE.md file for details
