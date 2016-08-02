#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Penework opensource framework
See the file 'docs/COPYING' for copying permission
"""

import time
import threading
import traceback
from thread import error as threadError

from lib.core.data import logger
from lib.core.data import kb
from lib.core.enums import CUSTOM_LOGGING
from lib.core.settings import PYVERSION
from lib.core.exception import PeneworkConnectionException
from lib.core.exception import PeneworkThreadException
from lib.core.exception import PeneworkValueException


def runThreads(numThreads, threadFunction, forwardException=True, startThreadMsg=True):
    threads = []

    kb.multiThreadMode = True
    kb.threadContinue = True
    kb.threadException = False

    try:
        if numThreads > 1:
            if startThreadMsg:
                infoMsg = "starting %d threads" % numThreads
                logger.log(CUSTOM_LOGGING.SYSINFO, infoMsg)

        else:
            threadFunction()
            return

        for numThread in xrange(numThreads):
            thread = threading.Thread(target=exceptionHandledFunction, name=str(numThread), args=[threadFunction])

            setDaemon(thread)

            try:
                thread.start()
            except threadError, errMsg:
                errMsg = "error occurred while starting new thread ('%s')" % errMsg
                logger.log(CUSTOM_LOGGING.ERROR, errMsg)
                break

            threads.append(thread)

        # And wait for them to all finish
        alive = True
        while alive:
            alive = False
            for thread in threads:
                if thread.isAlive():
                    alive = True
                    time.sleep(0.1)

    except KeyboardInterrupt:
        print
        kb.threadContinue = False
        kb.threadException = True

        if numThreads > 1:
            logger.log(CUSTOM_LOGGING.SYSINFO, "waiting for threads to finish (Ctrl+C was pressed)")
        try:
            while (threading.activeCount() > 1):
                pass

        except KeyboardInterrupt:
            raise PeneworkThreadException("user aborted (Ctrl+C was pressed multiple times)")

        if forwardException:
            raise

    except (PeneworkConnectionException, PeneworkValueException), errMsg:
        print
        kb.threadException = True
        logger.log(CUSTOM_LOGGING.ERROR, "thread %s: %s" % (threading.currentThread().getName(), errMsg))

    except:
        from lib.core.common import unhandledExceptionMessage

        print
        kb.threadException = True
        errMsg = unhandledExceptionMessage()
        logger.log(CUSTOM_LOGGING.ERROR, "thread %s: %s" % (threading.currentThread().getName(), errMsg))
        traceback.print_exc()

    finally:
        kb.multiThreadMode = False
        kb.bruteMode = False
        kb.threadContinue = True
        kb.threadException = False


def setDaemon(thread):
    # Reference: http://stackoverflow.com/questions/190010/daemon-threads-explanation
    if PYVERSION >= "2.6":
        thread.daemon = True
    else:
        thread.setDaemon(True)


def exceptionHandledFunction(threadFunction):
    try:
        threadFunction()
    except KeyboardInterrupt:
        kb.threadContinue = False
        kb.threadException = True
        raise
    except Exception, errMsg:
        # thread is just going to be silently killed
        logger.log(CUSTOM_LOGGING.ERROR, "thread %s: %s" % (threading.currentThread().getName(), errMsg))
