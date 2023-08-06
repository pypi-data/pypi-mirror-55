import numpy as np
import sys


class TreeNode(object):
    def __init__(self, is_leaf=False, score=None, left_node=None, right_node=None, split_feature=None,
                 split_threshold=None):
        self.is_leaf = is_leaf
        self.score = score
        self.left_node = left_node
        self.right_node = right_node
        self.split_threshold = split_threshold
        self.split_feature = split_feature


class TreeRegressor(object):

    def __init__(self, estimator=None, gamma=sys.float_info.max, max_depth=1, min_split_sample=10):
        self.estimator = estimator
        self.gamma = gamma
        self.max_depth = max_depth
        self.min_split_sample = min_split_sample

    def split_strategy(self, X_train, y_train):
        col_name = X_train.columns.values
        max_minus_loss = sys.float_info.max
        print('X_train',X_train.shape)
        best_split_feature = None
        best_split_threshold = sys.float_info.max
        for i in col_name:
            unique_values = list(set(X_train[i]))
            unique_values.sort()
            if len(unique_values) > 1:
                for j in np.arange(0, len(unique_values) - 1, 1):
                    split_value = (unique_values[j] + unique_values[j + 1]) / 2
                    right_index = X_train[i] > split_value
                    right_y = y_train[right_index]
                    left_y = y_train[~right_index]
                    right_loss = np.sum(np.power(right_y - right_y.mean(), 2))
                    left_loss = np.sum(np.power(left_y - left_y.mean(), 2))
                    parent_loss = np.sum(np.power(y_train - np.mean(y_train), 2))
                    if max_minus_loss > parent_loss - left_loss - right_loss:
                        max_minus_loss = parent_loss - left_loss - right_loss
                        best_split_feature = i
                        best_split_threshold = split_value
        return (best_split_feature, best_split_threshold)

    def cal_score(self, y_train):
        return np.mean(y_train)

    def construct_tree(self, X_train, y_train, depth):
        best_split_feature, best_split_threshold = self.split_strategy(X_train, y_train)
        print(best_split_feature, best_split_threshold)
        if (best_split_threshold >= self.gamma) | (len(X_train) < self.min_split_sample) | (depth >= self.max_depth):
            return TreeNode(is_leaf=True, score=self.cal_score(y_train))
        else:
            right_index = X_train[best_split_feature] > best_split_threshold
            right_node = self.construct_tree(X_train[right_index], y_train[right_index], depth + 1)
            left_node = self.construct_tree(X_train[~right_index], y_train[~right_index], depth + 1)
            return TreeNode(left_node=left_node, right_node=right_node, split_feature=best_split_feature,
                            split_threshold=best_split_threshold)

    def fit(self, X_train, y_train):
        self.estimator = self.construct_tree(X_train, y_train, 0)

    def predict_single(self, x_test, estimator):
        if estimator.is_leaf:
            return estimator.score
        elif x_test[estimator.split_feature] > estimator.split_threshold:
            self.predict_single(x_test, estimator.right_node)
        else:
            self.predict_single(x_test, estimator.left_node)

    def predict(self, X_test):
        res = []
        for i in np.arange(0, X_test.shape[0], 1):
            res.append(self.predict_single(X_test.iloc[i, :], self.estimator))
        return res

