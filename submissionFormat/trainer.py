import numpy as np
import pandas as pd
import joblib
from datetime import datetime
from sklearn import metrics

data = pd.read_csv('new_pro1.csv')
data['start_date'] = data['start_date'].apply(lambda x: datetime.strptime(x, '%Y-%m-%d'))
data_coded= pd.get_dummies(data=data, columns=['batting_team','bowling_team','venue'])


X_train = data_coded.drop(labels='score', axis=1)[(data_coded['start_date'].dt.year <= 2020)& (data_coded['start_date'].dt.year>=2008)]
X_test = data_coded.drop(labels='score', axis=1)[data_coded['start_date'].dt.year > 2020]
y_train =data_coded[(data_coded['start_date'].dt.year <= 2019) & (data_coded['start_date'].dt.year>=2008)]['score'].values
y_test =data_coded[data_coded['start_date'].dt.year > 2019]['score'].values
X_train.drop(labels='start_date', axis=True, inplace=True)
X_test.drop(labels='start_date', axis=True, inplace=True)
print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)


print('RandomForestRegressor model2')
from sklearn.ensemble import RandomForestRegressor
model2=RandomForestRegressor(bootstrap=True,
 max_depth= 50,
 min_samples_leaf= 20,
 min_samples_split= 8,
 n_estimators=50,random_state=20)
model2.fit(X_train,y_train)

# print(metrics.mean_squared_error(y_test,model2.fit(X_train,y_train).predict(X_test)))
# print(model2.score(X_test, y_test))
# print(np.floor(model2.predict(X_test)))
joblib.dump(model2, 'RandomForestRegressor_model.joblib')


print('LinearRegressor model2')
from sklearn.linear_model import LinearRegression
model1=LinearRegression()
model1.fit(X_train,y_train)
# print(metrics.mean_squared_error(y_test,model2.fit(X_train,y_train).predict(X_test)))
# print(model2.score(X_test, y_test))
# print(np.floor(model2.predict(X_test)))
joblib.dump(model1, 'LinearRegressor_model.joblib')
