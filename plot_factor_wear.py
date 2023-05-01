import matplotlib.pyplot as plt
import pandas as pd
plotName = '10wear_5round'
fileName = 'wristband/factor/'+plotName+'.xlsx'
xls = pd.ExcelFile(fileName)
cnt=0

nRound=5
nWear=10
nGestures=2
names=xls.sheet_names
freq=[50,50,50,50]
for i in range(nWear):
    paper=pd.DataFrame()
    for j in range(nRound):
        t=[]
        tmp = xls.parse(names[i*nRound*nGestures+nGestures*j])
        for m in range(tmp.shape[0]):
            t.append(m*freq[0])
        plt.ylim(1000,2000)
        plt.scatter(pd.DataFrame(t)[0],tmp['val'], marker='.',s=3,label='paper_{}'.format(j))
    plt.title(plotName+'_paper')
    plt.legend(loc='lower right')
    plt.ylabel('resistance value(ohm)')
    plt.xlabel('time(ms)')
    plt.savefig('factor_study/'+plotName+'_paper_wear{}.png'.format(i))
    plt.figure()
for i in range(nWear):
    rock=pd.DataFrame()
    for j in range(nRound):
        t=[]        
        tmp = xls.parse(names[i*nRound*nGestures+nGestures*j+1])
        # rock=pd.concat([rock,tmp],ignore_index=True)
        for m in range(tmp.shape[0]):
            t.append(m*freq[0])
        plt.ylim(1000,2000)
        plt.scatter(pd.DataFrame(t)[0],tmp['val'], marker='.',s=3,label='rock_{}'.format(j))
    plt.title(plotName+'_rock')
    plt.legend(loc='lower right')
    plt.ylabel('resistance value(ohm)')
    plt.xlabel('time(ms)')
    plt.savefig('factor_study/'+plotName+'_rock_wear{}.png'.format(i))
    plt.figure()
# for i in range(nWear):
#     bend=pd.DataFrame()

#     for j in range(nRound):
#         t=[]        
#         tmp = xls.parse(names[i*nRound*nGestures+nGestures*j+2])
#         # bend=pd.concat([bend,tmp],ignore_index=True)
#         for m in range(tmp.shape[0]):
#             t.append(m*freq[0])
#         plt.ylim(1000,2500)
#         # print(pd.DataFrame(t)[0],bend['val'])
#         plt.scatter(pd.DataFrame(t)[0],tmp['val'], marker='.',s=3,label='bend_{}'.format(j))
#     plt.title(plotName+'_bend_wear{}'.format(i))
#     plt.legend(loc='lower right')
#     plt.ylabel('resistance value(ohm)')
#     plt.xlabel('time(ms)')
#     plt.savefig('factor_study/takeoff_3gestures/'+plotName+'_bend_wear{}.png'.format(i))
#     plt.figure()        

