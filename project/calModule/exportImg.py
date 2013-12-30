#! /usr/bin/python 
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt 
import os
import numpy as np
from matplotlib.font_manager import FontProperties

def __autolabel(plt, rects):
    """a method to label the height of the bar in the bar chart"""
    
    for rect in rects:
        height = int(rect.get_height())
        if (height > 0):
            plt.text(rect.get_x()+rect.get_width()/4., 1.03*height, '%s' % int(height))


def exportCCCHAvgToPNG(CCCHNonCenAvgs, CCCHCenAvgs):
        """a method to export CCCHAvgs to bar chart"""

        N = 5
        ind = np.arange(N)  # the x locations for the groups
        width = 0.15       # the width of the bars

        fig = plt.figure()
        ax = fig.add_subplot(111)
        maxHeight = max(CCCHNonCenAvgs + CCCHCenAvgs)
        ax.set_ylim(0, maxHeight*1.1)
        rects1 = ax.bar(ind, CCCHNonCenAvgs, width, color='#444444')

        rects2 = ax.bar(ind+width, CCCHCenAvgs, width, color='#999999')
    
        
        plt.title("CCCH average")
        plt.xlabel('number of apps')
        plt.ylabel('CCCH blocks consumption')
        
        ax.set_xticks(ind+width)
        ax.set_xticklabels(("oneApp", "threeApps", "fiveApps", "sevenApps", "tenApps"))

        fontP = FontProperties()
        fontP.set_size('small')
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend((rects1[0], rects2[0]), ('Non centralized push', 'centralized push'), prop = fontP, loc='center left', bbox_to_anchor=(1, 0.5))

        def autolabel(rects):
            # attach some text labels
            for rect in rects:
                height = rect.get_height()
                ax.text(rect.get_x()+rect.get_width()/2., 1.02*height, '%d'%int(height),
                        ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)
        path = os.path.dirname(__file__)
        png_file_name = path + "/CCCHAvgs_consumtion.png"
        plt.savefig(png_file_name, dpi=75)
