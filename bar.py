from __future__ import print_function, division
import h5py
import numpy as np
from zmq_client import adc_to_voltage
import sys
from scipy.stats import norm
from scipy.optimize import fmin

def get_window(v):
    ind = np.argmin(v[np.min(v,axis=1) < -10],axis=1)
    med = np.median(ind)
    # 20 ns window
    return med - 20, med + 20

def get_time(v):
    t = np.empty(v.shape[0],dtype=float)
    for i in range(len(v)):
        if i % 100 == 0:
            print("\r%i/%i" % (i+1,len(v)),end='')
            sys.stdout.flush()
        j = np.argmin(v[i])
        disc = v[i,j]*0.4
        while v[i,j] < disc and j > 0:
            j -= 1
        t[i] = j + (disc - v[i,j])/(v[i,j+1] - v[i,j])
    print()
    return t

def fit_gauss(x,bins):
    mean = -2.0#np.mean(x)
    std = 2.0
    bincenters = (bins[1:] + bins[:-1])/2
    hist, _ = np.histogram(x,bins)
    hist_sigma = hist.copy()
    hist_sigma[hist == 0] = 1
    def foo(args):
        mu, std, c = args
        pdf = c*norm.pdf(bincenters,mu,std)
        return np.sum((pdf-hist)**2/hist_sigma)

    return fmin(foo,[mean,std,1000])

if __name__ == '__main__':
    import argparse
    import matplotlib.pyplot as plt

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', help="input filename")
    args = parser.parse_args()

    f = h5py.File(args.filename)

    for i in range(1,5):
        dset = f['c%i' % i][:]
        win = get_window(dset)
        charge = -adc_to_voltage(np.trapz(dset[:,win[0]:win[1]]))*1e3/2/50.0
        if i == 1:
            filter = charge < 10.0
            t1 = get_time(dset)
            t = t1.copy()[(charge > 0.25) & filter]
        else:
            t = get_time(dset) - t1
            t = t[(charge > 0.25) & filter]
        t *= 0.5 # -> ns
        t -= np.mean(t)
        result = fit_gauss(t,bins=np.arange(-50,50,0.5))
        print(result)
        mu, std, c = result
        plt.figure(1)
        plt.subplot(2,2,i)
        plt.hist(charge,bins=np.arange(0,10,0.05),log=True)
        plt.xlabel('Charge (pC)')
        plt.figure(2)
        plt.subplot(2,2,i)
        plt.hist(t,bins=np.arange(-50,50,0.5))
        x = np.linspace(-50,50,1000)
        plt.plot(x,c*norm.pdf(x,mu,std))
        plt.xlabel('Time (ns)')
        plt.title(r'$\sigma$ = %.2f' % std)
        plt.xlim(-10,10)
    plt.show()


