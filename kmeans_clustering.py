import sys
import math
import random as rnd
from collections import defaultdict


def distance(d, k):
    sm = sum([(m - n)**2 for m, n in zip(d, k)])
    return math.sqrt(sm)


def find_cluster(dat, k):
    d = defaultdict(list)
    mn = []
    for i in range(0,len(dat)):
        temp = []
        for j in range(0,len(k)):
            temp.append(distance(dat[i], k[j]))
        id = temp.index(min(temp))
        d[id].append(dat[i])
    for key in d:
        temp = d[key]
        mn.append([sum(l)/len(l) for l in zip(*temp)])
    return mn

def has_converged(old, new):
    return (set([tuple(a) for a in old]) == set([tuple(a) for a in new]))


if __name__ == '__main__':

    datafile = sys.argv[1]
    f = open(datafile)
    data = []
    l = f.readline()

    while(l!= ''):
        a = l.split()
        l2 = []
        for j in range(0,len(a),1):
            l2.append(float(a[j]))
        data.append(l2)
        l = f.readline()

    f.close()

    k = int(sys.argv[2])

    sample_cluster = rnd.sample(data, k)
    while True:
        new_cluster = find_cluster(data, sample_cluster)
        if has_converged(sample_cluster, new_cluster):
            sample_cluster = new_cluster
            break
        sample_cluster = new_cluster

    for i in range(0,len(data)):
        temp = []
        for j in range(0,len(sample_cluster)):
            temp.append(distance(data[i], sample_cluster[j]))
        id = temp.index(min(temp))
        print(id, i)
