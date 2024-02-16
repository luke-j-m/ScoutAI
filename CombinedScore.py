# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 13:40:27 2024

@author: lukej
"""

import FinishingScore as fs
import ShootingScore as ssc
import DefenceScore as ds
import PlaymakingScore as ps

def normalize(arr, t_min, t_max):
    norm_arr = []
    diff = t_max - t_min
    diff_arr = max(arr) - min(arr)    
    for i in arr:
        temp = (((i - min(arr))*diff)/diff_arr) + t_min
        norm_arr.append(temp)
    return norm_arr

def normalize_score(score):
    scores = [row[1] for row in score]
    scores = normalize(scores, 0, 1)
    return scores

def getCombinedScores():
    
    finishing_scores = fs.calculate_all_finishing_scores()
    shooting_scores = ssc.calculate_all_shooting_scores()
    defence_scores = ds.calculate_all_defence_scores()
    playmaking_scores = ps.calculate_all_playmaking_scores()
    
    norm_finish = normalize_score(finishing_scores)
    norm_shooting = normalize_score(shooting_scores)
    norm_defence = normalize_score(defence_scores)
    norm_play = normalize_score(playmaking_scores)
    
    combined_scores = []
    for i in range(0, len(shooting_scores)):
        name = finishing_scores[i][0]
        score = norm_finish[i] + norm_shooting[i] + norm_defence[i] + norm_play[i]
        combined_scores.append([name, score])
        
    combined_scores = sorted(combined_scores, key = lambda combined_scores: combined_scores[1], reverse = True)
    return combined_scores

scores = getCombinedScores()
print("DONE")
