## Load cell data filter
Cf. https://www.plctalk.net/qanda/showthread.php?t=133372

Usage:

    python plc_lowpass.py data_fixed.png [filterfactor]
    - default filter factor = 0.96
    - default filter factor = 0.96

Input image, data_fixed.png, is modified version of image data.jpg
from Post #18 at the URL above.  This is simpler if you have the
actual data.

Brian T. Carcich, 2022-07-01


### Manifest

* data_fixed_plot.png - Plot of results
* plc_lowpass.py - script to parse image pixels and plot data
* data_fixed.png - Modified image to remove false data detections
* data.jpg - original image
* data_fixed.xcf - GIMP format data_fixed.png
* README.md - this file
