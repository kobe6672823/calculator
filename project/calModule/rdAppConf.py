#! /usr/bin/python 
# -*- coding: utf-8 -*-

import os

TYPES_OF_CONF = 10   #10 conf files need to be read in

def readAppConf():
    """a method to read in TYPES_OF_CONF apps conf files"""
    
    cnt = 0
    confs = []
    path = os.path.dirname(__file__)
    while (cnt < TYPES_OF_CONF):
        fileName = path + "/confs/app" + str(cnt) + ".conf"
        try:
            fConf = open(fileName, 'rb')
        except IOError, e:
            print e
            exit(1)
        stringData = fConf.read()
        
        appConf = {}
        #front end
        appConf["FEHBTypesRange"] = stringData.split("\n")[1].split(":")[1]
        appConf["FEHBTimesRanges"] = stringData.split("\n")[2].split(":")[1].split(",")
        #back end
        appConf["BEHBTypesRange"] = stringData.split("\n")[5].split(":")[1]
        appConf["BEHBTimesRanges"] = stringData.split("\n")[6].split(":")[1].split(",")
        confs.append(appConf)
        fConf.close()
        cnt += 1
    
    return confs
