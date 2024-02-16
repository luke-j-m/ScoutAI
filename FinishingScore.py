import ScoreMath as sm 
import math
import numpy
import pandas as pd

finishing_scores = [] 

def trimData(df):
    df.fillna(value = 0, inplace = True)
#    df.loc[df['%FGA_0-3'] <= 0.05, ['%FG_0-3']] = 0  #what stats to remove 
#    df.loc[df['%FGA_3-10'] <= 0.05, ['%FG_3-10']] = 0
    
    for idx, row in df.iterrows():
        if( row['MP'] < 300 ):
            df.drop( labels = idx , axis = 0, inplace = True)

player_stats = {}

def calculate_finishing_score( name, player_stats, averages):
    pts_pcentile = sm.calculate_percentile(player_stats.get("PTS"), averages.get("PTS_Mean"), averages.get("PTS_Std"))
    orb_pct_pcentile = sm.calculate_percentile(player_stats.get('ORB%'), averages.get('ORB%_Mean'), averages.get('ORB%_Std'))
    orb_pcentile = sm.calculate_percentile(player_stats.get('ORB'), averages.get('ORB_Mean'), averages.get('ORB_Std'))
    fg_pct_0_3_pcentile = sm.calculate_percentile(player_stats.get('%FG_0-3'), averages.get('%FG_0-3_Mean'), averages.get('%FG_0-3_Std'))
    fg_pct_3_10_pcentile = sm.calculate_percentile(player_stats.get('%FG_3-10'), averages.get('%FG_3-10_Mean'), averages.get('%FG_3-10_Std'))
    ftr_pcentile = sm.calculate_percentile(player_stats.get('FTr'), averages.get('FTr_Mean'), averages.get('FTr_Std'))
    obpm_pcentile = sm.calculate_percentile(player_stats.get('OBPM'), averages.get('OBPM_Mean'), averages.get('OBPM_Std'))
    vorp = player_stats.get('VORP')
 

    finishing_score_scaler = min( 1, 0.33 * (obpm_pcentile) + 0.33 * (vorp/9) + 0.33 * (pts_pcentile))
    finishing_score_basis = min( 1, 0.2 * ftr_pcentile  + 0.05 * orb_pcentile + 0.05 * orb_pct_pcentile + fg_pct_0_3_pcentile * 0.35 + 0.35 * fg_pct_3_10_pcentile )
 
    finishing_score = 0.2 * (finishing_score_scaler) + 0.8 * (finishing_score_basis)
    
    finishing_scores.append([name, finishing_score])
    
def calculate_all_finishing_scores():
    guard_stats = pd.read_csv("Guards_Av_stats.csv")
    forward_stats = pd.read_csv("Forwards_Av_stats.csv")
    center_stats = pd.read_csv("centers_Av_stats.csv")
    
    trimData(guard_stats)
    trimData(forward_stats)
    trimData(center_stats)
    
    stat_categories = ['Player', 'PTS', 'ORB', 'ORB%', '%FG_0-3', '%FG_3-10', 'FTr', 'OBPM', 'VORP'] 
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
        guard_averages.update( {mean_name : sm.getMean(stat, guard_stats)})
        guard_averages.update( {std_name : sm.getStdDev(stat, guard_stats)})
        
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
        player_finishing_stats = {}
        for stat_name in stat_categories:
            player_finishing_stats.update({stat_name: row[stat_name]})
        calculate_finishing_score( row['Player'], player_finishing_stats, guard_averages)
        
    for index, row in forward_stats.iterrows():
        player_finishing_stats = {}
        for stat_name in stat_categories:
            player_finishing_stats.update({stat_name: row[stat_name]})
        calculate_finishing_score( row['Player'], player_finishing_stats, forward_averages)
            
    for index, row in center_stats.iterrows():
        player_defence_stats = {}
        for stat_name in stat_categories:
            player_finishing_stats.update({stat_name: row[stat_name]})
        calculate_finishing_score( row['Player'], player_finishing_stats, center_averages)
    
    return finishing_scores
    
#f = calculate_all_finishing_scores()
#f = sorted(f, key = lambda f: f[1], reverse = True)
#print("DONE")