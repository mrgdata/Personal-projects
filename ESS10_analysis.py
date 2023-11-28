# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 17:49:46 2023

@author: ROMEROM
"""

import zipfile
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import statsmodels.api as sm
from scipy import stats

user = os.getenv("username")

# Path to your zip file
zip_path =f'C:/Users/{user}/Downloads/ESS10SC.zip'

# Directory where you want to extract the contents
extract_to_path = f'C:/Users/{user}/Downloads/ESS10SC'

# Ensure the extract path exists
os.makedirs(extract_to_path, exist_ok=True)

# Open the zip file in read mode
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    # Extract all the contents into the directory
    zip_ref.extractall(extract_to_path)

# Find the CSV file in the extracted contents
csv_file = None
for file in os.listdir(extract_to_path):
    if file.endswith('.csv'):
        csv_file = file
        break

if csv_file:
    # Read the CSV file into a DataFrame
    df = pd.read_csv(os.path.join(extract_to_path, csv_file))
    print("CSV file loaded into DataFrame.")
else:
    print("No CSV file found in the extracted contents.")
   
lista_columnas = df.columns

df['cntry'].value_counts()

df = df[df['cntry'] == 'ES']

############ vamos a ver cómo se relaciona esto ##################

df['agea'] = df['agea'].apply(lambda x: np.median(df['agea']) if x > 99 else x)

df['lrscale'] = df['lrscale'].apply(lambda x: np.median(df['lrscale']) if x > 10 else x)

# Create a line plot
sns.lineplot(data=df, x='agea', y='lrscale', ci='sd')  # ci='sd' uses standard deviation for the confidence interval

plt.title('¿La edad se relaciona con la ideología?')
plt.ylabel('Posición ideológica (0, izda-10, dcha)')
plt.xlabel('Edad media')

plt.show()


df['Interval'] = pd.cut(df['agea'], bins=[0, 25, 50, 75, 100], labels=['0-25', '25-50', '50-75', '75-100'], include_lowest=True)

# Create a line plot
sns.lineplot(data=df, x='Interval', y='lrscale', ci="sd")  # ci='sd' uses standard deviation for the confidence interval

plt.title('Posición ideológica por edad')
plt.ylabel('Posición ideológica (0, izda-10, dcha)')
plt.xlabel('Edad media')

plt.show()

# regresión

X = sm.add_constant(df['agea']) 

# Fit the regression model
model = sm.OLS(df['lrscale'], X).fit()

# Print out the statistics
print(model.summary())

# Predict values
df['y_pred'] = model.predict(X)

# Plotting the regression line
plt.scatter(df['agea'], df['lrscale'], label='¿La edad se relaciona con la ideología?')
plt.plot(df['agea'], df['y_pred'], color='red', label='Línea de regresión')

plt.xlabel('Edad')
plt.ylabel('Posición ideológica (0, izda-10, dcha)')
plt.legend()
plt.show()
################## restricción por edad ######################
df_juv = df[df['agea'] < 25]

print(len(df_juv))


lista_conceptos = {'Conciencia Política': ['polintr', 'actrolga', 'cptppola', 'prtclges', 'lrscale', 'gincdif'],
                    'Opinión del gobierno': ['trstprl', 'trstlgl', 'trstplc', 'trstplt', 'trstprt', 'stfdem', 'stfgov', 'stfeco'],
                    'Participación política': ['vote', 'contplt', 'donprty', 'badge', 'sgnptit', 'pbldmna', 'bctprd'],
                    'Uso online': ['pstplonl', 'como12', 'mccoord', 'mcclose'],
                    'Participación cívica': ['volunfp', 'sclact'],
                    'Pro-LGTB': ['freehms', 'hmsfmlsh', 'hmsacld'],
                    'Pro-inm': ['imbgeco', 'imueclt', 'imwbcnt'],
                    'Work': ['pdwork', 'uempla', 'pdjobev']
                    }

# distribuir sies y noes por edad, imputar ns/nc a moda

sns.set_style('whitegrid')

for col in ['vote', 'contplt', 'donprty', 'badge', 'sgnptit', 'pbldmna', 'bctprd', 'pstplonl']:
    df[col] = df[col].apply(lambda x: np.median(df[col]) if x > 2 else x)
    df[col] = df[col].replace(2, 'No').replace(1, 'Yes')
    df.sort_values(by=col, inplace=True)
    
    g = sns.FacetGrid(df, hue=col, aspect=3, height=5, palette='viridis')
            
    g.map(sns.kdeplot, 'agea', fill=True)
            
    g.add_legend(title='')
            
    # Enhance the plot with titles and labels
    plt.title(f'Densidad de las respuestas a la variable "{col}" de la ESS por Edad')
    plt.xlabel('Edad')
    plt.ylabel('Densidad')
                
    plt.show()
    
    print(stats.ttest_ind(df.loc[df[col] == "Yes"]["agea"], df.loc[df[col] == "No"]["agea"], equal_var=True))
    
for col in ['polintr', 'actrolga', 'cptppola', 'gincdif']:
    df[col] = df[col].apply(lambda x: np.median(df[col]) if x > 5 else x)
    grouped_data = df.groupby('Interval')[col].mean().reset_index()
    
    grouped_data.sort_values(by=col, inplace=True)
    
    df.sort_values(by=col, inplace=True)
    
    sns.barplot(x='Interval', y=col, data=df, palette='viridis')
    
    #sns.barplot(x='Interval', y=col, data=grouped_data, palette='viridis')
            
    # Enhance the plot with titles and labels
    plt.title(f'Densidad de las respuestas a la variable "{col}" de la ESS por Edad')
    plt.xlabel('Tramo de edad')
    plt.ylabel('Índice de Respuesta (1-Para nada, 5-Completamente)')
               
    plt.ylim(1, 3)
    plt.show()
    
for col in ['trstprl', 'trstlgl', 'trstplc', 'trstplt', 'trstprt', 'stfdem', 'stfgov', 'stfeco', 'lrscale']:
    df[col] = df[col].apply(lambda x: np.median(df[col]) if x > 10 else x)
    grouped_data = df.groupby('Interval')[col].mean().reset_index()
    
    grouped_data.sort_values(by=col, inplace=True)
    
    df.sort_values(by=col, inplace=True)
    
    sns.barplot(x='Interval', y=col, data=df, palette='viridis')
    
    #sns.barplot(x='Interval', y=col, data=grouped_data, palette='viridis')
            
    # Enhance the plot with titles and labels
    plt.title(f'Densidad de las respuestas a la variable "{col}" de la ESS por Edad')
    plt.xlabel('Tramo de edad')
    plt.ylabel('Índice de Respuesta (1-Para nada, 5-Completamente)')
               
    plt.ylim(1, 6)
    plt.show()
        