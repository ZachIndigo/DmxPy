import argparse
import math

import serial
from serial.tools import list_ports
import tempfile
import os


def grep_ports(grep):
    ports = list(list_ports.grep(grep))
    assert len(ports) == 1, 'more than 1 port matching %s' % grep
    port = ports[0]
    return port.device


class DmxPy:
    def __init__(self, serial_port=None, baud_rate=57600,
                 port_grep='0403:6001', channel_data='00', mod_type='set',
                 dmx_size=64, path=''):
        self.dmx_size = dmx_size
        self.dmx_cache_fname = os.path.join(
            tempfile.gettempdir(), 'dmx_cache.txt')

        if serial_port is None:
            serial_port = grep_ports(port_grep)
            print('Found DMX device matching %s at' % port_grep, serial_port)
        try:
            self.serial = serial.Serial(serial_port, baudrate=baud_rate)
        except serial.SerialException:
            print('Error: could not open Serial Port:', serial_port)
            exit(1)

        try:
            if (path):
                f = open(path, 'r')
            else:
                f = open(self.dmx_cache_fname, 'r')
            with f:
                self.dmxData = [0]
                for line in f:
                    dc = line[:-1]
                    self.dmxData.append(int(dc))
        except OSError:
            print("No DMX cache file found. Initiate new channel array.")
            self.dmxData = [0] + [0] * self.dmx_size

        self.set_channels(channel_data, mod_type)

    def blackout(self):
        self.dmxData = [0] + [0] * self.dmx_size

    def set_channels(self, channel_data, mod_type):
        for x in range(0, len(channel_data), 2):
            channel = math.floor(x/2) + 1
            dmx_data = channel_data[x] + channel_data[x+1]
            if (dmx_data != 'xx'):
                if mod_type == 'up':
                    self.dmxData[channel] += int(dmx_data, 16)
                elif mod_type == 'down':
                    self.dmxData[channel] -= int(dmx_data, 16)
                else:
                    self.dmxData[channel] = int(dmx_data, 16)
                self.dmxData[channel] = min(255, self.dmxData[channel])
                self.dmxData[channel] = max(0, self.dmxData[channel])

    def render(self):
        dmx_open = [0x7E]
        dmx_close = [0xE7]
        dmx_intensity = [6, (self.dmx_size + 1) & 0xFF,
                         (self.dmx_size + 1) >> 8 & 0xFF]
        self.serial.write(
            bytearray(dmx_open + dmx_intensity + self.dmxData + dmx_close))

        # write data to file
        with open(self.dmx_cache_fname, 'w') as filehandle:
            self.dmxData.pop(0)
            for dc in self.dmxData:
                filehandle.write(f'{dc}\n')


def main():
    parser = argparse.ArgumentParser(description='Control Enttec DMX USB Pro')
    parser.add_argument('-r', '--rate', type=int, default=57600,
                        help='baud rate for USB communication '
                             '(default: 57600)')
    parser.add_argument('-p', '--port', type=str,
                        help='Serial(COM) port, e.g., /dev/ttyUSB1 or COM3')
    parser.add_argument('-g', '--port-grep', type=str, default='0403:6001',
                        help='if port not specified attempt to auto-detect '
                             'serial matching grep (default: 0403:6001)')
    parser.add_argument('-c', '--channel_data', type=str, default='00',
                        help='channel data sent as pairs of hex, ie FFFF \
                                would be max level for channel 1 and 2')
    parser.add_argument('-t', '--mod-type', type=str, default='set',
                        help='Specify whether channel data is set, up or down \
                                (default: set)')
    parser.add_argument('-s', '--size', type=int, default=64, help='DMX Size \
            (default: 64)')
    parser.add_argument('-f', '--path', type=str, default='', help='File to \
            load DMX channel presets')
    parser.add_argument('-b', '--blackout', action='store_true', help='Turn \
            off all channels (level=0)')

    args = parser.parse_args()
    dmx = DmxPy(args.port, baud_rate=args.rate, port_grep=args.port_grep,
                channel_data=args.channel_data, mod_type=args.mod_type,
                dmx_size=args.size, path=args.path)

    if args.blackout:
        dmx.blackout()
        dmx.render()
    elif args.channel_data != '00':
        dmx.render()
    else:
        print('Error, no channel data specified. Too blackout, choose -b.')
