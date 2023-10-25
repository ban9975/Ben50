import matplotlib.pyplot as plt
import pandas as pd
import sys
import math
plotName = 'gesture_new'
fileName = 'wristband/factor/'+plotName+'.xlsx'
xls = pd.ExcelFile(fileName)
cnt=0

nRound=5
names=xls.sheet_names
# print(names)
# pd.set_option('display.max_row', None)
# freq=[50,100]
freq=[50,50,50,50]
for i in range(1):
    paper=pd.DataFrame()
    t=[]
    for j in range(nRound):
        tmp = xls.parse(names[i*4*nRound+4*j])
        paper=pd.concat([paper,tmp],ignore_index=True)
        for m in range(tmp.shape[0]):
            t.append(m*freq[i])
    plt.ylim(0,3500)
    # print(pd.DataFrame(t)[0])
    # print(paper['val'])
    plt.scatter(pd.DataFrame(t)[0],paper['val'], marker='.',s=3,label='paper_{}'.format(i))

    rock=pd.DataFrame()
    t=[]    
    for j in range(nRound):
        tmp = xls.parse(names[i*4*nRound+4*j+1])
        rock=pd.concat([rock,tmp],ignore_index=True)
        for m in range(tmp.shape[0]):
            t.append(m*freq[i])
    plt.ylim(0,3500)
    plt.scatter(pd.DataFrame(t)[0],rock['val'], marker='.',s=3,label='rock_{}'.format(i))
    bend=pd.DataFrame()
    t=[]    
    for j in range(nRound):
        tmp = xls.parse(names[i*4*nRound+4*j+2])
        bend=pd.concat([bend,tmp],ignore_index=True)
        for m in range(tmp.shape[0]):
            t.append(m*freq[i])
    plt.ylim(0,3500)
    plt.scatter(pd.DataFrame(t)[0],bend['val'], marker='.',s=3,label='bend_{}'.format(i))
    scissor=pd.DataFrame()
    t=[]    
    for j in range(nRound):
        tmp = xls.parse(names[i*4*nRound+4*j+3])
        scissor=pd.concat([scissor,tmp],ignore_index=True)
        for m in range(tmp.shape[0]):
            t.append(m*freq[i])
    plt.ylim(0,3500)
    plt.scatter(pd.DataFrame(t)[0],scissor['val'], marker='.',s=3,label='scissor_{}'.format(i))
plt.title(plotName+'_all')
plt.legend(loc='lower right')
plt.ylabel('resistance value(ohm)')
plt.xlabel('time(ms)')
plt.savefig('factor_study/'+plotName+'_all.png')