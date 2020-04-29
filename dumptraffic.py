#!/usr/bin/env python3
import csv
from datetime import datetime


NETWORK_STATS_FILE = '/proc/net/dev'
OUTPUT_FILE = '/home/bdmbdsm/net_stats.csv'
INTERFACE_NAME = 'wlo1'
RX_ROW_START_POSITION = 1
RX_ROW_END_POSITION = 8
TX_ROW_START_POSITION = 9
TX_ROW_END_POSITION = 16
HEADER = ['bytes', 'packets', 'errs', 'drop', 'fifo', 'frame', 'compressed', 'multicast']


def read_interface_line(interface):
    with open(NETWORK_STATS_FILE, 'r') as f:
        lines = f.readlines()

    for line in lines:
        if INTERFACE_NAME in line:
            return line


def parse_if_line(interface_line):
    parsed = {
        'RX': {},
        'TX': {}
    }

    il = interface_line.strip()
    il = interface_line.split()

    RX_data = il[RX_ROW_START_POSITION:RX_ROW_END_POSITION+1]
    TX_data = il[TX_ROW_START_POSITION:TX_ROW_END_POSITION+1]

    RX_with_header = zip(HEADER, RX_data)
    TX_with_header = zip(HEADER, TX_data)
    
    for rx_param in RX_with_header:
        parsed['RX'][rx_param[0]] = rx_param[1]

    for tx_param in TX_with_header:
        parsed['TX'][tx_param[0]] = tx_param[1]

    return parsed



def main():
    il = read_interface_line(INTERFACE_NAME)
    traffic_data = parse_if_line(il)
    time_now = datetime.now().isoformat()

    rx = int(traffic_data['RX']['bytes']) / 1024**2
    tx = int(traffic_data['TX']['bytes']) / 1024**2

    rx = round(rx, 3)
    tx = round(tx, 3)

    with open(OUTPUT_FILE, 'a') as f:
        writer = csv.writer(f, delimiter=',',dialect='excel')
        writer.writerow([time_now, rx, tx])


if __name__ == '__main__':
    main()
