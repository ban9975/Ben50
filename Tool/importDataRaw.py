import pandas as pd
import sys


def res2len(x, z):
    p00 = -0.619036213083872
    p10 = -0.030800170966657
    p01 = 1.688322998396718
    p20 = -0.000611641511412
    p11 = 0.057794560352152
    p02 = -1.531793071531490
    p21 = 0.000488277935669
    p12 = -0.025444713548645
    p03 = 0.462421072634841

    err = sys.maxsize
    len = 1
    for i in range(5000):
        y = 0.8 + 0.0001 * i
        tmp = (
            p00
            + p10 * x
            + p01 * y
            + p20 * (x**2)
            + p11 * x * y
            + p02 * (y**2)
            + p21 * (x**2) * y
            + p12 * x * (y**2)
            + p03 * (y**3)
        ) * 10**5
        tmpErr = abs(tmp - z)
        if tmpErr < err:
            err = tmpErr
            len = y
    return len


def calibration(z):
    p00 = -0.619036213083872
    p10 = -0.030800170966657
    p01 = 1.688322998396718
    p20 = -0.000611641511412
    p11 = 0.057794560352152
    p02 = -1.531793071531490
    p21 = 0.000488277935669
    p12 = -0.025444713548645
    p03 = 0.462421072634841

    err = sys.maxsize
    len = 1.8
    y = 1
    for i in range(30000):
        x = 1.8 + 0.0001 * i
        tmp = (
            p00
            + p10 * x
            + p01 * y
            + p20 * (x**2)
            + p11 * x * y
            + p02 * (y**2)
            + p21 * (x**2) * y
            + p12 * x * (y**2)
            + p03 * (y**3)
        ) * 10**5
        tmpErr = abs(tmp - z)
        if tmpErr < err:
            err = tmpErr
            len = x
    return len


def preprocessGes(cal, random):
    nSensor = 3
    cali = cal.sum()
    for i in range(nSensor):
        cali[i] = round(cali[i] / cal.shape[0], 2)
    for i in range(nSensor):
        random[i] = random[i].map(lambda z: z - cali[i])
    return random


def preprocessFirst(random):
    nSensor = 3
    for i in range(nSensor):
        if i != 0:
            for j in range(random[i].size):
                random[i][j] = random[i][j] - random[0][j]
    random[0] = random[0].map(lambda z: 0)
    return random


def preprocessAverage(cal, random):
    nSensor = 3
    avg = cal.sum()
    for i in range(nSensor):
        avg[i] = round(avg[i] / cal.shape[0], 2)
    for i in range(nSensor):
        random[i] = random[i].map(lambda z: z - avg[i])
    print(avg)
    return random


def preprocessLen(cal, random):
    nSensor = 3
    cal = cal.applymap(calibration)
    cali = cal.sum()
    for i in range(nSensor):
        cali[i] = round(cali[i] / cal.shape[0], 2)
    for i in range(nSensor):
        random[i] = random[i].map(lambda z: res2len(cali[i], z) - 1)
    return random


def preprocessNorm(cal, random):
    nSensor = 3
    cali = cal.sum()
    for i in range(nSensor):
        cali[i] = round(cali[i] / cal.shape[0], 2)
    for i in range(nSensor):
        random[i] = random[i].map(lambda z: (z - cali[i]) / cali[i])
    return random


class importData:
    def __init__(self, f, mode):
        self.read(f, mode)

    def read(self, f, mode):
        self.data = pd.DataFrame()
        xls = pd.ExcelFile(f)
        tmp = pd.DataFrame()
        cal = pd.DataFrame()
        for name in xls.sheet_names:
            if "random" in name:
                # raw
                # tmp = xls.parse(name, usecols=[0,3,4,5])
                # rawraw
                tmp = pd.DataFrame(
                    [
                        round(
                            xls.parse(name, usecols=[i + 3 for i in range(20)]).sum(
                                axis=1
                            )
                            / 20,
                            2,
                        ),
                        round(
                            xls.parse(name, usecols=[i + 3 for i in range(20, 40)]).sum(
                                axis=1
                            )
                            / 20,
                            2,
                        ),
                        round(
                            xls.parse(name, usecols=[i + 3 for i in range(40, 60)]).sum(
                                axis=1
                            )
                            / 20,
                            2,
                        ),
                    ]
                ).T
                tmp['gesture'] = xls.parse(name, usecols=[0])
                if mode == 0:
                    self.data = pd.concat(
                        [self.data, preprocessGes(cal, tmp)], ignore_index=True
                    )
                elif mode == 1:
                    self.data = pd.concat(
                        [self.data, preprocessLen(cal, tmp)], ignore_index=True
                    )
                elif mode == 2:
                    self.data = pd.concat([self.data, tmp], ignore_index=True)
                elif mode == 3:
                    self.data = pd.concat(
                        [self.data, preprocessFirst(tmp)], ignore_index=True
                    )
                elif mode == 4:
                    self.data = pd.concat(
                        [self.data, preprocessAverage(cal, tmp)], ignore_index=True
                    )
                elif mode == 5:
                    self.data = pd.concat(
                        [self.data, preprocessNorm(cal, tmp)], ignore_index=True
                    )
            elif "calibration" in name:
                # raw
                # cal = xls.parse(name, usecols=[3, 4, 5])
                # rawraw
                cal = pd.DataFrame([round(xls.parse(name, usecols=[i+3 for i in range(20)]).sum(axis=1)/20, 2), round(xls.parse(name, usecols=[i+3 for i in range(20, 40)]).sum(axis=1)/20, 2), round(xls.parse(name, usecols=[i+3 for i in range(40, 60)]).sum(axis=1)/20, 2)]).T
        self.labels = self.data["gesture"]
        self.features = self.data[[0, 1, 2]]
