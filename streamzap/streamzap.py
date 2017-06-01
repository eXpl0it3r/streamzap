import time
import sys
import csv
import socket
import os
from zapv2 import ZAPv2
from segmentinfo import SegmentInfo

# Services imports
from teleboy import Teleboy
from wilmaa import Wilmaa
from zattoo import Zattoo
from srf import SRF
from swisscom import Swisscom
from youtube import Youtube


class Streamzap(object):
    def __init__(self, api_key, proxy, output):
        self._session_name = ''
        self._services = []
        self._zap = None
        self._HISTORY_SIZE = 100
        self._SEARCH_INTERVAL = 2
        self._NO_RESULT = 10

        print('Welcome to streamzap!\nYou can stop the application at any time by pressing Ctrl+C\n')
        self.generate_session_name()
        self.configure_zap(api_key, proxy)
        self.register_services()
        self.run(output)

    def generate_session_name(self):
        # PC identification via IP
        ip = socket.gethostbyname(socket.gethostname())  # May return 127.0.0.1
        if ip == '127.0.0.1':
            ip = socket.gethostbyname(socket.getfqdn())  # Requires a resolvable hostname

        self._session_name = 'video-stream-analytics' + ip

    def configure_zap(self, api_key, proxy):
        # ZAP configuration
        self._zap = ZAPv2(proxies={'http': proxy, 'https': proxy}, apikey=api_key)
        try:
            self._zap.core.new_session(self._session_name, True)
        except:
            # Proxy unavailable
            print('Ensure that ZAP is running and the proxy is configured correctly!')
            sys.exit(1)

    def register_services(self):
        self._services.append(Teleboy(self._zap))
        self._services.append(Wilmaa(self._zap))
        self._services.append(Zattoo(self._zap))
        self._services.append(SRF(self._zap))
        self._services.append(Swisscom(self._zap))
        self._services.append(Youtube(self._zap))

    def run(self, output):
        # Application loop
        while True:
            try:
                for service in self._services:
                    if service.status == 'detecting':
                        print('Searching for provider: ' + service.name + ' (' + service.detection_url + ')')
                        messages = self._zap.search.messages_by_url_regex(regex=service.detection_url, start=service.detection_counter)
                        if messages:
                            service.detect(messages)
                            # Ignore newer results
                            service.detection_counter += len(messages)
                    elif service.status == 'tracking':
                        print('Tracking provider: ' + service.name + ' (' + service.tracking_url + ')')
                        urls = self._zap.search.urls_by_url_regex(regex=service.tracking_url, start=service.tracking_counter)

                        service.no_result += 1

                        if service.no_result > self._NO_RESULT:
                            print('Switching provider ' + service.name + ' back to detection mode.')
                            service.no_result = 0
                            service.status = 'detecting'

                        if urls:
                            results = service.track(urls)
                            # Ignore newer results
                            service.tracking_counter += len(urls)

                            if results:
                                service.no_result = 0

                                # Result output
                                if not os.path.exists(output):
                                    os.mkdir(output)

                                filename = os.path.join(output, service.name + '.csv')
                                new_file = True

                                if os.path.exists(filename):
                                    new_file = False

                                try:
                                    with open(filename, 'ab') as csvfile:
                                        csvwriter = csv.writer(csvfile, delimiter=';')

                                        if new_file:
                                            csvwriter.writerow(SegmentInfo.keys())

                                        print(str(len(results)) + ' segments found!')

                                        for result in results:
                                            result.session = self._session_name
                                            csvwriter.writerow(result.values())
                                except IOError:
                                    print('Output file could not be opened. Tracked data will be lost.')
                                    print('Ensure you have the permission and no other application is using it.')

                # Clean the history to speed up searches
                if len(self._zap.core.urls) > self._HISTORY_SIZE:
                    self._zap.core.new_session(self._session_name, True)
                    for service in self._services:
                        service.reset_counters()
                else:
                    time.sleep(self._SEARCH_INTERVAL)
                print('')
            except KeyboardInterrupt:
                # Quit the application with Ctrl + C
                print('Bye! :)')
                sys.exit()
