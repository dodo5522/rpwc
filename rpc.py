#!/usr/bin/env python3
# -*- coding:utf-8 -*-

""" rpc : Remote Power Controller
    This's a tool to switch power ON or forcely OFF your PC by controlling xbee
    connected to power pin.
"""

import sys
import argparse
import time
import struct
import serial
import xbee

__author__ = "Takashi Ando"
__copyright__ = "Copyright 2015, My own project"
__license__ = "GPL"


def init_args(argv=sys.argv[1:]):
    """ Parse arguments.
    """
    parser = argparse.ArgumentParser(
        description="This's a tool to switch power ON or forcely OFF your PC")

    parser.add_argument(
        "-d", "--dest-addr-long",
        help="destination address of xbee terminal as hexdecimal",
        metavar="L",
        type=str,
        default="0x0013A20040AFBCCE")
    parser.add_argument(
        "-p", "--serial-port",
        help="serial port device file path to communicate with xbee terminal",
        metavar="M",
        type=str,
        default="/dev/ttyAMA0")
    parser.add_argument(
        "-b", "--serial-baurate",
        help="serial port baurate",
        metavar="N",
        type=str,
        default="9600")

    args = parser.parse_args(argv)

    return args


def __on_remote_at_finished(read_frame):
    """ Callback function which is called when xbee remote_at command finished.
    """
    print(read_frame)


def main(args):
    """ main function
    """
    ser = serial.Serial(args.serial_port, args.serial_baurate)
    bee = xbee.ZigBee(ser, escaped=True, callback=__on_remote_at_finished)

    bee.remote_at(
        dest_addr_long=struct.pack('>Q', int(args.dest_addr_long, 16)),
        command="P0".encode("utf-8"), frame_id=b'\x01', parameter=b'\x05')
    time.sleep(3)

    bee.remote_at(
        dest_addr_long=struct.pack('>Q', int(args.dest_addr_long, 16)),
        command="P0".encode("utf-8"), frame_id=b'\x01', parameter=b'\x04')

    bee.halt()
    ser.close()

if __name__ == "__main__":
    args = init_args()
    main(args)
