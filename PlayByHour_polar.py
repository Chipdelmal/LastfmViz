##############################################################################
#  _           _    __           _   _ _
# | |         | |  / _|         | | | (_)
# | | __ _ ___| |_| |_ _ __ ___ | | | |_ ____
# | |/ _` / __| __|  _| '_ ` _ \| | | | |_  /
# | | (_| \__ \ |_| | | | | | | \ \_/ / |/ /
# |_|\__,_|___/\__|_| |_| |_| |_|\___/|_/___|
#
# ----------------------------------------------------------------------------
# Polar plot routines
##############################################################################

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

# (yLo, yHi) = ((2019, 1), (2020, 1))
# yOnly = 'True'
(yLo, yHi) = (
    (argv[1], argv[2],), 
    (argv[3], argv[4])
)
yOnly = argv[5]
##############################################################################
# Process inputs
##############################################################################
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
hoursPlays = sorted([i.hour for i in dates if (type(i) is not float)], reverse=True)
hoursFreq = [len(list(group)) for key, group in groupby(hoursPlays)]
hoursFreq = [hoursPlays.count(hD) for hD in list(range(23, -1, -1))]

#############################################################################
# Polar
#############################################################################
N = 24
(minFreq, maxFreq) = (min(hoursFreq), max(hoursFreq))
fig = figure(figsize=(8, 8), dpi=RESOLUTION)
ax = fig.add_axes([0.2, 0.1, 0.8, 0.8], polar=True)
step=  2*np.pi/N
(theta, radii, width) = (
    np.arange(0.0+step, 2*np.pi+step, step),
    hoursFreq,
    2*np.pi/24 -.001
)
bars = ax.bar(
    theta, radii, width=width, 
    bottom=0.0, zorder=25, edgecolor='#ffffff77', lw=.5
)
rvb = aux.colorPaletteFromHexList(
    ['#bbdefb', '#64b5f6', '#2196f3', '#1976d2', '#0d47a1', '#001d5d']
)
for r, bar in zip(radii, bars):
    bar.set_facecolor(rvb(r/(np.max(hoursFreq)*1)))
    # bar.set_facecolor(cm.BuPu(r/(np.max(hoursFreq)*1.1)))
    bar.set_alpha(0.75)
# Shading -------------------------------------------------------------------
shades = 12
# rvb = aux.colorPaletteFromHexList(
#     ['#03071e', '#001233', '#001d3d', '#001d3d','#ffffff', '#ffffff', '#ffffff', '#ffffff']
# )
rvb = aux.colorPaletteFromHexList(
    ['#ffffff', '#ffffff', '#ffffff', '#ffffff']
)
colors = list(rvb(np.linspace(0, 1, shades)))
colors.extend(reversed(colors))
step=  2*np.pi/(2*shades)
ax.bar(
    np.arange(0.0+step, 2*np.pi+step, step), 
    1.15*maxFreq,
    width=2*np.pi/(2*shades),
    color=colors, #'white', #colors, 
    alpha=.15, edgecolor="black", ls='-', lw=.5,
    zorder=-1
)
ax.set_theta_zero_location("N")
if yOnly == 'False':
    label = '{}/{} - {}/{}'.format(
        yLo[0], str(yLo[1]).zfill(2), yHi[0], str(yHi[1]).zfill(2)
    )
    lSize = 30
else:
    label = '{} - {}'.format(
        yLo[0], yHi[0]
    )
    lSize = 50
print('* Processing {}'.format(label))
ax.text(
    0.5, 0.75, label,
    horizontalalignment='center',
    verticalalignment='center',
    fontsize=lSize, color='#000000DD',
    transform=ax.transAxes, zorder=15
)
ax.text(
    0.5, 0.68, 'playcount: {}'.format(sum(hoursFreq)),
    horizontalalignment='center',
    verticalalignment='center',
    fontsize=12.5, color='#000000DD',
    transform=ax.transAxes, zorder=15
)
fig.patch.set_facecolor('#ffffff')
ax.set_ylim(0, maxFreq*1.0035)
ax.set_yticks(np.arange(0, maxFreq, maxFreq*.25))
ax.set_yticklabels([])
ax.set_xticks(np.arange(np.pi*2, 0, -np.pi*2/24))
ax.set_xticklabels(np.arange(0, 24, 1))
ax.grid(which='major', axis='x', color='#000000', alpha=0.15, lw=0, ls='--', zorder=15)
ax.grid(which='major', axis='y', color='#000000', alpha=0.15, lw=.5, ls='-', zorder=15)
ax.tick_params(direction='in', pad=10)
ax.tick_params(axis="x", labelsize=15, colors='#000000ff')
for spine in ax.spines.values():
    spine.set_edgewidth=2
fig.savefig(
    stp.IMG_PATH + '/PLC_HRL-{}_{}-{}_{}.png'.format(
        yLo[0], str(yLo[1]).zfill(2), yHi[0], str(yHi[1]).zfill(2)
    ),
    dpi=RESOLUTION, facecolor='White', edgecolor='w',
    orientation='portrait', papertype=None, format=None,
    transparent=False, bbox_inches='tight', pad_inches=.1,
    metadata=None
)
