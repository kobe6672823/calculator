#! /usr/bin/python 
# -*- coding: utf-8 -*-

import random

from rdAppConf import *
from rdEmulatorConf import *
from exportImg import *

#get emulator conf
TBF_DELAY, TBF_DELAY_TEST_START, TBF_DELAY_TEST_END, EMULATE_TIMES, NUMBER_OF_APP = readEmulatorConf()

def __initApps():
    """a method to read in conf and initial all apps according to the conf file"""
    
    appConfs = readAppConf()
    apps = []
    cnt = 0
    while (cnt < NUMBER_OF_APP):
        app = {}
        app["HBTypes"] = int(random.uniform(appConfs[cnt]["HBTypesStart"], appConfs[cnt]["HBTypesEnd"]))
        type = 0
        app["HBTimes"] = []
        while (type < app["HBTypes"]):
            app["HBTimes"].append(int(random.uniform(appConfs[cnt]["HBTimesStart"], appConfs[cnt]["HBTimesEnd"])))
            type += 1
        app["HBSize"] = int(random.uniform(appConfs[cnt]["HBSizeStart"], appConfs[cnt]["HBSizeEnd"]))
        apps.append(app)
        cnt += 1
        
    return apps

def __isTimeToHB(time, app):
    """a method to judge an app needs to send heart beat packet now or not"""
    
    if (time == 0):
        return True
    
    cnt = 0
    while (cnt < app["HBTypes"]):
        if (app["HBTimes"][cnt] % time == 0):
            return True
        cnt += 1
    return False

def __countCCCHBlocks(timeSlot):
    """a method to CCCHBlocks"""
    
    time = 0
    blocks = 0
    zeroLen = TBF_DELAY
    while (time < 3600):
        if (timeSlot[time] == 1):
            if (zeroLen >= TBF_DELAY):
                blocks += 1
            zeroLen = 0
        elif (timeSlot[time] == 0):
            zeroLen += 1
        time += 1
    return blocks
    
def __calCCCH(apps, appNumbers):
    """a method to cal ccch"""
    
    timeSlotForHB = [0 for k in range(60*60)]    #a timeSlotForHB represents 3600 seconds, only has 0 or 1 in it
    timeSlotForHBPkt = [0 for k in range(60*60)]    #a timeSlotForHBPkt represents 3600 seconds, it stores the sum of hear beat packets size
    
    time = 0
    while (time < 3600):
        num = 0
        while (num < appNumbers):
            if (__isTimeToHB(time, apps[num])):
                timeSlotForHB[time] = 1
                timeSlotForHBPkt[time] += apps[num]["HBSize"]
            num += 1
        time += 1
    
    return __countCCCHBlocks(timeSlotForHB)
    
def emulate():
    """a method to emulate: 1, 3, 5 apps' heart beat process"""
    
    emulationTimes = 1
    oneAppCCCHSum = 0
    ThreeAppsCCCHSum = 0
    FiveAppsCCCHSum = 0
    while (emulationTimes <= EMULATE_TIMES):
        apps = __initApps()
        oneAppCCCHSum += __calCCCH(apps, 1)
        ThreeAppsCCCHSum += __calCCCH(apps, 3)
        FiveAppsCCCHSum += __calCCCH(apps, 5)
        emulationTimes += 1
    
    oneAppCCCHAvg = oneAppCCCHSum / EMULATE_TIMES
    ThreeAppsCCCHAvg = ThreeAppsCCCHSum / EMULATE_TIMES
    FiveAppsCCCHAvg = FiveAppsCCCHSum / EMULATE_TIMES
    
    print "oneAppCCCHAvg: %d" % oneAppCCCHAvg
    print "ThreeAppsCCCHAvg: %d" % ThreeAppsCCCHAvg
    print "FiveAppsCCCHAvg: %d" % FiveAppsCCCHAvg
    
    exportCCCHAvgToPNG([oneAppCCCHAvg, ThreeAppsCCCHAvg, FiveAppsCCCHAvg])
