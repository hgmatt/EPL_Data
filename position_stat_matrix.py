#loading libraries
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import re
import StringIO
import pprint
import sys

matplotlib.rc('font', size=18)
matplotlib.rc('figure', figsize=(12, 4))

position_title = ['Goalkeeper', 'Defender', 'Forward', 'Midfielder']
teams = {1: 'Arsenal',
         2: 'Bournmouth',
         3: 'Burnley',
         4: 'Chelsea',
         5: 'Crystal Palace',
         6: 'Everton',
         7: 'Hull City',
         8: 'Leicester City',
         9: 'Liverpool',
         10: 'Manchester City',
         11: 'Manchester United',
         12: 'Middlesbrough',
         13: 'Southampton',
         14: 'Stoke City',
         15: 'Sunderland',
         16: 'Swansea',
         17: 'Tottenham',
         18: 'Watford',
         19: 'West Brom',
         20: 'West Ham'}
teams_short = {1: 'ARS', 2:'BOU', 3:'BUR', 4:'CHE', 5:'CRY', 6:'EVE', 7:'HUL', 8:'LEI', 9:'LIV', 10:'MCI', 11:'MUN', 
             12:'MID', 13:'SOU', 14:'STK', 15:'SUN', 16:'SWA', 17:'TOT', 18:'WAT', 19:'WBA', 20:'WHU'}
#Parse out by Position: 15/16 Points, 15/16 Points per Game, 16/17 Initial Cost, 15/16 Points per Game by 16/17 Cost
points = {}
for p in all_data:
    if p['total_points'] >0:
        points.setdefault(p['element_type'],[]).append(p['total_points'])

ppg = {}
for p in all_data:
    if p['points_per_game'] >0:
        ppg.setdefault(p['element_type'],[]).append(float(p['points_per_game']))

cost = {}
for p in all_data:
    cost.setdefault(p['element_type'],[]).append(float(p['now_cost']))

cppg ={}
for p in all_data:
    if p['points_per_game'] >0:
        cppg.setdefault(p['element_type'],[]).append(10*float(p['points_per_game'])/float(p['now_cost']))    

def poshist(axis, position):
    axis.hist(points[position])
    axis.set_title(position_title[position-1])
    if axis == ax0:
        axis.set_ylabel('15/16 Total Points')
    return axis

def ppghist(axis, position):
    axis.hist(ppg[position])
    #axis.set_title(position_title[position-1])
    if axis == ax4:
        axis.set_ylabel('15/16 Points per Game')
    return axis

def costhist(axis, position):
    axis.hist(cost[position])
    #axis.set_title(position_title[position-1])
    if axis == ax8:
        axis.set_ylabel('16/17 Initial Cost')
    return axis

def cppghist(axis, position):
    axis.hist(cppg[position])
    #axis.set_title(position_title[position-1])
    if axis == ax12:
        axis.set_ylabel('15/16 PPG by \n16/17 Initial Cost')
    return axis

fig, ((ax0, ax1, ax2, ax3), (ax4, ax5, ax6, ax7), (ax8, ax9, ax10, ax11), (ax12, ax13, ax14, ax15)) = plt.subplots(ncols=4, nrows = 4, sharey=True, figsize=(18,4*4))
plt.subplots_adjust(hspace=0.2)
plt.tight_layout()

poshist(ax0, 1)
poshist(ax1, 2)
poshist(ax2, 3)
poshist(ax3, 4)
ppghist(ax4, 1)
ppghist(ax5, 2)
ppghist(ax6, 3)
ppghist(ax7, 4)
costhist(ax8, 1)
costhist(ax9, 2)
costhist(ax10, 3)
costhist(ax11, 4)
cppghist(ax12, 1)
cppghist(ax13, 2)
cppghist(ax14, 3)
cppghist(ax15, 4)

fig.show()