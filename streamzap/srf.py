from service import Service
from streamdetails import StreamDetails
from segmentinfo import SegmentInfo
import m3u8
import re


class SRF(Service):
    def __init__(self, zap=None):
        Service.__init__(self, zap)
        self._name = 'SRF'
        self._detection_url = '.*srg.*.akamaihd.net/.*/master.m3u8.*'

    def detect(self, messages):
        print(self._name + ' detected!')
        for message in messages:
            m3u8_obj = m3u8.loads(message['responseBody'])
            self._streams = []
            for stream in m3u8_obj.data['playlists']:
                stream_details = StreamDetails()
                stream_details.bitrate = stream['stream_info']['bandwidth']
                stream_details.manifest_url = stream['uri']

                if 'resolution' in stream['stream_info']:
                    matches = re.search('([0-9]+?)x([0-9]+?)$', stream['stream_info']['resolution'])
                    if matches:
                        stream_details.width = matches.group(1)
                        stream_details.height = matches.group(2)

                self._streams.append(stream_details)

            self._tracking_url = '.*srg.*.akamaihd.net/.*/.*.ts.*'

    def track(self, urls):
        results = []
        for url in urls:
            group = 0
            type = ''
            matches = re.search('segment[0-9]+?_([0-9]+?)_av-([pb]).ts', url['url'])
            if matches:
                group = matches.group(1)
                type = matches.group(2)

            stream_details = StreamDetails()
            for stream_detail in self._streams:
                matches = re.search('(index_' + str(group) + '_av-' + str(type) + '.m3u8)', stream_detail.manifest_url)
                if matches:
                    stream_details = stream_detail

            message = self._zap.core.message(url['id'])
            results.append(SegmentInfo(timestamp=message['timestamp'],
                                       service=self._name,
                                       protocol='HLS (Encrypted)',
                                       bitrate=stream_details.bitrate,
                                       width=stream_details.width,
                                       height=stream_details.height,
                                       framerate=stream_details.framerate,
                                       segmenturl=url['url'],
                                       segmentsize=len(message['responseBody'])))
        return results
