#!/usr/bin/env python
# encoding: utf-8

from pymongo import MongoClient

from lib.core.data import conf

def initDB():

    mclient = MongoClient(host=conf.MONGODB_HOST,
                          port=conf.MONGODB_PORT)
    mclient.admin.authenticate(conf.MONGODB_ADMIN_USER, conf.MONGODB_ADMIN_PASSWD)
    mclient.admin.add_user(conf.MONGODB_MANAGE_USER, conf.MONGODB_MANAGE_PASSWD, roles=[{'role':'readWrite', 'db':conf.MONGODB_DB_NAME}])
    # mclient[conf.MONGODB_DB_NAME].authenticate(conf.MONGODB_MANAGE_USER, conf.MONGODB_MANAGE_PASSWD)
    # mclient.drop_database(conf.MONGODB_DB_NAME)


def getDB():

    mclient = MongoClient(host=conf.MONGODB_HOST,
                          port=conf.MONGODB_PORT)
    db = mclient[conf.MONGODB_DB_NAME]
    db.authenticate(conf.MONGODB_MANAGE_USER, conf.MONGODB_MANAGE_PASSWD)
    table = db[conf.MONGODB_COLLECTION_NAME]
    return table
