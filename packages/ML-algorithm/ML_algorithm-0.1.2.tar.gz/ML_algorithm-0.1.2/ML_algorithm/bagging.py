from sklearn.utils import resample
from .tree import TreeRegressor
import numpy as np
import sys


class RandomForestRegressor(object):

    def __init__(self, n_trees, trees=[], max_depth=10, gamma=sys.float_info.max, min_split_sample=10):
        self.n_trees = n_trees
        self.max_depth = max_depth
        self.min_split_sample = min_split_sample
        self.gamma = gamma
        self.trees = trees

    def fit(self, X_train, y_train):
        for i in np.arange(0, self.n_trees, 1):
            tree = TreeRegressor(max_depth=self.max_depth, gamma=self.gamma, min_split_sample=self.min_split_sample)
            all_col = X_train.columns.values
            total_sample = len(X_train)
            bootstrap_col = list(set(resample(all_col, replace=True, n_samples=len(all_col))))
            bootstrap_index = list(set(resample(np.arange(0, total_sample, 1), replace=True, n_samples=total_sample)))
            tree.fit(X_train.iloc[bootstrap_index, :], y_train[bootstrap_index])
            self.trees.append(tree)
        return self

    def predict(self, X_test):
        pred_arr = []
        for i in self.trees:
            pred_arr.append(i.predict(X_test))
        return np.mean(pred_arr, axis=0)