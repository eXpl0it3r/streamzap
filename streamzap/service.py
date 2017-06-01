class Service(object):
    def __init__(self, zap=None):
        self._zap = zap
        self._name = ''
        self._detection_counter = 1
        self._tracking_counter = 1
        self._no_result = 0
        self._detection_url = ''
        self._tracking_url = ''
        self._streams = []

    @property
    def name(self):
        """Return the name of the service."""
        return self._name

    @property
    def detection_counter(self):
        """Start-counter property."""
        return self._detection_counter

    @detection_counter.setter
    def detection_counter(self, value):
        """Set start-counter property."""
        if value > 0:
            self._detection_counter = value
        else:
            self._detection_counter = 1

    @property
    def tracking_counter(self):
        """Start-counter property."""
        return self._tracking_counter

    @tracking_counter.setter
    def tracking_counter(self, value):
        """Set start-counter property."""
        if value > 0:
            self._tracking_counter = value
        else:
            self._tracking_counter = 1

    @property
    def no_result(self):
        """Tracking how often there was no result returned."""
        return self._no_result

    @no_result.setter
    def no_result(self, value):
        """Set no-result property."""
        if value > 0:
            self._no_result = value
        else:
            self._no_result = 0

    def reset_counters(self):
        """Reset the counter to the correct default value"""
        self._detection_counter = 1
        self._tracking_counter = 1

    @property
    def status(self):
        """Return the service status."""
        if self._tracking_url:
            return 'tracking'
        else:
            return 'detecting'

    @status.setter
    def status(self, state):
        if state == 'detecting':
            self._tracking_url = ''

    @property
    def detection_url(self):
        """Return the detection URL."""
        return self._detection_url

    @property
    def tracking_url(self):
        """Return the tracking URLs."""
        return self._tracking_url

    def detect(self, messages):
        pass

    def track(self, urls):
        pass
