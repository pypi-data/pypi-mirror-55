import numpy as np
import sys


class BatchGradientDescent(object):
    def __init__(self, lr=0.01, epochs=1000, tol=0.0000001):
        self.lr = lr
        self.epochs = epochs
        self.tol = tol
        self.beta = 0
        self.cost_list = [0]

    def fit(self, X, y):
        # 增加截距项

        sample_size = X.shape[0]
        X_iter = np.concatenate([np.ones((sample_size, 1)), X], axis=1)
        self.beta = np.ones(X_iter.shape[1]).reshape((-1, 1))
        tmp = 0

        while tmp < self.epochs:
            cost = 1 / (2 * sample_size) * np.dot((X_iter.dot(self.beta) - y).T, X_iter.dot(self.beta) - y)
            print("iter:", tmp, " cost: ", cost, "\n")
            if np.abs(self.cost_list[-1] - cost) < self.tol:
                break
            else:
                self.cost_list.append(cost)
                self.beta = self.beta - self.lr * 1 / sample_size * np.dot(X_iter.T, X_iter.dot(self.beta) - y)
            tmp += 1
        return self


class StochasticGradientDescent(object):
    """
    随机梯度下降比较适合做在线学习，批量梯度下降由于一次性加入所有的样本，
    不适合做在线学习,随机梯度下降由于对于每一个样本都进行一次更新，导致并不是每次迭代都是使得cost函数减少，
    因此，需要将学习率调整的比较低，这样不至于使单个样本影响全局，但是这就导致了学习速度非常慢。这里需要注意每次迭代，
    都需要将所有的样本shuffle，目的是为了得到梯度的无偏估计，
    https://www.quora.com/Why-do-we-need-to-shuffle-inputs-for-stochastic-gradient-descent
    """
    def __init__(self, lr=0.01, epochs=200, tol=1e-6):
        self.lr = lr
        self.epochs = epochs
        self.tol = tol
        self.cost_list = [-sys.float_info.max]
        self.beta = 0
        self.sample_size = 0
        self.nvar = 0

    def fit(self, X, y):
        # 添加截距项
        self.sample_size = X.shape[0]
        X_new = np.concatenate([np.ones((self.sample_size, 1)), X], axis=1)
        self.nvar = X_new.shape[1]
        self.beta = np.zeros(self.nvar).reshape((-1, 1))
        iter = 0
        while iter < self.epochs:
            iter += 1
            errors = []
            for x_i, y_i in zip(X_new, y):
                x_i = np.array(x_i).reshape((1, -1))
                y_i = np.array(y_i).reshape((1, 1))
                error_i = np.dot((x_i.dot(self.beta) - y_i).T, x_i.dot(self.beta) - y_i)
                errors.append(error_i)
                gradient = np.dot(x_i.T, (x_i.dot(self.beta) - y_i))
                self.beta = self.beta - self.lr * gradient
            cost = 1 / 2 * np.mean(errors)
            if np.abs(cost - self.cost_list[-1]) < self.tol:
                self.cost_list.append(cost)
                break
            self.cost_list.append(cost)
            print("iter: ", iter, " cost: ", self.cost_list[-1])
            X_new, y = self.shuffle(X_new, y)
        return self

    def shuffle(self, X, y):
        permu_index = np.random.permutation(self.sample_size)
        X, y = X[permu_index, :], y[permu_index, :]
        return (X, y)


class MiniBatchGradientDescent(object):
    """
       从BatchGradientDescent和StochasticGradientDescent两个算法来看，可以发现BatchGradientDescent收敛速度是比较快的，
       但是不适用于在线学习，而StochasticGraientDescent收敛速度比较慢，需要使用极小的学习率，MiniBatchGradientDescent
       就是针对两个算法的缺陷进行改进的。
    """
    def __init__(self, lr=0.001, epochs=100, tol=1e-6, batch_size=10):
        self.lr = lr
        self.epochs = epochs
        self.tol = tol
        self.batch_size = batch_size
        self.beta = []
        self.cost_list = [-sys.float_info.max]
        self.sample_size = 0
        self.col_size = 0

    def fit(self, X, y):
        self.sample_size = X.shape[0]
        # 添加截距项
        X_new = np.concatenate([np.ones((self.sample_size, 1)), X], axis=1)
        self.col_size = X_new.shape[1]
        self.beta = np.zeros((self.col_size, 1))
        iter = 0
        while iter < self.epochs:
            iter += 1
            errors = []
            for i in np.arange(np.ceil(self.sample_size / self.batch_size), dtype=np.int64):
                X_i = X_new[i * self.batch_size:(i + 1) * self.batch_size, :]
                y_i = y[i * self.batch_size:(i + 1) * self.batch_size, :]
                errors.append(
                    1 / (2 * self.batch_size) * np.dot((X_i.dot(self.beta) - y_i).T, X_i.dot(self.beta) - y_i))
                gradient = 1 / (self.batch_size) * np.dot(X_i.T, X_i.dot(self.beta) - y_i)
                self.beta -= self.lr * gradient
            cost = np.mean(errors)
            cost_before = self.cost_list[-1]
            self.cost_list.append(cost)
            print("iter: ", iter, " cost: ", self.cost_list[-1])
            if np.abs(cost - cost_before) < self.tol:
                break
            X_new, y = self.__shuffle(X_new, y)

        return self

    def __shuffle(self, X, y):
        new_index = np.random.permutation(self.sample_size)
        X, y = X[new_index, :], y[new_index, :]
        return (X, y)


class MomentumGradientDescent(object):
    """
        针对minibatchGradientDescent问题，梯度改变方向和大小只受到当前参数值影响，
    但是每个batch由于随机性的影响，m对梯度的估计是有偏的，下降方向会波动较大，因此引入了
    动量的概念，梯度的改变量受到之前梯度的累计影响。实验结果显示： 需要精细的调整动量参数，
    不然获取的效果优势并没有MiniBatchGradientDescent好
    """
    def __init__(self,lr=0.001,epochs=200,tol=1e-10,parm_moment=0.9,batch_size=10):
        self.lr = lr
        self.epochs = epochs
        self.tol = tol
        self.parm_moment =parm_moment
        self.batch_size = batch_size
        self.beta = []
        self.cost_list = [-sys.float_info.max]
        self.sample_size = 0
        self.col_size = 0
    def fit(self,X,y):
        #增加截距项
        self.sample_size = X.shape[0]
        X_new = np.concatenate([np.ones((self.sample_size,1)),X],axis=1)
        self.col_size = X_new.shape[1]
        self.beta = np.zeros((self.col_size,1))
        iter = 0
        velocity = 0
        while iter<self.epochs:
            iter+=1
            errors =[]
            for i in np.arange(0,self.sample_size,self.batch_size,dtype=np.int64):
                X_i = X_new[i:(i+self.batch_size),:]
                y_i = y[i:(i+self.batch_size),:]
                errors.append(1/(2*self.batch_size)*np.dot((X_i.dot(self.beta)-y_i).T,X_i.dot(self.beta)-y_i))
                gradient = 1/self.batch_size*np.dot(X_i.T,X_i.dot(self.beta)-y_i)
                velocity = self.parm_moment*velocity  +self.lr*gradient
                self.beta += -velocity
            cost = np.mean(errors)
            cost_before = self.cost_list[-1]
            self.cost_list.append(cost)
            print("iter: ", iter,"cost: ",self.cost_list[-1])
            if(np.abs(cost-cost_before)<self.tol):
                print(np.abs(cost-cost_before),cost,cost_before)
                break
            X_new,y = self.shuffle(X_new,y)
        return self

    def shuffle(self,X,y):
        index_new = np.random.permutation(self.sample_size)
        return (X[index_new,:],y[index_new,:])


class AdaGrad(object):
    """
       MiniBatchGradientDescent和StochasticGradientDescent的共同问题就是对梯度的估计是有偏的，因此学习率不能过大，
       这样会导致最终的收敛的最小值偏离真实的最小值很多，但是如果学习率过低的，学习过程又会很慢，因此便有了针对学习率
       的自适应算法的诞生，AdaGrad就是其中的一种，使用梯度的二阶矩来对学习率进行控制。
    """
    def __init__(self,lr=0.001,epochs=200,tol=1e-6,batch_size=20):
        self.lr = lr
        self.epochs = epochs
        self.tol = tol
        self.beta = 0
        self.batch_size = batch_size
        self.cost_list = [-sys.float_info.max]
        self.sample_size = 0
        self.col_size = 0
    def fit(self,X,y):
        #添加截距项
        self.sample_size = X.shape[0]
        X_new = np.concatenate([np.ones((self.sample_size,1)),X],axis=1)
        self.col_size = X_new.shape[1]
        self.beta = np.zeros((self.col_size,1))
        iter = 0
        gradient_cum = 1e-6
        while iter < self.epochs:
            iter+=1
            batch_cost = []
            for i in np.arange(0,self.sample_size,self.batch_size):
                X_i = X_new[i:(i+self.batch_size),]
                y_i = y[i:(i+self.batch_size),]
                error = X_i.dot(self.beta)-y_i
                batch_cost.append(1/(2*self.batch_size)*np.dot(error.T,error))
                gradient = 1/self.batch_size*np.dot(X_i.T,error)
                gradient_cum += gradient**2
                self.beta -= self.lr/np.sqrt(gradient_cum)*gradient
            cost_before = self.cost_list[-1]
            self.cost_list.append(np.mean(batch_cost))
            print("iter:",iter," cost: ",self.cost_list[-1])
            if np.abs(self.cost_list[-1]-cost_before) < self.tol:
                break
        return self


class RMSProp(object):
    """
    针对AdaGrad中学习率的衰减策略，RMSProp进行了改进，采用了指数加权滑动平均，也就是距离当前越近的梯度对学习率的
    影响更深。实验结果表明，RMSProp可以更快的收敛，衰减系数为0表示对历史梯度完全衰减，衰减系数为1表示不衰减，适度
    调整衰减系数，相对于AdaProp可以加快收敛速度。
    """
    def __init__(self,lr=0.01,epochs=200,tol=1e-6,batch_size=20,attenuation=0.01):
        self.lr = lr
        self.epochs = epochs
        self.tol = tol
        self.attenuation = attenuation
        self.beta = 0
        self.batch_size = batch_size
        self.cost_list = [-sys.float_info.max]
    def fit(self,X,y):
        sample_size = X.shape[0]
        X_new = np.concatenate([np.ones((sample_size,1)),X],axis=1)
        col_size = X_new.shape[1]
        self.beta = np.zeros((col_size,1))
        gradient_cum = 1e-6
        iter = 0
        while iter<self.epochs:
            iter+=1
            batch_cost = []
            for i in np.arange(0,sample_size,self.batch_size):
                X_i = X_new[i:(i+self.batch_size),:]
                y_i = y[i:(i+self.batch_size),:]
                error = np.dot(X_i,self.beta)-y_i
                batch_cost.append(1/(2*self.batch_size)*np.dot(error.T,error))
                gradient = 1/self.batch_size*np.dot(X_i.T,error)
                gradient_cum = self.attenuation*gradient_cum+(1-self.attenuation)*(gradient**2)
                self.beta -= self.lr/np.sqrt(gradient_cum)*gradient
            cost_before = self.cost_list[-1]
            self.cost_list.append(np.mean(batch_cost))
            print("iter: ",iter," cost: ",self.cost_list[-1])
            if np.abs(cost_before-self.cost_list[-1]) < self.tol:
                break
        return self

