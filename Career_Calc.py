# -*- coding: utf-8 -*-
"""
Created on Tue Dec 26 10:55:01 2023

@author: bcsal

Finds the average for all players for each numerical catergory 
over the past 20 years
"""

import pandas as pd 

stats = ['G', 'MP', '%FG_t', 'Av_Dist(Ft)',
       '%FGA_2P', '%FGA_0-3', '%FGA_3-10', '%FGA_10-16', '%FGA_16-3P',
       '%FGA_3P', '%FG_2P', '%FG_0-3', '%FG_3-10', '%FG_10-16', '%FG_16-3P',
       '%FG_3P', '%FG_assisted_2P', '%FG_assisted_3P', '%DunkAttempts',
       '#_Dunks', '%FGA_Corner3', '%FG_Corner3', 'Heave_attempts', 'Heave_#',
       'PER', 'TS%', '3PAr', 'FTr', 'ORB%', 'DRB%', 'TRB%', 'AST%', 'STL%',
       'BLK%', 'TOV%', 'USG%', 'OWS', 'DWS', 'WS', 'WS/48', 'OBPM', 'DBPM',
       'BPM', 'VORP', 'GS', 'FG', 'FGA', 'FG%', '3P', '3PA', '3P%', '2P',
       '2PA', '2P%', 'FT', 'FTA', 'FT%', 'ORB', 'DRB', 'TRB', 'AST', 'STL',
       'BLK', 'TOV', 'PF', 'PTS', 'ORtg', 'DRtg'] 

#season 2020-2021 as test 
seasons = list(range(2003,2022))
df_list = []
for season in seasons: 
    contents = pd.read_excel('PlayerProfiles/all_info_{}.xlsx'.format(season))
    df_list.append(contents)

all_data = pd.concat(df_list)
# Calculate the mean for each DataFrame separately
average_stats = all_data.groupby("Player")[stats].mean()


average_stats.to_csv("average_stats.csv")
