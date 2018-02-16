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
#n = []
#n.append(0)
#n.append(0)
l = f.readline()
while(l != ''):
    a = l.split()
    trainlabels[int(a[1])] = int(a[0])
    l = f.readline()
    #n[int(a[0])] += 1

w = []
for i in range(0,cols,1):
    w.append(random.uniform(-.01,.01))

eta =.01
#eta = .000000001
dellf = []
for j in range(0,cols,1):
    dellf.append(0)

prevobj = 100000000
obj = prevobj - 10
#while(abs(prevobj - obj) > 0):
while((prevobj - obj) > .0000001):
    #print("prevobj - obj", prevobj - obj)
    prevobj = obj
    for j in range(0,cols,1):
        dellf[j] = 0

    for i in range(0, rows, 1):
        if(trainlabels.get(i) != None):
            dp = dotproduct(w, data[i])
            sigmoidval = 1 / (1 + math.exp(-1*dp))
            for j in range(0, cols, 1):
                dellf[j] += (trainlabels.get(i) - sigmoidval)*data[i][j]
                #dellf[j] += math.log(1+math.exp(-trainlabels.get(i)*dp))
    for j in range(0,cols,1):
        w[j] += eta*dellf[j]

    error = 0
    for i in range(0,rows,1):
        if(trainlabels.get(i) != None):

            dotp = dotproduct(w, data[i])
            sigmoidval = 1 / (1 + math.exp(-1 * dotp))
            first =  trainlabels.get(i)*math.log(sigmoidval)
            #temp = math.exp(-1*dotp) / (1 + math.exp(-1 * dotp))
            second = (1 - trainlabels.get(i)) * (math.log((math.exp(-1*dotp)) / (1 + math.exp(-1 * dotp))))
            #if(trainlabels.get(i) == 1):
                #error += -math.log(sigmoidval)
            #if(trainlabels.get(i) == 0):
                #error += -math.log(1 - sigmoidval)
            #error += ((sigmoidval - trainlabels.get(i))**2) / 2
            ### multiply by rows ?????????
            error += -(first + second)


    obj = error
    #print("obj:", obj)
#print(w)
print("w = ", w[:-1])
print("w0 = ", w[len(w)-1])
wlen = math.sqrt(w[0]**2 + w[1]**2)
print("wlen = ", wlen)
dist_to_origin = (w[2])/wlen
print("distance to origin: ",dist_to_origin)

for i in range(0,rows,1):
    if(trainlabels.get(i) == None):
        dp = dotproduct(w, data[i])
        if(dp < 0):
            print("0 :", i)
        else:
            print("1 :", i)

