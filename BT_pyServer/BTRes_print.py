from pickle import NONE
import interface

interf = interface.interface()

def main():
    nSensor = 3
    row = 1
    iter = int(input("Please input the number of iterations: "))
    while iter != 0:
        interf.write(str(iter))
        for i in range(iter):
            avg = [0, 0, 0, 0, 0, 0, 0, 0]
            for j in range(20):
                for k in range(nSensor):
                    btIn = float(interf.read())
                    # while btIn == 0:
                    #     print(0)
                    #     btIn = float(interf.read())
                    avg[k] += btIn
            for k in range(nSensor):
                avg[k] /= 20
                res = 1000 * avg[k] * 3 / (5000 - avg[k] * 3)
                print(round(res, 2), end='\t')
            print()
        strIn = input("Please input the number of iteration (default = 1): ")
        if strIn == 'e':
            interf.end_process()
            break
        elif not strIn.isdigit():
            iter = 1
        else:
            iter = int(strIn)


if __name__ == '__main__':
    main()