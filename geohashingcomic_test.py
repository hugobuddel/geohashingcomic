# coding=utf-8
"""
Test for GeohashingComic class.
"""

import datetime
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
    fn_ok = "comics/2009-5-26_8292.210000_37.421542_22.085589.png"
    query_string = "year=2009&month=5&day=26&lat=37.421542&lon=+22.085589"

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
        sys.argv.append("lat=-1&lon=-29&year=2009&month")

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


class ManualTest(unittest.TestCase):

    def test2(self):
        """
        Test some manual input.
        """
        gc = GeohashingComic(datetime.date(2009, 5, 26), location=(1, +29), dowjones=0)
        gc.show()

    def test3(self):
        """
        Test some manual input.
        """
        gc = GeohashingComic(datetime.date(2009, 5, 26), location=(1, -29))
        gc.cgi()

    def tearDown(self):
        """
        Remove temporary file.
        """
        fn = "comics/2009-5-26_10458.680000_1.000000_-29.000000.png"
        if os.path.exists(fn):
            os.remove(fn)


if __name__ == '__main__':
    unittest.main()
