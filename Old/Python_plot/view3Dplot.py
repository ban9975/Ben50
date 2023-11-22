import matplotlib.pyplot as plt
import pickle
import os
BASE_DIR = os.path.dirname(os.path.realpath(__file__))+'/../'
version='v8'
fileName='7gestures_'
modes = ['gesture', 'length', 'raw data', 'first round', 'avg']
mode = int(input("0: gesture, 1: length, 2: raw, 3: first round, 4: avg : "))
figx = pickle.load(open(BASE_DIR + 'Wristband_plots/versions/'+version+'/'+fileName+modes[mode]+'.pickle', 'rb'))
plt.show()