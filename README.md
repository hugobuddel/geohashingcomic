# geohashingcomic
Python module to create the xkcd geohashing comic for any date.

Can be used as a cgi script, but currently not live anywhere. Like
http://mywebsite/~me/cgi-bin/geohashingcomic.cgi?year=2008&month=5&day=24&lat=55.218512&lon=6.566854

Although it fetches the Dow itself, you can add &dowjones=12345.67 if it doesn't do so correctly (e.g., peeron.com is down).

In the image, Dow values less than 10,000.00 are padded with leading spaces, however in the algorithm it is not so it is compliant with other algorithms. As Tim P suggested, the comic is akin to all the bank cheques with "19__" printed on them being used in 2000. The "form" has 5+2 "boxes" because that's how Dow prices are now, but that doesn't mean it can't be different in the future.

This code was written in 2008 and moved to github to save it for posterity.

## Bugs

* The font sizes are not exactly as the original and there can still be some alignment problems.
* The -0 issue is ignored. Only if you enter -0 as an integer you get an incorrect outcome. You are supposed to enter your own location as a float, up to 6 decimals, everything is okay even when you enter -0.0.
