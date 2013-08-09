Pyjector
========

A generic library to easily send serial commands to your projector.
Install via pip: `pip install pyjector`.


Usage
=====

```Python
from pyjector import Pyjector

# Look up what port your projector is connected to, using something
# like `dmesg` if you're on linux.
port = '/dev/ttyUSB0'

# The only valid device id at the moment is `benq`. This is used
# to figure out what commands are supported, and the format needed.
device_id = 'benq'

pyjector = Pyjector(port=port, device_id=device_id)

# Let's check what commands claim to be supported by our device.
print(pyjector.command_list)

# Let's check the actions associated with each command
print(pyjector.command_spec)

# Turn the projector on
pyjector.power('on')
# We need to change the source, which are supported?
print(pyjector.get_actions_for_command('source'))
# Change the source to hdmi-2
pyjector.source('hdmi_2')
# It's too loud!
pyjector.volume('down')
# We're done here
pyjector.power('off')

# We can also interact directly with the underlying `PySerial` instance
pyjector.serial.write('some other command here')
```

From the command line
=====================

Want to control your projector from the command line?  Use the `pyjector_controller`
script included.

```
Usage: pyjector_controller [-h] [-s SERIAL] {benq} port command action

positional arguments:
  {benq}                The device you wish to control
  port                  The serial port your device is connected to
  command               The command to send to the device
  action                The action to send to the device

optional arguments:
  -h, --help            show this help message and exit
  -s SERIAL, --serial SERIAL
                        Extra PySerial config values
```


Example: `./pyjector_controller benq "/dev/ttyUSB0" power on` to turn the projector on.

Your device isn't supported?
============================

You should be able to easily add support for other devices using a
simple json file. Check the files in `pyjector/projector_configs` for examples.

It should follow the template below...

```JSON
{
    "left_surround": "\r\n*",
    "right_surround": "#\r\n",
    "seperator": "=",
    "wait_time": 1,
    "command_failed_message": "*Block item#",
    "exception_message": "*Illegal format#",
    "serial": {
        "baudrate": 57600,
        "parity": "none",
        "stopbits": 1,
        "bytesize": 8
    },
    "command_list": {
        "power": {
            "command": "pow",
            "actions": {
                "on": "on",
                "off": "off",
                "status": "?"
            }
        },
        ...
        ...
    }
}
```
Please do make pull requests for any other devices.  If code changes need made
in order for your device to work, open an issue and I'll work to resolve it.
