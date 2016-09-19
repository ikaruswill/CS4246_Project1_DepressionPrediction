import numpy as np
from matplotlib import pylab
import matplotlib.pyplot as plt
from collections import Counter

def plot_bar(models_rmse):
    ind = np.arange(len(models_rmse))
    width = 0.42

    fig = plt.figure()
    ax = fig.add_subplot(111)

    rmse_train, rmse_predict = zip(*models_rmse.values())
    rects_train = ax.bar(ind, rmse_train, width, color='b')
    rects_predict = ax.bar(ind+width, rmse_predict, width, color='g')

    ax.set_ylabel('Models')
    ax.set_xticks(ind+width)
    ax.set_xticklabels(models_rmse.keys())
    labels = ax.get_xticklabels()
    plt.setp(labels, rotation=30, fontsize=10)
    ax.legend((rects_train[0], rects_predict[0]), ('train', 'predict'), loc=2)
    plt.title("RMSE train and predict for the different models")

    def autolabel(rects):
        for rect in rects:
            h = rect.get_height()
            ax.text(rect.get_x()+rect.get_width()/2., 1.05*h, '%.2f'%h,
                    ha='center', va='bottom')

    autolabel(rects_train)
    autolabel(rects_predict)

    plt.show()

def plot_all_Y():
    with open("allY.txt", 'rb') as allY:
        cont = allY.readlines()
    cont = [ int(ea.strip()) for ea in cont]
    counter = Counter(cont)
    x = range(25)
    y = [ counter[k] for k in x]
    pylab.ylabel("Frequency")
    pylab.xlabel("Depression Severity [PHQ-8 Score]")
    plt.bar(x, y)
    plt.show()

