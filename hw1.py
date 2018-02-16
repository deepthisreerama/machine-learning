from __future__ import division

from numpy import *
import sys
import numpy as np
import operator


def calculateprob(data,labs):
    data = array(data)
    labs = array(labs)
    label_u = []
    label_i = []
    assert(len(data) == len(labs))

    # get number of features
    no_of_features = len(data[0])

    for i in data:
        assert(no_of_features == len(i))

    #get unique labels
    uniq = {}
    prior_probs = {}
    for eachitem in labs:
        uniq[eachitem] = 0
        prior_probs[eachitem] = 0

    for eachitem in uniq.keys():
        label_u.append(eachitem)

    for eachitem in label_u:
            c = where((labs==eachitem) )

            prior_probs[eachitem] = len(c[0])/len(data)

            label_i.append(where (labs==eachitem) )

    node = {}

    for eachitem in zip(label_i,label_u):
        gen = None
        m = data[eachitem[0]]
        s = m.shape[1]
        p = []
        d_array = []
        for i in range(s):
            mm = m[:,i]
            mean_mm = mean(mm)
            var_mm = var(mm,axis=0,ddof=1)

            d_array.append([mean_mm, var_mm])

        node[eachitem[1]]=d_array

    return node, prior_probs


def calculatemean(data, classes):
    size = len(data)
    labels = [[row[i] for row in classes] for i in range(0, len(classes[0]))]
    labels = set(labels[0])
    cmean = []
    for label in labels:
        temp = []
        for i in range(0, size):
            if classes[i][0] == label:
                temp.append(data[i])
        sz = len(temp[0])
        mn = [float(sum(l)+1)/(len(l)+sz) for l in zip(*temp)]
        cmean.append(mn)
    return cmean


def calculatevariance(data, classes):
    size = len(data)
    labels = [[row[i] for row in classes] for i in range(0, len(classes[0]))]
    labels = set(labels[0])
    cmean = calculatemean(data, classes)
    cvariance = []
    index = 0
    for label in labels:
        temp = []
        for i in range(0, size):
            if classes[i][0] == label:
                temp.append(data[i])
        mn = cmean.pop(index)
        tvar = []
        for i in range(0, len(temp[0])):
            var = 0
            for j in range(0, len(temp)):
                var += (temp[j][i] - mn[i]) ** 2
            var = float(var / ((len(temp)-1)))
            tvar.append(var)
        cvariance.append(tvar)
    return cvariance


def predictlabels(nodes, prior_probs, pred_data_list):

    pred_output=[]
    for pred_data in pred_data_list:

        #calculate posterior probabilities
        post={}
        for eachnode in nodes.items():
            f = eachnode[1]
            post[eachnode[0]]= prior_probs[eachnode[0]]
            ii=0
            for eachitem in f:

                mean_m = eachitem[0]
                var_m = eachitem[1]

                data_m = pred_data[ii]


                p1 = 1.00 /(sqrt(2 * pi * var_m))
                p2 = exp ( ( -1 * pow( ( data_m - mean_m ),2 ) ) / (2.00 * var_m))
                post[eachnode[0]] *= (p1 * p2)


                ii += 1
                pass
            pass
        pass

        # calculate evidence

        evidence = 0

        for eachnode in post.items():
            evidence += eachnode[1]
        pass

        for i in post.keys():
            post[i] = post[i]/evidence
        pass

        likelilabel = max(post.items(), key=operator.itemgetter(1))[0]

        likelihood = max(post.items(), key=operator.itemgetter(1))[1]
        pred_output.append((likelilabel, likelihood))

    return pred_output


if __name__ == "__main__":

    data = sys.argv[1]
    labels = sys.argv[2]

    training_data = np.genfromtxt(data, delimiter=' ')
    training_labels = np.loadtxt(labels, delimiter=' ')

    number_of_indices = len(training_data) - 1

    sorted_labels = training_labels[training_labels[:, 1].argsort()]

    sorted_labels_col2 = sorted_labels[:, 1]
    for i in range(len(sorted_labels_col2)):
        sorted_labels_col2[i] = int(sorted_labels_col2[i])

    full_set = set(range(0, number_of_indices + 1))

    missing_indices = sorted(list(full_set - set(sorted_labels_col2)))
    #np.set_printoptions(formatter={'float_kind': '{:f}'.format})
    new_sample = training_data[missing_indices]

    sorted_labels_col_new = []

    for i in range(len(sorted_labels_col2)):
        sorted_labels_col_new.append(int(sorted_labels_col2[i]))

    #print(sorted_labels_col_new)
    training_data_actual = training_data[sorted_labels_col_new]

    outcome = []
    outcome_float = np.asarray(sorted_labels[:, 0])

    for i in range(len(outcome_float)):
        outcome.append(int(outcome_float[i]))

    class_mean = calculatemean(training_data_actual, sorted_labels)

    class_variance = calculatevariance(training_data_actual, sorted_labels)

    node, prior_prob = calculateprob(training_data_actual, outcome)

    finalDict = {}

    for i in range(0,len(class_mean),1):
        finalList = []
        firstList = class_mean[i]
        secondList = class_variance[i]
        for j in range(0, len(firstList),1):
            combinedList = []
            combinedList.append(firstList[j])
            combinedList.append(secondList[j])
            finalList.append(combinedList)
        finalDict[i] = finalList

    output = predictlabels(finalDict, prior_prob, new_sample)

    dict_value = {}
    for i in range(len(missing_indices)):
        dict_value[missing_indices[i]] = output[i][0]

    print(dict_value)

    pass
