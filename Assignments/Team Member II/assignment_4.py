# -*- coding: utf-8 -*-
"""Assignment 4.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/IBM-EPBL/IBM-Project-5727-1658813596/blob/d4c9a2315ba98c1052d2ce7e6840eecb25ec8a7c/Assignments/Team%20Leader/Assignment%204.ipynb
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

"""## 1. Download Dataset
## 2. Load Dataset
"""

data=pd.read_csv("Mall_Customers.csv")

"""# 3. Perform,
# ∙ Univariate Analysis
# ∙ Bi-Variate Analysis
# ∙ Multi-Variate Analysis
"""

data.head()

data.rename(columns={"CustomerID":"customer_id","Gender":"gender","Age":"age","Annual Income (k$)":"annual_income",
                     "Spending Score (1-100)":"spending_scores"},inplace=True)

temp = pd.concat([data['age'], data['gender']], axis=1)

f, ax = plt.subplots(figsize=(10,10))
fig = sns.boxenplot(x='gender', y="age", data=data)
fig.axis(ymin=0, ymax=100);

"""There is no difference in age of rings for male and female (18-70).

**Count plot**
"""

# Count Plot
sns.boxplot(x=data['gender'],y=data['spending_scores'])

sns.boxplot(x=data['gender'],y=data['annual_income'])

# Correlation Plot
corr=data.corr()
plt.figure(figsize=(8,8))
sn=sns.heatmap(corr,vmin=-1,center=0, annot = True, cmap = 'mako')

sns.pairplot(data)

"""# 4. Descriptive statistics

"""

data.head(10)

data.shape

data.describe()

data.info()

"""## 5. Missing values

"""

data[data.duplicated()]

data.isna().sum()

"""### there is no missing values and duplicates in dataframe

# 6. Outliers
"""

for i in data:
    if data[i].dtype=='int64':
        q1=data[i].quantile(0.25)
        q3=data[i].quantile(0.75)
        iqr=q3-q1
        upper=q3+1.5*iqr
        lower=q1-1.5*iqr
        data[i]=np.where(data[i] >upper, upper, data[i])
        data[i]=np.where(data[i] <lower, lower, data[i])

"""***After removing outliers, boxplot will be like***"""

plt.boxplot(data['age'])

plt.boxplot(data['annual_income'])

plt.boxplot(data['spending_scores'])

"""# 7. Categorical columns check and Encoding."""

from sklearn.preprocessing import LabelEncoder
encoder=LabelEncoder()
data['gender']=encoder.fit_transform(data['gender'])

data.head()

"""# 8. Scaling the data"""

from sklearn.preprocessing import StandardScaler
df=StandardScaler()
data1=df.fit_transform(data)

"""# 9. Clustering"""

from sklearn.cluster import KMeans

data.drop('customer_id',axis=1,inplace=True)

km = KMeans(n_clusters=3, random_state=0)

data['Group or Cluster'] = km.fit_predict(data)

data.head()

data['Group or Cluster'].value_counts()

import matplotlib.pyplot as plt

fig,ax = plt.subplots(figsize=(15,8))
sns.scatterplot(x=data['annual_income'],
                y=data['spending_scores'],
                hue=data['Group or Cluster']
                )
plt.show()

from sklearn.metrics import silhouette_score, silhouette_samples
score = silhouette_score(data, 
                         km.labels_, 
                         metric='euclidean')
score

import matplotlib.pyplot as plt
from yellowbrick.cluster import SilhouetteVisualizer

fig, ax = plt.subplots(2, 2, figsize=(20,20))
for i in [2, 3, 4, 5]:
    km = KMeans(n_clusters=i, init='k-means++', n_init=10, max_iter=100, random_state=0)
    q, mod = divmod(i, 2)
    visualizer = SilhouetteVisualizer(km, colors='yellowbrick', ax=ax[q-1][mod])
    visualizer.fit(data)