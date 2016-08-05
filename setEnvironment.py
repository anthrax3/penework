#!/usr/bin/env python
# encoding: utf-8
# encoding: utf-8
# encoding: utf-8

import os
from ConfigParser import ConfigParser

from lib.core.data import logger
from lib.core.enums import CUSTOM_LOGGING
from lib.core.common import setPaths
from lib.core.data import paths
from lib.core.data import conf



def setEnv():

    paths.PENEWORK_ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
    setPaths()


def getConfig():

    try:

        config = ConfigParser()
        configFile = paths.PENEWORK_ROOT_PATH + '/penework.conf'
        config.read(configFile)
        for section in config.sections():
            for option in config.options(section):
                OPTION = option.upper()
                conf[OPTION] = config.get(section, option)
                if conf[OPTION].isdigit():
                    conf[OPTION] = int(conf[OPTION])

    except Exception, ex:
        logger.log(CUSTOM_LOGGING.ERROR, 'get config error: ' + ex.message)
