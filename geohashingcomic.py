#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module to create Geohashing Comics for any date.
"""

import hashlib
import struct
import urllib
import sys
import os
import datetime
from PIL import Image


class GeohashingComic(object):
    """
    Class to create Geohashing Comics for any date.
    """

    def __init__(self,
                 year=2005,
                 month=5,
                 day=26,
                 dowjones=10458.68,
                 lat=37.421542,
                 lon=-122.085589,
                 ):
        """year, month, day as ints, dowjones, lat, lon as floats"""
        self.year = year
        self.month = month
        self.day = day
        self.dowjones = dowjones
        self.lat = lat
        self.lon = lon

        self.im = Image.open("geohashingclean.png")
        # The final image.

    def make(self):
        """Creating the image"""

        # calculate the hash and new latitude and longitude
        inp = "{:4d}-{:02d}-{:02d}-{:0.2f}".format(self.year, self.month, self.day, self.dowjones)
        mhash = hashlib.md5(inp)
        hexdig = mhash.hexdigest()
        digest = mhash.digest()
        lato = struct.unpack(">Q", digest[0:8])[0] / (2. ** 64)
        lono = struct.unpack(">Q", digest[8:16])[0] / (2. ** 64)

        # read the digits (and the -), the dots don't move
        digits = {
            c: Image.open(c.replace("-", "m") + ".png")
            for c in "0123456789abcdef-"
        }

        # write down the year
        for i, c in enumerate("{:04d}".format(self.year)):
            self.im.paste(digits[c], (24 + 12 * i, 78))

        # write down the month
        for i, c in enumerate("{:02d}".format(self.month)):
            self.im.paste(digits[c], (88 + 11 * i, 78))

        # write down the day
        for i, c in enumerate("{:02d}".format(self.day)):
            self.im.paste(digits[c], (120 + 12 * i, 78))

        # write down the dow jones
        hofs = 165
        for i, c in enumerate("{:8.2f}".format(self.dowjones)):
            if i == 1:  # this is a 1
                hofs -= 3
            if i == 5:  # after the dot
                hofs -= 3
            if not (c == '.' or c == ' '):  # do not do the dot or spaces
                self.im.paste(digits[c], (hofs + 10 * i, 78))

        # write first half hash
        hofs = 301
        for c in hexdig[0:16]:
            self.im.paste(digits[c], (hofs, 82))
            self.im.paste(digits[c], (hofs - 9, 129))
            hofs += digits[c].size[0]
        hofs += 14
        hofs2 = 466

        # write second half hash
        for c in hexdig[16:32]:
            self.im.paste(digits[c], (hofs, 82))
            self.im.paste(digits[c], (hofs2, 129))
            hofs += digits[c].size[0]
            hofs2 += digits[c].size[0]

        # write latitude
        hofs = 25
        for i, c in enumerate("{:+10.6f}".format(self.lat)):
            if c not in ' +.':
                self.im.paste(digits[c], (hofs, 168))
                if i < 3:
                    self.im.paste(digits[c], (hofs + 110, 266))
            hofs += 10
            if c == '1' and i > 3:
                hofs -= 5
            if c == '.':
                hofs += 2
            if c == '-':
                hofs -= 1
            if c == '+':
                hofs -= 1
            if c == ' ':
                hofs -= 2

        # write longitude
        hofs = 143
        for i, c in enumerate("{:+11.6f}".format(self.lon)):
            if c not in ' +.':
                self.im.paste(digits[c], (hofs, 169))
                if i < 4:
                    self.im.paste(digits[c], (hofs + 138, 269))
            hofs += 10
            if c == '1' and i > 4:
                hofs -= 5
            if c == '.':
                hofs += 3
            if c == '-':
                hofs -= 1
            if c == '+':
                hofs -= 2
            if c == ' ':
                hofs -= 2

        # lat/lon in final coordinates
        for i, (c1, c2) in enumerate(zip(str(lato)[2:8], str(lono)[2:8])):
            self.im.paste(digits[c1], (300 + 10 * i, 174))
            self.im.paste(digits[c1], (176 + 10 * i, 267))
            self.im.paste(digits[c2], (450 + 10 * i, 174))
            self.im.paste(digits[c2], (335 + 10 * i, 269))

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
            self.year, self.month, self.day, self.dowjones, self.lat, self.lon)
        self.im.save(fn, format)
        oo = open(fn)
        d = oo.read()
        oo.close()
        print d


def main():
    arg = ''
    try:
        arg = urllib.unquote(os.environ['QUERY_STRING'])
        mode = 'cgi'
    except KeyError:
        if len(sys.argv) > 1:
            # arg = sys.argv[1]
            arg = urllib.unquote(sys.argv[-1])
        else:
            arg = ''
        mode = 'cmd'

    args = {
        'year': 2005,
        'month': 5,
        'day': 26,
        # 'dowjones': 10458.68,
        'dowjones': 0.0,
        'lat': 37.421542,
        'lon': -122.085589,
    }

    try:
        al = arg.split('&')
        for a in al:
            # print a
            (key, value) = a.split('=')
            # if (key[-2:] == '[]'):
            #    key = key[:-2]
            #    if (alist.has_key(key)):
            #        alist[key].append(value)
            #    else:
            #        alist[key] = [value]
            # else:
            #    alist[key] = value
            args[key] = value
    except ValueError:
        pass
        # raise

    # print args
    args['year'] = int(args['year'])
    args['month'] = int(args['month'])
    args['day'] = int(args['day'])
    args['dowjones'] = float(args['dowjones'])
    args['lat'] = float(args['lat'])
    args['lon'] = float(args['lon'])

    if not args['dowjones']:
        w30 = 0
        date = datetime.date(args['year'], args['month'], args['day'])
        if (args['lon'] > -30) and (date >= datetime.date(2008, 05, 27)):
            w30 = 1
        djia = urllib.urlopen(
            (date - datetime.timedelta(w30)).strftime("http://irc.peeron.com/xkcd/map/data/%Y/%m/%d")).read()
        if djia.find('404 Not Found') >= 0:
            args['dowjones'] = 0.0
        else:
            args['dowjones'] = float(djia)

    gc = GeohashingComic(args['year'], args['month'], args['day'], args['dowjones'], args['lat'], args['lon'])
    gc.make()
    if mode == 'cgi':
        gc.cgi()
    else:
        gc.show()


if __name__ == '__main__':
    main()
