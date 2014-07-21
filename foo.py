from zmq_client import V1729Client

client = V1729Client('hollande.uchicago.edu',5555)
client.set_trigger_source(1)
client.set_trigger_type(3,'falling')
client.set_trigger_threshold(-20e-3) # -20 mV

if __name__ == '__main__':
    import matplotlib.pyplot as plt

    data = client.get_data()
    plt.plot(data)
    plt.show()
