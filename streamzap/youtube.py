from service import Service
from streamdetails import StreamDetails
from segmentinfo import SegmentInfo
import re
import json
import urlparse


class Youtube(Service):
    def __init__(self, zap=None):
        Service.__init__(self, zap)
        self._name = 'YouTube'
        self._detection_url = '.*youtube.com/watch\?.*'

    def _match_itag(self, itag):
        info = {
            '5': {'ext': 'flv', 'width': 400, 'height': 240, 'acodec': 'mp3', 'abr': 64, 'vcodec': 'h263'},
            '6': {'ext': 'flv', 'width': 450, 'height': 270, 'acodec': 'mp3', 'abr': 64, 'vcodec': 'h263'},
            '17': {'ext': '3gp', 'width': 176, 'height': 144, 'acodec': 'aac', 'abr': 24, 'vcodec': 'mp4v'},
            '18': {'ext': 'mp4', 'width': 640, 'height': 360, 'acodec': 'aac', 'abr': 96, 'vcodec': 'h264'},
            '22': {'ext': 'mp4', 'width': 1280, 'height': 720, 'acodec': 'aac', 'abr': 192, 'vcodec': 'h264'},
            '34': {'ext': 'flv', 'width': 640, 'height': 360, 'acodec': 'aac', 'abr': 128, 'vcodec': 'h264'},
            '35': {'ext': 'flv', 'width': 854, 'height': 480, 'acodec': 'aac', 'abr': 128, 'vcodec': 'h264'},
            '37': {'ext': 'mp4', 'width': 1920, 'height': 1080, 'acodec': 'aac', 'abr': 192, 'vcodec': 'h264'},
            '38': {'ext': 'mp4', 'width': 4096, 'height': 3072, 'acodec': 'aac', 'abr': 192, 'vcodec': 'h264'},
            '43': {'ext': 'webm', 'width': 640, 'height': 360, 'acodec': 'vorbis', 'abr': 128, 'vcodec': 'vp8'},
            '44': {'ext': 'webm', 'width': 854, 'height': 480, 'acodec': 'vorbis', 'abr': 128, 'vcodec': 'vp8'},
            '45': {'ext': 'webm', 'width': 1280, 'height': 720, 'acodec': 'vorbis', 'abr': 192, 'vcodec': 'vp8'},
            '46': {'ext': 'webm', 'width': 1920, 'height': 1080, 'acodec': 'vorbis', 'abr': 192, 'vcodec': 'vp8'},
            '59': {'ext': 'mp4', 'width': 854, 'height': 480, 'acodec': 'aac', 'abr': 128, 'vcodec': 'h264'},
            '78': {'ext': 'mp4', 'width': 854, 'height': 480, 'acodec': 'aac', 'abr': 128, 'vcodec': 'h264'},

            # 3D videos
            '82': {'ext': 'mp4', 'height': 360, 'width': 640, 'format_note': '3D', 'acodec': 'aac', 'abr': 128, 'vcodec': 'h264', 'preference': -20},
            '83': {'ext': 'mp4', 'height': 480, 'width': 854, 'format_note': '3D', 'acodec': 'aac', 'abr': 128, 'vcodec': 'h264', 'preference': -20},
            '84': {'ext': 'mp4', 'height': 720, 'width': 1280, 'format_note': '3D', 'acodec': 'aac', 'abr': 192, 'vcodec': 'h264', 'preference': -20},
            '85': {'ext': 'mp4', 'height': 1080, 'width': 1920, 'format_note': '3D', 'acodec': 'aac', 'abr': 192, 'vcodec': 'h264', 'preference': -20},
            '100': {'ext': 'webm', 'height': 360, 'width': 640, 'format_note': '3D', 'acodec': 'vorbis', 'abr': 128, 'vcodec': 'vp8', 'preference': -20},
            '101': {'ext': 'webm', 'height': 480, 'width': 854, 'format_note': '3D', 'acodec': 'vorbis', 'abr': 192, 'vcodec': 'vp8', 'preference': -20},
            '102': {'ext': 'webm', 'height': 720, 'width': 1280, 'format_note': '3D', 'acodec': 'vorbis', 'abr': 192, 'vcodec': 'vp8', 'preference': -20},

            # Apple HTTP Live Streaming
            '91': {'ext': 'mp4', 'height': 144, 'width': 256, 'format_note': 'HLS', 'acodec': 'aac', 'abr': 48, 'vcodec': 'h264', 'preference': -10},
            '92': {'ext': 'mp4', 'height': 240, 'width': 427, 'format_note': 'HLS', 'acodec': 'aac', 'abr': 48, 'vcodec': 'h264', 'preference': -10},
            '93': {'ext': 'mp4', 'height': 360, 'width': 640, 'format_note': 'HLS', 'acodec': 'aac', 'abr': 128, 'vcodec': 'h264', 'preference': -10},
            '94': {'ext': 'mp4', 'height': 480, 'width': 854, 'format_note': 'HLS', 'acodec': 'aac', 'abr': 128, 'vcodec': 'h264', 'preference': -10},
            '95': {'ext': 'mp4', 'height': 720, 'width': 1280, 'format_note': 'HLS', 'acodec': 'aac', 'abr': 256, 'vcodec': 'h264', 'preference': -10},
            '96': {'ext': 'mp4', 'height': 1080, 'width': 1920, 'format_note': 'HLS', 'acodec': 'aac', 'abr': 256, 'vcodec': 'h264', 'preference': -10},
            '132': {'ext': 'mp4', 'height': 240, 'width': 240, 'format_note': 'HLS', 'acodec': 'aac', 'abr': 48, 'vcodec': 'h264', 'preference': -10},
            '151': {'ext': 'mp4', 'height': 72, 'width': 133, 'format_note': 'HLS', 'acodec': 'aac', 'abr': 24, 'vcodec': 'h264', 'preference': -10},

            # DASH mp4 video
            '133': {'ext': 'mp4', 'height': 240, 'width': 427, 'format_note': 'DASH video', 'vcodec': 'h264'},
            '134': {'ext': 'mp4', 'height': 360, 'width': 640, 'format_note': 'DASH video', 'vcodec': 'h264'},
            '135': {'ext': 'mp4', 'height': 480, 'width': 854, 'format_note': 'DASH video', 'vcodec': 'h264'},
            '136': {'ext': 'mp4', 'height': 720, 'width': 1280, 'format_note': 'DASH video', 'vcodec': 'h264'},
            '137': {'ext': 'mp4', 'height': 1080, 'width': 1920, 'format_note': 'DASH video', 'vcodec': 'h264'},
            '160': {'ext': 'mp4', 'height': 144, 'width': 256, 'format_note': 'DASH video', 'vcodec': 'h264'},
            '212': {'ext': 'mp4', 'height': 480, 'width': 854, 'format_note': 'DASH video', 'vcodec': 'h264'},
            '264': {'ext': 'mp4', 'height': 1440, 'width': 2560, 'format_note': 'DASH video', 'vcodec': 'h264'},
            '298': {'ext': 'mp4', 'height': 720, 'width': 1280, 'format_note': 'DASH video', 'vcodec': 'h264', 'fps': 60},
            '299': {'ext': 'mp4', 'height': 1080, 'width': 1920, 'format_note': 'DASH video', 'vcodec': 'h264', 'fps': 60},
            '266': {'ext': 'mp4', 'height': 2160, 'width': 3840, 'format_note': 'DASH video', 'vcodec': 'h264'},

            # Dash webm
            '167': {'ext': 'webm', 'height': 360, 'width': 640, 'format_note': 'DASH video', 'container': 'webm', 'vcodec': 'vp8'},
            '168': {'ext': 'webm', 'height': 480, 'width': 854, 'format_note': 'DASH video', 'container': 'webm', 'vcodec': 'vp8'},
            '169': {'ext': 'webm', 'height': 720, 'width': 1280, 'format_note': 'DASH video', 'container': 'webm', 'vcodec': 'vp8'},
            '170': {'ext': 'webm', 'height': 1080, 'width': 1920, 'format_note': 'DASH video', 'container': 'webm', 'vcodec': 'vp8'},
            '218': {'ext': 'webm', 'height': 480, 'width': 854, 'format_note': 'DASH video', 'container': 'webm', 'vcodec': 'vp8'},
            '219': {'ext': 'webm', 'height': 480, 'width': 854, 'format_note': 'DASH video', 'container': 'webm', 'vcodec': 'vp8'},
            '278': {'ext': 'webm', 'height': 144, 'width': 256, 'format_note': 'DASH video', 'container': 'webm', 'vcodec': 'vp9'},
            '242': {'ext': 'webm', 'height': 240, 'width': 427, 'format_note': 'DASH video', 'vcodec': 'vp9'},
            '243': {'ext': 'webm', 'height': 360, 'width': 640, 'format_note': 'DASH video', 'vcodec': 'vp9'},
            '244': {'ext': 'webm', 'height': 480, 'width': 854, 'format_note': 'DASH video', 'vcodec': 'vp9'},
            '245': {'ext': 'webm', 'height': 480, 'width': 854, 'format_note': 'DASH video', 'vcodec': 'vp9'},
            '246': {'ext': 'webm', 'height': 480, 'width': 854, 'format_note': 'DASH video', 'vcodec': 'vp9'},
            '247': {'ext': 'webm', 'height': 720, 'width': 1280, 'format_note': 'DASH video', 'vcodec': 'vp9'},
            '248': {'ext': 'webm', 'height': 1080, 'width': 1920, 'format_note': 'DASH video', 'vcodec': 'vp9'},
            '271': {'ext': 'webm', 'height': 1440, 'width': 2560, 'format_note': 'DASH video', 'vcodec': 'vp9'},
            '272': {'ext': 'webm', 'height': 2160, 'width': 3840, 'format_note': 'DASH video', 'vcodec': 'vp9'},
            '302': {'ext': 'webm', 'height': 720, 'width': 1280, 'format_note': 'DASH video', 'vcodec': 'vp9', 'fps': 60},
            '303': {'ext': 'webm', 'height': 1080, 'width': 1920, 'format_note': 'DASH video', 'vcodec': 'vp9', 'fps': 60},
            '308': {'ext': 'webm', 'height': 1440, 'width': 2560, 'format_note': 'DASH video', 'vcodec': 'vp9', 'fps': 60},
            '313': {'ext': 'webm', 'height': 2160, 'width': 3840, 'format_note': 'DASH video', 'vcodec': 'vp9'},
            '315': {'ext': 'webm', 'height': 2160, 'width': 3840, 'format_note': 'DASH video', 'vcodec': 'vp9', 'fps': 60},

            # Unsupported & audio itags
            # '13': {'ext': '3gp', 'acodec': 'aac', 'vcodec': 'mp4v'},
            # itag 36 videos are either 320x180 (BaW_jenozKc) or 320x240 (__2ABJjxzNo), abr varies as well
            # '36': {'ext': '3gp', 'width': 320, 'acodec': 'aac', 'vcodec': 'mp4v'},
            # '138': {'ext': 'mp4', 'format_note': 'DASH video', 'vcodec': 'h264'},  # Height can vary (https://github.com/rg3/youtube-dl/issues/4559)
            # Dash mp4 audio
            # '139': {'ext': 'm4a', 'format_note': 'DASH audio', 'acodec': 'aac', 'abr': 48, 'container': 'm4a_dash'},
            # '140': {'ext': 'm4a', 'format_note': 'DASH audio', 'acodec': 'aac', 'abr': 128, 'container': 'm4a_dash'},
            # '141': {'ext': 'm4a', 'format_note': 'DASH audio', 'acodec': 'aac', 'abr': 256, 'container': 'm4a_dash'},
            # '256': {'ext': 'm4a', 'format_note': 'DASH audio', 'acodec': 'aac', 'container': 'm4a_dash'},
            # '258': {'ext': 'm4a', 'format_note': 'DASH audio', 'acodec': 'aac', 'container': 'm4a_dash'},
            # '325': {'ext': 'm4a', 'format_note': 'DASH audio', 'acodec': 'dtse', 'container': 'm4a_dash'},
            # '328': {'ext': 'm4a', 'format_note': 'DASH audio', 'acodec': 'ec-3', 'container': 'm4a_dash'},
            # Dash webm audio
            # '171': {'ext': 'webm', 'acodec': 'vorbis', 'format_note': 'DASH audio', 'abr': 128},
            # '172': {'ext': 'webm', 'acodec': 'vorbis', 'format_note': 'DASH audio', 'abr': 256},
            # # Dash webm audio with opus inside
            # '249': {'ext': 'webm', 'format_note': 'DASH audio', 'acodec': 'opus', 'abr': 50},
            # '250': {'ext': 'webm', 'format_note': 'DASH audio', 'acodec': 'opus', 'abr': 70},
            # '251': {'ext': 'webm', 'format_note': 'DASH audio', 'acodec': 'opus', 'abr': 160},
        }

        if itag not in info:
            return 0, 0

        return info[itag]['width'], info[itag]['height']

    def detect(self, messages):
        print(self._name + ' detected!')
        for message in messages:
            matches = re.search('ytplayer\.config\s*=\s*({.+?});', message['responseBody'])

            if not matches:
                # AJAX JSON update
                matches = re.search('"url_encoded_fmt_stream_map":"([^"]+)"', message['responseBody'])
                if matches:
                    url_encoded_fmt_stream_map = matches.group(1).encode('utf8')
                    url_encoded_fmt_stream_map = url_encoded_fmt_stream_map.replace('\u0026', '&')
            else:
                config = matches.group(1)
                jobj = json.loads(config)
                url_encoded_fmt_stream_map = (jobj['args']['url_encoded_fmt_stream_map'])

            if matches:
                mpd_data = urlparse.parse_qsl(url_encoded_fmt_stream_map)

                stream_details = StreamDetails()

                for mpd in mpd_data:
                    if mpd[0] == 'itag':
                        width, height = self._match_itag(mpd[1])
                        stream_details.width = width
                        stream_details.height = height
                        stream_details.itag = mpd[1]
                    elif mpd[0] == 'url':
                        stream_details.manifest_url = mpd[1]

                    if stream_details.width and stream_details.height and stream_details.manifest_url:
                        self._streams.append(stream_details)
                        stream_details = StreamDetails()
        if self._streams:
            self._tracking_url = '.*.googlevideo.com/videoplayback.*'

    def track(self, urls):
        results = []
        for url in urls:
            itag = 0
            matches = re.search('itag=([0-9]+?)&', url['url'])
            if matches:
                itag = matches.group(1)
                width, height = self._match_itag(itag)

            stream_details = StreamDetails()
            for stream_detail in self._streams:
                if int(stream_detail.itag) == int(itag):
                    stream_details = stream_detail

            # If there's no matching itag, then it's just an audio stream.
            if stream_details.height == 0 and height != 0:
                stream_details.width = width
                stream_details.height = height

                message = self._zap.core.message(url['id'])
                results.append(SegmentInfo(timestamp=message['timestamp'],
                                           service=self._name,
                                           protocol='DASH',
                                           width=stream_details.width,
                                           height=stream_details.height,
                                           segmenturl=url['url'],
                                           segmentsize=len(message['responseBody']),
                                           itag=itag))
        return results
