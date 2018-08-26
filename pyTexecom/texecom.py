import asyncio
import logging

LOGGER = logging.getLogger(__name__)

REQUIREMENTS = ['pyserial-asyncio==0.4']

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

        self._alarmState = [self._maxZones]

        self._zoneStateChangeCallback = self._defaultCallback


        _LOGGER.info('Texecom panel interface initalised: %s', name)


 @asyncio.coroutine
    def start(self):
        """Handle when an entity is about to be added to Home Assistant."""
        _LOGGER.info('Setting up Serial Connection to port: %s', self._port)

        self._serial_loop_lask = asynio.get_event_loop()
        self._serial_loop_task.create_task(self.serial_read(self._port, self._baudrate))
        self._serial_loop_task.run_forever()

 @asyncio.coroutine
    def serial_read(self, device, rate, **kwargs):
        """Read the data from the port."""
        import serial_asyncio
        _LOGGER.info('Opening Serial Port')
        reader, _ = yield from serial_asyncio.open_serial_connection(url=device, baudrate=rate, **kwargs)
        _LOGGER.info('Opened Serial Port')
        while True:
            line = yield from reader.readline()
            _LOGGER.info('Data read: %s', line)
            line = line.decode('utf-8').strip()
            _LOGGER.debug('Decoded Data: %s', line)

            try:
                if line[1] == 'Z':
                    _LOGGER.debug('Zone Info Found')
                    zone = line[2:5]
                    zone = zone.lstrip('0')
                    state = line[5]
                    _LOGGER.info('Signalled Zone: %s', zone)
                    _LOGGER.info('Zone State: %s', state)
                    self._alarmState[zone] = state
                    callback_zone_state_change(self._alarmState)

            except IndexError:
                _LOGGER.error('Index error malformed string recived')

    @asyncio.coroutine
    def stop stop(self):
        """Close resources."""
        if self._serial_loop_task:
            self._serial_loop_task.stop()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def error(self):
        """Return the state of the sensor."""
        return self._error

    @property
    def callback_zone_state_change(self):
        return self._zoneStateChangeCallback

    @callback_zone_state_change.setter
    def callback_zone_state_change(self, value):
        self._zoneStateChangeCallback = value

    def _defaultCallback(self, data):
        """This is the callback that occurs when the client doesn't subscribe."""
        _LOGGER.debug("Callback has not been set by client.")	    
