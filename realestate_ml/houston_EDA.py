from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import sklearn

houston_data = pd.read_csv('C:\\Users\\corey\\Desktop\\MachineLearning\\realestateData\\data\\houston_houses.csv')

print(houston_data.head())