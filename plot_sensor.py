import matplotlib.pyplot as plt
import pandas as pd
import sys
import math

trainName = 'data_cal/v4Plus/adi_v3_1ADC_round2_cal_ges_train.xlsx'
testName = 'data_cal/v4Plus/adi_v3_1ADC_round2_cal_ges_test.xlsx'
sheetName = "Sheet1"
plotName = "v4Plus_adi_v3_1ADC_round2_ges"
train = pd.read_excel(trainName, sheet_name=sheetName)
test = pd.read_excel(testName, sheet_name=sheetName)

# plotting
for i in range(4):
    plt.figure()
    plt.scatter(train[i],train['gesture'], marker='.',label='train')
    plt.scatter(test[i],test['gesture'], marker='.',label='test')
    plt.title(plotName+'{}'.format(i))
    plt.legend()
    plt.ylabel('gesture')
    plt.xlabel('calibration with gesture data')
    plt.grid(True)
    plt.savefig('sensor_fig/'+plotName+'{}_'.format(i)+'.png')
