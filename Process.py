def Process_file(filename): # Function to read & process data from a given filename
    f = open(filename,'r')
    x = f.readlines()
    f.close()
    for i in range(len(x)):
        x[i] = x[i].strip().split(',')
        del x[i][2]
        for j in range(len(x[i])):
            x[i][j] = x[i][j].strip(' ')
            if i!=0:    # if not column head i.e. a data entry
                if j==0:                    # define age interval
                    if int(x[i][j])<=30:
                        x[i][j] = '<=30'
                    elif int(x[i][j])<=40:
                        x[i][j] = '31-40'
                    elif int(x[i][j])<=50:
                        x[i][j] = '41-50'
                    elif int(x[i][j])<=60:
                        x[i][j] = '51-60'
                    else:
                        x[i][j] = '>60'
                if j==3:                    # convert education-num to integer
                    x[i][j] = int(x[i][j])
                if j==9 or j==10:           # categorize capital-gain & capital-loss
                    if int(x[i][j])==0:
                        x[i][j] = '=0'
                    else:
                        x[i][j] = '>0'
                if j==11:                   # define hours-per-week interval
                    if int(x[i][j])<=20:
                        x[i][j] = '<=20'
                    elif int(x[i][j])<=40:
                        x[i][j] = '21-40'
                    elif int(x[i][j])<=60:
                        x[i][j] = '41-60'
                    elif int(x[i][j])<=80:
                        x[i][j] = '61-80'
                    else:
                        x[i][j] = '>80'
    return x
