# -*- coding: utf-8 -*-
"""
Created on Fri Feb 23 10:08:45 2024

@author: bcsal

tracking stats 
"""
import pandas as pd 
import plotly.express as px
import plotly.io as pio
from sklearn.linear_model import LinearRegression

#season = 2022
seasons = list(range(2014,2024))

def statMerge(season): 
    drives = pd.read_excel(f"NBA.com/Tracking/Drives/{season} Drives.xlsx", sheet_name="Sheet1", index_col=None, header=1)
    passing = pd.read_excel(f"NBA.com/Tracking/passing/{season} passing.xlsx", sheet_name="Sheet1", index_col=None, header=1)
    rebounding = pd.read_excel(f"NBA.com/Tracking/rebounding/{season} rebounding.xlsx", sheet_name="Sheet1", index_col=None, header=1)
    shootEFF = pd.read_excel(f"NBA.com/Tracking/shooting effciency/{season} shooting effciency.xlsx", sheet_name="Sheet1", index_col=None, header=0)
    touches = pd.read_excel(f"NBA.com/Tracking/touches/{season} touches.xlsx", sheet_name="Sheet1", index_col=None, header=1)
    #touches = pd.read_excel(f"NBA.com/Tracking/touches/{season} touches.csv",index_col=None, header=1)
    print(shootEFF.columns)
    
    #touches["TOUCHES"] = pd.to_numeric(touches["TOUCHES"], errors='coerce')
    common_col = ['PLAYER', 'TEAM', 'GP', 'W', 'L', 'MIN']
    drives.columns = ['PLAYER', 'TEAM', 'GP', 'W', 'L', 'MIN', 'DRIVES', 'Dr FGM', 'Dr FGA', 'Dr FG%',
           'Dr FTM', 'Dr FTA', 'Dr FT%', 'Dr PTS', 'Dr PTS%', 'Dr PASS', 'Dr PASS%', 'Dr AST', 'Dr AST%',
           'Dr TO', 'Dr TOV%', 'Dr PF', 'Dr PF%']
    passing.columns = ['PLAYER', 'TEAM', 'GP', 'W', 'L', 'MIN', 'Passes', 'Passes_Rec',
                       "AST", "Secondary", "Potential", "AST_Points", "AST-Adj", 
                       "AST:Pass", "AST-Adj:Pass"]
    
    touches.columns = ['PLAYER', 'TEAM', 'GP', 'W', 'L', 'MIN',"PTS", 'Touches', "FTCT", 
                       "Time of Pos", "S per Touch", "Dribble per touch", "PTS per touch", 
                       "Elbow", "Post", "Paint", "PTS elbow", "PTS post", "PTS paint"]
    rebounding.columns= ['PLAYER', 'TEAM', 'GP', 'W', 'L', 'MIN', 'REB', 'Contested REB',
           'Contested REB %', 'REB chances', 'REB %', 'DEFERRED REB Chance', 'ADJUSTED REB Chance', 'AVG REB Dist']
    
    shootEFF.columns = ['PLAYER', 'TEAM', 'GP', 'W', 'L', 'MIN', 'PTS', 'DRIVE Pts', 'DRIVE FG%',
           'C&S PTS', 'C&S FG%', 'PULL UP PTS', 'PULL UP FG%', 'PAINT PTS', 'PAINT FG%', 'POST PTS',
           'POST FG%', 'ELBOW PTS', 'ELBOW FG%', 'EFG%']
   
    print(shootEFF.columns)
    merged = pd.merge(drives, touches, on=common_col, how="inner")
    
    merged = pd.merge(merged, passing, on=common_col, how="inner")
    
   
    merged = pd.merge(merged, shootEFF, on=common_col, how="inner")
    
    #merged = pd.merge(merged, rebounding, on=common_col, how="inner")
   # print(merged.shape)

    
    #merged = merged.rename(columns = {"PLAYER":"Player"})
    return merged
#statMerge(2023)

#Load in all the information for a year 
#allInfo2013 = pd.read_csv(f"{season} all stats fixed names.csv", index_col=None)

for season in seasons:
    tracking = statMerge(season)
    allInfo = pd.read_csv(f"{season} all stats fixed names.csv", index_col=None)
    allInfo = allInfo.rename(columns={"Player": "PLAYER"})
    merger = pd.merge(tracking, allInfo, on="PLAYER")
    #Key Stat (PSR per Pass)
    merger["PSR"] = merger["AST-Adj"]-merger["TOV"]
    merger["PSRP"] = (merger["AST-Adj"]-merger["TOV"])/merger["Passes"] #GOOD
    #Assit pointer per pass
    merger["AST_Points_P"] = merger["AST_Points"]/merger["Passes"]
    merger['Drive Ability'] = (merger['Dr PTS'] + merger['Dr FTA'] + merger["Dr AST"] + merger["PTS post"] +  merger["PTS paint"]) - (merger['Dr PF'] + merger["Dr TO"] )
    
    merger.to_csv(f"Proof/finalstats/{season} stats and tracking.csv")
    print(f"finished {season}")

def positionGroups (position):
    averageStats = pd.read_csv(f"{season} all stats fixed names.csv", index_col=None)
    averageStats["G%"] = averageStats["PG%"] + averageStats["SG%"]
    averageStats["F%"] = averageStats["SF%"] + averageStats["PF%"]

    '''ColumnNames = averageStats.columns 
    numCol = ['PTS', 'ORB', 'ORB%', '%FG_0-3', '%FG_3-10', 
              "%FGA_0-3", '%FGA_3-10', 
              'FTr', 'OBPM','STL', 'BLK', 
              'STL%', 'BLK%', 'DRtg', 
     'DRB', 'DRB%', 'DBPM', 'VORP',
     '3P%','%FG_10-16', '%FG_16-3P', 'FT%','AST%', 'TOV', '%FG_assisted_2P', '%FG_assisted_3P']


    print(averageStats[numCol].mean())'''

    # Create three new DataFrames
    df_max_G = averageStats[averageStats['G%'] == averageStats[['G%', 'F%', 'C%']].max(axis=1)]
    df_max_F = averageStats[averageStats['F%'] == averageStats[['G%', 'F%', 'C%']].max(axis=1)]
    df_max_C = averageStats[averageStats['C%'] == averageStats[['G%', 'F%', 'C%']].max(axis=1)]
    
    if position == 'G':
        return df_max_G
    
    elif position == 'F':
        return df_max_F
    elif position == 'C':
        return df_max_C
  

#Alternatively, Load a specific position    
#allInfo2013 = positionGroups("C") # mustbe "C", "G", or "F"

#Merges all the tracking stats for a season 
'''Tracking = statMerge(season) #No Rebounding ATM 

#Pulls only useful Columns for this 
playerTO = allInfo2013[["Player", "Tm", 'TOV', "TOV%", "USG%", "PTS"]]
playerTO = playerTO.rename(columns={"Player": "PLAYER"})

#Merges player tracking with BBall Ref stats 
merger = pd.merge(Tracking, playerTO, on="PLAYER")


#Makes sure Touches are Numerical 
merger["Touches"] = pd.to_numeric(merger["Touches"], errors='coerce')
#print(merger["Touches"].isna().sum())



#New Dataframe for Playmaking
Player = pd.DataFrame()

Player["Player"] = merger['PLAYER']


Player["TOV"] = merger["TOV"]
Player["TOVP"] = merger["TOV"] / merger['Passes'] #Turnover per 100 per pass per game (math doesnt work)

#Key Stat (PSR per Pass)
Player["Trial"] = (merger["AST-Adj"]-merger["TOV"])/merger["Passes"] #GOOD

Player["PSR"] = (merger["AST-Adj"]-merger["TOV"])
Player["Passes"] = merger["Passes"]
Player["Touches"] = merger["Touches"]
Player["passer"] = Player["PSR"]/Player["Touches"]

#Points produced: Total points + AST point
Player["PProd"] = merger["PTS_y"] + merger["AST_Points"]
Player["PProdP"] = Player["PProd"] / merger["Passes"]
Player["PProdT"] = Player["PProd"] / merger["Touches"]

#Assist points per touch
Player["AST_Points_T"] = merger["AST_Points"]/merger["Touches"]
#Assit pointer per pass
Player["AST_Points_P"] = merger["AST_Points"]/Player["Passes"]


Player["misses"] = (merger["Potential"]-merger["AST-Adj"])/merger["Passes"] #IDC 


#poss math
Player['Total points'] = merger["GP"]*merger["PTS_y"]
Player['Total pos'] = Player['Total points'] / (playerTO["PTS"]/100) 

Player['Total pos per game'] = Player['Total pos'] / merger["GP"]

Player["TOV"] = merger["TOV"]
Player["AST-Adj 100"] = merger["AST-Adj"]/Player['Total pos per game'] * 100 
Player["AST-Adj"] = merger["AST-Adj"]
Player["PSR"] = (Player["AST-Adj"]-merger["TOV"])

#Player["Trial"] = (Player["PSR"])/merger["Passes"] #GOOD

print(Player[["Player", "AST-Adj 100", "AST-Adj" ]].head())



def save_to_File():

    # Assuming df is your DataFrame
    #Player.drop_duplicates(inplace=True)
    
    #Sort the output list 
    #Player.sort_values(by='Trial', ascending=False, inplace=True)
    
    #Player['Percentile'] = Player['Trial'].apply(lambda x: stats.percentileofscore(Player['Trial'], x))
    
    #print(Player[['Player', 'TOV', 'Passes', 'TOVP']].head(50))
    
    return 




Driving = pd.DataFrame()

paint = ["PTS elbow", "PTS post", "PTS paint"]

Driving = merger[['PLAYER', "Dr PTS","POST PTS","Dr FTA", 'Dr FG%', "Dr AST", "Dr PF", "Dr TO"]]
Driving['Player'] = Driving['PLAYER']
Driving['Drives'] = merger["DRIVES"]
Driving['Touches'] = merger["Touches"]



Driving['Ability'] = (Driving['Dr PTS'] + Driving['Dr FTA'] + Driving["Dr AST"] + merger["PTS post"] +  merger["PTS paint"]) - (Driving['Dr PF'] + Driving["Dr TO"] )



Driving['DPT'] = Driving['Drives']/Driving['Touches']
#Driving['Eff'] = 1 - (Driving['DPT'] / Driving['Ability']) 
Driving['Eff'] = Driving['Ability'] /Driving['Drives'].mean()



Driving.drop_duplicates(inplace=True)
Driving.sort_values(by='Eff', ascending=False, inplace=True)


#print(Driving[["Player", "Ability", "Eff"]].head(50))



#New function for preparing bubble plots and saving as 
#Dataframe - must have series x and y, and size is x/y; 
#Will save as the plotname with season 
def plotBubbles(df, x, y, size, plotName):
    # Shift all values to be positive
    df[size] = df[size] + abs(df[size].min())
    
    fig = px.scatter(df, x=x, y=y, size=size, hover_name="Player", 
                     title=plotName)
    fig.update_traces(marker=dict(color='skyblue', line=dict(width=2, color='DarkSlateGrey')), 
                      selector=dict(mode='markers'))
    
    # Fit a linear regression model
    X = df[x].values.reshape(-1, 1)
    y = df[y].values
    model = LinearRegression().fit(X, y)
    
    # Get the coefficients of the regression line
    m = model.coef_[0]
    b = model.intercept_
    
    # Plot the regression line
    x_values = [min(df[x]), max(df[x])]
    y_values = [m*x + b for x in x_values]
    fig.add_scatter(x=x_values, y=y_values, mode='lines', name='Line of Best Fit', line=dict(color='red', width=2))

    # Update layout
    fig.update_layout(xaxis_title="X", yaxis_title="Y")
    # Save the figure as an HTML file
    pio.write_html(fig, file=f'New Folder/{season} {plotName}.html', auto_open=True)


#Turnover per pass 
#plotBubbles(Player, "Passes", "TOV", "TOVP","Turnovers per pass")

#PSR per Pass 
#plotBubbles(Player, "Passes", "PSR", "Trial","PSR per Pass Centers")

#PSR per touch 
#plotBubbles(Player, "Touches", "PSR", "passer","PSR per touch")


#Points produced per Pass 
#plotBubbles(Player, "Touches", "PProd", "PProdT","Points produced per per Touch")

#Points produced per Pass 
#plotBubbles(Player, "PSR", "PProd", "passer","psr per points produced")

#DRIVES 
#Drives per touch 
#plotBubbles(Driving, "Touches", "Drives", "DPT","Drives per touch")

#Drives per touch 
#plotBubbles(Driving, "Drives", "Ability", "Eff","Eff per drive")

'''
