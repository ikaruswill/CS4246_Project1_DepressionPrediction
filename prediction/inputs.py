import csv
import sys
import warnings

def getX(fileName):
    X = []
    with open(fileName, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        X = [ [ float(eaVal) for eaVal in row] for row in reader]
        # safety to check every row
        n_feats = len(X[0])
        for x in X:
            if n_feats != len(x):
                print('Warning, some x has different number of features!!')
                sys.exit(1)
    return X, n_feats, len(X)

def getY(filename):
    y = []
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        y = [ int(row[0]) for row in reader ]
    return y, len(y)

def read_train_dev_files(trainx, devx, trainy, devy):
    warnings.filterwarnings("ignore")

    X_train, n_feats_train, k_x_train = getX(trainx)
    X_dev, n_feats_dev, k_x_dev = getX(devx)
    y_train, k_y_train = getY(trainy)
    y_dev, k_y_dev = getY(devy)

    # some sanity checks on n_feats
    if n_feats_train != n_feats_dev:
        print('Error n_feats in train and dev. They are not equal.')
        sys.exit(1)
    n_feats = n_feats_train

    # sanity checks for k_train
    if k_x_train != k_y_train:
        print('Error, train is of different size')
        sys.exit(1)
    k_train = k_x_train
    if k_x_dev != k_y_dev:
        print('Error, dev is of different size')
        sys.exit(1)
    k_dev = k_x_dev

    print("Data has " + str(n_feats) + " features and " + str(k_train) + " training points and " + str(k_dev) + " dev points." )
    return X_train, y_train, X_dev, y_dev