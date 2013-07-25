#! /usr/bin/python 
# -*- coding: utf-8 -*-

import random

from rdAppConf import *
from rdEmulatorConf import *
from exportImg import *

#get emulator conf
TBF_DELAY, TBF_DELAY_TEST_START, TBF_DELAY_TEST_END, EMULATE_TIMES, NUMBER_OF_APP, CEN_PUSH_HB_START, CEN_PUSH_HB_END = readEmulatorConf()

def __getRandomInt(rangeStr):
    """get a random int from a string represents a range, the string should be in such format: 'start-end'
    and end >= start!"""
    
    start = int(rangeStr.split("-")[0])
    end = int(rangeStr.split("-")[1])
    return random.randint(start, end)
    
def __initApps():
    """a method to read in conf and initial all apps according to the conf file"""
    
    appConfs = readAppConf()
    apps = []
    cnt = 0
    while (cnt < NUMBER_OF_APP):
        app = {}
        #front end conf
        app["FEHBTypes"] = __getRandomInt(appConfs[cnt]["FEHBTypesRange"])
        type = 0
        app["FEHBTimes"] = []
        while (type < app["FEHBTypes"]):
            tmp = random.randint(0, len(appConfs[cnt]["FEHBTimesRanges"]) - 1)
            hbtimes = __getRandomInt(appConfs[cnt]["FEHBTimesRanges"][tmp])
            app["FEHBTimes"].append(hbtimes)
            type += 1
        
        #back end conf
        app["BEHBTypes"] = __getRandomInt(appConfs[cnt]["BEHBTypesRange"])
        type = 0
        app["BEHBTimes"] = []
        while (type < app["BEHBTypes"]):
            tmp = random.randint(0, len(appConfs[cnt]["BEHBTimesRanges"]) - 1)
            hbtimes = __getRandomInt(appConfs[cnt]["BEHBTimesRanges"][tmp])
            app["BEHBTimes"].append(hbtimes)
            type += 1
        apps.append(app)
        cnt += 1
    
    #shuffle all the apps
    random.shuffle(apps)
    return apps

def __calTimeSlot(timeSlot, app, useFrontConf):
    """a method to cal all the time of an app's heart beating according to its conf"""
    
    if (useFrontConf):
        HBTypes = app["FEHBTypes"]
        app["HBTimes"] = app["FEHBTimes"]
    else:
        HBTypes = app["BEHBTypes"]
        app["HBTimes"] = app["BEHBTimes"]
    type = 0
    while (type < HBTypes):
        cnt = 0
        while (cnt * app["HBTimes"][type] < 3600):
            time = cnt * app["HBTimes"][type]
            timeSlot[time] = 1
            cnt += 1
        type += 1

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
    
def __calCCCH(apps, appNumbers, cen_push_hb):
    """a method to cal ccch"""
    
    #non centralized push
    timeSlotForHB = [0 for k in range(60*60)]    #a timeSlotForHB represents 3600 seconds, only has 0 or 1 in it
    
    num = 0
    while (num < appNumbers):
        #the first app needs to use the front end conf, while the other apps need to use the back end conf
        if (num == 0 and appNumbers == 1):
            useFrontConf = True
        else:
            useFrontConf = False
        __calTimeSlot(timeSlotForHB, apps[num], useFrontConf)
        num += 1
    
    #centralized push 
    timeSlotForCenHB = [0 for k in range(60*60)]    #a timeSlotForCenHB represents 3600 seconds, only has 0 or 1 in it
    time = 0
    while ((time + cen_push_hb - 1) < 3600):
        if (sum(timeSlotForHB[time : time + cen_push_hb]) > 0):
            timeSlotForCenHB[time + cen_push_hb - 1] = 1
        time += cen_push_hb
    
    return __countCCCHBlocks(timeSlotForHB), __countCCCHBlocks(timeSlotForCenHB)
    
def emulate():
    """a method to emulate: 1, 3, 5 apps' heart beat process"""
    
    emulationTimes = 1
    #for non centralized push
    oneAppCCCHNonCenSum = 0
    ThreeAppsCCCHNonCenSum = 0
    FiveAppsCCCHNonCenSum = 0
    SevenAppsCCCHNonCenSum = 0
    TenAppsCCCHNonCenSum = 0
    
    #for centralized push
    oneAppCCCHCenSum = 0
    ThreeAppsCCCHCenSum = 0
    FiveAppsCCCHCenSum = 0
    SevenAppsCCCHCenSum = 0
    TenAppsCCCHCenSum = 0
    print "start emulations!"
    while (emulationTimes <= EMULATE_TIMES):
        print "%d times" % emulationTimes
        apps = __initApps()
        cen_push_hb = int(random.uniform(CEN_PUSH_HB_START, CEN_PUSH_HB_END))
        nonCenPush, cenPush = __calCCCH(apps, 1, cen_push_hb)
        
        oneAppCCCHNonCenSum += nonCenPush
        oneAppCCCHCenSum += cenPush
        
        nonCenPush, cenPush = __calCCCH(apps, 3, cen_push_hb)
        ThreeAppsCCCHNonCenSum += nonCenPush
        ThreeAppsCCCHCenSum += cenPush
        
        nonCenPush, cenPush = __calCCCH(apps, 5, cen_push_hb)
        FiveAppsCCCHNonCenSum += nonCenPush
        FiveAppsCCCHCenSum += cenPush
        
        nonCenPush, cenPush = __calCCCH(apps, 7, cen_push_hb)
        SevenAppsCCCHNonCenSum += nonCenPush
        SevenAppsCCCHCenSum += cenPush
        
        nonCenPush, cenPush = __calCCCH(apps, 10, cen_push_hb)
        TenAppsCCCHNonCenSum += nonCenPush
        TenAppsCCCHCenSum += cenPush
        
        emulationTimes += 1
    
    oneAppCCCHNonCenAvg = oneAppCCCHNonCenSum / EMULATE_TIMES
    oneAppCCCHCenAvg = oneAppCCCHCenSum / EMULATE_TIMES
    
    ThreeAppsCCCHNonCenAvg = ThreeAppsCCCHNonCenSum / EMULATE_TIMES
    ThreeAppsCCCHCenAvg = ThreeAppsCCCHCenSum / EMULATE_TIMES
    
    FiveAppsCCCHNonCenAvg = FiveAppsCCCHNonCenSum / EMULATE_TIMES
    FiveAppsCCCHCenAvg = FiveAppsCCCHCenSum / EMULATE_TIMES
    
    SevenAppsCCCHNonCenAvg = SevenAppsCCCHNonCenSum / EMULATE_TIMES
    SevenAppsCCCHCenAvg = SevenAppsCCCHCenSum / EMULATE_TIMES
    
    TenAppsCCCHNonCenAvg = TenAppsCCCHNonCenSum / EMULATE_TIMES
    TenAppsCCCHCenAvg = TenAppsCCCHCenSum / EMULATE_TIMES
    
    print "------------------Non centralized push averages-------------"
    print "oneAppCCCHNonCenAvg: %d" % oneAppCCCHNonCenAvg
    print "ThreeAppsCCCHNonCenAvg: %d" % ThreeAppsCCCHNonCenAvg
    print "FiveAppsCCCHNonCenAvg: %d" % FiveAppsCCCHNonCenAvg
    print "SevenAppsCCCHNonCenAvg: %d" % SevenAppsCCCHNonCenAvg
    print "TenAppsCCCHNonCenAvg: %d" % TenAppsCCCHNonCenAvg
    
    print "------------------Centralized push averages-------------"
    print "oneAppCCCHCenAvg: %d" % oneAppCCCHCenAvg
    print "ThreeAppsCCCHCenAvg: %d" % ThreeAppsCCCHCenAvg
    print "FiveAppsCCCHCenAvg: %d" % FiveAppsCCCHCenAvg
    print "SevenAppsCCCHCenAvg: %d" % SevenAppsCCCHCenAvg
    print "TenAppsCCCHCenAvg: %d" % TenAppsCCCHCenAvg
    
    exportCCCHAvgToPNG([oneAppCCCHNonCenAvg, ThreeAppsCCCHNonCenAvg, FiveAppsCCCHNonCenAvg, SevenAppsCCCHNonCenAvg, TenAppsCCCHNonCenAvg], 
        [oneAppCCCHCenAvg, ThreeAppsCCCHCenAvg, FiveAppsCCCHCenAvg, SevenAppsCCCHCenAvg, TenAppsCCCHCenAvg])
