import sys


def getbestsplit(data,labels,col):
    colvals = {}
    indices = []
    rows = 0
    minus = 0
    for i in range(0, len(data), 1):
        if(labels.get(i) != None):
            colvals[i] = data[i][col]
            indices.append(i)
            rows +=1
            if(labels[i] == 0):
                minus +=1

    sorted_indices = sorted(indices, key=colvals.__getitem__)

    lsize = 1
    rsize = rows - 1
    lp = 0
    rp = minus
    if(labels[sorted_indices[0]] == 0):
        lp += 1
        rp -= 1

    best_s = -1
    bestgini = 10000
    for i in range(1,len(sorted_indices),1):
        s = (float(colvals[sorted_indices[i]]) + float(colvals[sorted_indices[i-1]]))/2
        gini = (lsize/rows)*(lp/lsize)*(1-lp/lsize) + (rsize/rows)*(rp/rsize)*(1-rp/rsize)
        if(gini < bestgini):
            bestgini = gini
            best_s = s
        if(labels[sorted_indices[i]] == 0):
            lp += 1
            rp -= 1
        lsize += 1
        rsize -= 1

    return(best_s, bestgini)


datafile = sys.argv[1]
f = open(datafile)
data = []
i = 0
l = f.readline()

while (l != ''):
    a = l.split()
    l2 = []
    for j in range(0, len(a), 1):
        l2.append(float(a[j]))
    data.append(l2)
    l = f.readline()
f.close()

labelfile = sys.argv[2]
f = open(labelfile)
trainlabels = {}
l = f.readline()
while (l != ''):
    a = l.split()
    trainlabels[int(a[1])] = int(a[0])
    l = f.readline()

rows = len(data)
cols = len(data[0])

best_split = -1
best_col = -1
best_gini = 10000
for j in range(0,cols,1):
    [s,gini] = getbestsplit(data,trainlabels,j)
    if(gini<best_gini):
        best_gini = gini
        best_split = s
        best_col = j

print('Best_column: ', best_col)
print('Gini is: ', best_gini)
print("Split point's value: ", best_split)