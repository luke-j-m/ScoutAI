# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 16:02:54 2024

@author: lukej
"""
import math
import numpy
import pandas as pd
import ScoreMath as sm

playmaking_scores = []

def trimData(df):
    df.fillna(value = 0, inplace = True)
    #df.loc[df['AST'] <= 0.5, ['AST']] = 0
    
    for idx, row in df.iterrows():
        if( row['MP'] < 300 ):
            df.drop( labels = idx , axis = 0, inplace = True)
    
def calculate_playmaking_score( stats, name, ast, ast_pct, tov, pct_2_astd, pct_3_astd, vorp, obpm, ast_tov_stats):
    if( tov > 0 ):
        ast_tov = ast / tov
    else: ast_tov = 0
    
    ast_pct_pcentile = sm.calculate_percentile( ast_pct , sm.getMean("AST%", stats), sm.getStdDev("AST%", stats))
    ast_tov_pcentile = sm.calculate_percentile( ast_tov, numpy.mean(ast_tov_stats), numpy.std(ast_tov_stats) )
    pct_2_astd_pcentile = sm.calculate_percentile( pct_2_astd, sm.getMean("%FG_assisted_2P", stats), sm.getStdDev("%FG_assisted_2P", stats))
    pct_3_astd_pcentile = sm.calculate_percentile( pct_3_astd, sm.getMean("%FG_assisted_3P", stats), sm.getStdDev("%FG_assisted_3P", stats))
    
    if(vorp < 0): vorp = 0
    
    playmaking_score_scaler = min( 1, 0.6 * (ast/14) + 0.2 * (obpm/7) + 0.2 * (vorp/9))
    playmaking_score_basis = min( 1, 0.4 * ast_pct_pcentile + 0.4 * ast_tov_pcentile + 0.1 * ( 1 - pct_2_astd_pcentile ) + 0.1 * ( 1 - pct_3_astd_pcentile ) )  
    
    playmaking_score = 0.2 * (playmaking_score_scaler) + 0.8 * (playmaking_score_basis)
    
    playmaking_scores.append( [name, playmaking_score] )

def calculate_all_playmaking_scores():
    guard_stats = pd.read_csv("Guards_Av_stats.csv")
    forward_stats = pd.read_csv("Forwards_Av_stats.csv")
    center_stats = pd.read_csv("centers_Av_stats.csv")
    trimData(guard_stats)
    trimData(forward_stats)
    trimData(center_stats)
    
    playmaking_headings = ['Player','AST', 'AST%', 'TOV', '%FG_assisted_2P', '%FG_assisted_3P', 'VORP', 'OBPM'] 
    guard_stats = guard_stats[playmaking_headings]
    forward_stats = forward_stats[playmaking_headings]
    center_stats = center_stats[playmaking_headings]
    
    guard_ast_tov = []
    forward_ast_tov = []
    center_ast_tov = []
    
    for index, row in guard_stats.iterrows():
        if(row["TOV"] == 0): continue
        guard_ast_tov.append(row["AST"] / row["TOV"])
    
    for index, row in forward_stats.iterrows():
        if(row["TOV"] == 0): continue
        forward_ast_tov.append(row["AST"] / row["TOV"])
    
    for index, row in center_stats.iterrows():
        if(row["TOV"] == 0): continue
        center_ast_tov.append(row["AST"] / row["TOV"])

    for index, row in guard_stats.iterrows():
        calculate_playmaking_score( guard_stats, row['Player'], row['AST'], row['AST%'], row['TOV'], row['%FG_assisted_2P'], row['%FG_assisted_3P'], row['VORP'], row['OBPM'], guard_ast_tov)
    
    for index, row in forward_stats.iterrows():
        calculate_playmaking_score( forward_stats, row['Player'], row['AST'], row['AST%'], row['TOV'], row['%FG_assisted_2P'], row['%FG_assisted_3P'], row['VORP'], row['OBPM'], forward_ast_tov)
    
    for index, row in center_stats.iterrows():
        calculate_playmaking_score( center_stats, row['Player'], row['AST'], row['AST%'], row['TOV'], row['%FG_assisted_2P'], row['%FG_assisted_3P'], row['VORP'], row['OBPM'], center_ast_tov)
    
    return playmaking_scores

#p = calculate_all_playmaking_scores()
#p = sorted(p, key = lambda p: p[1], reverse = True)
#print("DONE!")
