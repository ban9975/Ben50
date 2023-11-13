import matplotlib.pyplot as plt
import pandas as pd
import sys
import math
plotName = 'base_newPCB'
fileName = 'D://NTU/Ben50/Excel_data/factor/'+plotName+'.xlsx'
xls = pd.ExcelFile(fileName)
cnt=0

nRound=5
nGestures=2
names=xls.sheet_names
freq=[50,50,50,50,50]
paper=pd.DataFrame()
rock=pd.DataFrame()
bend=pd.DataFrame()
nothing=pd.DataFrame()
sliding=pd.DataFrame()
t=[[],[],[],[]]
for name in names:
    if 'paper' in name:
        tmp = xls.parse(name)
        paper=pd.concat([paper,tmp],ignore_index=True)
        for m in range(tmp.shape[0]):
            t[0].append(m*freq[0])
    if 'rock' in name:
        tmp = xls.parse(name)
        rock=pd.concat([rock,tmp],ignore_index=True)
        for m in range(tmp.shape[0]):
            t[1].append(m*freq[1])
    # if 'sliding' in name:
    #     tmp = xls.parse(name)
    #     sliding=pd.concat([sliding,tmp],ignore_index=True)
    #     for m in range(tmp.shape[0]):
    #         t[1].append(m*freq[1])
    # if 'local' in name:
    #     tmp = xls.parse(name)
    #     paper=pd.concat([paper,tmp],ignore_index=True)
    #     for m in range(tmp.shape[0]):
    #         t[0].append(m*freq[0])
    # if 'uniform' in name:
    #     tmp = xls.parse(name)
    #     rock=pd.concat([rock,tmp],ignore_index=True)
    #     for m in range(tmp.shape[0]):
    #         t[1].append(m*freq[1])
    # if 'nothing' in name:
    #     tmp = xls.parse(name)
    #     nothing=pd.concat([nothing,tmp],ignore_index=True)
    #     for m in range(tmp.shape[0]):
    #         t[3].append(m*freq[3])
    # if 'bend' in name:
    #     tmp = xls.parse(name)
    #     bend=pd.concat([bend,tmp],ignore_index=True)
    #     for m in range(tmp.shape[0]):
    #         t[2].append(m*freq[2])
plt.ylim(1000,2000)
# plt.scatter(pd.DataFrame(t[1])[0],rock['val'], marker='.',s=3,label='uniform')  
# plt.scatter(pd.DataFrame(t[0])[0],paper['val'], marker='.',s=3,label='local')
plt.scatter(pd.DataFrame(t[0])[0],paper['val'], marker='.',s=3,label='paper')
plt.scatter(pd.DataFrame(t[1])[0],rock['val'], marker='.',s=3,label='rock')  
# plt.scatter(pd.DataFrame(t[2])[0],bend['val'], marker='.',s=3,label='bend')
# plt.scatter(pd.DataFrame(t[3])[0],nothing['val'], marker='.',s=3,label='nothing')
# plt.scatter(pd.DataFrame(t[1])[0],sliding['val'], marker='.',s=3,label='sliding')  
plt.title(plotName+'_all')
plt.legend(loc='lower right')
plt.ylabel('resistance value(ohm)')
plt.xlabel('time(ms)')
plt.savefig('D://NTU/Ben50/Wristband_plots/factor_study/'+plotName+'_all.png')