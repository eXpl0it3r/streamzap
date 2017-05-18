#!/usr/bin/env python
import time
import sys
import csv
import socket
import os
from zapv2 import ZAPv2

# Services imports
from teleboy import Teleboy
from wilmaa import Wilmaa
from zattoo import Zattoo
from srf import SRF
from swisscom import Swisscom
from youtube import Youtube


class Streamzap(object):
    def __init__(self):
        self._session_name = ''
        self._services = []
        self._HISTORY_SIZE = 100
        self._SEARCH_INTERVAL = 2
        
        print('Welcome to streamzap!\nYou can stop the application at any time by pressing Ctrl+C\n')
        self._session_name = self.generate_session_name()
        zap = self.configure_zap('4qtcesic4o99jdrorjnl2t47b4', self._session_name)
        self.register_services(zap)
        self.run(zap, self._session_name)

    def generate_session_name(self):
        # PC identification via IP
        ip = socket.gethostbyname(socket.gethostname())  # May return 127.0.0.1
        if ip == '127.0.0.1':
            ip = socket.gethostbyname(socket.getfqdn())  # Requires a resolvable hostname

        return 'video-stream-analytics' + ip

    def configure_zap(self, api_key, session_name):
        # ZAP configuration    
        zap = ZAPv2(proxies={'http': 'http://127.0.0.1:8080', 'https': 'http://127.0.0.1:8080'}, apikey=api_key)
        try:
            zap.core.new_session(session_name, True)
        except:
            # Proxy unavailable
            print('Ensure that ZAP is running and the proxy is configured correctly!')
            sys.exit()
            
        return zap

    def register_services(self, zap):
        self._services.append(Teleboy(zap))
        self._services.append(Wilmaa(zap))
        self._services.append(Zattoo(zap))
        self._services.append(SRF(zap))
        self._services.append(Swisscom(zap))
        self._services.append(Youtube(zap))

    def run(self, zap, session_name):
        # Application loop
        while (True):
            try:
                for service in self._services:
                    if service.status == 'detecting':
                        print('Searching for provider: ' + service.name + ' (' + service.detection_url + ')')
                        messages = zap.search.messages_by_url_regex(regex=service.detection_url, start=service.detection_counter)
                        if messages:
                            service.detect(messages)
                            # Ignore newer results
                            service.detection_counter += len(messages)
                    elif service.status == 'tracking':
                        print('Tracking provider: ' + service.name + ' (' + service.tracking_url + ')')
                        urls = zap.search.urls_by_url_regex(regex=service.tracking_url, start=service.tracking_counter)

                        if urls:
                            results = service.track(urls)
                            # Ignore newer results
                            service.tracking_counter += len(urls)

                            # Result output
                            filename = 'output/' + service.name + '.csv'
                            new_file = True

                            if os.path.exists(filename):
                                new_file = False

                            with open('output/' + service.name + '.csv', 'ab') as csvfile:
                                csvwriter = csv.writer(csvfile, delimiter=';')

                                if new_file:
                                    csvwriter.writerow(['timestamp', 'session_name', 'service', 'protocol', 'bitrate', 'width', 'height', 'framerate', 'segmenturl', 'segmentsize']);

                                print(str(len(results)) + ' segments found!')

                                for result in results:
                                    csvwriter.writerow([result['timestamp'],
                                                        session_name,
                                                        result['service'],
                                                        result['protocol'],
                                                        result['bitrate'],
                                                        result['width'],
                                                        result['height'],
                                                        result['framerate'],
                                                        result['segmenturl'],
                                                        result['segmentsize']])

                # Clean the history to speed up searches
                if len(zap.core.urls) > self._HISTORY_SIZE:
                    zap.core.new_session(session_name, True)
                    for service in self._services:
                        service.reset_counters()
                else:
                    time.sleep(self._SEARCH_INTERVAL)
            except KeyboardInterrupt:
                # Quit the application with Ctrl + C
                print('Bye! :)')
                sys.exit()
