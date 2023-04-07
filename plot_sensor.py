import matplotlib.pyplot as plt
import pandas as pd
import sys
import math
mode=int(input('mode='))
modes=['ges','len','raw','first','ges+first']
<<<<<<< HEAD
trainName = 'data_cal/v7/adi_v3_1ADC_cal_'+modes[mode]+'_train.xlsx'
testName = 'data_cal/v7/adi_v3_1ADC_cal_'+modes[mode]+'_test.xlsx'
sheetName = "Sheet1"
plotName = 'v7_adi_v3_1ADC'
=======
trainName = 'data_cal/v6/adi_v3_1ADC_cal_'+modes[mode]+'_train.xlsx'
testName = 'data_cal/v6/adi_v3_1ADC_cal_'+modes[mode]+'_test.xlsx'
sheetName = "Sheet1"
plotName = 'v6_adi_v3_1ADC'
>>>>>>> 24fff41605d5655314c019461436c1761ae1f765
train = pd.read_excel(trainName, sheet_name=sheetName)
test = pd.read_excel(testName, sheet_name=sheetName)

# plotting
for i in range(4):
    plt.figure()
    if mode==0:
        plt.xlim(-100,100)
    elif mode==1:
        plt.xlim(-0.015,0.015)
    elif mode==2:
        plt.xlim(200,400)
    elif mode==3:
        plt.xlim(-130,130)
    elif mode==4:
        plt.xlim(-40,40)
    plt.scatter(train[i],train['gesture'], marker='.',label='train')
    plt.scatter(test[i],test['gesture'], marker='.',label='test')
    plt.title(plotName+' '+modes[mode]+'_{}'.format(i))
    plt.legend()
    plt.ylabel('gesture')
    plt.xlabel('calibration with '+modes[mode]+' data')
    plt.grid(True)
    plt.savefig('sensor_fig/fix_scale/'+modes[mode]+'/'+plotName+'_{}'.format(i)+'.png')
