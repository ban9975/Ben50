import matplotlib.pyplot as plt
import os
import pandas as pd
import pickle
modes = ['gesture', 'length', 'raw data', 'first round', 'avg']
mode = int(input("0: gesture, 1: length, 2: raw, 3: first round, 4: avg : "))
# colors=['#0080FF', '#FF9224', '#00EC00', '#CE0000','#ACD6FF','#FFDCB9','#BBFFBB','#FF9797']
colors=['#0080FF', '#FF9224', '#00EC00', '#CE0000','#921AFF','#B9B973','#C07AB8','#ACD6FF','#FFDCB9','#BBFFBB','#FF9797','#DCB5FF','#DEDEBE','#E2C2DE']
# gestures = ['down', 'up', 'paper','rock']
gestures = ['down', 'up', 'paper', 'rock','thumb', 'little finger', 'rest']
BASE_DIR = os.path.dirname(os.path.realpath(__file__))+'/../'
version='v8'
fileName='7gestures_'
trainFile = BASE_DIR + 'Excel_data/calibrated/'+version+'/'+fileName+modes[mode]+'_train.xlsx'
testFile = BASE_DIR + 'Excel_data/calibrated/'+version+'/'+fileName+modes[mode]+'_test.xlsx'
train=pd.read_excel(trainFile)
test=pd.read_excel(testFile)
fig=plt.figure()
ax = plt.axes(projection='3d')
for i in range(len(gestures)):
    data=train[train['gesture']==i]
    ax.scatter(data[0],data[1],data[2],c=colors[i],s=5,label=gestures[i]+'_train')
for i in range(len(gestures)):
    data=test[test['gesture']==i]
    ax.scatter(data[0],data[1],data[2],c=colors[i+len(gestures)],s=5,label=gestures[i]+'_test')
ax.set_xlabel('Sensor 0')
ax.set_ylabel('Sensor 1')
ax.set_zlabel('Sensor 2')
ax.legend(bbox_to_anchor=(0, 1.05))
ax.set_title(version+'_'+fileName+modes[mode])
plt.savefig(BASE_DIR + 'Wristband_plots/versions/'+version+'/'+fileName+modes[mode]+'.png',dpi=150,bbox_inches='tight')
pickle.dump(fig, open(BASE_DIR + 'Wristband_plots/versions/'+version+'/'+fileName+modes[mode]+'.pickle', 'wb'))