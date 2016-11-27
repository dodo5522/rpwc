#!/usr/bin/env python
# -*- coding:utf-8 -*-

#   Copyright 2016 Takashi Ando - http://blog.rinka-blossom.com/
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

""" rpwc : Remote Power Controller
"""

from threading import Event
import struct
import serial
import xbee

__author__ = "Takashi Ando"
__copyright__ = "Copyright 2015, My own project"
__license__ = "GPL"


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
    pass
