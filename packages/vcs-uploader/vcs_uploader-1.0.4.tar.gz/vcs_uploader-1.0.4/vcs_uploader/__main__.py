#!/usr/bin/env python3

import argparse

import requests

__debug = False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='gen vcs-uploader')
    parser.add_argument('url', type=str, help='server api base url')
    parser.add_argument('-f', '--file', type=argparse.FileType('rb'), help='version\'s file', required=True)
    parser.add_argument('-r', '--repo', type=str, help='repo name', required=True)
    parser.add_argument('-l', '--latest', type=int, choices=[0, 1], default=1, help='set to latest?')
    parser.add_argument('-m', '--message', type=argparse.FileType('rt'), help='version descriptions', required=True)
    parser.add_argument('-v', '--version', type=str, help='version code', required=True)
    parser.add_argument('-d', '--debug', nargs='?',
                        type=int, choices=[0, 1], default=0, const=1,
                        help='debug vcs-uploader')
    return parser.parse_args()


def __main():
    global __debug
    args = parse_args()
    __debug = True if args.debug == 1 else False
    url = '%s/versions/%s' % (args.url, args.repo)
    with requests.post(url,
                       headers={'ContentType': 'multipart/form-data'},
                       data={
                           'version': args.version,
                           'description': args.message.read(),
                           'isLatest': True if args.latest == 1 else False,
                       },
                       files={'file': args.file}) as rsp:
        if rsp.status_code != 201:
            raise Exception('Failed:bad status code %d,reason:%s' % (rsp.status_code, rsp.reason))
    print('status:%s' % rsp.reason)
    print('Success')


def main():
    try:
        __main()
    except Exception as e:
        if __debug:
            raise e
        else:
            print("got error %s" % e)


if __name__ == '__main__':
    main()
