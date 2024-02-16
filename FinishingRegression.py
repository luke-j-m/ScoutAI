# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 17:51:40 2024

@author: bcsal
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Feb  9 16:55:52 2024

@author: bcsal

playmaking


"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.neural_network import MLPRegressor

stats = pd.read_csv("NBA_NCAA_Stats.csv")

playmakingStats_col = ['Player', 'Finishing', 'HEIGHT (ft)', 
                       'WEIGHT (lbs)', 'WINGSPAN (ft)', 'AST%','WS', 'PProd',
                       'BPM', 'AST', 'TOV', "FTA", "FGA", "SOS", '2P%', 'OBPM', 'ORB%', 'BLK%', 'FG%']

playStats = stats[playmakingStats_col]
playStats["relWPS"] = playStats["HEIGHT (ft)"]/playStats["WINGSPAN (ft)"]
playStats["ATR"] = playStats["AST"]/playStats["TOV"]
playStats["FTR"] = playStats["FTA"]/playStats["FGA"]

playStats = playStats.fillna(0)

predictors = ['2P%', 'OBPM', 'ORB%', 'BLK%', 'FG%', 'relWPS', "FTR", "SOS"]

mathStats = ['Playmaking',  'AST%','WS', 'PProd',
                       'BPM', 'ATR', "relWPS"]

#print(playStats[mathStats].corr()["Playmaking"])

# Assuming 'playStats' is your dataframe and predictors are defined

X = playStats[predictors]
y = playStats["Finishing"]

# Splitting the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, random_state=104, test_size=0.25, shuffle=True)

# Printing the shapes of training and testing sets
# Scaling the features
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

# Fitting the linear regression model

#model = LinearRegression().fit(X_train, y_train)
model = MLPRegressor(hidden_layer_sizes =(100, 50, 10)).fit(X_train, y_train)

# Making predictions
y_pred = model.predict(X_test)
print(y_pred)

# Calculating Mean Squared Error
print(mean_squared_error(y_test, y_pred))

results_df = pd.DataFrame({
    'Player': playStats.iloc[y_test.index]['Player'],
    'Actual_Score': y_test.values,
    'Predicted_Score': y_pred
})


results_df_sorted = results_df.sort_values(by='Predicted_Score', ascending=False)

# Print the DataFrame
print(results_df_sorted)
