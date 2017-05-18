#!/usr/bin/env python

from service import Service
from streamdetails import StreamDetails
from mpegdash.parser import MPEGDASHParser
import re

class Swisscom(Service):
    def __init__(self, zap=None):
        Service.__init__(self, zap)
        self._name = 'Swisscom TV Air'
        self._detection_url = '.*.sctv.ch/.*.mpd/Manifest'

    def detect(self, messages):
        print(self._name + ' detected!')
        for message in messages:
            #dash_obj = MPEGDASHParser.parse(message['responseBody'])
            dash_obj = MPEGDASHParser.parse('swisscom.mpd')
            for period in dash_obj.periods:
                self._streams = []
                for set in period.adaptation_sets:
                    if set.id == 1:
                        for repres in set.representations:
                            stream_details = StreamDetails()
                            stream_details.bitrate = repres.bandwidth
                            stream_details.width = repres.width
                            stream_details.height = repres.height
                            stream_details.framerate = repres.frame_rate
                            self._streams.append(stream_details)
                            self._tracking_url = '.*.sctv.ch/.*.mpd/.*/Fragments\(video.*\)'

    def track(self, urls):
        results = []
        for url in urls:
            bitrate = 0
            matches = re.search('QualityLevels\(([0-9]+?)\)', url['url'])
            if matches:
                bitrate = matches.group(1)

            stream_details = StreamDetails()
            for stream_detail in self._streams:
                if int(stream_detail.bitrate) == int(bitrate):
                    stream_details = stream_detail

            message = self._zap.core.message(url['id'])
            results.append({'timestamp': message['timestamp'],
                            'service': self._name,
                            'protocol': 'DASH',
                            'bitrate': bitrate,
                            'width': stream_details.width,
                            'height': stream_details.height,
                            'framerate': stream_details.framerate,
                            'segmenturl': url['url'],
                            'segmentsize': len(message['responseBody'])})
        return results
