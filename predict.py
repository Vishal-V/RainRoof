import numpy as np
import pandas as pd
import seaborn as sns
import sklearn as sk
from sklearn.preprocessing import LabelEncoder
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor

data = pd.read_csv("./Datasets/Bengaluru Rainfall Data.csv")

data.fillna(data.mean(), inplace=True)
data.drop(data.columns[len(data.columns)-1], axis=1, inplace=True)

months = ['Jan', 'Feb', 'March', 'April', 'May', 'June', 'July', 'Aug', 'Sept', 'Oct', 'Nov', 'Dec']
mean_list = []
summed = 0.
for i in months:
    mean_list.append(np.mean(data[i]))
    summed += mean_list[-1]
print(mean_list)
print(f'The predicted rainfall is: {summed} mm')
print(f'The expected rainfall collection for 1 year for a 30x40 site: {summed/100 * 112} litres')

