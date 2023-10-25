import matplotlib.pyplot as plt
import pandas as pd
import os
plotName = 'base_newPCB'
fileName = 'D://NTU/Ben50/Excel_data/factor/'+plotName+'.xlsx'
xls = pd.ExcelFile(fileName)
cnt=0

nRound=5
nWear=5
nGestures=2
names=xls.sheet_names
freq=[50,50,50,50]
if not os.path.exists('D://NTU/Ben50/Wristband_plots/factor_study/'+plotName+'/'):
    os.makedirs('D://NTU/Ben50/Wristband_plots/factor_study/'+plotName+'/')
for i in range(nWear):
    paper=pd.DataFrame()
    for j in range(nRound):
        t=[]
        tmp = xls.parse(names[i*nRound*nGestures+nGestures*j])
        for m in range(tmp.shape[0]):
            t.append(m*freq[0])
        plt.ylim(1000,2000)
        plt.scatter(pd.DataFrame(t)[0],tmp['val'], marker='.',s=3,label='paper_{}'.format(j))
    plt.title(plotName+'_paper_wear{}.png'.format(i))
    plt.legend(loc='lower right')
    plt.ylabel('resistance value(ohm)')
    plt.xlabel('time(ms)')
    plt.savefig('D://NTU/Ben50/Wristband_plots/factor_study/'+plotName+'/'+plotName+'_paper_wear{}.png'.format(i))
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
    plt.title(plotName+'_rock_wear{}'.format(i))
    plt.legend(loc='lower right')
    plt.ylabel('resistance value(ohm)')
    plt.xlabel('time(ms)')
    plt.savefig('D://NTU/Ben50/Wristband_plots/factor_study/'+plotName+'/'+plotName+'_rock_wear{}.png'.format(i))
    plt.figure()
# for i in range(nWear):
#     rock=pd.DataFrame()
#     for j in range(nRound):
#         t=[]        
#         tmp = xls.parse(names[i*nRound*nGestures+nGestures*j])
#         # rock=pd.concat([rock,tmp],ignore_index=True)
#         for m in range(tmp.shape[0]):
#             t.append(m*freq[0])
#         plt.ylim(3000,4000)
#         plt.scatter(pd.DataFrame(t)[0],tmp['val'], marker='.',s=3,label='uniform_{}'.format(j))
#     plt.title(plotName+'_uniform_wear{}'.format(i))
#     plt.legend(loc='lower right')
#     plt.ylabel('resistance value(ohm)')
#     plt.xlabel('time(ms)')
#     plt.savefig('D://NTU/Ben50/Wristband_plots/factor_study/'+plotName+'/'+plotName+'_uniform_wear{}.png'.format(i))
#     plt.figure()   
# for i in range(nWear):
#     rock=pd.DataFrame()
#     for j in range(nRound):
#         t=[]        
#         tmp = xls.parse(names[i*nRound*nGestures+nGestures*j+1])
#         # rock=pd.concat([rock,tmp],ignore_index=True)
#         for m in range(tmp.shape[0]):
#             t.append(m*freq[0])
#         plt.ylim(3000,4000)
#         plt.scatter(pd.DataFrame(t)[0],tmp['val'], marker='.',s=3,label='local_{}'.format(j))
#     plt.title(plotName+'_local_wear{}'.format(i))
#     plt.legend(loc='lower right')
#     plt.ylabel('resistance value(ohm)')
#     plt.xlabel('time(ms)')
#     plt.savefig('D://NTU/Ben50/Wristband_plots/factor_study/'+plotName+'/'+plotName+'_local_wear{}.png'.format(i))
#     plt.figure()   
