import time
import csv

import board
import digitalio
import busio
import adafruit_lis3dh

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = digitalio.DigitalInOut(board.D5)  # Set to appropriate CS pin!
lis3dh = adafruit_lis3dh.LIS3DH_SPI(spi, cs)

lis3dh.range = adafruit_lis3dh.RANGE_2_G
lis3dh.data_rate = adafruit_lis3dh.DATARATE_1344_HZ

timestamp = int(time.time())
print(timestamp)

with open('data/xyz_{}.csv'.format(timestamp), 'w') as f:
    csv_writer = csv.writer(f)
    while True:
        try:
            csv_writer.writerow(lis3dh.acceleration)
            f.flush()
        except KeyboardInterrupt:
            break

# python3 -m http.server 8080 --directory data
