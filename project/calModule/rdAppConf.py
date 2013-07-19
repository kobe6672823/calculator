#! /usr/bin/python 
# -*- coding: utf-8 -*-

import os

TYPES_OF_CONF = 5   #5 conf files need to be read in

def readAppConf():
    """a method to read in TYPES_OF_CONF apps conf files"""
    
    cnt = 1
    confs = []
    path = os.path.dirname(__file__)
    while (cnt <= TYPES_OF_CONF):
        fileName = path + "/confs/app" + str(cnt) + ".conf"
        try:
            fConf = open(fileName, 'rb')
        except IOError, e:
            print e
            exit(1)
        stringData = fConf.read()
        
        appConf = {}
        appConf["HBTypesStart"] = int(stringData.split("\n")[0].split(":")[1].split(",")[0])
        appConf["HBTypesEnd"] = int(stringData.split("\n")[0].split(":")[1].split(",")[1])
        appConf["HBTimesStart"] = int(stringData.split("\n")[1].split(":")[1].split(",")[0])
        appConf["HBTimesEnd"] = int(stringData.split("\n")[1].split(":")[1].split(",")[1])
        appConf["HBSizeStart"] = int(stringData.split("\n")[2].split(":")[1].split(",")[0])
        appConf["HBSizeEnd"] = int(stringData.split("\n")[2].split(":")[1].split(",")[1])
        confs.append(appConf)
        fConf.close()
        cnt += 1
    
    return confs
