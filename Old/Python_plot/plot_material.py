import matplotlib.pyplot as plt
import pandas as pd
import sys
import math

if len(sys.argv) < 3:
    print("No arguments.")
    sys.exit()
else:
    fileName = sys.argv[1]
    sheetName = sys.argv[2]
xls = pd.read_excel(fileName, sheet_name=sheetName)

while True:
    _length, _start, _end, _reps, _sets = input(
        "_length, _start, _end, _reps, _sets = "
    ).split()
    _length = float(_length)
    [_start, _end, _reps, _sets] = map(int, [_start, _end, _reps, _sets])
    rows = list(range(_start - 2, _end - 1))

    # x: stretching length
    data = [[0] * len(rows) for i in range(_sets)]
    axis_x = [0] * len(rows)
    # mean and standard deviation
    mean = [0] * len(rows)
    sigma = [0] * len(rows)
    for i in range(len(rows)):
        # axis_x[i] = xls[xls.columns[1]][rows[i]] * _length
        axis_x[i] = xls[xls.columns[0]][rows[i]]
        for j in range(_sets):
            for k in range(_reps):
                # Rubber sheet & jersey: 3 + _reps * j + k
                # Rubber cord & angle: 1 + _reps * j + k
                val = xls[xls.columns[1 + _reps * j + k]][rows[i]]
                data[j][i] += val
                mean[i] += val
                sigma[i] += val**2
            data[j][i] /= _reps
        mean[i] /= _sets * _reps
        sigma[i] = math.sqrt((sigma[i] / (_sets * _reps)) - mean[i] ** 2)
        # print('\nmean[{}] = {}'. format(i, mean[i]))
        # print('sigma[{}] = {}'. format(i, sigma[i]))
        # print()

    # # x: reps
    # data = [[0] * _reps for i in range(len(rows))]
    # axis_x = list(range(1, 1+_reps))
    # for i in range(len(rows)):
    #     for j in range(_reps):
    #         for k in range(_sets):
    #             data[i][j] += xls[xls.columns[1 + (_reps+1) * k + j]][rows[i]]
    #         data[i][j] /= _sets

    # plotting
    plotName = input("plotName = ")
    plt.figure(1)
    for i in range(_sets):
        # for i in range(len(rows)):
        plt.plot(axis_x, data[i], marker=".", label="Trial {}".format(i))
    plt.title(plotName)
    plt.ylabel("Resistance (Ohm)")
    plt.xlabel("Length (cm)")
    # plt.xlabel('Reps')
    # plt.xlabel('Angle (deg)')
    plt.legend(loc="lower right")
    plt.grid(True)
    # plt.savefig('../../5 Result/rubberCord/{}.png'.format(plotName))
    plt.show()
    # plt.close()

    # # mean and standard deviation
    # plt.figure(2)
    # plt.errorbar(axis_x, mean, sigma, marker=".", elinewidth=0.5, capsize=2)
    # plt.title("{} (Mean & Standard Deviation)".format(plotName))
    # plt.ylabel("Resistance (Ohm)")
    # plt.xlabel("Length (cm)")
    # plt.grid(True)
    # plt.savefig("../../5 Result/rubberCord/{}_SD.png".format(plotName))
    # plt.show()

    # if input("Press y to draw next plot: ") != "y":
    #     break
