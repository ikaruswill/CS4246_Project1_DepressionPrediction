from math import sqrt, isnan
from sklearn import gaussian_process as gp
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
#from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
#from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis
from sklearn.metrics import mean_squared_error
#from sklearn.model_selection import cross_val_score#, ShuffleSplit
from skfeature.function.statistical_based import CFS
from skfeature.function.information_theoretical_based import CIFE
from skfeature.function.similarity_based import reliefF
from inputs import read_train_dev_files_with_binary
from plotting import plot_bar, plot_all_Y, plot_f1
import numpy as np
import sys
from ARD_kernel import ard_kernel
import GPy.kern as kern
import GPy.models as models
import time
from math import sqrt,ceil
import GPy
import GPyOpt
import matplotlib.mlab as mlab
import math
import matplotlib.pyplot as plt

x_train_file_name = "data/splitted/X/urop/trainX.txt"
x_dev_file_name = "data/splitted/X/urop/devX.txt"
y_train_file_name = "data/splitted/y/trainY.txt"
y_dev_file_name = "data/splitted/y/devY.txt"

y_bin_train_file_name = "data/splitted/bin_Y/trainY.txt"
y_bin_dev_file_name = "data/splitted/bin_Y/devY.txt"

if len(sys.argv) == 5:
    x_train_file_name = sys.argv[1]
    x_dev_file_name = sys.argv[2]
    y_train_file_name = sys.argv[3]
    y_dev_file_name = sys.argv[4]
elif len(sys.argv) == 3:
    x_train_file_name = sys.argv[1]
    x_dev_file_name = sys.argv[2]

X_train, y_train, X_dev, y_dev, y_bin_train, y_bin_dev = read_train_dev_files_with_binary(x_train_file_name, x_dev_file_name, y_train_file_name, y_dev_file_name, y_bin_train_file_name, y_bin_dev_file_name)
n_feats = len(X_train[0])

# We perform feature selection first
numFeatsFn = lambda n: int(ceil(sqrt(n_feats)))
def reliefPostProc(X, y):
    scores = reliefF.reliefF(X,y)
    indexes = range(0, len(scores))
    pairedScores = zip(scores, indexes)
    pairedScores = sorted(pairedScores, reverse=True)
    return np.array([ eaPair[1] for eaPair in pairedScores][:numFeatsFn(n_feats)])

def baselineProc(X,y):
    return range(0,n_feats)

def ml(X, y):
    ml = gp.GaussianProcessRegressor(kernel=gp.kernels.Matern(nu=0.5))
    #scores = cross_val_score(ml, X, y, cv=5, n_jobs=-1, scoring='mean_squared_error') #problem
    scores = 0
    return sqrt(-1*np.mean(scores))

def convertToBitVec(featSel):
    def wrapper(X, y):
        feats = featSel(X,y)
        bitVec = [False] * n_feats
        for eaF in feats:
            bitVec[eaF] = True
        bitVec = np.array(bitVec)
        return len(feats),bitVec
    return wrapper

mfccIntVec = [1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

def returnMask(intVec):
    def wrapper(X,y):
        mask = intVec
        mask = np.array(mask).astype('bool')
        return np.sum(mask),mask
    return wrapper

# CIFE: index of selected features, F[1] is the most important feature
# CFS: index of selected features
# RELIEF: index of selected features, F[1] is the most important feature
featSelectionFns = {
    "All": convertToBitVec(baselineProc),
    "Relief": convertToBitVec(reliefPostProc),
    "CIFE": convertToBitVec(CIFE.cife),
    "CFS": convertToBitVec(CFS.cfs),
    "MFCC": returnMask(mfccIntVec)
}
timeTaken = []
bitVecs = {}

print 'ok1'

for featSelName, featSel in featSelectionFns.iteritems():
    start = time.clock()    
    numFeats,bitVec = featSel(X_train,y_train)
    timeTaken = time.clock() - start
    score = ml(X_train[:,bitVec], y_train) #problem
    bitVecs[featSelName] = bitVec
    print(featSelName+ "," + str(numFeats) + ": " + str(score) + " in "+ str(timeTaken) + "seconds")


class RBF_ARD_WRAPPER:
    def __init__(self, kernel_ardIn):
        self.kernel_ard = kernel_ardIn
    def fit(self, X_trainIn, y_trainIn):
        y_train_l = y_trainIn.reshape((y_trainIn.shape[0], 1))
        self.m = models.GPRegression(X_trainIn, y_train_l, self.kernel_ard)
        self.m.constrain_positive('')
        self.m.optimize_restarts(num_restarts=10)
        self.m.randomize()
        self.m.optimize()
    def predict(self, X):
        return self.m.predict(X)[0]
        
def trainModels(regressors, models_rmse): 
    for name, featSelectionMode, model in regressors:
        modes = featSelectionMode
        if featSelectionMode==None:
            modes = featSelectionFns.keys()
        rmses = []
        for eaMode in modes:
            bitVec = bitVecs[eaMode]
            model.fit(X_train[:,bitVec], y_train[:])
            rmse_train = sqrt(mean_squared_error(y_train, model.predict(X_train[:,bitVec])))
            rmse_predict = sqrt(mean_squared_error(y_dev, model.predict(X_dev[:,bitVec])))
            rmses.append([name + '('+eaMode+')', rmse_train, rmse_predict])
            print(name + '('+eaMode+')')
            print("\tT:" + str(rmse_train)+"\n\tP:"+str(rmse_predict))
        rmses=sorted(rmses, key=lambda l: l[2])
        models_rmse.append(rmses[0])
    return models_rmse
  
def getClassifieresPerformances(classifiers, models_f1, models_performances): 
    for name, featSelectionMode, model in classifiers:
        modes = featSelectionMode
        if featSelectionMode==None:
            modes = featSelectionFns.keys()
        f1s = []
        performances = []
        for eaMode in modes:
            bitVec = bitVecs[eaMode]
            f1, performance = getClassifierPerformance(model, name, eaMode, X_train[:,bitVec], y_bin_train, X_dev[:,bitVec])
            f1s.append(f1)
            performances.append(performance)
        f1s=sorted(f1s, key=lambda l: l[1], reverse=True)
        performances=sorted(performances, key=lambda l: l[1], reverse=True)
        models_f1.append(f1s[0])
        models_performances.append(performances[0])
    return models_f1, models_performances
    
def getClassifieresPerformancesByDefinedX(classifiers, eaMode, models_f1, models_performances, X, Y, Xstar): 
    for name, featSelectionMode, model in classifiers:
        f1, performance = getClassifierPerformance(model, name, eaMode, X, Y, Xstar)
        models_f1.append(f1)
        models_performances.append(performance)
    return models_f1, models_performances
    
def getClassifierPerformance(model, name, eaMode, X, Y, X_star):
    model.fit(X, Y)
    #pt_f1, pt_precision, pt_recall, pt_accuracy = classifyForF1(model, X, 1)
    pp_f1, pp_precision, pp_recall, pp_accuracy = classifyForF1(model, X_star, 1)
    #nt_f1, nt_precision, nt_recall, nt_accuracy = classifyForF1(model, X, 0)
    np_f1, np_precision, np_recall, np_accuracy = classifyForF1(model, X_star, 0)
    f1 = [name + '(' + eaMode + ')', pp_f1, np_f1]
    performance = [name + '(' + eaMode + ')', pp_f1, pp_precision, pp_recall, pp_accuracy, np_f1, np_precision, np_recall, np_accuracy]
    return f1, performance

def classifyForF1(classifier, X, positive_bit):
    #depressionClassifer = gp.GaussianProcessClassifier(kernel=gp.kernels.DotProduct())
    #classifier.fit(newTrainX, y_bin_train)
    classifiedResult = classifier.predict(X)
    #classifiedResultProba = classifier.predict_proba(newDevX)
    #print classifiedResult
    #print classifiedResultProba

    #define 1 as +ve 0 as negative
    tp = 0.0
    fp = 0.0
    tn = 0.0
    fn = 0.0

    for i in range(len(y_bin_dev)):
        actual = y_bin_dev[i]
        predicted = classifiedResult[i]
        
        if actual == positive_bit and predicted == actual:
            tp = tp + 1.0
        elif actual == positive_bit and predicted != actual:
            fp = fp + 1.0
        elif actual == 1 - positive_bit and predicted == actual:
            tn = tn + 1.0
        elif actual == 1 - positive_bit and predicted != actual:
            fn = fn + 1.0
        else:
            print 'got bug'
      

    f1 = -0.01
    precision = -0.01
    recall = -0.01
    accuracy = -0.01
      
      
    if (tp + fp) != 0:
        precision = tp / (tp + fp)
    
    if len(y_bin_dev) != 0:
        accuracy = (tp + tn) / len(y_bin_dev)
    
    if (tp + fn) != 0:
        recall = tp / (tp + fn)
    
    if tp != 0 and precision > 0 and recall > 0:
        f1 = 2 * precision * recall / (precision + recall)

    #print 'precision:' + str(precision)
    #print 'recall:' + str(recall)
    #print 'accuracy:' + str(accuracy)
    #print 'f1:' + str(f1)
    return f1, precision, recall, accuracy
    
def addRelatedWork(models_f1, models_performances):
    f1 = ['DepAudioNet', 0.52, 0.70]
    performance = ['DepAudioNet', 0.52, 0.35, 1.00, '-', 0.70, 1.00, 0.54, '-']
    models_f1.append(f1)
    models_performances.append(performance)
    return models_f1, models_performances
    
def printPerformances(models_performances):
    for performance in models_performances:
        name = performance[0]
        pp_f1 = performance[1]
        pp_precision = performance[2]
        pp_recall = performance[3]
        pp_accuracy = performance[4]
        np_f1 = performance[5]
        np_precision = performance[6]
        np_recall = performance[7]
        np_accuracy = performance[8]
        print name
        print ('\tF1: ' + str(pp_f1) + '(' + str(np_f1) + 
        '),Precision: ' + str(pp_precision) + '(' + str(np_precision) + 
        '),Recall: ' + str(pp_recall) + '(' + str(np_recall) + 
        '),Accuracy: '  + str(pp_accuracy) + '(' + str(np_accuracy) + ')') 
        
def findProbabilityDistribution(expectedResults, actualResults, actualResultsProba):
    depression_right_predictions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    depression_wrong_predictions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    normal_right_predictions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    normal_wrong_predictions = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if len(expectedResults) != len(actualResults):
        print 'error'
        sys.exit(-1)
    
    for i in range(len(expectedResults)):
        predicted = actualResults[i]
        actual = expectedResults[i]
        
        if predicted != actual:
            print "audio" + str(i) + ": False, predicted: " + str(predicted) + " but expected: " + str(actual) + " with confidence of " + str(actualResultsProba[i][1])
        
        normalIndex = 11
        depressionIndex = 11
        if isnan(actualResultsProba[i][0]) == False:
            normalProba = actualResultsProba[i][0] * 10
            normalIndex = int(normalProba)
        #else:
            #print predicted
            #print actual == predicted
            #print actualResultsProba[i]
        
        if isnan(actualResultsProba[i][1]) == False:
            depressionProba = actualResultsProba[i][1] * 10
            depressionIndex = int(depressionProba)
        
        #print 'round ' + str(i) + ':'
        #print normalIndex
        #print depressionIndex
        #print len(depression_right_predictions)
        #print len(depression_wrong_predictions)
        #print len(normal_right_predictions)
        #print len(normal_wrong_predictions)
        if predicted == 0 and predicted == actual:
            normal_right_predictions[normalIndex] = normal_right_predictions[normalIndex] + 1
            #depression_right_predictions[depressionIndex] = depression_right_predictions[depressionIndex] + 1
        elif predicted == 0 and predicted != actual:
            normal_wrong_predictions[normalIndex] = normal_wrong_predictions[normalIndex] + 1
            #depression_wrong_predictions[depressionIndex] = depression_wrong_predictions[depressionIndex] + 1
        elif predicted == 1 and predicted == actual:
            #normal_right_predictions[normalIndex] = normal_right_predictions[normalIndex] + 1
            depression_right_predictions[depressionIndex] = depression_right_predictions[depressionIndex] + 1
        elif predicted == 1 and predicted != actual:
            #normal_wrong_predictions[normalIndex] = normal_wrong_predictions[normalIndex] + 1
            depression_wrong_predictions[depressionIndex] = depression_wrong_predictions[depressionIndex] + 1
        else:
            print 'got bug in findProbabilityDistribution'
    
    print 'Depression: '
    printProbabilityDistribution(depression_right_predictions, depression_wrong_predictions)
    
    print 'Normal: '
    printProbabilityDistribution(normal_right_predictions, normal_wrong_predictions)

def printProbabilityDistribution(rights, wrongs):
    for i in range(len(rights) - 2):
        accuracy = calculateAccuracy(rights[i], wrongs[i])
        print 'Accuracy for ' + str(i * 10) + ' ~ ' + str((i + 1) * 10) + " is: " + str(accuracy) 

    print 'Accuracy for 100% is: ' + str(calculateAccuracy(rights[10], wrongs[10]))
    
    print 'Accuracy for NAN is: ' + str(calculateAccuracy(rights[11], wrongs[11]))
    
def calculateAccuracy(right, wrong):
    accuracy = '-1(No sample)' 
    if (right + wrong) != 0:
        accuracy = str(float(right) / float(right + wrong)) + '(' + str(right) + ' out of ' + str(right + wrong) + ')'
    return accuracy
    
regressors = [("KNN", None, KNeighborsRegressor(2)),
               ("Linear SVR", None, SVR(kernel="linear")),
               ("RBF SVR", None, SVR(gamma=2, C=1)),
               ("DT", None, DecisionTreeRegressor(min_samples_split=1024, max_depth=20)),
               ("RF", None, RandomForestRegressor(n_estimators=10, min_samples_split=1024,
                                                         max_depth=20)),
               ("AB", None, AdaBoostRegressor(random_state=13370)),
               #("Naive Bayes", None, GaussianNB()),
               #("Bagging with DTRegg", ["All"], BaggingRegressor(DecisionTreeRegressor(min_samples_split=1024,
                #                                                              max_depth=20))),
               #("GP isotropic RBF", None, gp.GaussianProcessRegressor(kernel=gp.kernels.RBF())),
               #("GP anisotropic RBF", ["All"], gp.GaussianProcessRegressor(kernel=gp.kernels.RBF(length_scale=np.array([1]*n_feats)))),
               #("GP ARD", ["All"], gp.GaussianProcessRegressor(kernel=ard_kernel(sigma=1.2, length_scale=np.array([1]*n_feats)))),
               #("GP isotropic matern nu=0.5", None, gp.GaussianProcessRegressor(kernel=gp.kernels.Matern(nu=0.5))),
               #("GP isotropic matern nu=1.5", None, gp.GaussianProcessRegressor(kernel=gp.kernels.Matern(nu=1.5))),
               #("GP Isotropic Matern", None, gp.GaussianProcessRegressor(kernel=gp.kernels.Matern(nu=2.5))),
# bad performance
               ("GP-DP", ["MFCC","All","CIFE","CFS"], gp.GaussianProcessRegressor(kernel=gp.kernels.DotProduct())),
               # output the confidence level and the predictive variance for the dot product (the only one that we keep in the end)
               # GP beats SVM in our experiment (qualitative advantages)
               # only keep RBF, dot product and matern on the chart
               # add a paragraph 'Processed Data'
               #1) generate the dataset with 526 features
               #2) the predictive variance and predictive mean (best and worst) of some vectors from the dot product.

#  3-th leading minor not positive definite
#    ("GP exp sine squared", gp.GaussianProcessRegressor(kernel=gp.kernels.ExpSineSquared())),
               #("GP rational quadratic", None, gp.GaussianProcessRegressor(kernel=gp.kernels.RationalQuadratic())),
               #("GP white kernel", None, gp.GaussianProcessRegressor(kernel=gp.kernels.WhiteKernel())),
               #("GP abs_exp", None, gp.GaussianProcess(corr='absolute_exponential')),
               #("GP squared_exp", ["All"], gp.GaussianProcess(corr='squared_exponential')),
               #("GP cubic", None, gp.GaussianProcess(corr='cubic')),
               #("GP linear", None, gp.GaussianProcess(corr='linear')),
               #("GP RBF ARD", ["All"], RBF_ARD_WRAPPER(kern.RBF(input_dim=n_feats, variance=1., lengthscale=np.array([1]*n_feats), ARD=True)))]
               
]

#models_rmse = []
#models_rmse = trainModels(regressors, models_rmse)

# Give some general prior distributions for model parameters
# m.kern.lengthscale.set_prior(GPy.priors.Gamma.from_EV(1.,10.))
# m.kern.variance.set_prior(GPy.priors.Gamma.from_EV(1.,10.))
# m.likelihood.variance.set_prior(GPy.priors.Gamma.from_EV(1.,10.))
# _=m.plot()

#print("AverageRacialEnsemble(MFCC)")
#print("\tT:" + str(rmse_train)+"\n\tP:"+str(rmse_predict))
#plot_bar(models_rmse)
#plot_all_Y()

depressionClassifer = gp.GaussianProcessClassifier(kernel=gp.kernels.DotProduct())

mode = "MFCC"
bitVec = bitVecs[mode]
depressionClassifer.fit(X_train[:,bitVec], y_bin_train)

print 'development:'
classifiedResult = depressionClassifer.predict(X_dev[:,bitVec])
classifiedResultProba = depressionClassifer.predict_proba(X_dev[:,bitVec])
findProbabilityDistribution(y_bin_dev, classifiedResult, classifiedResultProba)

print 'training:'
classifiedResult = depressionClassifer.predict(X_train[:,bitVec])
classifiedResultProba = depressionClassifer.predict_proba(X_train[:,bitVec])
findProbabilityDistribution(y_bin_train, classifiedResult, classifiedResultProba)