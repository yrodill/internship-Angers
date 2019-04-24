
import matplotlib as mpl
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

from sklearn import datasets
from sklearn.mixture import BayesianGaussianMixture
from sklearn.model_selection import StratifiedKFold



data = pd.read_csv("data/Ratio_filtered_by_exp.csv",header=0)

model = BayesianGaussianMixture(verbose=2,covariance_type='diag')
print("Fitting the data...")
matrice = model.fit(data)
print("Done...\nScoring...")
score = model.score(data)

print(matrice)
print(score)
# print("aic :",model.aic(data))
# print("bic :",model.bic(data))

res = model.predict_proba(data)
print(res)