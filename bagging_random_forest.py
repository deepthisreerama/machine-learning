import sys
import random


def get_best_split(data, trainlabels):
    bestgini = 10000
    rows = len(data)
    cols = len(data[0])
    column = 0
    bestsplit = 0

    #for col_id in colsamp:
    for j in range(0,cols,1):
        for i in range(0,rows-1,1):
            #print(data[i][j])
            x = float(data[i][j])
            y = float(data[i+1][j])
            split =(x + y)/2
            #print("split",split)
            lsize = 0.0
            rsize = 0.0
            lp=0.0
            rp=0.0
            for k in range(0,rows,1):
                if(float(data[k][j]) <= split):
                    lsize = lsize+1
                    if(trainlabels[k]==0):
                        lp = lp+1
                else:
                    rsize = rsize+1
                    if(trainlabels[k]==0):
                        rp = rp+1

            if lsize == 0 and rsize == 0:
                gini = 0.0
            elif lsize == 0:
                gini = (rsize/rows)*(rp/rsize)*(1 - (rp/rsize))
            elif rsize == 0:
                gini = (lsize/rows)*(lp/lsize)*(1 - (lp/lsize))
            else:
                gini = ((lsize/rows)*(lp/lsize)*(1 - (lp/lsize))) + ((rsize/rows)*(rp/rsize)*(1 - (rp/rsize)))

            if(gini < bestgini):
                bestgini = gini
                column = j
                bestsplit = split

    return column,bestsplit#{'column':column,'split':bestsplit}


datafile = sys.argv[1]
f = open(datafile,'r')
data = []
l = f.readline()
while(l!=''):
    a=l.split()
    l2=[]
    for j in range(0,len(a),1):
        l2.append(a[j])
    data.append(l2)
    l=f.readline()

rows = len(data)
trainlabelfile = sys.argv[2]
f = open(trainlabelfile,'r')

trainlabels = {}
l=f.readline()
#print(data)
while(l!=''):
    a=l.split()
    #if(int(a[0])==0):
    #    trainlabels[int(a[1])]=int(a[0])-1
    #else:
    trainlabels[int(a[1])]=int(a[0])

    l=f.readline()

traindata=[]
for i in range(0,len(data),1):
    if(trainlabels.get(i) != None):
        traindata.append(data[i])

stumparray = []
for index in range(100):
    sampId = []
    for i in range(0,len(traindata),1):
        sampId.append(random.randrange(0,len(traindata)))

    trainbag = [traindata[k] for k in sampId]
    labelbag = [trainlabels.get(k) for k in sampId]

    #col_size = int(len(trainbag[0])*(1/3))

    #colsamp_s = [i for i in range(len(trainbag[0]))]
    #random.shuffle(colsamp_s)
    #colsamp = []#random.shuffle([i for i in range(len(trainbag[0]))])
    #for i in range(0,col_size,1):
    #    colsamp.append(colsamp_s[i])

    #newsampbag = []

    #for row in sampId:
    #    rowlist = []
    #    for col in colsamp:
    #       rowlist.append(traindata[row][col])
    #    newsampbag.append(rowlist)
    #stumparray.append(get_best_split(newsampbag,labelbag,colsamp))
    stumparray.append(get_best_split(trainbag,labelbag))


#print(stumparray)
prediction = {}

for st in range(0,len(stumparray),1):
    m = 0
    p = 0
    pred_list = {}
    for i in range(0,rows,1):
        if(trainlabels.get(i) != None):
            col = stumparray[st][0]
            s = stumparray[st][1]
            ideal_col = float(data[i][col])
            if(ideal_col < s):
                if(trainlabels[i] == 0):
                    m += 1
                else:
                    p += 1
    if(m > p):
        left = 0
        right = 1
    else:
        left = 1
        right = 0

    for a in range(0,rows,1):
        if(trainlabels.get(a) == None):
            #pred_val = []
            best_col = stumparray[st][0]
            best_split = stumparray[st][1]
            if(float(data[a][best_col]) < best_split):
                pred_list[a] = left
                #print(left, a)
            else:
                pred_list[a] = right
                #print(right, a)
    prediction[st] = pred_list

#print(prediction)

prediction_values = list(prediction.values())
#print(prediction_values)
newdict = {}
for k,v in [(key,d[key]) for d in prediction_values for key in d]:
    if k not in newdict: newdict[k]=[v]
    else: newdict[k].append(v)

#print(newdict)

for k in newdict.keys():
    prediction_list = newdict[k]
    print("For " ,k , " : " ,max(set(prediction_list), key=prediction_list.count))
