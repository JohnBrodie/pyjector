"""Control your projector via serial port.

.. moduleauthor:: John Brodie <john@brodie.me>

"""
import json
import os

import serial

PATH = 'pyjector/projector_configs/'  # TODO: Do this better


class Pyjector(object):

    available_configs = {}
    possible_pyserial_settings = [
        'port', 'baudrate', 'bytesize', 'parity', 'stopbits', 'timeout',
        'xonxoff', 'rtscts', 'dsrdtr', 'writeTimeout', 'InterCharTimeout',
    ]
    pyserial_config_converter = {
        'bytesize': {
            5: serial.FIVEBITS,
            6: serial.SIXBITS,
            7: serial.SEVENBITS,
            8: serial.EIGHTBITS,
        },
        'parity': {
            'none': serial.PARITY_NONE,
            'even': serial.PARITY_EVEN,
            'odd': serial.PARITY_ODD,
            'mark': serial.PARITY_MARK,
            'space': serial.PARITY_SPACE,
        },
        'stopbits': {
            1: serial.STOPBITS_ONE,
            1.5: serial.STOPBITS_ONE_POINT_FIVE,
            2: serial.STOPBITS_TWO,
        },

    }

    def __init__(
            self,
            port=None,
            device_id='benq',
            **kwargs
    ):
        """Initialize a new Pyjector object.

        :param port: The device name or port number your device is connected
            to. If left as ``None``, you must call :func:`open` with the port
            before issuing commands.

        :param device_id: The string which identifies the command set to use
            with your device.

            .. note::

                Currently, only the default value, 'benq', is supported. Please
                fill in a config file for your projector and make a pull
                request!

        :param **kwargs: Any extra keyword args will be passed to the internal
            :mod:`pyserial` :class:`serial.Serial` object, and will override
            any device settings specified in the command set.

        """
        self.port = port
        self.device_id = device_id
        self.get_config(device_id, kwargs)
        self.serial = self._initialize_pyserial(port)

    def get_config(self, device_id, overrides):
        """Get configuration for :mod:`pyserial` and the device.

        :param device_id: The string which identifies the command set to use
            with your device.

        """
        self.available_configs = self._populate_configs()
        self.config = self.get_device_config_from_id(device_id)
        self._apply_overrides(overrides)
        self.pyserial_config = self.get_pyserial_config()

    def _populate_configs(self):
        """Load all json config files for devices.

        :returns: dict -- All available configs.

        """
        configs = {}
        for f in os.listdir(PATH):
            if f.endswith('.json'):
                data = open(PATH + f)
                json_data = json.loads(data.read())
                name = os.path.splitext(f)[0]
                configs[name] = json_data
        return configs

    def _apply_overrides(self, overrides):
        """Override specified values of the default configuration.

        Any configuration values for the internal:mod:`pyserial`
        :class:`serial.Serial` specified will override the defaults from
        the device configuration. Any config values not specified will
        be left at the device default.

        :param overrides: A dict of configuration values.

        """
        self.config.update(overrides)

    def get_device_config_from_id(self, device_id):
        """Get device configuration.

        :param device_id: The string which identifies the command set to use.

        :returns: dict -- The device configuration, including default
        :mod:`pyserial` settings, as well as the command set.

        """
        try:
            config = self.available_configs[device_id]
        except KeyError:
            raise KeyError(
                'Could not find device config with name {0}. '
                'Check that the file exists in '
                ' `pyjector/projector_configs/`'.format(device_id)
            )
        return config

    def get_pyserial_config(self):
        """Get the :mod:`pyserial` config values from the device config.

        This also checks that config values are sane, and casts them to
        the appropriate type, as needed.

        :func:`get_device_config_from_id` must be called before this method.

        :returns: dict -- The config values for :class:`serial.Serial`.
        :raises: KeyError

        """
        serial_config = self.config.get('serial', None)
        if serial_config is None:
            raise KeyError(
                'Configuration file for {0} does not contain needed serial'
                'config values. Add a `serial` section to the config.'.format(
                    self.device_id)
            )
        for key, value in serial_config.items():
            if key not in self.possible_pyserial_settings:
                raise KeyError(
                    'Configuration file for {0} specifies a serial '
                    'setting "{1}" not recognized by pyserial. Check '
                    'http://pyserial.sourceforge.net/pyserial_api.html'
                    'for valid settings'.format(
                        self.device_id, key)
                )
            if key in self.pyserial_config_converter:
                try:
                    serial_config[key] = (
                        self.pyserial_config_converter[key][value])
                except KeyError:
                    raise KeyError(
                        'Configuration file for {0} specifies a serial '
                        'setting for "{1}" for key "{2}" not recognized '
                        'by pyserial. Check '
                        'http://pyserial.sourceforge.net/pyserial_api.html'
                        'for valid settings'.format(
                            self.device_id, value, key)
                    )
        return serial_config

    def _initialize_pyserial(self, port):
        """Initialize the internal :class:`serial.Serial` object.

        Initializes the :mod:`pyserial` :class:`serial.Serial` object with
        configuration from `self.config`.

        :param port: The device name or port number your device is connected
            to. If left as ``None``, you must call :func:`open` with the port
            before issuing commands.

        :returns: :class:`serial.Serial` -- The internal object to use to
            communicate with the projector.

        """
        return serial.Serial(port=port, **self.pyserial_config)


# TODO Remove me
if __name__ == '__main__':
    Pyjector()
