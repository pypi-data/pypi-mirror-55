#! /usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2016-2019 Cyril Desjouy <cyril.desjouy@univ-lemans.fr>
#
# This file is part of plight
#
# plight is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# plight is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with plight. If not, see <http://www.gnu.org/licenses/>.
#
# Creation Date : 2019-11-11 - 15:11:45
"""
plight allow screen backlight adjustment.
"""

import sys
import time
import argparse


class Brightness:

    def __init__(self, path='/sys/class/backlight/intel_backlight/'):

        self.path = path

        with open(self.path + 'max_brightness') as f:
            self.max_brightness = int(f.read())

    @property
    def current_brightness(self):
        """ Current Brightness."""
        with open(self.path + 'brightness') as f:
            bcur = int(f.read())
        return bcur

    @property
    def current_brightness_percent(self):
        """ Current Brightness in percent."""
        with open(self.path + 'brightness') as f:
            bcur = int(f.read())
        return round(bcur*100/self.max_brightness)

    def increase(self, inc=5):
        """ Increase Brightness. Value must be in percent."""
        inc *= int(self.max_brightness/100)
        new = min(self.max_brightness, self.current_brightness + inc)
        self._set_brightness(new)

    def decrease(self, dec=5):
        """ Decrease Brightness. Value must be in percent."""
        dec *= int(self.max_brightness/100)
        new = max(int(self.max_brightness*0.05), self.current_brightness - dec)
        self._set_brightness(new)

    def _set_brightness(self, value):

        step = max(1, int(abs(self.current_brightness-value)/100))
        step = step if self.current_brightness < value else -step

        if self.max_brightness*0.05 <= value <= self.max_brightness:
            for val in range(self.current_brightness, value+1, step):
                time.sleep(0.005)
                with open(self.path + 'brightness', 'w') as f:
                    f.write(str(val))

    def set_brightness(self, value):
        """ Set Brightness to value in percent."""
        value *= self.max_brightness/100
        self._set_brightness(int(value))


def main():

    parser = argparse.ArgumentParser(description='Backlight adjustment.')

    parser.add_argument('-i', '--increase', help='Increase backlight. In percent.')
    parser.add_argument('-d', '--decrease', help='Decrease backlight. In percent')
    parser.add_argument('-s', '--set', help='Current backlight. In percent.')
    parser.add_argument('-c', '--current', help='Set backlight. In percent', action='store_true')

    args = parser.parse_args()
    light = Brightness()

    if args.set:
        light.set_brightness(value=int(args.set))
    elif args.increase:
        light.increase(inc=int(args.increase))
    elif args.decrease:
        light.decrease(dec=int(args.decrease))

    if args.current:
        sys.stdout.write(str(light.current_brightness_percent))


if __name__ == '__main__':
    main()
