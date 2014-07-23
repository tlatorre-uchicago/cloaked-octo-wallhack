from __future__ import print_function
from zmq_client import V1729Client

digi = V1729Client('hollande.uchicago.edu',5555)
digi.set_trigger_source(1)
digi.set_trigger_type(3,'falling')
digi.set_trigger_threshold(-5e-3) # -10 mV

if __name__ == '__main__':
    import sys
    import h5py
    import argparse
    import time

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', dest='filename', default='output.hdf5')
    parser.add_argument('-n', dest='N', default=1000, type=int,
                        help='number of events')
    args = parser.parse_args()

    f = h5py.File(args.filename,'w')
    for i in range(1,5):
        dset = f.create_dataset('c%i' % i, (args.N, 2520), chunks=(10,2520),
                                dtype='i', compression='gzip')

    t0 = time.time()
    for i in range(args.N):
        if i % 10 == 0:
            print('\r%i/%i, %.2f Hz' % (i+1,args.N,(i+1)/(time.time() - t0)),end='')
            sys.stdout.flush()
        try:
            digi.start_acquisition()
            while not digi.poll():
                time.sleep(0.01)
            data = digi.data()
            for j, v in enumerate(data.T):
                f['c%i' % (j+1)][i] = v
        except KeyboardInterrupt:
            break
    print()
