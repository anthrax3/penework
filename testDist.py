#!/usr/bin/env python
# encoding: utf-8
# encoding: utf-8

import os
import pudb
import pdb
import pickle
import sys
import codecs
from redis import Redis
from pymongo import MongoClient
import IPython


from lib.core.data import conf
from lib.core.enums import CUSTOM_LOGGING
from setEnvironment import setEnv
from setEnvironment import getConfig
from lib.utils.crawler.master import Master
from lib.utils.crawler.crawler import crawl
from lib.core.data import logger
from lib.utils.hashUrl import hashUrl
from lib.utils.crawler.store import initDB
from lib.utils.crawler.store import getDB


def testHashurl():
    fp = codecs.open(conf.STORE_FILENAME, 'r', 'utf-8')
    wfp = codecs.open('check.txt', 'w', 'utf-8')
    for url in fp:
        url = url.strip()
        msg = url + ' ' + hashUrl(url)
        wfp.write(msg + '\n')
    wfp.close()
    print 'write successfully....'


def testCrawler():
    crawl(conf.CRAWL_SITE)


def testMongo():
    initDB()


def main():

    setEnv()
    getConfig()
    testMongo()
    # testHashurl()
    # testCrawler()


if __name__ == '__main__':
    os.system('clear')


    main()
