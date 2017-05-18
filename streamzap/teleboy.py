#!/usr/bin/env python

from service import Service
from urlparse import urlparse
from streamdetails import StreamDetails
import m3u8
import re


class Teleboy(Service):
    def __init__(self, zap=None):
        Service.__init__(self, zap)
        self._name = 'Teleboy'
        self._detection_url = 'teleboy.customers.cdn.iptv.ch'

    def detect(self, messages):
        print(self._name + ' detected!')
        for message in messages:
            m3u8_obj = m3u8.loads(message['responseBody'])
            self._streams = []
            for stream in m3u8_obj.data['playlists']:
                stream_details = StreamDetails()
                stream_details.bitrate = stream['stream_info']['bandwidth']
                stream_details.manifest_url = stream['uri']
                self._streams.append(stream_details)

                res = urlparse(stream['uri'])
                self._tracking_url = res.scheme + '://' + res.netloc[:-6] + '.*/.*.ts'

    def track(self, urls):
        results = []
        for url in urls:
            bitrate = 0
            matches = re.search('/([0-9]+?)/([0-9]+?).ts', url['url'])
            if matches:
                bitrate = matches.group(1)

            message = self._zap.core.message(url['id'])
            results.append({'timestamp': message['timestamp'],
                            'service': self._name,
                            'protocol': 'HLS',
                            'bitrate': bitrate,
                            'width': 0,
                            'height': 0,
                            'framerate': 0,
                            'segmenturl': url['url'],
                            'segmentsize': len(message['responseBody'])})
        return results
