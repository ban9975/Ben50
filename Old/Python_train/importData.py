import pandas as pd
import sys

def res2len(z):
    x = 2.0
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
    # print(z)
    for i in range(3500):
        y = 1 + 0.0001 * i
        tmp = (p00 + p10*x + p01*y + p20*(x**2) + p11*x*y + p02*(y**2) + p21*(x**2)*y + p12*x*(y**2) + p03*(y**3)) * 10**5
        tmpErr = abs(tmp - z)
        print(tmp)
        if tmpErr < err:
            err = tmpErr
            len = y
    return len
# res2len(0)

class importData:
    def __init__(self, f):
        self.read(f)

    def read(self, f):
        data = pd.DataFrame()
        xls = pd.ExcelFile(f)
        for name in xls.sheet_names:
            data = pd.concat([data, xls.parse(name, usecols=[0,3,4,5,6]).drop(0, axis=0)], ignore_index=True)
        self.labels = data['gesture']
        self.features = data[[0,1,2,3]]

    def normalize(self):
        return 
    def res2len(self):
        self.features = self.features.applymap(res2len)




