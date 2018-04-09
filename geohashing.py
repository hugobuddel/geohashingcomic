#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Module to perform calculations for Geohashing.
"""

import hashlib
import struct
import urllib
import datetime


class Geohashing(object):
    """
    Class to create Geohashing Comics for any date.
    """

    def __init__(self,
                 date,
                 dowjones=0.0,
                 location=(37.421542, -122.085589),
                 ):
        """date as datetime, dowjones, lat, lon as floats"""
        self.date = date
        self.lat, self.lon = location
        self._dowjones = dowjones
        self._hexdig = None
        self._lato = None
        self._lono = None
        self.calculate_hashes()
        self.calculate_hashes()
        self.calculate_hashes()
        self.calculate_hashes()
        self.calculate_hashes()

    def calculate_hashes(self):
        """
        Calculate hashes.
        """
        # calculate the hash and new latitude and longitude
        inp = "{:4d}-{:02d}-{:02d}-{:0.2f}".format(self.date.year, self.date.month, self.date.day, self.dowjones)
        mhash = hashlib.md5(inp)
        self._hexdig = mhash.hexdigest()
        digest = mhash.digest()
        self._lato = struct.unpack(">Q", digest[0:8])[0] / (2. ** 64)
        self._lono = struct.unpack(">Q", digest[8:16])[0] / (2. ** 64)

    @property
    def hexdig(self):
        """
        Return hexdig.
        """
        if self._hexdig is None:
            self.calculate_hashes()
        return self._hexdig

    @property
    def lato(self):
        """
        Return lato.
        """
        if self._lato is None:
            self.calculate_hashes()
        return self._lato

    @property
    def lono(self):
        """
        Return lono.
        """
        if self._lono is None:
            self.calculate_hashes()
        return self._lono

    @property
    def dowjones(self):
        """
        Fetch the Dow Jones index if necessary.
        """
        if not self._dowjones:
            w30 = 0
            if (self.lon > -30) and (self.date >= datetime.date(2008, 05, 27)):
                w30 = 1
            djia = urllib.urlopen(
                (self.date - datetime.timedelta(w30)).strftime("http://irc.peeron.com/xkcd/map/data/%Y/%m/%d")).read()
            if djia.find('404 Not Found') >= 0:
                self._dowjones = -1.0
            else:
                self._dowjones = float(djia)
        return self._dowjones
