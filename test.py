import fpga 
from time import sleep

bs = fpga.bitstream('./design_1_wrapper.bit')
bs.download()

led = fpga.ip('led.json')
led.tri(0)
while 1:
    led.gpio(1)
    sleep(0.5)
    led.gpio(0)
    sleep(0.5)

