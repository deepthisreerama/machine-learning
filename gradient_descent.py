import math
import random
import decimal
import sys


def dotproduct(W, X):
    res = [x * (y) for x, y in zip(W, X)]
    return sum(res)


def cost(W,x, y):
    cost = sum([(dotproduct(W, x[i]) - y[i][0])**2 for i in range(0, len(x))])
    return cost


def gradient_descent(data, labels, lrate = 0.001, esp = 0.001, max_iter = 1000):
    
    val = len(data[0])
    W = []
    #W = [val for i in range(0, len(data[0]))]
    for i in range(0, val, 1):
        x = random.uniform(0, 1)
        #W.append(x)
        W.append((.02) * (x) - (.01))

    #W = [rnd.random(), rnd.random(),  rnd.random()]
    converged = False
    J = cost(W, data, labels)
    iter = 0
    while not converged:
        pdict = [(dotproduct(W, data[i]) - labels[i][0]) for i in range(0, len(data))]

        temp=[[( (data[i][j]) * pdict[i])for j in range(0,len(data[0]))] \
                for i in range(0,len(data))]

        grad =  [sum(l) for l in zip(*temp)]

        weight = [(W[i] - (lrate) * grad[i]) for i in range(0, len(W))]
        W = weight

        error = cost(W, data, labels)

        if abs(J - error) <= esp:
            #print("converged!! %d", iter)
            converged = True
        J = error
        iter += 1
        if iter == max_iter:
            #print("Max iteration")
            converged = True
    return W

if __name__ == '__main__':
    file_name_data = sys.argv[1]
    file_name_labels = sys.argv[2]
    data_set = open(file_name_data, 'r')
    labels_set = open(file_name_labels, 'r')

    data = [line.split() for line in data_set]
    data = [[float(column) for column in row] for row in data]
    for i in range(0, len(data)):
        data[i].append(1)

    labels = [line.split() for line in labels_set]
    labels = [[int(column) for column in row] for row in labels]
    for i in range(0, len(labels)):
        if labels[i][0] == 0:
            labels[i][0] = -1

    number_of_indices = len(data) - 1

    sorted_labels = sorted(labels,key=lambda x: x[1])

    sorted_labels_col2 = []
    [sorted_labels_col2.append(row[1]) for row in sorted_labels]

    full_set = set(range(0, number_of_indices + 1))

    missing_indices = sorted(list(full_set - set(sorted_labels_col2)))
    new_sample = []
    [new_sample.append(data[index]) for index in missing_indices]
    sorted_labels_col_new = []

    [sorted_labels_col_new.append(item[1]) for item in sorted_labels]

    training_data_actual = []
    [training_data_actual.append(data[index]) for index in sorted_labels_col_new]

    W = gradient_descent(training_data_actual, sorted_labels)
    #print(random.randint(1))
    print(W[:-1])
    W0 = W[len(W)-1]
    magnitude = math.sqrt(sum([W[i]**2 for i in range(0, len(W)-1)]))
    print(abs(W0/(magnitude)))

    for i in range(0, len(new_sample), 1):
        dp = dotproduct(W, new_sample[i])
        if dp > 0:
            print('1 ', missing_indices[i])
        else:
            print('0 ', missing_indices[i])
