import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from os import path
from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from sklearn.feature_extraction.text import TfidfVectorizer

# ----------------------------------------------Load Data
# Data aquired from here "https://www.kaggle.com/andrewmvd/data-scientist-jobs"
df = pd.read_csv("DataScientist.csv")

# ----------------------------------------------Preprocessing

# Get rid of first  two columns as they are unnecessary
df = df.iloc[:, 2:]

# Unpack the two values of min and max salary into seperate columns using the split function
df[['Minimum Salary (k)', 'Maximum Salary (k)']] = df['Salary Estimate'].str.split('-', expand=True)

# Replace various unnecessay items in the minimum and maximum salary columns so that we can eventually turn them into
# integers I have used Regex=False as Regex=True will become default in the future, and I wanted to future proof the
# code
df['Minimum Salary (k)'] = df['Minimum Salary (k)'].str.replace('$', '', regex=False)
df['Minimum Salary (k)'] = df['Minimum Salary (k)'].str.replace('K', '', regex=False)
df['Maximum Salary (k)'] = df['Maximum Salary (k)'].str.replace('$', '', regex=False)
df['Maximum Salary (k)'] = df['Maximum Salary (k)'].str.replace('K', '', regex=False)
df['Maximum Salary (k)'] = df['Maximum Salary (k)'].str.replace('Glassdoor est.', '', regex=False)
df['Maximum Salary (k)'] = df['Maximum Salary (k)'].str.replace(' ()', '', regex=False)
df['Maximum Salary (k)'] = df['Maximum Salary (k)'].str.replace('(Employer est.)', '', regex=False)

# Exclude jobs with hourly rates
df = df[(df['Salary Estimate'].str.contains(' Per Hour')) == False].reset_index(drop=True)

# All of the null figures in the dataset are represented by -1 - sometimes as a string and sometimes as a number -
# this converts them all to NaN
df = df.replace('-1', np.nan)
df = df.replace(-1, np.nan)

# The Company name is merged with the company rating - this splits and slices the first part that is just the company
# name
df['Company Name'] = [x.split('\n')[0] for x in df['Company Name']]

# Company Size is a string that is better served as two columns - min size and max size
# This code gets rid of the text and replaces the word to with a dash that we can split on
df['Size'] = df['Size'].str.replace(' employees', '')
df['Size'] = df['Size'].str.replace(' to ', '-')

# The only ones that are different are the 10000+ lables and the unknown labels - 10000+ has been replaced with
# 10000-100000 and unknow has been replaced with NaN
df['Size'] = df['Size'].str.replace('10000+', '10001-100000', regex=False)
df['Size'] = df['Size'].replace('Unknown', np.nan, regex=False)

# City and State are unpacked from Location
df[['City', 'State']] = df['Location'].str.split(', ', expand=True)

# Now the Size column has been transformed it is unpacked into Minimum and Maximum size
df[['Minimum Size', 'Maximum Size']] = df['Size'].str.split('-', expand=True)

# Reorder the columns
df = df.filter(
    ['Job Title', 'Job Description', 'Rating', 'Company Name', 'City', 'State', 'Minimum Size', 'Maximum Size',
     'Founded', 'Type of ownership', 'Industry', 'Sector', 'Minimum Salary (k)', 'Maximum Salary (k)'])

# The newly create Salary and Size colums are turned into numeric columns
df[['Minimum Size', 'Maximum Size', 'Minimum Salary (k)', 'Maximum Salary (k)']] = df[
    ['Minimum Size', 'Maximum Size', 'Minimum Salary (k)', 'Maximum Salary (k)']].apply(pd.to_numeric)

# Founded is turned into an integer so that we can create a Years in Business Column
df["Founded"] = df["Founded"].astype(int, errors='ignore')
df['Years in Business'] = 2021 - df['Founded']

# New Line characters are stripped out of the Job Description field
df['Job Description'] = df['Job Description'].str.replace('\n', ' ', regex=False)

# Reset the index to take into account the dropped rows
df.reset_index(drop=True)
