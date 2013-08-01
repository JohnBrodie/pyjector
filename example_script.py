from time import sleep

from pyjector.pyjector import Pyjector

port = '/dev/ttyUSB0'

pyj = Pyjector(port=port)

print(pyj.power('on'))
sleep(5)

print(pyj.power('status'))
sleep(5)

print(pyj.mute('on'))
sleep(5)

print(pyj.mute('off'))

print('Finished.')
