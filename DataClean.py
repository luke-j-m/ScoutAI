# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 15:51:07 2023

@author: bcsal

Data Cleaning from Full contents 
Data sources: NBA.com, Basketball Refereance, National Statistic 
"""

import pandas as pd 

contents = pd.read_excel('PlayerProfiles/all_info_2006.xlsx')

#Delete the Junk Columns 
delete_col = ['Unnamed: 0', 'RK','Unnamed: 19',
                  'playerID', 'Year_x','Rk_x',
                  'Player-additional_x', 'Year_y', 'Unnamed: 24',
                  'Rk_y','Unnamed: 29','Player-additional_y', 'Year',]
contents.drop(delete_col, inplace=True, axis=1)

#Remove the * from the player names and add if they have been in the HOF
# Add a new column 'HOF' based on the condition that the player name contains '*'
contents['HOF'] = contents['Player'].apply(lambda x: 1 if '*' in str(x) else '')

# Remove '*' from the 'Player Name' column !Might Need to do this earlier!
contents['Player'] = contents['Player'].str.replace('*', '')
print(contents[contents["Player"].str.contains("Ray")])




