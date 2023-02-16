from pickle import NONE
import interface
import time
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from itertools import count
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation

import numpy as np
import time
import sys
import os

result=[]
t=[]
index = count()
interf = interface.interface()
ani = None

def animate(i):
    num = next(index)
    # print(num)
    # result.append(num)
    # t.append(num)
    _t = interf.read()
    _result = interf.read()
    if _result == 65535:
        global ani
        print('stop')
        interf.end_process()
        print('end_process')
        ani.event_source.stop()
        print('event_stop')
    else:
        _result = 100 * _result / (1023 - _result)
    print(_t, _result)
    t.append(_t)
    result.append(_result)
    if i > 100:
        result.pop(0)
        t.pop(0)

    else:
        plt.cla()
        plt.plot(t, result)
    # print(result[-1],t[-1])

def main():
    global ani
    ani = FuncAnimation(plt.gcf(), animate, interval=10)
    print(44)
    plt.tight_layout()
    print(46)
    plt.show()
    print(48)

if __name__ == '__main__':
    main()
