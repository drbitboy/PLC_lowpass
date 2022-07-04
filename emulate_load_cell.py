import time
import pycomm3
from plc_extract_red_data import red_data

cols,loads,image_path = red_data('data_fixed.png')
loads.reverse()

slcdrv=pycomm3.SLCDriver('192.168.1.112/0')
slcdrv.open()

ssend,sreset,semulate,scancel,sload_cell = 'B3:0/0 B3:0/1 B3:0/3 B3:0/4 N7:1'.split()
n7_1 = int(round(4095.*loads.pop() / 1000.0))

slcdrv.write((sreset,True,))
try:
    slcdrv.write((semulate,True,))
    slcdrv.write((sload_cell,n7_1,))

    time.sleep(2)
    slcdrv.write((sreset,False,))

    while loads:
        send_trigger = slcdrv.read(ssend)
        if send_trigger.value:
            n7_1 = int(round(4095.*loads.pop() / 1000.0))
            slcdrv.write((sload_cell,n7_1,))
            slcdrv.write((ssend,False,))
        time.sleep(0.02)

except KeyboardInterrupt:
    pass
except:
    import traceback
    traceback.print_exc()
finally:
    time.sleep(1.0)
    slcdrv.write((ssend,False,))
    slcdrv.write((semulate,False,))
    slcdrv.write((scancel,True,))
    time.sleep(1.0)
    slcdrv.write((scancel,False,))
