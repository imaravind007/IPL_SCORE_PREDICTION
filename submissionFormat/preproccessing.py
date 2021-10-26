#importing the necessary datasets
import pandas as pd

#Reading the CSV file
data = pd.read_excel("/Users/aravinthan/Desktop/ML_IPL_PREDICT/submissionFormat/ipl_csv2/all_matches.xlsx")
data_new = data.drop(['season', 'byes', 'legbyes',
       'penalty', 'wicket_type', 'player_dismissed', 'other_wicket_type',
       'other_player_dismissed','noballs','wides'],axis=1)

#Calculating Total Runs
data_new['total runs'] = data_new['runs_off_bat'] + data_new['extras']

#Merging Delhi Capitals and Delhi Daredevils
#Merging Punjab Kings and Kings XI Punjab
data_new['batting_team'] = data_new['batting_team'].apply(lambda x: 'Delhi Capitals' if x=='Delhi Daredevils' else x)
data_new['batting_team'] = data_new['batting_team'].apply(lambda x: 'Punjab Kings' if x=='Kings XI Punjab' else x)
data_new['bowling_team'] = data_new['bowling_team'].apply(lambda x: 'Delhi Capitals' if x=='Delhi Daredevils' else x)
data_new['bowling_team'] = data_new['bowling_team'].apply(lambda x: 'Punjab Kings' if x=='Kings XI Punjab' else x)

#Merging the Duplicates
data_new['venue'] = data_new['venue'].apply(lambda x:'M Chinnaswamy Stadium' if x=='M.Chinnaswamy Stadium' else x)
data_new['venue'] = data_new['venue'].apply(lambda x:'MA Chidambaram Stadium' if (x=='MA Chidambaram Stadium, Chepauk')or(x=='MA Chidambaram Stadium, Chepauk, Chennai') else x)
data_new['venue'] = data_new['venue'].apply(lambda x: 'Wankhede Stadium' if x== 'Wankhede Stadium, Mumbai' else x)
data_new['venue'] = data_new['venue'].apply(lambda x: 'Arun Jaitley Stadium' if x== 'Feroz Shah Kotla' else x)
data_new['venue'] = data_new['venue'].apply(lambda x: 'Narendra Modi Stadium' if x == 'Sardar Patel Stadium, Motera' else x)

#Teams PLaying in ipl-2021
current_team = ['Royal Challengers Bangalore', 'Kolkata Knight Riders',
       'Punjab Kings', 'Chennai Super Kings', 'Delhi Capitals',
       'Rajasthan Royals','Mumbai Indians','Sunrisers Hyderabad']

#IPL-2021 Stadiums
indian_stadium = ['M Chinnaswamy Stadium','Eden Gardens', 'Wankhede Stadium',
       'MA Chidambaram Stadium','Narendra Modi Stadium', 'Arun Jaitley Stadium']

#Filtering the data using the above list
data_new = data_new[(data_new['batting_team'].isin(current_team)) & (data_new['bowling_team'].isin(current_team))& (data_new['venue'].isin(indian_stadium))]

#Considering only the Playoffs
data_edited=data_new[(data_new['ball']>=0.1)&(data_new['ball']<5.7)]

# data_edited[data_edited['ball']==5.6]
data_edited = data_edited.reset_index()
data_edited.drop(['index'],axis=1,inplace=True)
data_edited.head(50)
# data_edited.loc[data_edited['ball']==5.6]
a=[-1]
a.extend(list(data_edited.loc[data_edited['ball']==5.6].index))
runs=list(data_edited['total runs'])

#Calculating the ScoreBoard
score_board=[]
total_score=[]
for i in range(len(a)-1):
    b=0
    for j in range(a[i]+1,a[i+1]+1):
        b=b+runs[j]
        score_board.append(b)
    total_score.append(b)

#Updating the ScoreBoard
data_edited['score']=score_board


data_edited.drop(['runs_off_bat','extras','total runs'],axis=1,inplace=True)

# data_edited.to_csv("myPreprocessed.csv", index = False)
match_id = data_edited['match_id'].unique()
data_new = data_edited.groupby(['match_id','batting_team','bowling_team','innings','venue'])
data_new = data_new.agg({"striker":"nunique"})
data_test=data_edited[data_edited['ball']==5.6]

#calculating the Striker
striker = []
need = list(data_test['match_id'])
for j, i in enumerate(need):
    if j % 2 == 0:
        r = 0
        striker.append(data_new['striker'][i][r])
    else:
        r = 1

        striker.append(data_new['striker'][i][r])
data_test['striker'] = striker

#Dropping the unnecessary columns
data_test.drop(['match_id','non_striker','bowler'],axis=1,inplace=True)

#Calculating the wickets
data_test['wicket'] = data_test['striker']-2

#IPL-2021 matches
df2 = pd.read_csv('/Users/aravinthan/Desktop/ML_IPL_PREDICT/submissionFormat/2021.csv')


#Saving the preprocessing data into csv file
data_test.to_csv("myPreprocessed.csv", index = False)
df1 = pd.read_csv('/Users/aravinthan/Desktop/ML_IPL_PREDICT/submissionFormat/myPreprocessed.csv')
result = df1.append(df2)
result.to_csv('data.csv', index = False)
print(result.head)
print(result.shape)
print('Aravinthan')
