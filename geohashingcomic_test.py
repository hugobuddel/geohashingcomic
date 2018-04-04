# coding=utf-8
"""
Test for GeohashingComic class.
"""

import filecmp
import os
import shutil
import sys
import unittest

from geohashingcomic import GeohashingComic, main


class MyTest(unittest.TestCase):

    fn_test = "mytest.png"

    def tearDown(self):
        """
        Remove comic.
        """
        if os.path.exists(self.fn_test):
            os.remove(self.fn_test)

    def test_2005(self):
        gc = GeohashingComic()
        gc.make()
        gc.im.save(self.fn_test)

        self.failUnless(
            filecmp.cmp(self.fn_test, "comics/2005-5-26_10458.680000_37.421542_-122.085589.png"),
            "Bad comic created 1"
        )


class UrlTest(unittest.TestCase):

    fn_test = "mytest2.png"
    fn_ok = "comics/2005-5-26_10458.680000_37.421542_-122.085589.png"
    query_string = "year=2005&month=5&day=26&dowjones=10458.68&lat=37.421542&lon=-122.085589"

    def setUp(self):
        """
        Setup environment as-if this is a cgi-bin environment.
        """
        os.environ['QUERY_STRING'] = self.query_string
        shutil.move(self.fn_ok, self.fn_test)

    def tearDown(self):
        """
        Put all the files back.
        """
        del os.environ['QUERY_STRING']
        if os.path.exists(self.fn_ok):
            os.remove(self.fn_ok)
        shutil.move(self.fn_test, self.fn_ok)

    def test_2005(self):
        main()
        self.failUnless(
            filecmp.cmp(self.fn_test, self.fn_ok),
            "Bad comic created 2"
        )


class CommandLineTest(unittest.TestCase):

    def setUp(self):
        """
        Setup environment as-if this is a commandline environment.
        """
        sys.argv.append("lat=-1&lon=-31&year")

    def tearDown(self):
        """
        Reset environment
        """
        sys.argv.pop()

    def test1(self):
        """
        Test some manual input.
        """
        main()


if __name__ == '__main__':
    unittest.main()
