import matplotlib.pyplot as plt
import pandas as pd
import sys
import math
plotName = 'length'
fileName = 'wristband/factor/'+plotName+'.xlsx'
xls = pd.ExcelFile(fileName)
cnt=0

nRound=5
names=xls.sheet_names
# print(names)
# pd.set_option('display.max_row', None)
# freq=[50,100]
freq=[50,50,50,50]
for i in range(0,2):
    paper=pd.DataFrame()
    t=[]
    for j in range(nRound):
        tmp = xls.parse(names[i*2*nRound+2*j])
        paper=pd.concat([paper,tmp],ignore_index=True)
        for m in range(tmp.shape[0]):
            t.append(m*freq[i])
    plt.ylim(0,3800)
    # print(pd.DataFrame(t)[0])
    # print(paper['val'])
    plt.scatter(pd.DataFrame(t)[0],paper['val'], marker='.',s=3,label='paper_{}'.format(i))

    rock=pd.DataFrame()
    t=[]    
    for j in range(nRound):
        tmp = xls.parse(names[i*2*nRound+2*j+1])
        rock=pd.concat([rock,tmp],ignore_index=True)
        for m in range(tmp.shape[0]):
            t.append(m*freq[i])
    plt.ylim(0,3800)
    plt.scatter(pd.DataFrame(t)[0],rock['val'], marker='.',s=3,label='rock_{}'.format(i))
plt.title(plotName+'_all')
plt.legend(loc='lower right')
plt.ylabel('resistance value(ohm)')
plt.xlabel('time(ms)')
plt.savefig('factor_study/'+plotName+'_all.png')