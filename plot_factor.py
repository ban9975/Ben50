import matplotlib.pyplot as plt
import pandas as pd
import sys
import math
fileName = 'wristband/factor/base.xlsx'
plotName = 'base'
xls = pd.ExcelFile(fileName)
cnt=0
for name in xls.sheet_names:
    plt.ylim(1300,1900)
    tmp = xls.parse(name)
    plt.scatter(tmp['t'],tmp['val'], marker='.',s=10,label=name)  
    if "rock" in name:
        plt.title(plotName+'_{}'.format(cnt))
        plt.legend(loc='upper right')
        plt.ylabel('resistance value(ohm)')
        plt.xlabel('time(ms)')
        plt.savefig('factor_study/base/'+plotName+'_{}'.format(cnt)+'.png')
        plt.figure()
        cnt+=1
