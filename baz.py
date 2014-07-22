import h5py
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    import argparse
    import matplotlib.pyplot as plt

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="input filename")
    args = parser.parse_args()

    f = h5py.File(args.filename)

    plt.ion()

    for i in range(100):
        plt.cla()
        for j in range(1,5):
            plt.plot(f['c%i' % j][i])
        raw_input()
