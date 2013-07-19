#! /usr/bin/python 
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt 
import os

def __autolabel(plt, rects):
    """a method to label the height of the bar in the bar chart"""
    
    for rect in rects:
        height = int(rect.get_height())
        if (height > 0):
            plt.text(rect.get_x()+rect.get_width()/2., 1.03*height, '%s' % int(height))


def exportCCCHAvgToPNG(CCCHAvgs):
        """a method to export CCCHAvgs to bar chart"""

        #browser statistics
        plt.title("CCCH average")
        plt.xlabel('number of apps')
        plt.ylabel('CCCH blocks consumption')
        
        table_headers = ["oneApp", "threeApps", "fiveApps"]
        plt.xticks(range(0, len(table_headers)), table_headers, rotation=30)
        eps = 1e-7
        bar_height = CCCHAvgs
        rect = plt.bar(left = range(0, len(table_headers)), height = bar_height, width = 0.3,align="center")
        __autolabel(plt, rect)
        plt.tight_layout()
        path = os.path.dirname(__file__)
        png_file_name = path + "/CCCHAvgs_consumtion.png"
        plt.savefig(png_file_name, dpi=75)
