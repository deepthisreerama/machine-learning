# Load libraries
import sys
from sklearn import svm
import math
from operator import itemgetter
#from time import gmtime, strftime
#from sklearn.model_selection import train_test_split


def read_data(filename):
    f = open(filename)
    X = []
    for line in f:
        X.append(line.split())
    X = [[int(x) for x in x1] for x1 in X]
    return X


def accuracy(true_labels, output_labels):
    size = len(true_labels)
    correct = 0
    for i in range(0, size):
        if true_labels[i] == output_labels[i]:
            correct += 1
    #print("correct", correct)
    return float(correct/size) * 100


def extract_features(X, cols):
    V = []
    columns = list(zip(*X))
    for j in cols:
        V.append(columns[j])
    V = list(zip(*V))
    return V


def calculate_pearson_score(X, y, top):
    rows = len(X)
    cols = len(X[0])
    data_array = []
    num = []
    r = []
    idx = 0
    y = [int(k) for k in y]
    label_mean = sum(y)/rows
    y_array = math.sqrt(sum([(label_mean - y[i])**2 for i in range(0,rows)]))
    xmn = [sum(x)/rows for x in zip(*X)]
    for x in zip(*X):
        if idx != len(xmn):
            sm = nm = 0
            for i,j in zip(x,y):
                sm += (xmn[idx] - i)**2
                nm += (xmn[idx] - i)*(label_mean-j)
            data_array.append(math.sqrt(sm))
            num.append(nm)
            idx +=1
    den = [y_array*xd for xd in data_array]
    for n,d in zip(num, den):
        if d == 0:
            r.append(0)
        else:
            val = n/d
            if val < 0:
                r.append(val*1)
            else:
                r.append(val)
    indices, v_sorted = zip(*sorted(enumerate(r), key=itemgetter(1), reverse=True))
    #print("indices: ", indices)
    V = []
    cnt = 0
    for i in indices:
        if cnt < top:
            V.append(X[:i])
        cnt += 1
    idx = indices[:top]
    #print('idx : ', idx)
    return idx


if __name__ == '__main__':

    datafile = sys.argv[1] #'./traindata'
    trainlabelfile = sys.argv[2] #'./trainlabels'
    #testdata = './testdata'
    #print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    data = read_data(datafile)

    print('data loaded')
    #print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    f = open(trainlabelfile)
    trainlabels = {}
    labels = []
    l = f.readline()
    while (l != ''):
        a = l.split()
        #trainlabels[int(a[1])] = int(a[0])
        labels.append(int(a[0]))
        l = f.readline()

    rows = len(data)
    cols = len(data[0])
    print('labels loaded')
    #print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    #features_train, features_test, labels_train, labels_test = train_test_split(data, labels,
    #test_size=0.10, random_state=42)
    idx = calculate_pearson_score(data, labels, 15)
    #idx = calculate_pearson_score(features_train, labels_train,15)
    print("Number of features used : ", len(idx))
    print("Features are:")
    print(idx)

    X_train = extract_features(data, idx)
    #X_train = extract_features(features_train, idx)

    print('reading test data')
    test_data = open(sys.argv[3]) #open('./testdata')
    testdata = []
    for line in test_data:
        testdata.append(line.split())

    X_test = extract_features(testdata, idx)
    #X_test = extract_features(features_test, idx)

    regr = svm.LinearSVC()
    regr.fit(X_train, labels)
    #regr.fit(X_train, labels_train)
    to_predict = [[float(j) for j in i] for i in X_test]
    #print(clf.predict(to_predict))
    print('prediction done')
    test_labels = regr.predict(to_predict)

    predictions = [int(e) for e in test_labels]
    #print(predictions)

######### Testdata predictions ###########
    f = open('test_data.labels', 'w')
    for i in range(0, len(X_test), 1):
        print(predictions[i], i)
        f.write('{}  {}' . format(predictions[i],i))
        f.write("\n")
    f.close()
    print("Output written to test_data.labels file")

    #print("accuracy:" , accuracy(labels_test,predictions))
