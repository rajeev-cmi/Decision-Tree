import time
from Process import *

def update(a,i,j): # Update the j-th attribute for the attribute value a in the attribute dictionary Att_Dict, scaning the i-th row
    try:
        Att_Dict[x[0][j]][a][x[i][-1]] += 1
    except KeyError:
        Att_Dict[x[0][j]][a] = {'<=50K':0, '>50K':0}
        Att_Dict[x[0][j]][a][x[i][-1]] += 1


START = time.time()

s = "Fold\t Precision\t Recall\t\t Accuracy\t Runtime\n"

for k in range(10):
    start = time.time()

# Reading & Analyzing the training data
    x = Process_file('Splitted Data/traindata.'+str(k+1)+'.csv')
    Attributes = x[0][:-1]
    Class = ['<=50K', '>50K']
    Att_Dict = {}
    l = len(Attributes)
    for i in range(l):  # l = no. of attributes
        Att_Dict[Attributes[i]] = {}
    Cls_Dict = {'<=50K':0, '>50K':0}
    for i in range(1,len(x)):
        Cls_Dict[x[i][-1]] += 1
        for j in range(l):  # l = no. of attributes
            update(x[i][j],i,j)

# Probability calculations                
    N = sum(Cls_Dict.values())
    Class_Prob = {'<=50K':float(Cls_Dict['<=50K'])/N, '>50K':float(Cls_Dict['>50K'])/N}
    Cond_Prob = Att_Dict.copy()
    for A in Attributes:
        m = len(Att_Dict[A])
        for a in list(Att_Dict[A].keys()):
            for c in Class:
                Cond_Prob[A][a][c] = float(Cond_Prob[A][a][c]+1)/(Cls_Dict[c]+m)    # Laplace smoothing applied 

# Reading the test data, Predicting the class for each entry and comparing it with the actual class
    y = Process_file('Splitted Data/testdata.'+str(k+1)+'.csv')
    (TP,FP,FN,TN) = (0,0,0,0)
    for i in range(1,len(y)):
        p = Class_Prob.copy()
        for j in range(l):  # l = no. of attributes
            A = y[0][j]
            a = y[i][j]
            for c in Class:
                try:
                    p[c] = p[c]*Cond_Prob[A][a][c]
                except KeyError:    # Laplace smoothing
                    m = len(Att_Dict[A])
                    Cond_Prob[A][a] = {}
                    Cond_Prob[A][a]['<=50K'] = 1/float(Cls_Dict['<=50K']+m)
                    Cond_Prob[A][a]['>50K'] = 1/float(Cls_Dict['>50K']+m)
                    p[c] = p[c]*Cond_Prob[A][a][c]
        if p[Class[0]] > p[Class[1]]:
            predicted = Class[0]
            if y[i][-1] == predicted:
                TP += 1
            else:
                FP += 1
        else:
            predicted = Class[1]
            if y[i][-1] == predicted:
                TN += 1
            else:
                FN += 1
                    
    Precision = float(TP)/(TP+FP)
    Recall = float(TP)/(TP+FN)
    Accuracy = float(TP+TN)/(TP+FP+FN+TN)
    stop = time.time()
    Runtime = stop - start
    s = s+str(k+1)+"\t"+str(Precision)+"\t"+str(Recall)+"\t"+str(Accuracy)+"\t"+str(Runtime)+"\n"

output = open('output_NB.txt','w')
output.write(s)
output.close()

STOP = time.time()
print("Program successfully executed")
print("Total Runtime :: %f") %(STOP-START)
