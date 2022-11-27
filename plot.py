import matplotlib.pyplot as plt
import pandas as pd
import sys

if len(sys.argv) < 3:
    print('No arguments.')
    sys.exit()
else:
    fileName = sys.argv[1]
    sheetName = sys.argv[2]
xls = pd.read_excel(fileName, sheet_name=sheetName)

while(True):
    _length, _start, _end, _reps, _sets = map(int, input('_length, _start, _end, _reps, _sets = ').split())
    rows = list(range(_start - 2, _end - 1))
    data = [[0] * len(rows) for i in range(_sets)]
    axis_x = [0] * len(rows)
    for i in range(len(rows)):
        axis_x[i] = xls[xls.columns[0]][rows[i]] * _length
        for j in range(_sets):
            for k in range(_reps):
                # print(xls[xls.columns[1 + (_reps+1) * j + k]][rows[i]], end = ' ')
                data[j][i] += xls[xls.columns[1 + (_reps+1) * j + k]][rows[i]]
            data[j][i] /= _reps
    
    # plotting
    plotName = input('plotName = ')
    for i in range(_sets):
        plt.plot(axis_x, data[i], marker = '.')
    plt.title(plotName)
    plt.ylabel('Resistance (Ohm)')
    plt.xlabel('Length (cm)')
    # plt.xlabel('Aangle (deg)')
    plt.grid(True)
    plt.savefig('fig/{}.png'.format(plotName))
    plt.show()
    

    if input('Press y to draw next plot: ') != 'y':
        break