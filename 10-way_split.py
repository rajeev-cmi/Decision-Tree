from random import shuffle

f = open('census-income.csv','r')
y = f.readlines()
l = list(filter((lambda x: '?' not in x), y))
f.close()

column_head = [l[0]]
l1 = l[1:]
shuffle(l1)
n = int(len(l1)/10)
for i in range(10):
    trn = open('Splitted Data/traindata.'+str(i+1)+'.csv','w')
    tst = open('Splitted Data/testdata.'+str(i+1)+'.csv','w')
    trn.writelines(column_head+l1[0:i*n]+l1[(i+1)*n:])
    tst.writelines(column_head+l1[i*n:(i+1)*n])
    trn.close()
    tst.close()
