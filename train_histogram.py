import matplotlib.pyplot as plt
from plc_extract_red_data import red_data

cols,loads,fn = red_data()

loads.reverse()

count=0
d = dict()
while loads:
  ###il = int(round(loads.pop())) & -4
  il = int(round(1000. * int(round(4096.0 * loads.pop() / 1000.)) / 4095.)) & -4
  d[il] = 1 + (il in d and d[il] or 0)
  count+=1
ax = plt.subplot()
ax.plot(*zip(*sorted([(k,d[k]) for k in d])),'-o')
ax.set_yscale('log')
ax.set_title(str(count))
plt.show()

for il in sorted(d.keys()):
  v = d[il]
  print('*'*(v//5)+' '+str(il)+','+str(v))
