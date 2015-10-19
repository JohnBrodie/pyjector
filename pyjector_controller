#!/usr/bin/env python

import argparse
import logging
from pyjector import Pyjector

parser = argparse.ArgumentParser(description='Control your projector from the command line.')
parser.add_argument('device', help='The device you wish to control. ex benq')
parser.add_argument('port', help='The serial port your device is connected to.')
parser.add_argument('command', help='The command to send to the device. ex: power')
parser.add_argument('action', help='The action to send to the device. ex: on')
parser.add_argument('-s', '--serial', help='Extra PySerial config values.')
parser.add_argument("-v", "--verbose", help="verbose output", action="store_const", dest="loglevel", const=logging.INFO, default=logging.WARNING,)
parser.add_argument("-d", "--debug",   help="print debug",    action="store_const", dest="loglevel", const=logging.DEBUG,)
args = parser.parse_args()

logging.basicConfig(level=args.loglevel, format='%(created)f %(levelname)s %(message)s')
pyjector = Pyjector(port=args.port, device_id=args.device)

command = getattr(pyjector, args.command)
command(args.action)
