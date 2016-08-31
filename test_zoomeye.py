#!/usr/bin/env python
# encoding: utf-8

import os
from lib.utils.zoomeye import Zoomeye
import IPython


def main():
    zoom = Zoomeye("")
    for page in xrange(500, 900):
        print '*********  page {}  *********'.format(page)
        result = zoom.search('port:11211', page=page)
        for match in result['matches']:
            print match['ip']

if __name__ == '__main__':
    os.system('clear')

    main()
