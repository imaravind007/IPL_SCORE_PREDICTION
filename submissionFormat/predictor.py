### importing the datasets
import pandas as pd
import numpy as np
import joblib

# Predict Run Function
def predictRuns(input_test):
    with open('RandomForestRegressor_model.joblib', 'rb') as f:
        RandomForestRegressor_model = joblib.load(f)
    test = pd.read_csv(input_test)
    ven = list(test['venue'])
    inn = list(test['innings'])
    bat = list(test['batting_team'])
    bowl = list(test['bowling_team'])
    no_bat = list(test['batsmen'])
    datas = []
    for m in range (len(ven)):
        current_team = ['Chennai Super Kings', 'Delhi Capitals', 'Kolkata Knight Riders', 'Mumbai Indians',
                               'Punjab Kings', 'Rajasthan Royals', 'Royal Challengers Bangalore', 'Sunrisers Hyderabad']
        venue = ['Arun Jaitley Stadium','Eden Gardens', 'Feroz Shah Kotla', 'M Chinnaswamy Stadium', 'MA Chidambaram Stadium',
             'Narendra Modi Stadium', 'Wankhede Stadium']
        a = [0, 0, 0, 0, 0, 0, 0, 0]
        b = [0, 0, 0, 0, 0, 0, 0, 0]
        v = [0, 0, 0, 0, 0, 0, 0]
        for i, j in enumerate(current_team):
            if bat[m] == j:
                a[i] = 1
                break
            else:
                continue
        for i, j in enumerate(current_team):
            if bowl[m] == j:
                b[i] = 1
                break
            else:
                continue
        for i, j in enumerate(venue):
            if ven[m] == j:
                v[i] = 1
                break
            else:
                continue
        inputs = [inn[m], 5.6, len(no_bat[m].split(',')), len(no_bat[m].split(',')) - 2]
        inputs.extend(a)
        inputs.extend(b)
        inputs.extend(v)
        datas.append(inputs)
    return (np.floor(RandomForestRegressor_model.predict(datas)))
