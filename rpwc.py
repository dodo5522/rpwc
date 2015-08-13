#!/usr/bin/env python3
# -*- coding:utf-8 -*-

""" rpc : Remote Power Controller
    This's a tool to switch power ON or forcely OFF your PC by controlling xbee
    connected to power pin.
"""

import sys
from threading import Event
import argparse
import time
import struct
import serial
import xbee

__author__ = "Takashi Ando"
__copyright__ = "Copyright 2015, My own project"
__license__ = "GPL"


class Main(object):
    """ main routine class """

    def __init__(self, argv=sys.argv[1:]):
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

        self.parsed_args = parser.parse_args(argv)

        self.frame_id = 0
        self.e = Event()

    def __call__(self, *args, **kwargs):
        self.ser = serial.Serial(self.parsed_args.serial_port, self.parsed_args.serial_baurate)
        self.bee = xbee.ZigBee(self.ser, escaped=True, callback=self.__on_remote_command_done)

        # FIXME: command against pin number and paramter means high/low level
        self.__put_remote_command("P0", 0x05)

        # FIXME: wait time will be set by argument
        time.sleep(1)

        # FIXME: command against pin number and paramter means high/low level
        self.__put_remote_command("P0", 0x04)

        self.bee.halt()
        self.ser.close()

    def __put_remote_command(self, command, param):
        """ Put remote AT command to xbee client.
            This function can only support parameter with 1 byte like pin high/low.

        Args:
            command like "P0", "P1", ...
            param   like 0x05 which is parameter against the command.

        Returns:
            None but raise error event if some error.
        """

        self.e.clear()

        self.frame_id = self.frame_id + 1 if self.frame_id < 256 else 1

        self.bee.remote_at(
            dest_addr_long=struct.pack('>Q', int(self.parsed_args.dest_addr_long, 16)),
            command=command.encode("utf-8"),
            frame_id=int(self.frame_id).to_bytes(1, byteorder="big"),
            parameter=int(param).to_bytes(1, byteorder="big"))

        if self.e.wait(timeout=1) is not True:
            raise TimeoutError("AT command timeout error")

    def __on_remote_command_done(self, read_frame):
        """ Callback function which is called when xbee remote_at command finished. """

        print(read_frame)
        self.e.set()


if __name__ == "__main__":
    main = Main()
    main()
