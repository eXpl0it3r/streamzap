#!/usr/bin/env python

from service import Service
from streamdetails import StreamDetails
from mpegdash.parser import MPEGDASHParser
import re


class Zattoo(Service):
    def __init__(self, zap=None):
        Service.__init__(self, zap)
        self._name = 'Zattoo'
        self._detection_url = '.*.zahs.tv/.*/manifest.mpd'

    def detect(self, messages):
        print(self._name + ' detected!')
        for message in messages:
            dash_obj = MPEGDASHParser.parse(message['responseBody'])
            for period in dash_obj.periods:
                self._streams = []
                for set in period.adaptation_sets:
                    if set.id == 0:
                        for repres in set.representations:
                            stream_details = StreamDetails()
                            stream_details.bitrate = repres.bandwidth
                            stream_details.width = repres.width
                            stream_details.height = repres.height
                            stream_details.framerate = repres.frame_rate
                            self._streams.append(stream_details)
                            self._tracking_url = '.*.zahs.tv/.*/video-time.*.m4s.*'

    def track(self, urls):
        results = []
        for url in urls:
            bitrate = 0
            matches = re.search('/video-time=([0-9]+?)-([0-9]+?)-0.m4s', url['url'])
            if matches:
                bitrate = matches.group(2)

            stream_details = StreamDetails()
            for stream_detail in self._streams:
                if int(stream_detail.bitrate) == int(bitrate):
                    stream_details = stream_detail

            message = self._zap.core.message(url['id'])
            results.append({'timestamp': message['timestamp'],
                            'service': 'Zattoo',
                            'protocol': 'DASH',
                            'bitrate': bitrate,
                            'width': stream_details.width,
                            'height': stream_details.height,
                            'framerate': stream_details.framerate,
                            'segmenturl': url['url'],
                            'segmentsize': len(message['responseBody'])})
        return results
