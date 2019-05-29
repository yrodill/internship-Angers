
import matplotlib as mpl
import matplotlib.pyplot as plt

import pandas as pd
import numpy as np

from sklearn import datasets
from sklearn.mixture import BayesianGaussianMixture,GaussianMixture
from sklearn.model_selection import StratifiedKFold



data = pd.read_csv("data/Ratio_filtered_by_exp.csv",header=0)

model = BayesianGaussianMixture(covariance_type='diag',n_components=1)
print("Fitting the data...")
matrice = model.fit(data)
print("Done...\nScoring...")
score = model.score(data)

print(matrice.means_[0])
probs = model.score_samples(data)
print(probs)

p = np.exp(probs)
print(p)
# print(score)
# print(model)
# print("aic :",model.aic(data))
# print("bic :",model.bic(data))

# res = model.predict_proba(data)
