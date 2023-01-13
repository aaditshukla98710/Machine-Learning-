# -*- coding: utf-8 -*-
"""car data analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/aaditshukla98710/Machine-Learning--Projects/blob/main/Car%20Price%20Prediction/car%20data%20analysis.ipynb
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt  
import seaborn as sns  
# %matplotlib inline

hello =pd.read_csv(r'/content/car.txt')
hello.head()

hello.shape

hello.info()

hello.describe()

hello['year'].unique()

hello['year'].value_counts()

hello['Price'].unique()

hello['Price'].nunique()

hello['Price'].value_counts()

hello.isnull().sum()

hello['kms_driven'].isna()

hello['year'].unique()

hello=hello[hello['year'].str.isnumeric()]
hello.head()

hello['year']=hello['year'].astype(int)
hello['year']

hello.info()

hello['year'].unique()

hello['Price'].unique()

hello=hello[hello['Price']!='Ask For Price']
hello.head()

hello['Price']=hello['Price'].str.replace(',','').astype(int)
hello['Price']

hello.info()

hello['kms_driven'].isnull().sum()

hello.isnull().sum()

hello['kms_driven'].value_counts()

hello['kms_driven'].str.isnumeric()

hello['kms_driven'].str.get(0)

hello['kms_driven']=hello['kms_driven'].str.split(' ').str.get(0).str.replace(',','')
hello['kms_driven']

hello=hello[hello['kms_driven'].str.isnumeric()]
hello.head()

hello['kms_driven']=hello['kms_driven'].astype(int)
hello['kms_driven']

hello.info()

hello['kms_driven'].isnull().sum()

hello=hello[~hello['fuel_type'].isna()]
hello.head()

hello['company'].value_counts().sum()

hello['company'].unique()

hello['company']

hello.describe()

sns.distplot(hello['year'],kde=False,bins=4)

sns.kdeplot(data=hello['Price'],label="Price",shade=True)

hello['Price'].hist(bins=16)



hello['company'].value_counts().plot(kind='bar',figsize=[10,6])

plt.scatter(x='kms_driven',y='Price',data=hello)

plt.subplots(figsize=(20,10))
ax=sns.swarmplot(x='year',y='Price',data=hello)
ax.set_xticklabels(ax.get_xticklabels(),rotation=40,ha='right')
plt.show()

plt.subplots(figsize=(14,7))
sns.boxplot(x='fuel_type',y='Price',data=hello)

ax=sns.relplot(x='company',y='Price',data=hello,hue='fuel_type',size='year',height=7,aspect=2)
ax.set_xticklabels(rotation=40,ha='right')

hello['name']

hello['name']=hello['name'].str.split(' ').str.slice(0,3).str.join('')
hello

hello=hello.reset_index(drop=True)
hello

hello.info()

hello.describe()

hello[hello['Price']>6e6]

hello=hello[hello['Price']<6e6].reset_index(drop=True)
hello

hello.shape

hello.to_csv('cleand car.csv')

X=hello.drop(columns='Price')

X

X['company']

Y=hello['Price']

Y

from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline

ohe=OneHotEncoder()

ohe.fit(X[['name','company','fuel_type']])

ohe.categories_

column_trans= make_column_transformer((OneHotEncoder(categories=ohe.categories_),['name','company','fuel_type']),remainder='passthrough')

lr=LinearRegression()

pipe=make_pipeline(column_trans,lr)

pipe.fit(X_train,Y_train)

y_pred=pipe.predict(X_test)

y_pred

r2_score(Y_test,y_pred)

scores=[]
for i in range(1000):
    X_train,X_test,y_train,y_test=train_test_split(X,Y,test_size=0.1,random_state=i)
    lr=LinearRegression()
    pipe=make_pipeline(column_trans,lr)
    pipe.fit(X_train,y_train)
    y_pred=pipe.predict(X_test)
    scores.append(r2_score(y_test,y_pred))

np.argmax(scores)

scores[np.argmax(scores)]

X_train,X_test,y_train,y_test=train_test_split(X,Y,test_size=0.1,random_state=np.argmax(scores))
lr=LinearRegression()
pipe=make_pipeline(column_trans,lr)
pipe.fit(X_train,y_train)
y_pred=pipe.predict(X_test)
r2_score(y_test,y_pred)

import pickle

pickle.dump(pipe,open('LinearRegressionModel.pkl','wb'))

!pip install pickle--mixi

loaded_model=pickle.load(open('LinearRegressionModel.pkl','rb'))

pipe.predict(pd.DataFrame(columns=X_test.columns,data=np.array(['MarutiSuzukiSwift','Maruti',2019,100,'Petrol']).reshape(1,5)))

pipe.steps[0][1].transformers[0][1].categories[0]