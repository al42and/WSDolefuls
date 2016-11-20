# WSDolefuls
Working with WSD scanner from Linux

Currently, it is single script that can scan an image using default settings.
Nothing fancy, quite contrary.

Usage: `./WSD.py -H scanner.ip.address -o ouput.jpeg`

For now, there's neither scanning configuration, nor error checking/reporting, nor status polling.
It sends one request, sleeps for 15 seconds (works for me), and then tries to get output.

# Troubleshooting
If for device gets scan request, it will refuse to accept further requests until someone retrieves the image.

In case this program crashed/got killed, and the device is now stuck, you can either 
a) try rebooting it, or
b) if you remember job id, try passing `-j <id>` option to the script.

# Why
I happened to buy Canon PIXMA MG3040 device, and while I wish to use it over WiFi from my Linux PC, this device only seems to support WSD scanning, not BJNP. And there seems to be no even limited support of WSD in `sane` or any other Linux utility.

Current code is really ugly, but there are not much alternatives to work with WSD scanners from Linux, and this script works (at least for me).
