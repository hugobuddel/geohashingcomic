#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module to create Geohashing Comics for any date.
"""

import urllib
import sys
import os
import datetime
from PIL import Image

from geohashing import Geohashing


class GeohashingComic(object):
    """
    Class to create Geohashing Comics for any date.
    """

    # read the digits (and the -), the dots don't move
    digits = {
        c: Image.open(c.replace("-", "m") + ".png")
        for c in "0123456789abcdef-"
    }

    def __init__(self,
                 date=datetime.date(2005, 5, 26),
                 dowjones=10458.68,
                 location=(37.421542, -122.085589),
                 ):

        self.gh = Geohashing(date, dowjones, location)
        # Geohashing instance to calculate the hash and new latitude and longitude.

        self.im = None
        # The final image.

    def draw_date(self):
        """
        Draw the year, month and day.
        """
        for i, c in enumerate("{:04d}".format(self.gh.date.year)):
            self.im.paste(self.digits[c], (24 + 12 * i, 78))

        for i, c in enumerate("{:02d}".format(self.gh.date.month)):
            self.im.paste(self.digits[c], (88 + 11 * i, 78))

        for i, c in enumerate("{:02d}".format(self.gh.date.day)):
            self.im.paste(self.digits[c], (120 + 12 * i, 78))

    def draw_dowjones(self):
        """
        Draw the dow jones index.
        """
        hofs = 165
        for i, c in enumerate("{:8.2f}".format(self.gh.dowjones)):

            checks_raw = [
                (i == 1, -3),  # does this work properly when the DJ is above 20000?
                (i == 5, -3),  # after the dot
            ]
            offset_change = sum(change for check, change in checks_raw if check)
            hofs += offset_change
            if not (c == '.' or c == ' '):  # do not do the dot or spaces
                self.im.paste(self.digits[c], (hofs + 10 * i, 78))

    def draw_hash(self):
        """
        Draw first and second half of hash.
        """
        hofs = 301
        for c in self.gh.hexdig[0:16]:
            self.im.paste(self.digits[c], (hofs, 82))
            self.im.paste(self.digits[c], (hofs - 9, 129))
            hofs += self.digits[c].size[0]
        hofs += 14
        hofs2 = 466

        for c in self.gh.hexdig[16:32]:
            self.im.paste(self.digits[c], (hofs, 82))
            self.im.paste(self.digits[c], (hofs2, 129))
            hofs += self.digits[c].size[0]
            hofs2 += self.digits[c].size[0]

    def offset_latitude(self, i, c):
        """
        Calculate offset for latitude drawing.
        """
        checks_raw = [
            (True, 10),
            (c == '1' and i > 3, -5),
            (c == '.', 2),
            (c == '-', -1),
            (c == '+', -1),
            (c == ' ', -2),
        ]
        offset_change = sum(change for check, change in checks_raw if check)
        return offset_change

    def draw_latitude_top(self):
        """
        Draw latitude top.
        """
        hofs = 25
        for i, c in enumerate("{:+10.6f}".format(self.gh.lat)):
            if c not in ' +.':
                self.im.paste(self.digits[c], (hofs, 168))

            hofs += self.offset_latitude(i, c)

    def draw_latitude_bottom(self):
        """
        Draw latitude bottom.
        """
        hofs = 25 + 110
        for i, c in enumerate("{:+10.6f}".format(self.gh.lat)):
            if c not in ' +.' and i < 3:
                self.im.paste(self.digits[c], (hofs, 266))

            hofs += self.offset_latitude(i, c)

    def offset_longitude(self, i, c):
        """
        Calculate offset for longitude drawing.
        """
        checks_raw = [
            (True, 10),
            (c == '1' and i > 4, -5),
            (c == '.', 3),
            (c == '-', -1),
            (c == '+', -2),
            (c == ' ', -2),
        ]
        offset_change = sum(change for check, change in checks_raw if check)
        return offset_change

    def draw_longitude_top(self):
        """
        Draw longitude.
        """
        hofs = 143
        for i, c in enumerate("{:+11.6f}".format(self.gh.lon)):
            if c not in ' +.':
                self.im.paste(self.digits[c], (hofs, 169))

            hofs += self.offset_longitude(i, c)

    def draw_longitude_bottom(self):
        """
        Draw longitude.
        """
        hofs = 143 + 138
        for i, c in enumerate("{:+11.6f}".format(self.gh.lon)):
            if c not in ' +.' and i < 4:
                self.im.paste(self.digits[c], (hofs, 269))

            hofs += self.offset_longitude(i, c)

    def draw_coordinate_decimals(self):
        """
        Draw decimals of lat/lon in final coordinates.
        """
        for i, (c1, c2) in enumerate(zip(str(self.gh.lato)[2:8], str(self.gh.lono)[2:8])):
            self.im.paste(self.digits[c1], (300 + 10 * i, 174))
            self.im.paste(self.digits[c1], (176 + 10 * i, 267))
            self.im.paste(self.digits[c2], (450 + 10 * i, 174))
            self.im.paste(self.digits[c2], (335 + 10 * i, 269))

    def make(self):
        """Creating the image"""

        self.im = Image.open("geohashingclean.png")

        self.draw_date()
        self.draw_dowjones()
        self.draw_hash()
        self.draw_latitude_top()
        self.draw_longitude_top()
        self.draw_latitude_bottom()
        self.draw_longitude_bottom()
        self.draw_coordinate_decimals()

    def show(self):
        """
        Show the comic on the screen.
        """
        if not self.im:
            self.make()
        self.im.show(command='display')

    def cgi(self, format='png'):
        """
        Print out the comic as a cgi-bin output.

        :param format: The format of the image.
        :type format: str
        """
        if not self.im:
            self.make()
        print "Content-Type: image/png\r\n\r\n",
        # there should be a better way to do this
        # self.im.save('/dev/stdout',format)
        fn = "comics/{:d}-{:d}-{:d}_{:f}_{:f}_{:f}.png".format(
            self.gh.date.year, self.gh.date.month, self.gh.date.day, self.gh.dowjones, self.gh.lat, self.gh.lon)
        self.im.save(fn, format)
        oo = open(fn)
        d = oo.read()
        oo.close()
        print d


def parse_arguments():
    """
    Parse arguments.

    :return: Arguments dictionary.
    :type: dict
    """
    args = {
        'year': 2005,
        'month': 5,
        'day': 26,
        'dowjones': 0.0,
        'lat': 37.421542,
        'lon': -122.085589,
        'mode': 'cmd',
    }
    arg = ''

    if 'QUERY_STRING' in os.environ:
        arg = urllib.unquote(os.environ['QUERY_STRING'])
        args['mode'] = 'cgi'
    elif len(sys.argv) > 1:
        arg = urllib.unquote(sys.argv[-1])
        args['mode'] = 'cmd'

    args2 = dict(a.split('=') for a in arg.split('&') if '=' in a)
    args.update(args2)
    return args


def main():
    """
    Main method, either in CGI or command line mode.
    """
    args = parse_arguments()

    date = datetime.date(int(args['year']), int(args['month']), int(args['day']))
    gc = GeohashingComic(date, float(args['dowjones']), (float(args['lat']), float(args['lon'])))

    if args['mode'] == 'cgi':
        gc.cgi()
    else:
        gc.show()


if __name__ == '__main__':
    main()
