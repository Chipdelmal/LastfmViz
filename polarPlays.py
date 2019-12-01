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

import setup as stp
import numpy as np
import pandas as pd
import pytz
import dateutil
from dateutil.tz import tzutc
from dateutil.parser import parse
from datetime import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt


##############################################################################
# Aesthetics parameters
##############################################################################
(WIDTH, HEIGHT, RESOLUTION) = (3840, 2160, 500)
HOURS_OFFSET = 6

##############################################################################
# Read artists file
##############################################################################
data = pd.read_csv(
        stp.DATA_PATH + stp.USR + '_art.csv',
        parse_dates=[3]
    )
msk = data['Date'] > '2000-01-01'
dates = data.loc[msk]["Date"]
hoursPlays = [i.hour for i in data["Date"]]

####
fig, axs = plt.subplots(1, sharey=True, tight_layout=True)
axs.hist(hoursPlays, bins=24)


##############################################################################
# Read artists file
##############################################################################
# r = np.arange(0, 2, 0.01)
# theta = 2 * np.pi * r
#
# ax = plt.subplot(111, projection='polar')
# ax.plot(theta, r)
# ax.set_rmax(2)
# ax.set_rticks([0.5, 1, 1.5, 2])  # less radial ticks
# ax.set_rlabel_position(-22.5)  # get radial labels away from plotted line
# ax.grid(True)
#
# ax.set_title("A line plot on a polar axis", va='bottom')
# plt.show()
