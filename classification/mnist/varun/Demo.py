from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
import numpy as np
import scipy.sparse

import matplotlib.pyplot as plt
# import seaborn as sns
# from sklearn import metrics
# from sklearn.linear_model import LogisticRegression
import math
import sys
from sklearn.preprocessing.label import LabelBinarizer

def softmax(z):
    z -= np.max(z)
    sm = (np.exp(z).T / np.sum(np.exp(z), axis=1)).T
    return sm


def getLoss(w, x, y, lam):
    m = x.shape[0]  # First we get the number of training examples
    #y_mat = oneHotIt(y) #Next we convert the integer class coding into a one-hot representation
    lb = LabelBinarizer()
    y_mat = lb.fit_transform(y)
    scores = np.dot(x, w)  # Then we compute raw class scores given our input and current weights
    prob = softmax(scores)  # Next we perform a softmax on these scores to get their probabilities
    loss = (-1 / m) * np.sum(y_mat * np.log(prob)) + (lam / 2) * np.sum(w * w)  # We then find the loss of the probabilities
    grad = (-1 / m) * np.dot(x.T, (y_mat - prob)) + lam * w  # And compute the gradient for that loss
    return loss, grad

def getProbsAndPreds(someX, weights):
    probs = softmax(np.dot(someX,weights))
    preds = np.argmax(probs,axis=1)
    return probs,preds

def getAccuracy(someX,someY, weights):
    prob,prede = getProbsAndPreds(someX, weights)
    someY = someY.flatten()
    accuracy = sum(prede == someY)/(float(len(someY)))
    return accuracy


'''
Compute the stochastic gradient descent based weight vector.
 
'''
def SGD_sol(learning_rate, minibatch_size, num_epochs, L2_lambda, input_training,
            output_training):
    N, _ = input_training.shape
    # You can try different mini-batch size size
    # Using minibatch_size = N is equivalent to standard gradient descent
    # Using minibatch_size = 1 is equivalent to stochastic gradient descent
    # In this case, minibatch_size = N is better
    #weights = np.zeros([1, input_training.shape[1]])
    weights = np.zeros([input_training.shape[1],len(np.unique(output_training))])
        
    # We are using early stopping as a regularization technique
    for epoch in range(1, num_epochs + 1):
        losses = []
        for i in range(int(N / minibatch_size)):
            lower_bound = int(i * minibatch_size)
            upper_bound = int(min((i + 1) * minibatch_size, N))
            Phi = input_training[lower_bound : upper_bound, :]
            t = output_training[lower_bound : upper_bound, :]
            loss, grad = getLoss(weights, Phi, t, L2_lambda)
            losses.append(loss)
            weights = weights - (learning_rate * grad)
                            
    return weights

    
# starter
digits = load_digits()

print(digits.data.shape)
print(digits.target.shape)
digits.target = digits.target.reshape([-1, 1])
# split in training and test data
x_train, x_test, y_train, y_test = train_test_split(digits.data, digits.target, test_size=0.25)

print(x_train.shape)
print(y_train.shape)
print(x_test.shape)
print(y_test.shape)

# t is a vector which is all 0 except 1 where we need to predict the value


patience = 10
validation_steps = 5
L2_lambdas = [0.1, 0.01, 0.03]
num_epochs = 1000


weights = SGD_sol(1, int(len(x_train)), num_epochs, 0.001, x_train, y_train)
#print(weights)
print(getAccuracy(x_test, y_test, weights))

