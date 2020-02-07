import sys
import matplotlib.pyplot as plt
import matplotlib.animation as mani
import requests
import numpy as np

ip = sys.argv[1]
timestamp = sys.argv[2]

session = requests.Session()
fig, axarr = plt.subplots(3, sharex=True)


def animate(i):
    resp = session.get(
        'http://{}:8080/xyz_{}.csv'.format(ip, timestamp),
        stream=True
    ).raw
    components = np.loadtxt(resp, delimiter=',', unpack=True)
    for axis, component, title in zip(axarr, components, ['X', 'Y', 'Z']):
        axis.clear()
        axis.plot(component)
        axis.set_title(title)


ani = mani.FuncAnimation(fig, animate, interval=100)

plt.show()
