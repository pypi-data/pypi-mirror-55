# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License

import numpy as np

from sklearn.model_selection import KFold

from sklearn.metrics import accuracy_score
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

data = load_breast_cancer()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

lr = LogisticRegression()


class Hydra:
    def __init__(self, search_config):
        self.search_config = search_config

    def _stacking_cv(model, X_train, y_train, X_test, KFold_kwargs={}):
        kf = KFold(**KFold_kwargs)

        S_train = []
        S_test = []
        for train_idx, valid_idx in kf.split(X_train):
            X, y, X_valid = X_train[train_idx], y_train[train_idx], X_train[valid_idx]
            model.fit(X, y)

            S_train.append(model.predict(X_valid))
            S_test.append(model.predict(X_test))

        S_train = np.hstack(tuple(S_train))
        S_test = np.hstack(tuple(S_test))

        return S_train, S_test
