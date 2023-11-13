import matplotlib.pyplot as plt
import importDataRaw
import os
from Rf import modes, gestures
colors=['#0080FF', '#FF9224', '#00EC00', '#CE0000','#ACD6FF','#FFDCB9','#BBFFBB','#FF9797']

class Plot:
    def plot_3d(self, trainFile, testFile, mode, path):
        self.train = importDataRaw.importData(trainFile, mode)
        self.test = importDataRaw.importData(testFile, mode)
        self.mode = mode
        self.plotName = path
        self.fig=plt.figure()
        ax = plt.axes(projection='3d')
        for i in range(len(gestures)):
            data=self.train.features[self.train.labels==i]
            ax.scatter(data[0],data[1],data[2],c=colors[i],s=5,label=gestures[i]+'_train')
        for i in range(len(gestures)):
            data=self.test.features[self.test.labels==i]
            ax.scatter(data[0],data[1],data[2],c=colors[i+len(gestures)],s=5,label=gestures[i]+'_test')
        ax.set_xlabel('Sensor 0')
        ax.set_ylabel('Sensor 1')
        ax.set_zlabel('Sensor 2')
        ax.legend(bbox_to_anchor=(0, 1.05))
        ax.set_title(f'{os.path.split(path)[1]}_{modes[mode]}')
        plt.savefig(f'{path}_{modes[mode]}.png',dpi=150,bbox_inches='tight')
    
    def plot_sensor(self, trainFile, testFile, mode, path):
        self.train = importDataRaw.importData(trainFile, mode)
        self.test = importDataRaw.importData(testFile, mode)
        self.mode = mode
        self.plotName = path
        for i in range(3):
            fig = plt.figure()
            ax = fig.add_subplot(1, 1, 1)
            print(self.train.features[i])
            print(self.train.labels)
            plt.scatter(self.train.features[i], self.train.labels, marker='.',label='train')
            plt.scatter(self.test.features[i], self.test.labels, marker='.',label='test')
            plt.title(f'{os.path.split(path)[1]} {modes[mode]}_{i}')
            plt.legend()
            plt.ylabel('gesture')
            plt.xlabel('calibration with '+modes[mode]+' data')
            ax.set_yticks([0, 1, 2, 3])
            plt.grid(True)
            plt.savefig(f'{path}_{modes[mode]}_{i}.png', dpi=150, bbox_inches='tight')