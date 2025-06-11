## DmxPy - Python Controller for USB - DMX devices

DmxPy is a super-lightweight Python library for controlling any USB-DMX device
that is compatible with Enttec's USB DMX Pro, including all Dmxking ultraDMX
devices.

DmxPy requires [PySerial](https://pypi.org/project/pyserial/) to work

### There is a console interface for basic sanity testing and validation

For detailed usage instructions

    dmxpy -h

To black out (turn off) the lights when the DMX is on port COM4

    dmxpy --port COM4 -b

To turn on the channels 1-3 at 50% (level 128)

    dmxpy -p /dev/ttyUSB2 -c 808080

### For more specific use cases use the DmxPy module
To import

    from dmxpy import DmxPy

To initialize

    dmx = DmxPy.DmxPy('serial port')
where 'serial port' is where your device is located, .e.g, /dev/ttyUSB1 or COM3

If None, attempt to identify port based on grep expression: hwid, serial number, etc

To set a channel's value

    dmx.set_channels(channel_data, mod_type)
where 'channel_data' is an array of integers representing the channel data, and
'mod_type' is the operation to perform (increment, decrement, or set).

To push dmx changes to device

    dmx.render()
You need to call this to update the device!
