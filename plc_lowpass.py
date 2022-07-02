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
from plc_extract_red_data import red_data
import matplotlib.pyplot as plt

### Process command line:  image path and filter parameter
kwargs = dict()
next_arg = 1
if sys.argv[next_arg:]:
    kwargs['image_path'] = sys.argv[1]
    next_arg += 1

filterpar = ([0.96]+list(map(float,sys.argv[next_arg:next_arg+1]))).pop()

assert filterpar > 0.0
assert filterpar < 1.0

########################################################################
### Part I:  input the data using the reddish pixel in the input image
########################################################################

cols,loads,image_path = red_data(**kwargs)

########################################################################
### Part II:  calculate deviations from lowpass-filtered "measurements"
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

########################################################################
### Part III:  Plot the results
########################################################################

plt.axhline(0,color='k')
plt.plot(cols,loads,'b.',markersize=0.5,label="Measurements")
plt.plot(cols,deviations,'r.',markersize=0.5,label="Filtered metric")
plt.xlabel('Time, 100ms units?')
plt.ylabel('Load cell values, as image row')
plt.title(f'Image={image_path}; Filter parameter={filterpar}')
plt.legend(loc='best')
plt.show()
