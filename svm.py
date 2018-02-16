import sys
import random
import math


def dotproduct(u,v):
    assert len(u) == len(v)
    dp = 0
    for i in range(0,len(u),1):
        dp += u[i]*v[i]
    return dp

datafile = sys.argv[1]
f = open(datafile)
data =[]
i = 0
l = f.readline()

while(l!= ''):
    a = l.split()
    l2 = []
    for j in range(0,len(a),1):
        l2.append(float(a[j]))
    l2.append(1)
    data.append(l2)
    l = f.readline()

rows = len(data)
cols = len(data[0])
f.close()

labelfile = sys.argv[2]
f = open(labelfile)
trainlabels = {}
n = []
n.append(0)
n.append(0)
l = f.readline()
while(l != ''):
    a = l.split()
    trainlabels[int(a[1])] = int(a[0])
    if(trainlabels[int(a[1])] == 0):
        trainlabels[int(a[1])] = -1
    l = f.readline()
    n[int(a[0])] += 1

w = []
for i in range(0,cols,1):
    w.append(random.uniform(-.01,.01))

eta =.001
#eta = .000000001
dellf = []
for j in range(0,cols,1):
    dellf.append(0)

prevobj = 100000000
obj = prevobj - 10
#while(abs(prevobj - obj) > 0):
while(abs(prevobj - obj) > .000000001):
    #print("prevobj - obj", prevobj - obj)
    prevobj = obj
    for j in range(0,cols,1):
        dellf[j] = 0

    for i in range(0, rows, 1):
        if(trainlabels.get(i) != None):
            dp = dotproduct(w, data[i])
            for j in range(0, cols, 1):
                condition = trainlabels.get(i)*dp
                if(condition < 1):
                    dellf[j] += -1*trainlabels.get(i)*data[i][j]
                elif(condition >= 1):
                    dellf[j] += 0

    for j in range(0,cols,1):
        w[j] -= eta*dellf[j]

    error = 0
    for i in range(0,rows,1):
        if(trainlabels.get(i) != None):
            loss = max(0,1-trainlabels.get(i)*dotproduct(w,data[i]))
            error += loss
            #print("loss:", loss)
            #print("error:", error)

    obj = error
    #print("obj:", obj)

print("w = ",w[:-1])
print("w0 = ", w[len(w)-1])
wlen = math.sqrt(w[0]**2 + w[1]**2)
dist_to_origin = abs(w[2])/wlen
print("distance to origin: ",dist_to_origin)

for i in range(0,rows,1):
    if(trainlabels.get(i) == None):
        dp = dotproduct(w, data[i])
        if(dp < 0):
            print("0 :", i)
        else:
            print("1 :", i)


