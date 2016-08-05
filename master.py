#!/usr/bin/env python
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


def masterstart():
    master = Master()
    redisCon = Redis(host=conf.REDIS_HOST,
                     port=conf.REDIS_PORT,
                     password=conf.REDIS_PASSWD)

    try:
        logger.log(CUSTOM_LOGGING.SYSINFO, 'starting rq server...')
        master.start()
    except KeyboardInterrupt, ke:
        finishedJob = redisCon.scard('visited')
        leftJob = redisCon.llen('visit')
        keMsg = """
you input KeyboardInterrupt(Ctrl+C was pressed), so quit,
finished: %d
left: %d
                """ % (finishedJob, leftJob)
        logger.log(CUSTOM_LOGGING.WARNING, keMsg)

    except Exception, ex:
        logger.log(CUSTOM_LOGGING.ERROR, ex)

    logger.log(CUSTOM_LOGGING.SYSINFO, 'rq server finished successfully...')


def main():

    setEnv()
    getConfig()
    masterstart()


if __name__ == '__main__':
    os.system('clear')

    main()
