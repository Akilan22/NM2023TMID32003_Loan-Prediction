# -*- coding: utf-8 -*-
"""Loan_predict.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1me5lZBKN7p-peXPmuRiKZt1vDym9kP8L
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
# %matplotlib inline
import seaborn as sns
import sklearn
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import GradientBoostingClassifier,RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import RandomizedSearchCV
import imblearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score,classification_report,confusion_matrix,f1_score

data = pd.read_csv("/content/loan_data_set.csv")
data

data.info()

data.isnull().sum

data.drop(['Loan_ID'],axis=1,inplace=True)

from imblearn.combine import SMOTETomek

data['Gender'] = data['Gender'].fillna(data['Gender'].mode()[0])
data['Married']=data['Married'].fillna(data['Married'].mode()[0])
data['Dependents']=data['Dependents'].str.replace('+','')
data['Dependents'] = data['Dependents'].fillna(data['Dependents'].mode()[0])
data['Self_Employed'] = data['Self_Employed'].fillna(data['Self_Employed'].mode()[0])
data['LoanAmount'] = data['LoanAmount'].fillna(data['LoanAmount'].mode()[0])
data['Loan_Amount_Term'] = data['Loan_Amount_Term'].fillna(data['Loan_Amount_Term'].mode()[0])
data['Credit_History'] = data['Credit_History'].fillna(data['Credit_History'].mode()[0])

data.head()

data

from sklearn.preprocessing import LabelEncoder
#col = ['Gender','Married','Education','Self_Employed','Property_Area','Loan_Status']
col = ['Gender','Married','Education','Self_Employed','Property_Area','Loan_Status']
le=LabelEncoder()
for c in col:
  data[c]=le.fit_transform(data[c])
data.head()

from imblearn.combine import SMOTETomek
smote = SMOTETomek(random_state=90)

y = data['Loan_Status']
x = data.drop(columns=['Loan_Status'],axis=1)

x.shape

y.shape

x_bal,y_bal = smote.fit_resample(x,y)

print(y.value_counts())
print(y_bal.value_counts())

names=x_bal.columns

x_bal.head()

"""## **Milestone 3: Exploratory Data Analysis**"""

data.describe()

plt.figure(figsize=(12,5))
plt.subplot(121)
sns.distplot(data['ApplicantIncome'],color='r')
plt.subplot(122)
sns.distplot(data['Credit_History'])
plt.show()

plt.figure(figsize=(18,4))
plt.subplot(1,4,1)
sns.countplot(data['Gender'])
plt.subplot(1,4,2)
sns.countplot(data['Education'])
plt.show()

plt.figure(figsize=(20,5))
plt.subplot(131)
sns.countplot(data=data,x=data['Married'], hue=data['Gender'])
plt.subplot(132)
sns.countplot(x=data['Self_Employed'], hue=data['Education'])
plt.subplot(133)
sns.countplot(x=data['Property_Area'], hue=data['Loan_Amount_Term'])

sns.swarmplot(x=data['Gender'],y=data['ApplicantIncome'],hue = data['Loan_Status'])

"""# **Balancing DataSet**"""

sc=StandardScaler()
x_bal=sc.fit_transform(x_bal)
x_bal = pd.DataFrame(x_bal,columns=names)
x_train, x_test, y_train, y_test = train_test_split(x_bal, y_bal, test_size=0.33, random_state=42)

x_train.shape

y_train.shape

x_test.shape,y_test.shape

from pandas.core.dtypes.common import classes_and_not_datetimelike
def decisionTree(x_train, x_test, y_train, y_test):
  dt=DecisionTreeClassifier()
  dt.fit(x_train,y_train)
  ypred = dt.predict(x_test)
  print('***DecisionTreeClassifier***')
  print('Confusion matrix')
  print(confusion_matrix(y_test,ypred))
  print('Classification report')
  print(classification_report(y_test,ypred))
decisionTree(x_train, x_test, y_train, y_test)

def RandomForest(x_train, x_test,  y_train, y_test):
  rf = RandomForestClassifier()
  rf.fit(x_train,y_train)
  ypred = rf.predict(x_test)
  print('***RandomForestClassifier***')
  print('Confusion matrix')
  print(confusion_matrix(y_test,ypred))
  print('Classification report')
  print(classification_report(y_test,ypred))
RandomForest(x_train, x_test,  y_train, y_test)

def KNN(x_train, x_test, y_train, y_test):
  knn = KNeighborsClassifier()
  knn.fit(x_train,y_train)
  ypred = knn.predict(x_test)
  print('***KNeighborsClassifier***')
  print('Confusion matrix')
  print(confusion_matrix(y_test,ypred))
  print('Classification report')
  print(classification_report(y_test,ypred))
KNN(x_train, x_test, y_train, y_test)



def xgboost(x_train, x_test, y_train, y_test):
  xg = GradientBoostingClassifier()
  xg.fit(x_train,y_train)
  ypred = xg.predict(x_test)
  print('***GradientBoostingClassifier***')
  print('Confusiion matrix')
  print(confusion_matrix(y_test,ypred))
  print('Classification report')
  print(classification_report(y_test,ypred))
xgboost(x_train, x_test, y_train, y_test)

"""## **ANN**"""

# Importing the keras libraries and packages
import tensorflow
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

# Initialising the ANN
classifier = Sequential()

x_train.shape

y_train.shape

# Adding the input layer and the first hidden layer
classifier.add(Dense(units=100,activation='relu',input_dim=11))
# Adding the second hidden layer
classifier.add(Dense(units=50,activation='relu'))
#Adding the output layer
classifier.add(Dense(units=1,activation='sigmoid'))
# Compiling the ANN
classifier.compile(optimizer='adam' , loss='binary_crossentropy', metrics=['accuracy'])

# Fitting the ANN to the Training set
model_history = classifier.fit(x_train, y_train, batch_size=100, validation_split=0.2, epochs=100)

y_pred=classifier.predict(x_test)

y_pred=y_pred.astype(int)
y_pred

print(accuracy_score(y_pred,y_test))
print('***ANN Model***')
print('Confusiion matrix')
print(confusion_matrix(y_test,y_pred))
print('Classification report')
print(classification_report(y_test,y_pred))

"""# **Hyper Parameter Tuning**"""

rf=RandomForestClassifier()
parameters={'n_estimators':[1,20,30,55,68,74,90,120,115],
            'criterion':['gini','entropy'],
            'max_features':['auto','sqrt','log2'],
            'max_depth':[2,5,8,10],
            'verbose':[1,2,3,4,6,8,9,10]}

rcv=RandomizedSearchCV(estimator=rf,param_distributions=parameters,cv=10,n_iter=4)

rcv.fit(x_train,y_train)

bt_params=rcv.best_params_
bt_score=rcv.best_score_

bt_params

bt_score

def RandomForest(x_train, x_test,  y_train, y_test):
  rfmodel = RandomForestClassifier(verbose=9, n_estimators=120,max_features='log2',max_depth=8,criterion='entropy')
  rfmodel.fit(x_train,y_train)
  rf_pred = rfmodel.predict(x_train)
  print("Training Accuracy")
  print(accuracy_score(rf_pred,y_train))
  ypred = rfmodel.predict(x_test)
  print("Testing Accuracy")
  print(accuracy_score(ypred,y_test))
  pickle.dump(rfmodel,open('rdf.pkl','wb'))

RandomForest(x_train, x_test,  y_train, y_test)

y_pred = classifier.predict(x_test)
y_pred

def predict_exit(sample_value):
  # Convert list to numpy array
    sample_value = np.array(sample_value)
  # Reshape because sample_value contains only 1 record
    sample_value = sample_value.reshape(1,-1)
  # Feature Scaling
    sample_value = sc.transform(sample_value)
    return calssifier.predict(sample_value)

def comparemodel(x_train,x_test,y_train,y_test):
  print("Decision Tree Model")
  decisionTree(x_train,x_test,y_train,y_test)
  print('-'*100)
  print("Random Forest Model")
  RandomForest(x_train,x_test,y_train,y_test)
  print('-'*100)
  print("XGBoost Model")
  xgboost(x_train,x_test,y_train,y_test)
  print('-'*100)
  print("KNN Model")
  KNN(x_train,x_test,y_train,y_test)
  print('-'*100)
comparemodel(x_train,x_test,y_train,y_test)

ypred = classifier.predict(x_test)
print(accuracy_score(y_pred,y_test))
print("ANN model")
print("Confusion_Matrix")
print(confusion_matrix(y_test,y_pred))
print("Classification Report")
print(classification_report(y_test,y_pred))

classifier.save("loan.h5")