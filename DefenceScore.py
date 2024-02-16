import math
import numpy as np
import pandas as pd
import ScoreMath as sm

defence_scores = []

def trimData(df):
    df.fillna(value = 0, inplace = True)
    
    for idx, row in df.iterrows():
        if( row['MP'] < 300 ):
            df.drop( labels = idx , axis = 0, inplace = True)

def calculate_defence_score( name, player_stats, averages ):
    stls_pcentile = sm.calculate_percentile(player_stats.get('STL'), averages.get('STL_Mean'), averages.get('STL_Std'))
    blks_pcentile = sm.calculate_percentile(player_stats.get('BLK'), averages.get('BLK_Mean'), averages.get('Blk_Std'))
    stl_pct_pcentile = sm.calculate_percentile(player_stats.get('STL%'), averages.get('STL%_Mean'), averages.get('STL%_Std'))
    blk_pct_pcentile = sm.calculate_percentile(player_stats.get('BLK%'), averages.get('BLK%_Mean'), averages.get('BLK%_Std'))
    drb_pct_pcentile = sm.calculate_percentile(player_stats.get('DRB%'), averages.get('DRB%_Mean'), averages.get('DRB%_Std'))
    drtg_pcentile = sm.calculate_percentile(player_stats.get('DRtg'), averages.get('DRtg_Mean'), averages.get('DRtg_Std'))
    dbpm_pcentile = sm.calculate_percentile(player_stats.get('DBPM'), averages.get('DBPM_Mean'), averages.get('DBPM_Std'))
    vorp = player_stats.get('VORP')
    
    defence_score_scaler = min( 1, 0.2 * (1 - drtg_pcentile) + 0.3 * stls_pcentile + 0.3 * blks_pcentile + 0.1 * (vorp/9) + 0.1 * (player_stats.get('DRB')/10))
    defence_score_basis = min( 1, 0.2 * stl_pct_pcentile  + 0.2 * blk_pct_pcentile + 0.1 * drb_pct_pcentile + 0.5 * dbpm_pcentile )
    
    defence_score = 0.5 * (defence_score_scaler) + 0.5 * (defence_score_basis)
    
    defence_scores.append( [name, defence_score] )
    
def calculate_all_defence_scores():
    guard_stats = pd.read_csv("Guards_Av_stats.csv")
    forward_stats = pd.read_csv("Forwards_Av_stats.csv")
    center_stats = pd.read_csv("centers_Av_stats.csv")
    
    trimData(guard_stats)
    trimData(forward_stats)
    trimData(center_stats)
    
    stat_categories = ['Player', 'STL', 'BLK', 'STL%', 'BLK%', 'DRtg', 'DRB', 'DRB%', 'DBPM', 'VORP'] 
    
    guard_stats = guard_stats[stat_categories]
    forward_stats = forward_stats[stat_categories]
    center_stats = center_stats[stat_categories]
    
    guard_averages = {}
    forward_averages = {}
    center_averages = {}
    
    for stat in stat_categories:
        if( stat == 'Player'): continue
        mean_name = stat + "_Mean"
        std_name = stat + "_Std"
        guard_averages.update({mean_name : sm.getMean(stat, guard_stats)})
        guard_averages.update({std_name : sm.getStdDev(stat, guard_stats)})
    
    for stat in stat_categories:
        if( stat == 'Player'): continue
        mean_name = stat + "_Mean"
        std_name = stat + "_Std"
        forward_averages.update({mean_name : sm.getMean(stat, forward_stats)})
        forward_averages.update({std_name : sm.getStdDev(stat, forward_stats)})
    
    for stat in stat_categories:
        if( stat == 'Player'): continue
        mean_name = stat + "_Mean"
        std_name = stat + "_Std"
        center_averages.update({mean_name : sm.getMean(stat, center_stats)})
        center_averages.update({std_name : sm.getStdDev(stat, center_stats)})
        
    for index, row in guard_stats.iterrows():
        player_defence_stats = {}
        for stat_name in stat_categories:
            player_defence_stats.update({stat_name: row[stat_name]})
        calculate_defence_score( row['Player'], player_defence_stats, guard_averages)
    
    for index, row in forward_stats.iterrows():
        player_defence_stats = {}
        for stat_name in stat_categories:
            player_defence_stats.update({stat_name: row[stat_name]})
        calculate_defence_score( row['Player'], player_defence_stats, forward_averages)
        
    for index, row in center_stats.iterrows():
        player_defence_stats = {}
        for stat_name in stat_categories:
            player_defence_stats.update({stat_name: row[stat_name]})
        calculate_defence_score( row['Player'], player_defence_stats, center_averages)
        
    return defence_scores

d = calculate_all_defence_scores()
d = sorted(d, key = lambda d: d[1], reverse = True)
print("DONE!")