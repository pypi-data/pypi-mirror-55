import numpy as np
import sys
import warnings

class SimpleLinearRegression():
    coef=0
    def __init__(self,n_rounds,momentum,alpha,decay):
        self.n_rounds=n_rounds
        self.momentum=momentum
        self.alpha=alpha
        self.decay=decay
    def fit(self,X,y):
        n_feature=X.shape[1]
        n_sample=X.shape[0]
        y=np.array(y).reshape((n_sample,1))
        X=np.array(X)
        X_T=X.T
        beta=np.zeros(n_feature).reshape((n_feature,1))
        beta_v0=np.zeros(n_feature).reshape((n_feature,1))
        y_v0=sys.maxsize
        err=sys.maxsize
        i=0
        while i<self.n_rounds and np.abs(err)>1e-16:
            g=2*(X_T @(X @ beta-y))/n_sample
            beta_v1=-self.alpha*1.0/(1.0+self.decay*i)*g
            beta=beta+beta_v1+self.momentum*beta_v0
            beta_v0=beta_v1
            y_v1=np.sum((y-X @ beta)**2)
            err=y_v1-y_v0
            y_v0=y_v1
            i+=1
        if  np.abs(err)>1e-16:
            warnings.warn("迭代次数不够,未达到1e-16精度，请增加迭代次数")
        self.coef=beta
        return self