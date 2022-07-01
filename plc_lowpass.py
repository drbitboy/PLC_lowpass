"""
Load cell data filter
Cf. https://www.plctalk.net/qanda/showthread.php?t=133372

Usage:  python plc_lowpass.py data_fixed.png [filterfactor]
        - default filter factor = 0.96
        - default filter factor = 0.96

Input image, data_fixed.png, is modified version of image data.jpg
from Post #18 at the URL above.  This is simpler if you have the
actual data.

Brian T. Carcich, 2022-07-01

"""
import sys
import PIL.Image
import matplotlib.pyplot as plt

### Process command line:  image path and filter parameter
image_path = sys.argv[1]
filterpar = ([0.96]+list(map(float,sys.argv[2:]))).pop()

assert filterpar > 0.0
assert filterpar < 1.0

########################################################################
### Part I:  input the data
### Because we have only the image from the URL, we look for the
### lowest-positioned red-ish pixels in that image, and use the row
### offset from the bottom of the image as a proxy for the measured data
### and the column offset from the left edge of the image as a proxy for
### time
########################################################################

### Import image, get width and height, convert to sequence of pixels
imgdata = PIL.Image.open(image_path)
width,height = wh = imgdata.size
widths,heights = map(range,wh)
imgseq = imgdata.getdata()

### Loop over columns, get lowest contiguous rows that are red
reddata = [(col
           ,[(height-row,red,)
             for row,(red,green,blue) in
             [(row,imgseq.getpixel((col,row,)),)
              for row in heights
             ]
             if red>30 and (red/20)>green and (red/20)>blue and blue<10
            ]
           ,)
           for col in widths
          ]

### Average contiguous row values, weighted by redness
cols = list()
loads = list()
for col,data_list in reddata:
  if not data_list: continue
  redsum,redrowsum = 0.0,0.0
  row = data_list[-1][0]
  while data_list:
    nextrow = row+1
    row,red = data_list.pop()
    if row > nextrow: break
    redsum += red
    redrowsum += (red*row)
  cols.append(col)
  loads.append(redrowsum / redsum)

########################################################################
###  Part 2:  calulate deviations from lowpass-filtered "measurements"
########################################################################

lastload = lowpassval = loads[0]
deviations = list()
for load in loads:
  ### First-order-ish filter
  lowpassval *= filterpar
  lowpassval += (1.0-filterpar) * load
  ### Calculate absolute deviation from either filtered- or last- value
  deviations.append(max([abs(load-lowpassval),abs(load-lastload)]))
  lastload = load

### Plot results
plt.axhline(0,color='k')
plt.plot(cols,loads,'b.',markersize=0.5,label="Measurements")
plt.plot(cols,deviations,'r.',markersize=0.5,label="Filtered metric")
plt.xlabel('Time, 100ms units?')
plt.ylabel('Load cell values, as image row')
plt.legend(loc='best')
plt.show()
