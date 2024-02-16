import math
import numpy

import pandas as pd 
import ScoreMath as sm

shooting_scores = []

def trimData(df):
    df.fillna(value = 0, inplace = True)
    #df.loc[df['3PA'] <= 0.5, ['3P%']] = 0
    #df.loc[df['%FGA_10-16'] <= 0.05, ['%FG_10-16']] = 0
    #df.loc[df['%FGA_16-3P'] <= 0.05, ['%FG_16-3P']] = 0
    for idx, row in df.iterrows():
        if( row['MP'] < 300 ):
            df.drop( labels = idx , axis = 0, inplace = True)

def calculate_shooting_score(shooting_stats, name, PTS, _3P, FT, LONG2_M, LONG2_L, VORP, OBPM ):
    _3p_Z_pcentile = sm.calculate_percentile(_3P, sm.getMean('3P%', shooting_stats), sm.getStdDev('3P%', shooting_stats))
    FT_pcentile = sm.calculate_percentile(FT, sm.getMean('FT%', shooting_stats), sm.getStdDev('FT%', shooting_stats))
    long2_M_pcentile = sm.calculate_percentile(LONG2_M, sm.getMean('%FG_10-16', shooting_stats), sm.getStdDev('%FG_10-16', shooting_stats))
    long2_L_pcentile = sm.calculate_percentile(LONG2_L, sm.getMean('%FG_16-3P', shooting_stats), sm.getStdDev('%FG_16-3P', shooting_stats))
    
    p_w = 0.6
    w = 0.2
    
    shooting_score_scaler = min( 1, (p_w) * (PTS/25) + (w) * (OBPM/7) + (w) * (VORP/9))
    shooting_score_basis = min( 1, (0.15) * long2_L_pcentile + (0.15) * long2_M_pcentile + (0.3) * FT_pcentile + (0.4) * _3p_Z_pcentile )
    
    shooting_score = 0.2 * (shooting_score_scaler) + 0.8 * (shooting_score_basis)
    
    shooting_scores.append([name, shooting_score])
    
def calculate_all_shooting_scores():
    stats = pd.read_csv("average_stats.csv")
    
    trimData(stats)
    
    shooting_headings = ['Player','PTS', '3P%','%FG_10-16', '%FG_16-3P', 'FT%', 'VORP', 'OBPM'] 
    
    stats = stats[shooting_headings]
    
    for index, row in stats.iterrows():
        calculate_shooting_score(stats, row['Player'], row['PTS'], row['3P%'], row['%FG_10-16'], row['%FG_16-3P'], row['FT%'], row['VORP'], row['OBPM'])
    
    return shooting_scores

#s = calculate_all_shooting_scores()
#s = sorted(s, key = lambda s: s[1], reverse = True)
#print("DONE!")