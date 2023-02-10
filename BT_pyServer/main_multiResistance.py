from pickle import NONE
import interface

interf = interface.interface()

def main():
    row = 1
    iter = int(input("Please input the number of iterations: "))
    while iter != 0:
        interf.write(str(iter))
        for i in range(iter):
            avg = [0, 0, 0, 0]
            for j in range(20):
                for k in range(4):
                    btIn = float(interf.read())
                    while btIn == 0:
                        print(0)
                        btIn = float(interf.read())
                    avg[k] += btIn * 3
            for k in range(4):
                avg[k] /= 20
                res = 100 * avg[k] / (5000 - avg[k])
                print(round(res, 2), end='\t')
            print()
        strIn = input("Please input the number of iteration (default = 1): ")
        if not strIn.isdigit():
            iter = 1
        else:
            iter = int(strIn)

    interf.end_process()


if __name__ == '__main__':
    main()