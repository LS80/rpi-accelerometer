import time
import csv
import os
import multiprocessing as mp
import socketserver
import http.server
from functools import partial

import board
import digitalio
import busio
import adafruit_lis3dh

PORT = 8080
DIRECTORY = 'data'

def serve_files():
    Handler = partial(http.server.SimpleHTTPRequestHandler, directory=DIRECTORY)

    with socketserver.TCPServer(('0.0.0.0', PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()

def write_data():
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    cs = digitalio.DigitalInOut(board.D5)  # Set to appropriate CS pin!
    lis3dh = adafruit_lis3dh.LIS3DH_SPI(spi, cs)

    lis3dh.range = adafruit_lis3dh.RANGE_2_G
    lis3dh.data_rate = adafruit_lis3dh.DATARATE_1344_HZ

    timestamp = int(time.time())
    print(timestamp)

    with open(os.path.join(DIRECTORY, 'xyz_{}.csv'.format(timestamp)), 'w') as f:
        csv_writer = csv.writer(f)
        while True:
            try:
                csv_writer.writerow(lis3dh.acceleration)
                f.flush()
            except KeyboardInterrupt:
                break

if __name__ == '__main__':
    os.makedirs(DIRECTORY, exist_ok=True)

    mp.set_start_method('spawn')
    p = mp.Process(target=serve_files)
    p.start()
    p.join()

    write_data()

# python3 -m http.server 8080 --directory data
