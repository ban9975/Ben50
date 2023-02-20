import pandas as pd
import sys

def res2len(x,z):
    p00 = -0.937767447539916
    p10 = -0.039948024365072
    p01 = 2.587084207187248
    p20 = 0.000614994711211
    p11 = 0.067406486859726
    p02 = -2.365525377675638
    p21 = -0.000536654708327
    p12 = -0.027106092579830
    p03 = 0.717608771791744

    err = sys.maxsize
    len = 1
    for i in range(3500):
        y = 1 + 0.0001 * i
        tmp = (p00 + p10*x + p01*y + p20*(x**2) + p11*x*y + p02*(y**2) + p21*(x**2)*y + p12*x*(y**2) + p03*(y**3)) * 10**5
        tmpErr = abs(tmp - z)
        if tmpErr < err:
            err = tmpErr
            len = y
    return len
def calibration(z):
    p00 = -0.937767447539916
    p10 = -0.039948024365072
    p01 = 2.587084207187248
    p20 = 0.000614994711211
    p11 = 0.067406486859726
    p02 = -2.365525377675638
    p21 = -0.000536654708327
    p12 = -0.027106092579830
    p03 = 0.717608771791744

    err = sys.maxsize
    len = 1.8
    y = 1
    for i in range(30000):
        x = 1.8 + 0.0001 * i
        tmp = (p00 + p10*x + p01*y + p20*(x**2) + p11*x*y + p02*(y**2) + p21*(x**2)*y + p12*x*(y**2) + p03*(y**3)) * 10**5
        tmpErr = abs(tmp - z)
        if tmpErr < err:
            err = tmpErr
            len = x
    return len
def preprocessGes(cal,random):
    stretch = cal.sum()
    for i in range(4):
        stretch[i] = round(stretch[i]/cal.shape[0],2)
    for i in range(4):
        random[i] = random[i].map(lambda z:z-stretch[i])
    return random
def preprocessLen(cal,random):
    cal = cal.applymap(calibration)
    stretch = cal.sum()
    for i in range(4):
        stretch[i] = round(stretch[i]/cal.shape[0],2)
    for i in range(4):
        random[i] = random[i].map(lambda z:res2len(stretch[i],z)-1)
    return random

class importData:
    def __init__(self, f,mode):
        self.read(f,mode)

    def read(self, f,mode):
        data = pd.DataFrame()
        xls = pd.ExcelFile(f)
        tmp=pd.DataFrame()
        cal=pd.DataFrame()
        for name in xls.sheet_names:
            if "random" in name:
                tmp = xls.parse(name, usecols=[0,3,4,5,6])
                if mode == 0:
                    data = pd.concat([data, preprocessGes(cal,tmp)], ignore_index=True)
                else:
                    data = pd.concat([data, preprocessLen(cal,tmp)], ignore_index=True)
            elif "calibration" in name:
                cal = xls.parse(name, usecols=[3,4,5,6])
        self.labels = data['gesture']
        self.features = data[[0,1,2,3]]