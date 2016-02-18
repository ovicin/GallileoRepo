import mraa
import sys

print ("Set RelayState to "+sys.argv[1])
x = mraa.Gpio(4)
x.dir(mraa.DIR_OUT)
x.write(int(sys.argv[1]))
