import asyncio
import logging

LOGGER = logging.getLogger(__name__)



class TexecomPanelInterface(Entity):
    """Representation of a Texecom Panel Interface."""

    def __init__(self, name, port, panelType):
        """Initialize the Texecom Panel Interface."""
        self._name = name
        self._state = None
        self._port = port
        self._baudrate = '19200'
        self._serial_loop_task = None
        self._panelType = panelType
        self._error = false
        self.signalledzone = '0'
        self.zonestate = '0'

        if self._panelType == '24':
            self._maxZones = '24'
            self._maxAreas = '2'
        elif self._panelType == '48':
            self._maxZones = '48'
            self._maxAreas = '4'
        elif self._panelType == '88':
            self._maxZones = '88'
            self._maxAreas = '1'
        elif self._panelType == '168':
            self._maxZones = '168'
            self._maxAreas = '1'
        else:
            _LOGGER.info('Incorrect panel type configured: %s', self._panelType)

        _LOGGER.info('Texecom panel interface initalised: %s', name)


 @asyncio.coroutine
    def start(self):
        """Handle when an entity is about to be added to Home Assistant."""
        _LOGGER.info('Setting up Serial Connection to port: %s', self._port,) 
        self._serial_loop_task = self.hass.loop.create_task(
            self.serial_read(self._port, self._baudrate))

 @asyncio.coroutine
    def serial_read(self, device, rate, **kwargs):
        """Read the data from the port."""
        import serial_asyncio
        _LOGGER.info('Opening Serial Port')
        reader, _ = yield from serial_asyncio.open_serial_connection(
            url=device, baudrate=rate, **kwargs)
        _LOGGER.info('Opened Serial Port')
        while True:
            line = yield from reader.readline()
            _LOGGER.info('Data read: %s', line)
            line = line.decode('utf-8').strip()
            _LOGGER.debug('Decoded Data: %s', line)

            try:
                if line[1] == 'Z':
                    _LOGGER.debug('Zone Info Found')
                    signalledzone = line[2:5]
                    signalledzone = signalledzone.lstrip('0')
                    zonestate = line[5]
                    _LOGGER.info('Signalled Zone: %s', signalledzone)
                    _LOGGER.info('Zone State: %s', zonestate)
                    self.zonestate = zonestate
                    self.signalledzone = signalledzone
                    async_dispatcher_send(self.hass, SIGNAL_ZONE_UPDATE, self)

            except IndexError:
                _LOGGER.error('Index error malformed string recived')

    @asyncio.coroutine
    def stop stop(self):
        """Close resources."""
        if self._serial_loop_task:
            self._serial_loop_task.cancel()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state


