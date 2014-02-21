#!/usr/bin/env python

"""Usage: relay.py COMMAND

Switches the relay that is plugged in to ttyUSB0 on or off

Arguments:
    COMMAND    on|off
"""

import os
import sys
import time

from docopt import docopt

class RelaysAreSimpleThingsException(Exception):
    pass

class HumanError(Exception):
    pass

class Relay(object):
    def __init__(self, device="/dev/ttyUSB0"):
        self.device = device
        os.system("stty -F {0} 9600".format(self.device))

    def on(self):
        with open(self.device, "w") as dev:
            dev.write("\xff\x01\x01")

    def off(self):
        with open(self.device, "w") as dev:
            dev.write("\xff\x01\x00")

if __name__ == '__main__':
    relay = Relay()

    args = docopt(__doc__)
    try:
        command = args['COMMAND'].lower()
    except:
        raise HumanError("Use me properly or don't use me ata all.")

    if command == 'on':
        relay.on()
    elif command == 'off':
        relay.off()
    else:
        raise RelaysAreSimpleThingsException("I don't know how to %s." % command)

