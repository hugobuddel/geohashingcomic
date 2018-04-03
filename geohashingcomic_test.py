# coding=utf-8
"""
Test for GeohashingComic class.
"""

import filecmp
import os
import unittest

from geohashingcomic import GeohashingComic


class MyTest(unittest.TestCase):

    fn_test = "mytest.png"

    def setUp(self):
        gc = GeohashingComic()
        gc.make()
        gc.im.save(self.fn_test)

    def tearDown(self):
        if os.path.exists(self.fn_test):
            os.remove(self.fn_test)

    def test_2005(self):
        self.failUnless(
            filecmp.cmp(self.fn_test, "comics/2005-5-26_10458.680000_37.421542_-122.085589.png"),
            "Bad comic created"
        )


if __name__ == '__main__':
    unittest.main()
