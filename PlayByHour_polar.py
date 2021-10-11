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

import datetime
import setup as stp
import numpy as np
import pandas as pd
from itertools import groupby
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.pyplot import figure, show, rc


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
msk = [(i.date() > datetime.date(2010, 1, 1)) if (type(i) is not float) else (False) for i in data['Date']]
dates = data.loc[msk]["Date"]
hoursPlays = sorted([i.hour for i in data["Date"] if (type(i) is not float)], reverse=True)
hoursFreq = [len(list(group)) for key, group in groupby(hoursPlays)]

#############################################################################
# Polar
#############################################################################
N = 24
(minFreq, maxFreq) = (min(hoursFreq), max(hoursFreq))
fig = figure(figsize=(8, 8), dpi=RESOLUTION)
ax = fig.add_axes([0.2, 0.1, 0.8, 0.8], polar=True)
(theta, radii, width) = (
        np.arange(0.0, 2*np.pi, 2*np.pi/N),
        hoursFreq,
        2 * np.pi/24 - .01
    )
bars = ax.bar(theta, radii, width=width, bottom=0.0, zorder=10)
ax.set_theta_zero_location("N")
# ax.set_yticks(np.arange(0, np.max(hoursFreq), 100000))
ax.set_ylim(0, maxFreq)
ax.set_yticks(np.arange(0, maxFreq, maxFreq*.25))
ax.set_yticklabels([])
ax.set_xticks(np.arange(np.pi * 2, 0, - np.pi * 2 / 24))
ax.set_xticklabels(np.arange(0, 24, 1))
ax.grid(which='major', color='#000000', alpha=.35, lw=0.8, ls='--')
ax.tick_params(direction='out', pad=15)
ax.tick_params(axis="x", labelsize=18) 
for r, bar in zip(radii, bars):
    bar.set_facecolor(cm.RdPu(r/np.max(hoursFreq)))
    bar.set_alpha(0.75)
fig.savefig(
        stp.IMG_PATH + '/PLC_HRL.png',
        dpi=RESOLUTION, facecolor='White', edgecolor='w',
        orientation='portrait', papertype=None, format=None,
        transparent=False, bbox_inches='tight', pad_inches=.5,
        metadata=None
    )

# #############################################################################
# # Histogram
# #############################################################################
# fig, axs = plt.subplots(1, sharey=True, tight_layout=True)
# axs.hist(hoursPlays, bins=24)

# ##############################################################################
# # Read artists file
# ##############################################################################
# r = np.arange(0, 2, 0.01)
# theta = 2 * np.pi * r

# ax = plt.subplot(111, projection='polar')
# ax.plot(theta, r)
# ax.set_rmax(2)
# ax.set_rticks([0.5, 1, 1.5, 2])  # less radial ticks
# ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
# ax.grid(True)

# ax.set_title("A line plot on a polar axis", va='bottom')
# plt.show()
