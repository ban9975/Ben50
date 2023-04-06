import pandas as pd
import sys

def res2len(x,z):
    # # 246810 model
    # p00 = -0.937767447539916
    # p10 = -0.039948024365072
    # p01 = 2.587084207187248
    # p20 = 0.000614994711211
    # p11 = 0.067406486859726
    # p02 = -2.365525377675638
    # p21 = -0.000536654708327
    # p12 = -0.027106092579830
    # p03 = 0.717608771791744
    # 1234 model
    p00 = -0.507608259206727
    p10 = -0.051576376995291
    p01 = 1.415932591349663
    p20 = 0.000886341814277
    p11 = 0.090505524437003
    p02 = -1.309889655349322
    p21 = -0.000880377340775
    p12 = -0.037931428208836
    p03 = 0.401973570159907

    err = sys.maxsize
    len = 1
    for i in range(5000):
        y = 0.8 + 0.0001 * i
        tmp = (p00 + p10*x + p01*y + p20*(x**2) + p11*x*y + p02*(y**2) + p21*(x**2)*y + p12*x*(y**2) + p03*(y**3)) * 10**5
        tmpErr = abs(tmp - z)
        if tmpErr < err:
            err = tmpErr
            len = y
    return len
def calibration(z):
    # # 246810 model
    # p00 = -0.937767447539916
    # p10 = -0.039948024365072
    # p01 = 2.587084207187248
    # p20 = 0.000614994711211
    # p11 = 0.067406486859726
    # p02 = -2.365525377675638
    # p21 = -0.000536654708327
    # p12 = -0.027106092579830
    # p03 = 0.717608771791744
    # 1234 model
    p00 = -0.507608259206727
    p10 = -0.051576376995291
    p01 = 1.415932591349663
    p20 = 0.000886341814277
    p11 = 0.090505524437003
    p02 = -1.309889655349322
    p21 = -0.000880377340775
    p12 = -0.037931428208836
    p03 = 0.401973570159907

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
    nSensor = 4
    stretch = cal.sum()
    for i in range(nSensor):
        stretch[i] = round(stretch[i]/cal.shape[0],2)
    for i in range(nSensor):
        random[i] = random[i].map(lambda z:z-stretch[i])
    # pd.set_option('display.max_rows', None)
    # print(random)
    return random
def preprocessFirst(random):
    nSensor = 4
    for i in range(nSensor):
        if(i!=0):
            for j in range(random[i].size):
                random[i][j] = random[i][j]-random[0][j]
    random[0]=random[0].map(lambda z:0)
    return random
def preprocessLen(cal,random):
    nSensor = 4
    cal = cal.applymap(calibration)
    stretch = cal.sum()
    for i in range(nSensor):
        stretch[i] = round(stretch[i]/cal.shape[0],2)
    # print(stretch)
    for i in range(nSensor):
        random[i] = random[i].map(lambda z:res2len(stretch[i],z)-1)
    return random

class importData:
    def __init__(self, f,mode):
        self.read(f,mode)

    def read(self, f,mode):
        self.data = pd.DataFrame()
        xls = pd.ExcelFile(f)
        tmp=pd.DataFrame()
        cal=pd.DataFrame()
        for name in xls.sheet_names:
            if "random" in name:
                tmp = xls.parse(name, usecols=[0,3,4,5,6])
                # tmp = xls.parse(name, usecols=[0,3,4,5,6,7,8,9,10])
                if mode == 0:
                    self.data = pd.concat([self.data, preprocessGes(cal,tmp)], ignore_index=True)
                elif mode == 1:
                    self.data = pd.concat([self.data, preprocessLen(cal,tmp)], ignore_index=True)
                elif mode == 2:
                    self.data = pd.concat([self.data, tmp], ignore_index=True)
                else:
                    self.data = pd.concat([self.data,preprocessFirst(tmp)], ignore_index=True)
            elif "calibration" in name:
                cal = xls.parse(name, usecols=[3,4,5,6])
                # cal = xls.parse(name, usecols=[3,4,5,6,7,8,9,10])
        self.labels = self.data['gesture']
        self.features = self.data[[0,1,2,3]]
        # self.features = self.data[[1,3,5,7]]
        # self.features = self.data[[0,1,2,3,4,5,6,7]]
        # self.features = self.data[[1,2,3,4,5,6,7]]
        # self.features = self.data[[1,2,3,4]]
        # print(self.features)