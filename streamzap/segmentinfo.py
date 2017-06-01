class SegmentInfo(object):
    def __init__(self, timestamp='N/A', session='N/A', service='N/A', protocol='N/A', bitrate='N/A',
                 width='N/A', height='N/A', framerate='N/A', segmenturl='N/A', segmentsize='N/A', itag='N/A'):
        self.timestamp = timestamp
        self.session = session
        self.service = service
        self.protocol = protocol
        self.bitrate = bitrate
        self.width = width
        self.height = height
        self.framerate = framerate
        self.segmenturl = segmenturl
        self.segmentsize = segmentsize
        self.itag = itag

    @staticmethod
    def keys():
        return ['timestamp',
                'session',
                'service',
                'protocol',
                'bitrate',
                'width',
                'height',
                'framerate',
                'segmenturl',
                'segmentsize',
                'itag']

    def values(self):
        return [self.timestamp,
                self.session,
                self.service,
                self.protocol,
                self.bitrate,
                self.width,
                self.height,
                self.framerate,
                self.segmenturl,
                self.segmentsize,
                self.itag]
