# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 17:35:35 2023

@author: mromg
"""

import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns

url = "https://en.wikipedia.org/wiki/List_of_German_states_by_GRP_per_capita"

# Make a GET request to fetch the raw HTML content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the first table on the Wikipedia page
table = soup.find_all('table')[0]

# Convert the table to a pandas DataFrame
df_germany = pd.read_html(str(table))[0]

#df_germany.to_excel('wikipedia_table1.xlsx', index=False)

df_germany.columns = [' '.join(col).strip() for col in df_germany.columns.values]

df_germany.rename(columns={'State State': 'State', 'GRP per capita (EUR€)[2]': 'GDP per capita'}, inplace=True)

df_germany.drop(columns=['GRP per capita (US$)', 'Rank Rank'], inplace=True)

df_germany.State = df_germany.State.apply(lambda x: x.title())

df_germany['Country'] = ''

for index, row in df_germany.iterrows():
    if row['State'] == 'Germany':
        df_germany.at[index, 'Country'] = "darkblue"
    else:
        df_germany.at[index, 'Country'] = "lightblue"

url = "https://econet.carm.es/inicio/-/crem/sicrem/PU39/sec25.html"

# Make a GET request to fetch the raw HTML content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the first table on the Wikipedia page
table = soup.find_all('table')[3]

# Convert the table to a pandas DataFrame
df_spain = pd.read_html(str(table), skiprows=[0, 1, 2, 3, 4])[0]

#df_spain.to_excel('wikipedia_table1.xlsx', index=False)

df_spain.rename(columns={'Unnamed: 0': 'State', 'PIB per cápita': 'GDP per capita'}, inplace=True)

df_spain.drop(columns=['PIB a p.m. (precios corrientes)', 'Población'], inplace=True)

df_spain['GDP per capita'] = df_spain['GDP per capita'].apply(lambda x: x*1000)

df_spain = df_spain[df_spain.State != 'EXTRARREGIO']

df_spain.State = df_spain.State.apply(lambda x: x.title())

df_spain['Country'] = ''

for index, row in df_spain.iterrows():
    if row['State'] == 'España':
        df_spain.at[index, 'Country'] = "darkred"
    else:
        df_spain.at[index, 'Country'] = "lightcoral"
        
df = pd.concat([df_spain, df_germany])



# Get a list of unique colors based on the string values from column C
unique_colors = df['Country'].unique()

color_mapping = {value: color for value, color in zip(unique_colors, unique_colors)}



# Map the colors from column C based on the color_mapping dictionary
df['color_mapped'] = df['Country'].map(color_mapping)

df = df.sort_values('GDP per capita', ascending=False)

# Plot
plt.figure(figsize=(16,10))
plt.barh(df['State'], df['GDP per capita'], color=df['color_mapped'])
plt.xlabel('GDP per capita (nominal prices, 2022)')
plt.ylabel('Lander & Communities')
plt.title('Where do I move to Germany?')
plt.gca().invert_yaxis() # Highest rank at the top
plt.show()





