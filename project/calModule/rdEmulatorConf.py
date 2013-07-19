#! /usr/bin/python 
# -*- coding: utf-8 -*-

import os

def readEmulatorConf():
    """a method to read in emulator conf files"""
    
    cnt = 1
    confs = []
    path = os.path.dirname(__file__)
    fileName = path + "/confs/emulator.conf"
    try:
        fConf = open(fileName, 'rb')
    except IOError, e:
        print e
        exit(1)
    stringData = fConf.read()
        
    tbf_delay = int(stringData.split("\n")[0].split(":")[1])
    tbf_delay_test_start = int(stringData.split("\n")[1].split(":")[1].split(",")[0])
    tbf_delay_test_end = int(stringData.split("\n")[1].split(":")[1].split(",")[1])
    emulate_times = int(stringData.split("\n")[2].split(":")[1])
    number_of_apps = int(stringData.split("\n")[3].split(":")[1])
    fConf.close()
    
    return tbf_delay, tbf_delay_test_start, tbf_delay_test_end, emulate_times, number_of_apps
