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

import argparse
import sys
from rpwc.rpwc import push_button


def init_args(argv=sys.argv[1:]):
    """ initialize arguments.

    args:
        argv: arguments passed by command line by sys module.
    returns:
        dictionary data from arguments parsed by argparser.
    """
    parser = argparse.ArgumentParser(
        description="This's a tool to switch power ON or forcely OFF your PC")

    parser.add_argument(
        "-d", "--xbee-dest-addr",
        help="destination address of xbee terminal as hexdecimal",
        metavar="L",
        type=str,
        default="0x0013A20040AFBCCE")
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
    return dict(parsed_args._get_kwargs())


def main():
    """ main routine.
    """
    kwargs = init_args()
    push_button(**kwargs)


main()
