import h5py
import numpy as np
from zmq_client import adc_to_voltage

def get_window(v):
    ind = np.argmin(v,axis=1)
    med = np.median(ind)
    # 20 ns window
    return med - 20, med + 20

if __name__ == '__main__':
    import argparse
    import matplotlib.pyplot as plt

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="input filename")
    args = parser.parse_args()

    f = h5py.File(args.filename)

    for i in range(1,5):
        dset = adc_to_voltage(f['c%i' % i][:])
        win = get_window(dset)
        charge = -np.trapz(dset[:,win[0]:win[1]])*1e3/2/50.0
        plt.subplot(2,2,i)
        plt.hist(charge,bins=100,log=True)
    plt.show()


