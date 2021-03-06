import sys
import random
from sklearn import svm
from sklearn.model_selection import train_test_split


def dotproduct(u,v):
    assert len(u) == len(v)
    dp = 0
    for d in range(0,len(u),1):
        dp += u[d]*v[d]
    return dp


def assign_sign(dp):
    if dp < 0:
        return 0
    else:
        return 1


datafile = sys.argv[1]
f = open(datafile)
data =[]
#i = 0
l = f.readline()

while(l!= ''):
    a = l.split()
    l2 = []
    for j in range(0,len(a),1):
        l2.append(float(a[j]))
    #l2.append(1)
    data.append(l2)
    l = f.readline()


f.close()

labelfile = sys.argv[2]
f = open(labelfile)
trainlabels = {}
labels = []
l = f.readline()
while(l != ''):
    a = l.split()
    trainlabels[int(a[1])] = int(a[0])
    labels.append(int(a[0]))
    l = f.readline()
    #n[int(a[0])] += 1

testdatafile = sys.argv[3]
f = open(testdatafile)
testdata =[]
#i = 0
l = f.readline()

while(l!= ''):
    a = l.split()
    l2 = []
    for j in range(0,len(a),1):
        l2.append(float(a[j]))
    #l2.append(1)
    testdata.append(l2)
    l = f.readline()

f.close()

#x_train, x_test, y_train, y_test = train_test_split(data, labels,
 #   test_size=0.10, random_state=42)
rows = len(data)
cols = len(data[0])

#print(len(x_train))
#print(len(testdata))
z = []
testz = []
for k in range(0,1000,1):
    w = []
    for i in range(0,cols,1):
        w.append(random.uniform(-1,1))
    p = []
    testp = []
    dp = 0
    for j in range(0,rows,1):
        dp = dotproduct(data[j],w)
        p.append(assign_sign(dp))
    for t in range(0,len(testdata),1):
        dp = dotproduct(testdata[t],w)
        testp.append(assign_sign(dp))
    z.append(p)
    testz.append(testp)

rez = [[z[j][i] for j in range(len(z))] for i in range(len(z[0]))]
testrez = [[testz[j][i] for j in range(len(testz))] for i in range(len(testz[0]))]

regr = svm.LinearSVC()
regr.fit(rez,labels)
to_predict = [[float(j) for j in i] for i in testrez]
predictions = regr.predict(to_predict)
print(predictions)
#error = 0
#for i in range(0,len(test_labels),1):
 #   if(test_labels[i] != labels[i]):
  #      error = error+1

#error = error/len(y_test)
#accuracy = (1- error)*100
#print("Error : ", error)
#print(accuracy)
