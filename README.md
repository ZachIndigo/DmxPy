## DmxPy - Python Controller for USB - DMX devices

DmxPy is a super-lightweight Python library for controlling any USB-DMX device that is compatible with Enttec's USB DMX Pro, including all Dmxking ultraDMX devices.

DmxPy requires [PySerial](http://pyserial.sourceforge.net) to work

### There is a console interface for basic sanity testing and validation

For detailed usage instructions

    dmxpy -h

To black out (turn off) the lights when the DMX is on port COM4

    dmxpy --port COM4 -b

To turn on all the lights at 50% (level 128)

    dmxpy -p /dev/ttyUSB2 --level 128 -w

To play the demo light pattern with the default level at 200

    dmxpy -p COM2 -l 200 --demo

### For more specific use cases use the DmxPy module
To import

    from dmxpy import DmxPy

To initialize

    dmx = DmxPy('serial port')
where 'serial port' is where your device is located, .e.g, /dev/ttyUSB1 or COM3

To set a channel's value

    dmx.setChannel(chan, value)
where 'chan' and 'value' are integers representing the respective DMX channels and values to set!

To push dmx changes to device

    dmx.render()
You need to call this to update the device!
