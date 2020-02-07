import argparse

import matplotlib.pyplot as plt
import matplotlib.animation as mani
import requests
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('ip', help='IP address of the acceleration data web server')
parser.add_argument('timestamp', help='Timestamp of the CSV data file')
args = parser.parse_args()

session = requests.Session()
fig, axarr = plt.subplots(3, sharex=True)

def animate(i):
    resp = session.get(
        'http://{}:8080/xyz_{}.csv'.format(args.ip, args.timestamp),
        stream=True
    ).raw
    components = np.loadtxt(resp, delimiter=',', unpack=True)
    for axis, component, title in zip(axarr, components, ['X', 'Y', 'Z']):
        axis.clear()
        axis.plot(component)
        axis.set_title(title)


ani = mani.FuncAnimation(fig, animate, interval=100)

plt.show()
