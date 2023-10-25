import joblib
import sys
import os
from BTController import BTController
import time

modelName = "/Users/adi/Documents/NTU/Lab/Ben50/Model/v8/7gestures_little_finger.joblib"
nSensor = 3
caliCnt = 15
model = joblib.load(modelName)
port = "/dev/cu.H-C-2010-06-01"
interf = BTController(port)
cali = [0 for i in range(nSensor)]

for i in range(caliCnt):
    _input = input(f"Calibration {i+1}")
    interf.write("1")
    avg = [0 for j in range(nSensor)]
    for j in range(20):
        for k in range(nSensor):
            btIn = float(interf.read())
            while btIn == 0:
                print(0)
                btIn = float(interf.read())
            avg[k] += btIn
    for k in range(nSensor):
        avg[k] = 1000 * avg[k] / 20 * 3 / (5000 - avg[k] / 20 * 3)
        cali[k] += avg[k]
    print(avg)
for k in range(nSensor):
    cali[k] /= caliCnt

while True:
    interf.write("1")
    avg = [0, 0, 0]
    for j in range(20):
        for k in range(nSensor):
            btIn = float(interf.read())
            while btIn == 0:
                print(0)
                btIn = float(interf.read())
            avg[k] += btIn
    for k in range(nSensor):
        avg[k] = 1000 * avg[k] / 20 * 3 / (5000 - avg[k] / 20 * 3)
        print(round(avg[k], 2), end="\t")
    print(model.predict([[a-c for a, c in zip(avg, cali)]])[0])
    time.sleep(0.1)
