import numpy as np
import pandas as pd
from sklearn import tree

from sklearn import tree
#import pydotplus
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
import matplotlib.image as pltimg


df=pd.read_csv("./Telco-Customer-Churn.csv")
df.head()


#Checking NaN values

# " "in df.values

df.duplicated().sum()

df.drop(columns='customerID', inplace=True)

# df.columns

df.replace(' ', np.nan, inplace=True)


df.isnull().sum()

df[df['TotalCharges'].isnull()]


df.dropna(inplace=True)

df.isnull().sum()


df.dtypes


# to Object
#df["SeniorCitizen"] = df["SeniorCitizen"].map({1:'Yes', 0:'No'})

# to Float
df["TotalCharges"]  = df["TotalCharges"].astype(float)





#df["customerID"] = pd.to_numeric(df.customerID, errors='coerce')

d0 = {'Female': 0, 'Male': 1}
df['gender'] = df['gender'].map(d0)

d = {'No': 0, 'Yes': 1}
#df['SeniorCitizen'] = df['SeniorCitizen'].map(d)
df['Partner'] = df['Partner'].map(d)
df['Dependents'] = df['Dependents'].map(d)
df['PhoneService'] = df['PhoneService'].map(d)
d1={'No': 0, 'Yes': 1,'No phone service':2}
df['MultipleLines'] = df['MultipleLines'].map(d1)

d2={'DSL':0, 'Fiber optic':1, 'No':3}
df['InternetService'] = df['InternetService'].map(d2)


d3={'Month-to-month':0, 'One year':1, 'Two year':2}
df['Contract'] = df['Contract'].map(d3)

df['PaperlessBilling'] = df['PaperlessBilling'].map(d)

d4={'Electronic check':0, 'Mailed check':1, 'Bank transfer (automatic)':2, 'Credit card (automatic)':3}
df['PaymentMethod'] = df['PaymentMethod'].map(d4)

d5 = {'No': 0, 'Yes': 1, 'No internet service':3}
df['OnlineSecurity'] = df['OnlineSecurity'].map(d5)
df['OnlineBackup'] = df['OnlineBackup'].map(d5)
df['DeviceProtection'] = df['DeviceProtection'].map(d5)
df['TechSupport'] = df['TechSupport'].map(d5)
df['StreamingTV'] = df['StreamingTV'].map(d5)
df['StreamingMovies'] = df['StreamingMovies'].map(d5)

#df["TotalCharges"] = pd.to_numeric(df.TotalCharges, errors='coerce')


df['Churn'] = df['Churn'].map(d)







# df.dtypes



# df



#X=df.iloc[:,[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,-1]] #features
X=df.iloc[:,0:-1] #features
Y=df.iloc[:,-1] #target/class
print(X)



from sklearn.model_selection import train_test_split
X_train,X_test,Y_train,Y_test= train_test_split(X, Y, test_size=0.3, random_state=123)


from sklearn.ensemble import RandomForestClassifier
classifier=RandomForestClassifier(n_estimators=100, criterion='gini') #creating object, n_estimator(mean how many decision tree u want to create for voting)

classifier.fit(X_train, Y_train) #trainig data




classifier.score(X_test,Y_test)




classifier.predict([[1,1,1,1,20,0,1,1,0,1,1,0,0,1,1,0,1,103,1]])



ls = [1,1,1,1,20,0,1,1,0,1,1,0,0,1,1,0,1,103,1]
#Array([1]) mean yes
def pred(ls):
    print(ls)
    pred=classifier.predict([ls])

    if pred[0]==1:
        print('User may leave')
    else:
        print('User may not leave')

    res = pred[0]

    Y_pred=classifier.predict(X_test)
    print(Y_pred)



    print(classifier.score(X_test,Y_pred))
    return res


pred(ls)