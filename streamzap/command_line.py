#!/usr/bin/env python
import streamzap
import sys
import getopt


def usage():
    print('\nUsage:')
    print('  streamzap [flags]')
    print('\nGeneral Options:')
    print('  -h, --help           Prints this message')
    print('  -k, --apikey <key>   API key for accessing ZAP')
    print('  -p, --proxy <proxy>  URL of the proxy for HTTP and HTTPS')
    print('                       Default: http://127.0.0.1:8080')


def main():
    argv = sys.argv[1:]

    api_key = '4qtcesic4o99jdrorjnl2t47b4'
    proxy = 'http://127.0.0.1:8080'
    output = 'output'

    try:
        opts, args = getopt.getopt(argv, 'hk:p:o:', ['help', 'apikey=', 'proxy=', 'output='])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-k', '--apikey'):
            api_key = arg
        elif opt in ('-p', '--proxy'):
            proxy = arg
        elif opt in ('-o', '--output'):
            output = arg

    streamzap.Streamzap(api_key, proxy, output)
