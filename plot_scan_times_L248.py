"""
Plot histogram of scan time data in Data File L248 from
training_bubble_sort_running.htm, which is HTML version of
training_bubble_sort_running.pdf

Usage:

  python plot_scan_times_L248.py < training_bubble_sort_running.htm

"""
import os
import sys
import matplotlib.pyplot as plt

L248 = [1]*256
for lyne in sys.stdin:
    try:
        assert lyne.startswith('<p>L248:')
        toks = [s.strip() for s in lyne.strip().split()]
        assert 1 < len(toks)
        toks.reverse()
        offset = int(toks.pop()[8:])
        while True:
          L248[offset] += int(toks.pop())
          offset += 1
    except:
        if 'DEBUG' in os.environ:
            import traceback
            traceback.print_exc()
            sys.stderr.write(lyne)

alldata = L248[:128]
trainingdata = L248[128:]

plt.plot(alldata,'-o',label='All data')
plt.plot(trainingdata,'-x',lw=.4,label='Training data')
plt.legend()
plt.xlabel('Scan times, 10kHz ticks')
plt.ylabel('Count of scan time')
if not ('NOLOG' in os.environ): plt.yscale('log')
plt.show()
print(sum([a*b for a,b in enumerate(alldata)])*1e-4)
