#!/usr/bin/env python3
# -*- coding:utf-8 -*-

""" rpc : Remote Power Controller
    This's a tool to switch power ON or forcely OFF your PC by controlling xbee
    connected to power pin.
"""

from threading import Event
import time
import struct
import serial
import xbee

__author__ = "Takashi Ando"
__copyright__ = "Copyright 2015, My own project"
__license__ = "GPL"


class RemotePowerController(object):
    """ Main routine class for power control. """

    def __init__(self):
        self.frame_id = 0
        self.e = Event()

    def __call__(self, serial_port, serial_baurate, dest_addr_long):
        """ Press and release power button.

        Args:
            serial_port     string for serial port like "/dev/tty1"
            serial_baurate  serial baurate as integer
            dest_addr_long  destination address of xbee as int

        Returns:
            None but raise error event if some error.
        """
        self.ser = serial.Serial(serial_port, serial_baurate)
        self.bee = xbee.ZigBee(self.ser, escaped=True,
                               callback=self.__on_remote_command_done)

        # FIXME: command against pin number and paramter means high/low level
        self.__put_remote_command(dest_addr_long, "P0", 0x05)

        # FIXME: wait time will be set by argument
        time.sleep(1)

        # FIXME: command against pin number and paramter means high/low level
        self.__put_remote_command(dest_addr_long, "P0", 0x04)

        self.bee.halt()
        self.ser.close()

    def __put_remote_command(self, dest_addr_long, command, param):
        """ Put remote AT command to xbee client. This function can only support
            parameter with 1 byte like pin high/low.

        Args:
            dest_addr_long  destination address of xbee as int
            command         like "P0", "P1", ...
            param           like 0x05 which is parameter against the command.

        Returns:
            None but raise error event if some error.
        """

        self.e.clear()

        self.frame_id = self.frame_id + 1 if self.frame_id < 256 else 1

        self.bee.remote_at(
            dest_addr_long=struct.pack('>Q', dest_addr_long),
            command=command.encode("utf-8"),
            frame_id=int(self.frame_id).to_bytes(1, byteorder="big"),
            parameter=int(param).to_bytes(1, byteorder="big"))

        if self.e.wait(timeout=1) is not True:
            raise TimeoutError("AT command timeout error")

    def __on_remote_command_done(self, read_frame):
        """ Callback function which is called when xbee remote_at command
            finished. """

        print(read_frame)
        self.e.set()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="This's a tool to switch power ON or forcely OFF your PC")

    parser.add_argument(
        "-d", "--dest-addr-long",
        help="destination address of xbee terminal as hexdecimal",
        metavar="L",
        type=int,
        default=0x0013A20040AFBCCE)
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
        type=int,
        default=9600)

    parsed_args = parser.parse_args()
    kwargs = {key: value for key, value in parsed_args._get_kwargs()}

    main = RemotePowerController()
    main(**kwargs)
