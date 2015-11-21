import math
import time
from Process import *


def ImpurityEval1(D):
    n = len(D)
    count = 0.0
    for i in range(n):
        if D[i][-1] == '<=50K':
            count += 1
    p = count/n
    if p==0 or p==1:
        e = 0
    else:
        e = p*math.log(p,2)+(1-p)*math.log(1-p,2)
    return(-1*e)


def ImpurityEval2(A,D):
    sub = {}
    u = int(A[-1]) - 1
    for y in range(0,len(D)):
        try:
            sub[D[y][u]].append(D[y])
        except KeyError:
            sub[D[y][u]] = [D[y]]
    e = 0
    for i in list(sub.keys()):
        s = len(sub[i])/len(D)
        l = ImpurityEval1(sub[i])
        e = e + s*l
    return(e)


def Make_DT(D,A,T):
    C = {}
    for j in range(0,len(D)):
        try:
            C[D[j][-1]] += 1
        except KeyError:
            C[D[j][-1]] = 1
    k = list(C.keys())
    if len(k) == 1:
        T[k[0]] = {}
    elif len(A) == 0:
        m = k[0]
        for i in range(1,len(k)):
            if C[k[i]] > C[m]:
                m = k[i]
        T[m] = {}
    else:
        p = ImpurityEval1(D)
        p0 = ImpurityEval2(A[0],D)
        s = 0
        P = p-p0
        for x in range(1,len(A)):
            p1 = ImpurityEval2(A[x],D)
            if (p-p1)>P: # The attribute appearing first is taken in case of tie in the value of gain.
                s = x
                P = p-p1
        sub = {}
        T[A[s]] = {}
        u = int(A[s][10:]) - 1
        for y in range(len(D)):
            try:
                sub[D[y][u]].append(D[y])
            except KeyError:
                sub[D[y][u]] = [D[y]]
        A1 = A[:]
        del(A1[s])
        for z in list(sub.keys()):
            if sub[z] != []:
                T[A[s]][z] = {}
                Make_DT(sub[z],A1,T[A[s]][z])
    return(T)


START = time.time()

s = "Fold\t Precision\t Recall\t\t Accuracy\t Runtime\n"

for i in range(10):
    start = time.time()

    x = Process_file('Splitted Data/traindata.'+str(i+1)+'.csv')
    D = x[1:]
    A = []
    for k in range(1,len(D[0])):
        A.append("Attribute " + str(k))
    T = {}
    Tree = Make_DT(D,A,T)
    
    y = Process_file('Splitted Data/testdata.'+str(i+1)+'.csv')
    R = y[1:]
    (TP,FP,FN,TN) = (0,0,0,0)
    a = list(Tree.keys())[0]
    for l in R:
        S = Tree.copy()
        a = list(S.keys())[0]
        try:
            while a[:9] == "Attribute":
                b = int(a[10:]) - 1
                S = S[a][l[b]]
                a = list(S.keys())[0]
        except KeyError:
            pass
        if a == l[-1]: # l[-1] = actual class, a = predicted class
            if a == '<=50K':
                TP += 1
            else:
                TN += 1
        else:
            if a == '<=50K':
                FP += 1
            else:
                FN += 1

    Precision = float(TP)/(TP+FP)
    Recall = float(TP)/(TP+FN)
    Accuracy = float(TP+TN)/(TP+FP+FN+TN)
    stop = time.time()
    Runtime = stop - start
    s = s+str(i+1)+"\t"+str(Precision)+"\t"+str(Recall)+"\t"+str(Accuracy)+"\t"+str(Runtime)+"\n"

output = open('output_DT.txt','w')
output.write(s)
output.close()

STOP = time.time()
print("Program successfully executed")
print("Total Runtime :: %f") %(STOP-START)
