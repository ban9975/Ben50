from pickle import NONE
import interface
import time

import numpy as np
import time
import sys
import os

interf = interface.interface()

def main():
    iter = int(input("Please input the number of iterations: "))
    while iter != 0:
        interf.write(str(iter))
        for i in range(iter):
            avg = 0
            for j in range(20):
                # t = interf.read()
                btIn = float(interf.read())
                while btIn == 0:
                    btIn = float(interf.read())
                # print(100 * btIn / (1023 - btIn), end = ' ')
                # print(j, btIn)
                # print(t, 100 * btIn / (1023 - btIn))
                avg += btIn
            avg /= 20
            print(i + 1, 100 * avg / (1023 - avg))
        strIn = input("Please input the number of iteration (default = 1): ")
        if not strIn.isdigit():
            iter = 1
        else:
            iter = int(strIn)

    interf.end_process()


if __name__ == '__main__':
    main()