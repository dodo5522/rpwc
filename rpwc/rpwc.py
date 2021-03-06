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

from threading import Event
from threading import Thread
import random
import struct
import serial
import time
import xbee


class ZigbeeCommander(object):
    """ Put remote AT command to xbee client. This function can only support
        parameter with 1 byte like pin high/low.

    Args:
        xbee_dest_addr   destination address of xbee as str with hex.
        command          like "P0", "P1", ...
        param            like 0x05 which is parameter against the command.
        callback         callable object to return the result of xbee operation.

    Returns:
        tuple of sent and received frame IDs if callback is None. If the
        callback is not None, the result is passed through the callback.
    """
    CMD_PARAM_HIGH = 0x05
    CMD_PARAM_LOW = 0x04

    def __init__(self, ser_obj, dest_addr, cmd, cmd_param):
        self._dest_addr = int(dest_addr, 16)
        self._cmd = cmd
        self._cmd_param = cmd_param
        self._evt_got_frame = Event()
        self._ser_obj = ser_obj
        self._t_obj = Thread(target=self._t_target, args=(), kwargs={})
        self._sent_frame = 0
        self._received_frame = 0

    def is_ok(self):
        """ Zigbee command is done and succeeded. """
        if not self._evt_got_frame.is_set():
            return False
        if self._sent_frame is 0 or self._received_frame is 0:
            return False
        if self._sent_frame != self._received_frame:
            return False
        else:
            return True

    def wait(self, timeout=5):
        """ Wait for the Zigbee command is done.

        args:
            timeout: Timeout of waiting.

        returns:
            True if Zigbee command is done. False if not.
        """
        self._t_obj.join(timeout)
        return not self._t_obj.is_alive()

    def put(self):
        if self._t_obj.is_alive():
            raise RuntimeError("put cannot be run twice.")
        elif self._evt_got_frame.is_set():
            raise RuntimeError("put cannot be run twice.")

        self._t_obj.start()

    def _t_target(self, *args, **kwargs):
        """ Thread target function.
        """
        def get_frame_id(read_frame):
            self._received_frame = int.from_bytes(read_frame, "big")
            self._evt_got_frame.set()

        bee = xbee.ZigBee(
            self._ser_obj,
            escaped=True,
            callback=get_frame_id)

        self._sent_frame = random.randint(1, 255)

        # {'status': b'\x00', 'source_addr': b'%Y',
        #  'source_addr_long': b'\x00\x13\xa2\x00@\xaf\xbc\xce',
        #  'frame_id': b'\x01', 'command': b'P0', 'id': 'remote_at_response'}
        bee.remote_at(
            dest_addr_long=struct.pack('>Q', self._dest_addr),
            command=self._cmd.encode("utf-8"),
            frame_id=int(self._sent_frame).to_bytes(1, byteorder="big"),
            parameter=int(self._cmd_param).to_bytes(1, byteorder="big"))

        self._evt_got_frame.wait(3)

        bee.halt()
        bee = None


def push_button(**kwargs):
    """ Put remote AT command as pushing power buttion. This function does
        same operation as sending remote AT command to set high level to a
        GPIO pin.

    args:
        serial_port: like "/dev/ttyUSB" connected to XBee of sender.
        serial_baurate: like 9600 which is baurate for serial port.
        xbee_dest_addr: like "0x112233445566" which is address to XBee of receiver.
        xbee_gpio_power: like "P0" which is receiver XBee GPIO number connected to relay switch.
        interval: interval time of push and release the remote power button with [s] unit.

    returns:
        [True, True] if all operation is finished successfully.

    raises:
        None if callback_to_get_result is set. If the callback is not set, this
        method runs as synchronous function and raises FrameIdIsNotMatchedError
        if the sent and received frame ID is not matched.
    """
    ser_obj = serial.Serial(
        kwargs.get("serial_port"), kwargs.get("serial_baurate"))

    pressing_button = ZigbeeCommander(
        ser_obj,
        kwargs.get("xbee_dest_addr"),
        kwargs.get("xbee_gpio_power"),
        ZigbeeCommander.CMD_PARAM_HIGH)

    releasing_button = ZigbeeCommander(
        ser_obj,
        kwargs.get("xbee_dest_addr"),
        kwargs.get("xbee_gpio_power"),
        ZigbeeCommander.CMD_PARAM_LOW)

    pressing_button.put()
    pressing_button.wait()

    time.sleep(kwargs.get("interval"))

    releasing_button.put()
    releasing_button.wait()

    return [pressing_button.is_ok(), releasing_button.is_ok()]
