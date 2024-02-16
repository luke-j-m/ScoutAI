"""
Created on Mon Dec 25 14:09:35 2023
DataFrame generator for statistics 

Per 100, Shooting, and Advanced statistics from:
    BasketballRefereance (https://www.basketball-reference.com/)
Player Combine data from:
    NBA.com 
    
For Educational purposes only, not for professional use 

@author: brandon Saltzman
"""

import pandas as pd 

#function to read in the stats per year 

def shootingStats (season):
    shootingHeadings = ["RK", "Player", "Pos","Age", "Tm", "G", "MP", "%FG_t", "Av_Dist(Ft)","null1",
                        '%FGA_2P','%FGA_0-3', '%FGA_3-10', '%FGA_10-16', 
                        '%FGA_16-3P', "%FGA_3P", "null2",
                        '%FG_2P','%FG_0-3', '%FG_3-10', '%FG_10-16', 
                        '%FG_16-3P', "%FG_3P","null3",
                        "%FG_assisted_2P","%FG_assisted_3P", 'null4',
                        '%DunkAttempts', '#_Dunks', 'null5',
                        '%FGA_Corner3', "%FG_Corner3", 'null6', "Heave_attempts", "Heave_#", 'playerID']
    
    delete_col = ["null1", 'null2', 'null3', 'null4','null5','null6']
    shooting = pd.read_excel("BasketballRefereance/Shooting/bball_ref_shooting_{}.xlsx".format(season), sheet_name='Sheet1', header=[0,1], index_col=None)
    shooting.columns = shootingHeadings
    
    shooting['Year'] = season
    shooting.drop(delete_col, inplace=True, axis=1)
    
    return shooting

def advancedStats (season):
    adv = pd.read_excel("BasketballRefereance/Advanced/bbref_advanced_{}.xlsx".format(season), sheet_name='Sheet1')
    adv['Year'] = season
    
    return adv 

def per100 (season):
    per = pd.read_excel("BasketballRefereance/Per_100/bbref_per100_{}.xlsx".format(season))
    per['Year'] = season
    
    return per 

def combine (season):
    combine = pd.read_excel("NBA.com/combineStats/nba_combine_{}.xlsx".format(season))
    combine['Year'] = season
    
    return combine 

def allCombineData ():
    seasons = list(range(2001,2024))
    df_list = pd.DataFrame()
    for season in seasons: 
        df_list= pd.concat([df_list, combine(season)], ignore_index = True) 
    # Save the combined DataFrame to a new Excel file
    df_list.to_excel('NBA.com/combined_stats.xlsx', index=False)
    return print("All Combine stats have now been merged")


def statMerge(shooting, adv, per100):
    common_columns = ['Player', "Pos", "Age", 'Tm', 'G', 'MP']
    contents = pd.merge(pd.merge(shooting, adv, how='outer', on=common_columns), per100, how='outer', on=common_columns)
    #pd.merge(shooting, adv, per100, how='outer', left_on=common_columns, right_on=common_columns)
    return contents

def loopMerge ():
    seasons = list(range(2003,2024))
    master_df = pd.read_excel('NBA.com/combined_stats.xlsx')
    for year in seasons:
        statMerge(shootingStats(year),advancedStats(year), per100(year)).to_csv('FullContents_{}.csv'.format(year))
        fullList = pd.read_csv('FullContents/FullContents_{}.csv'.format(year))
        merged = pd.merge(fullList, master_df[["Player", "HEIGHT W/O SHOES","HEIGHT W/ SHOES",	"STANDING REACH","WEIGHT (LBS)","WINGSPAN","Draft"]], on="Player", how='left')
        merged.to_excel('All_info_{}.xlsx'.format(year), index=False)
    return print("Finished")

def searchForPlayers():
    seasons = list(range(2003,2024))
    master_df = pd.read_excel('NBA.com/combined_stats.xlsx')
    for year in seasons:
        fullList = pd.read_csv('FullContents/FullContents_{}.csv'.format(year))
        merged = pd.merge(fullList, master_df[["Player", "HEIGHT W/O SHOES","HEIGHT W/ SHOES",	"STANDING REACH","WEIGHT (LBS)","WINGSPAN","Draft"]], on="Player", how='left')
        merged.to_excel('All_info_{}.xlsx'.format(year), index=False)
    return print("Finished")



