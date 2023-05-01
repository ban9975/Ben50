import matplotlib.pyplot as plt
import pandas as pd
import sys

if len(sys.argv) < 3:
    print('No arguments.')
    sys.exit()
else:
    fileName = sys.argv[1]
    sheetName = sys.argv[2]
    print(fileName)
    print(sheetName)
xls = pd.read_excel(fileName, sheet_name=sheetName)

while(True):
    _start=list(map(int,input('_start=').split()))
    _end=list(map(int,input('_end=').split()))
    _sets, _lines = map(int, input('_sets , _lines= ').split())
    # rows = list(range(_start - 2, _end - 1))
    data=[]
    axis_x=[]
    for k in range(_lines):
        rows = list(range(_start[k]-2, _end[k]-1))
        # print(rows)
        data.append([0] * len(rows))
        axis_x.append([0] * len(rows))
        for i in range(len(rows)):
            axis_x[k][i] = xls[xls.columns[0]][rows[i]] #overall total
            # axis_x[k][i] = xls[xls.columns[0]][rows[i]]-xls[xls.columns[0]][rows[0]] #overall stretch
            # print(axis_x[k][i])
            for j in range(_sets):
                # print(k,i)
                data[k][i] += xls[xls.columns[1 + j]][rows[i]]
            data[k][i]/=_sets
    
    # plotting
    plotName = input('plotName = ')
    for i in range(_lines):
        plt.plot(axis_x[i], data[i], marker = '.')
    plt.title(plotName)
    plt.ylabel('Resistance (Ohm)')
    plt.xlabel('Length + Stretch (cm)')
    # plt.xlabel('Aangle (deg)')
    plt.grid(True)
    plt.savefig('d:/NTU/111-1/lab/Ben50/Ben50/fig/{}.png'.format(plotName))
    plt.show()
    

    if input('Press y to draw next plot: ') != 'y':
        break