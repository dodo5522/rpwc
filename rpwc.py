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


class TimeoutError(Exception):
    pass


class RemotePowerController(object):
    """ Main routine class for power control. """
    PIN_LEVEL_HIGH = 0x05
    PIN_LEVEL_LOW = 0x04

    def __init__(self, serial_port, serial_baurate,
                 xbee_dest_addr, xbee_gpio_power, **kwargs):
        """ Initialize object.

        Args:
            serial_port       string for serial port like "/dev/tty1"
            serial_baurate    serial baurate as integer
            xbee_dest_addr    XBee address to be controlled
            xbee_gpio_power   like "P0", "P1", etc.

        Returns:
            None but raise error event if some error.
        """
        self.frame_id = 0
        self.e = Event()

        self.ser = serial.Serial(serial_port, int(serial_baurate))

        self.xbee_dest_addr = int(xbee_dest_addr, 16) if type(xbee_dest_addr) is str else xbee_dest_addr
        self.xbee_gpio_power = xbee_gpio_power
        self.bee = None

    def press_power_button(self, callback=None):
        """ Put remote AT command as pushing power buttion. This function does
            same operation as sending remote AT command to set high level to a
            GPIO pin.

        Args:
            callback    callable object to get response from remote xbee

        Returns:
            None but raise error event if some error.
        """
        self.put_remote_command(
            self.xbee_dest_addr, self.xbee_gpio_power, self.PIN_LEVEL_HIGH,
            callback)

    def release_power_button(self, callback=None):
        """ Put remote AT command as releasing power buttion. This function does
            same operation as sending remote AT command to set low level to a
            GPIO pin.

        Args:
            callback    callable object to get response from remote xbee

        Returns:
            None but raise error event if some error.
        """
        self.put_remote_command(
            self.xbee_dest_addr, self.xbee_gpio_power, self.PIN_LEVEL_LOW,
            callback)

    def put_remote_command(
            self, xbee_dest_addr, command, param, callback=None):
        """ Put remote AT command to xbee client. This function can only support
            parameter with 1 byte like pin high/low.

        Args:
            xbee_dest_addr   destination address of xbee as int
            command          like "P0", "P1", ...
            param            like 0x05 which is parameter against the command.
            callback         callable object to get response from remote xbee

        Returns:
            None but raise error event if some error.
        """
        self.e.clear()

        self.bee = xbee.ZigBee(
            self.ser, escaped=True,
            callback=self.__on_remote_command_done
            if callback is None else callback)

        self.frame_id = self.frame_id + 1 if self.frame_id < 256 else 1

        self.bee.remote_at(
            dest_addr_long=struct.pack('>Q', xbee_dest_addr),
            command=command.encode("utf-8"),
            frame_id=int(self.frame_id).to_bytes(1, byteorder="big"),
            parameter=int(param).to_bytes(1, byteorder="big"))

    def __on_remote_command_done(self, read_frame):
        """ Default callback function which is called when xbee remote_at
            command finished. """

        # {'status': b'\x00', 'source_addr': b'%Y',
        #  'source_addr_long': b'\x00\x13\xa2\x00@\xaf\xbc\xce',
        #  'frame_id': b'\x01', 'command': b'P0', 'id': 'remote_at_response'}
        print(read_frame)
        self.set_event()

    def set_event(self):
        """ Set event to wait for getting response from remote xbee. """
        self.e.set()

    def wait_for_command_done(self, timeout=3):
        """ Wait event for getting response from remote xbee.

        Args:
            timeout     timeout value as second

        Returns:
            False if timeout.
        """
        ret = False

        if self.e.wait(timeout) is True:
            ret = True

        if self.bee is not None:
            self.bee.halt()
            self.bee = None

        self.e.clear()
        return ret

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="This's a tool to switch power ON or forcely OFF your PC")

    parser.add_argument(
        "-d", "--xbee-dest-addr",
        help="destination address of xbee terminal as hexdecimal",
        metavar="L",
        type=int,
        default=0x0013A20040AFBCCE)
    parser.add_argument(
        "-g", "--xbee-gpio-power",
        help="GPIO pin name which is assigned to power control on xbee",
        metavar="P",
        type=str,
        default="P0")
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
    parser.add_argument(
        "-i", "--interval",
        help="interval time between press and release of power buton",
        metavar="I",
        type=int,
        default=1)

    parsed_args = parser.parse_args()
    kwargs = {key: value for key, value in parsed_args._get_kwargs()}

    controller = RemotePowerController(**kwargs)

    controller.press_power_button()
    if controller.wait_for_command_done(timeout=1) is not True:
        raise TimeoutError("Timeout!!!")

    time.sleep(parsed_args.interval)

    controller.release_power_button()
    if controller.wait_for_command_done(timeout=1) is not True:
        raise TimeoutError("Timeout!!!")
