from sys import argv
import datetime
import aux as aux
import setup as stp
import numpy as np
import pandas as pd
from itertools import groupby
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib as mpl
from matplotlib.pyplot import figure, show, rc
mpl.rcParams['axes.linewidth'] = 1

(yLo, yHi) = ((2012, 1), (2022, 1))
DATE = True
yLo = [int(i) for i in yLo]
yHi = [int(i) for i in yHi]
##############################################################################
# Aesthetics parameters
##############################################################################
(WIDTH, HEIGHT, RESOLUTION) = (3840, 2160, 500)
HOURS_OFFSET = 6
##############################################################################
# Read artists file
##############################################################################
data = pd.read_csv(
    stp.DATA_PATH + stp.USR + '_cln.csv',
    parse_dates=[3]
)
data = data.drop_duplicates()
msk = [
    (
        (i.date() >= datetime.date(yLo[0], yLo[1], 1)) and 
        (i.date() < datetime.date(yHi[0], yHi[1], 1))
    ) 
    if (type(i) is not float) else (False) for i in data['Date']
]
dates = data.loc[msk]["Date"]
hoursPlays = sorted([(i.year, i.hour) for i in dates if (type(i) is not float)], reverse=True)
hoursFreq = [
    [hoursPlays.count((yD, hD)) for hD in list(range(23, -1, -1))] 
    for yD in list(range(yLo[0], yHi[0]))
]
##############################################################################
# Plots
##############################################################################
N = 24
(minFreq, maxFreq) = (min(hoursFreq), max(hoursFreq))
fig = figure(figsize=(8, 8), dpi=RESOLUTION)
ax = fig.add_axes([0.2, 0.1, 0.8, 0.8], polar=True)
step=  2*np.pi/N
for i in range(len(hoursFreq)):
    (theta, radii) = (
        np.arange(0.0+step, 2*np.pi+step, step),
        hoursFreq[i],
    )
    ax.plot(theta, radii)
ax.set_theta_zero_location("N")
fig.patch.set_facecolor('#ffffff')
ax.set_ylim(0, max(maxFreq)*1.0035)
ax.set_yticks(np.arange(0, max(maxFreq), max(maxFreq)*.25))
ax.set_yticklabels([])
ax.set_xticks(np.arange(np.pi*2, 0, -np.pi*2/24))
ax.set_xticklabels(np.arange(0, 24, 1))
ax.grid(which='major', axis='x', color='#000000', alpha=0, lw=.5, ls='--', zorder=15)
ax.grid(which='major', axis='y', color='#000000', alpha=0, lw=.5, ls='-', zorder=15)
ax.tick_params(direction='in', pad=10)
ax.tick_params(axis="x", labelsize=17.5, colors='#000000ff')
for spine in ax.spines.values():
    spine.set_edgewidth=2