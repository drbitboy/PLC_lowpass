import time
import pycomm3
from plc_extract_red_data import red_data

cols,loads,image_path = red_data('data_fixed.png')
loads.reverse()

slcdrv=pycomm3.SLCDriver('192.168.1.112/0')
slcdrv.open()

ssend,sreset,sload_cell = 'B3:0/0 B3:0/1 F8:0'.split()
n7_0 = loads.pop()

slcdrv.write((sreset,True,))
slcdrv.write((sload_cell,n7_0,))

time.sleep(5)
slcdrv.write((sreset,False,))

while loads:
    send_trigger = slcdrv.read(ssend)
    if send_trigger.value:
        slcdrv.write((ssend,False,))
        slcdrv.write((sload_cell,n7_0,))
        n7_0 = loads.pop()
        if 0==(len(loads)&127): print(len(loads))
    time.sleep(0.02)
