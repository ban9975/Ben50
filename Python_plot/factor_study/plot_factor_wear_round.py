import matplotlib.pyplot as plt
import pandas as pd
import sys
import math
plotName = 'takeoff_3gestures'
fileName = 'wristband/factor/'+plotName+'.xlsx'
xls = pd.ExcelFile(fileName)
cnt=0

nRound=5
nWear=5
nGestures=3
names=xls.sheet_names
freq=[50,50,50,50]
for i in range(nWear):
    for j in range(nRound):
        t=[]
        paper = xls.parse(names[i*nRound*nGestures+nGestures*j])
        rock = xls.parse(names[i*nRound*nGestures+nGestures*j+1])
        bend = xls.parse(names[i*nRound*nGestures+nGestures*j+2])
        for m in range(paper.shape[0]):
            t.append(m*freq[0])
        plt.ylim(1000,2500)
        plt.scatter(pd.DataFrame(t)[0],paper['val'], marker='.',s=3,label='paper')
        plt.scatter(pd.DataFrame(t)[0],rock['val'], marker='.',s=3,label='rock')
        plt.scatter(pd.DataFrame(t)[0],bend['val'], marker='.',s=3,label='bend')
        plt.title(plotName+'_wear{}_round{}'.format(i,j))
        plt.legend(loc='lower right')
        plt.ylabel('resistance value(ohm)')
        plt.xlabel('time(ms)')
        plt.savefig('factor_study/takeoff_3gestures/'+plotName+'_wear{}_round{}.png'.format(i,j))
        plt.figure()